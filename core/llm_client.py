import json
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

    generation_config = {"max_output_tokens": max_tokens}
    if json_mode:
        generation_config["response_mime_type"] = "application/json"

    model = genai.GenerativeModel(
        model_name="gemini-2.5-flash",
        system_instruction=system_prompt,
        generation_config=generation_config,
    )
    response = model.generate_content(user_message)

    if json_mode:
        return json.loads(response.text)
    return response.text
