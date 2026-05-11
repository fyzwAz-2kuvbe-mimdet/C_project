import collections
import json
import re
import time

import google.generativeai as genai
import streamlit as st

_configured = False

_RPM_LIMIT   = 14       # 안전 마진 포함 (실제 한도 15 - 1)
_WINDOW      = 60.0     # 슬라이딩 윈도우(초)
_MAX_RETRIES = 4        # 429 발생 시 최대 재시도 횟수

_req_times: collections.deque = collections.deque()


def _ensure_configured():
    global _configured
    if not _configured:
        try:
            api_key = st.secrets["GEMINI_API_KEY"]
        except KeyError:
            raise ValueError("Streamlit Secrets에 GEMINI_API_KEY를 등록해주세요.")
        genai.configure(api_key=api_key)
        _configured = True


def _wait_for_rate_limit():
    """분당 14회(안전 마진)를 넘지 않도록 필요 시 대기."""
    while True:
        now = time.time()
        while _req_times and now - _req_times[0] >= _WINDOW:
            _req_times.popleft()
        if len(_req_times) < _RPM_LIMIT:
            break
        wait = _WINDOW - (now - _req_times[0]) + 1.0
        st.toast(f"분당 요청 한도 도달 — {wait:.0f}초 대기 중...", icon="⏳")
        time.sleep(min(wait, 5.0))


def _parse_retry_delay(err: str) -> float:
    """에러 메시지에서 재시도 권장 대기 시간(초) 추출."""
    patterns = [
        r"retry in (\d+(?:\.\d+)?)s",                            # "Please retry in 45.62s"
        r"retry_delay\s*\{\s*seconds:\s*(\d+(?:\.\d+)?)\s*\}",   # "retry_delay { seconds: 45 }"
        r'"seconds":\s*(\d+(?:\.\d+)?)',                           # JSON {"seconds": 45}
        r"retryDelay['\"]?\s*[:=]\s*['\"]?(\d+(?:\.\d+)?)",      # retryDelay: 45
    ]
    for pat in patterns:
        m = re.search(pat, err, re.IGNORECASE)
        if m:
            return float(m.group(1))
    return 0.0


def _is_daily_quota(err: str) -> bool:
    return "PerDay" in err or "per_day" in err.lower()


def ask(
    system_prompt: str,
    user_message: str,
    max_tokens: int = 8192,
    json_mode: bool = False,
) -> str | dict | list:
    _ensure_configured()

    generation_config = {"max_output_tokens": max_tokens}
    if json_mode:
        generation_config["response_mime_type"] = "application/json"

    model = genai.GenerativeModel(
        model_name="gemini-2.5-flash-lite",
        system_instruction=system_prompt,
        generation_config=generation_config,
    )

    for attempt in range(1, _MAX_RETRIES + 2):
        _wait_for_rate_limit()

        try:
            _req_times.append(time.time())
            response = model.generate_content(user_message)
            if json_mode:
                return json.loads(_extract_json(response.text))
            return response.text

        except Exception as e:
            _req_times.pop()   # 실패 요청은 카운트 제외
            err = str(e)
            is_quota = "429" in err or "quota" in err.lower() or "rate" in err.lower()

            if not is_quota or attempt > _MAX_RETRIES:
                raise

            delay = _parse_retry_delay(err)
            daily = _is_daily_quota(err)

            if daily:
                # 일일 한도: Google이 제시한 대기 시간 사용, 없으면 60초
                delay = delay if delay > 0 else 60.0
                msg = (
                    f"일일 API 요청 한도(20회) 초과 — "
                    f"{delay:.0f}초 후 재시도합니다 ({attempt}/{_MAX_RETRIES}). "
                    f"한도가 지속되면 유료 플랜 전환을 권장합니다."
                )
            else:
                # 분당 한도: 최소 5초, Google 제시값 우선
                delay = max(delay, 5.0 * attempt)
                msg = f"분당 요청 한도 초과 — {delay:.0f}초 후 재시도합니다 ({attempt}/{_MAX_RETRIES})"

            st.toast(msg, icon="⏳")
            time.sleep(delay)


def _extract_json(text: str) -> str:
    text = text.strip()
    text = re.sub(r"^```(?:json)?\s*", "", text)
    text = re.sub(r"\s*```$", "", text)
    text = text.strip()
    for start, end in [("{", "}"), ("[", "]")]:
        s = text.find(start)
        e = text.rfind(end)
        if s != -1 and e != -1 and e > s:
            candidate = text[s : e + 1]
            try:
                json.loads(candidate)
                return candidate
            except json.JSONDecodeError:
                continue
    return text
