import collections
import json
import re
import time

import google.generativeai as genai
import streamlit as st

_configured = False

_RPM_LIMIT   = 15       # 분당 최대 요청 수
_WINDOW      = 60.0     # 슬라이딩 윈도우 (초)
_MAX_RETRIES = 3        # 429 발생 시 추가 재시도 횟수
_RETRY_BASE  = 5.0      # 429 재시도 첫 대기(초)

# 최근 요청 타임스탬프 (프로세스 내 전역 — Streamlit 세션 간 공유)
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
    """분당 15회 제한을 넘지 않도록 필요 시 대기."""
    while True:
        now = time.time()
        # 윈도우 밖 타임스탬프 제거
        while _req_times and now - _req_times[0] >= _WINDOW:
            _req_times.popleft()

        if len(_req_times) < _RPM_LIMIT:
            break  # 여유 있음 → 즉시 진행

        # 가장 오래된 요청이 윈도우를 벗어날 때까지 대기
        wait = _WINDOW - (now - _req_times[0]) + 0.5  # 0.5초 여유
        st.toast(
            f"분당 요청 한도({_RPM_LIMIT}회) 도달 — {wait:.0f}초 대기 중...",
            icon="⏳",
        )
        time.sleep(min(wait, 5.0))   # 최대 5초씩 끊어서 대기


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

    retry_wait = _RETRY_BASE
    for attempt in range(1, _MAX_RETRIES + 2):  # +1 for initial attempt
        _wait_for_rate_limit()   # 호출 전 RPM 체크

        try:
            _req_times.append(time.time())   # 요청 시각 기록
            response = model.generate_content(user_message)

            if json_mode:
                return json.loads(_extract_json(response.text))
            return response.text

        except Exception as e:
            _req_times.pop()     # 실패한 요청은 카운트에서 제외
            err = str(e)
            is_rate_limit = "429" in err or "quota" in err.lower() or "rate" in err.lower()

            if is_rate_limit and attempt <= _MAX_RETRIES:
                m = re.search(r"retryDelay['\"]?\s*[:=]\s*['\"]?(\d+(?:\.\d+)?)", err)
                suggested = float(m.group(1)) if m else 0.0
                delay = max(retry_wait, suggested + 1.0)
                st.toast(
                    f"API 한도 초과 — {delay:.0f}초 후 재시도 ({attempt}/{_MAX_RETRIES})",
                    icon="⏳",
                )
                time.sleep(delay)
                retry_wait *= 2
            else:
                raise


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
