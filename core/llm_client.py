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
            raise ValueError("Streamlit Secrets에 GEMINI_API_KEY를 등록해주세요.")
        genai.configure(api_key=api_key)
        _configured = True


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
    response = model.generate_content(user_message)

    if json_mode:
        return json.loads(_extract_json(response.text))
    return response.text


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
