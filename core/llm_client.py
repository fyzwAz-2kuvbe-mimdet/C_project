import json
import re
import streamlit as st
import google.generativeai as genai

_configured = False


def _ensure_configured():
    global _configured
    if not _configured:
        try:
            api_key = st.secrets["GEMINI_API_KEY"]
        except KeyError:
            raise ValueError(
                "GEMINI_API_KEY가 설정되지 않았습니다. .streamlit/secrets.toml을 확인하세요."
            )
        genai.configure(api_key=api_key)
        _configured = True


def ask(
    system_prompt: str,
    user_message: str,
    max_tokens: int = 2000,
    json_mode: bool = False,
):
    _ensure_configured()

    generation_config = {
        "max_output_tokens": max_tokens,
    }
    if json_mode:
        generation_config["response_mime_type"] = "application/json"

    model = genai.GenerativeModel(
        model_name="gemini-2.5-flash-lite",
        system_instruction=system_prompt,
        generation_config=generation_config,
    )
    response = model.generate_content(user_message)

    if json_mode:
        return json.loads(_extract_json(response.text))
    return response.text


def _extract_json(text: str) -> str:
    text = text.strip()
    # 마크다운 코드블록 제거
    text = re.sub(r"^```(?:json)?\s*", "", text)
    text = re.sub(r"\s*```$", "", text)
    text = text.strip()

    # { } 또는 [ ] 범위만 추출 (앞뒤 불필요한 텍스트 제거)
    for start_ch, end_ch in [("{", "}"), ("[", "]")]:
        start = text.find(start_ch)
        end = text.rfind(end_ch)
        if start != -1 and end != -1 and end > start:
            candidate = text[start : end + 1]
            try:
                json.loads(candidate)
                return candidate
            except json.JSONDecodeError:
                continue

    return text
