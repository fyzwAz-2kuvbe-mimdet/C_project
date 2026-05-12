import json
import streamlit as st

from core.llm_client import _extract_json, ask


def prompt_panel(
    system: str,
    prompt: str,
    result_key: str,
    *,
    json_mode: bool = True,
    spinner_text: str = "AI가 분석 중이에요...",
    btn_label: str = "AI에게 전송하기",
) -> bool:
    """
    Dual-mode AI panel.
    Tab 1 — Auto: sends to Gemini, stores result in session_state[result_key].
    Tab 2 — Manual: shows prompt for copying; user pastes AI response.
    Returns True when result is already in session_state[result_key].
    """
    if st.session_state.get(result_key):
        return True

    with st.expander("📋 프롬프트 보기 / 복사", expanded=False):
        st.caption("아래 내용을 복사해서 ChatGPT, Claude 등 다른 AI에도 사용할 수 있어요.")
        st.code(prompt, language="text")

    tab_auto, tab_manual = st.tabs(["🤖 AI 자동 전송", "✍️ 직접 붙여넣기"])

    with tab_auto:
        st.caption("Gemini AI가 자동으로 분석합니다.")
        if st.button(btn_label, key=f"_auto_{result_key}", type="primary", use_container_width=True):
            with st.spinner(spinner_text):
                try:
                    result = ask(system, prompt, json_mode=json_mode)
                    st.session_state[result_key] = result
                    st.rerun()
                except Exception as e:
                    st.error(f"AI 오류: {e}")

    with tab_manual:
        st.caption("위 프롬프트를 복사 → 원하는 AI에 붙여넣기 → 응답을 아래에 입력하세요.")
        manual = st.text_area(
            "AI 응답",
            height=220,
            key=f"_manual_{result_key}",
            placeholder="AI의 응답을 여기에 붙여넣으세요...",
            label_visibility="collapsed",
        )
        if st.button("결과 적용하기", key=f"_apply_{result_key}", type="primary", use_container_width=True):
            if manual.strip():
                try:
                    if json_mode:
                        parsed = json.loads(_extract_json(manual))
                    else:
                        parsed = manual.strip()
                    st.session_state[result_key] = parsed
                    st.rerun()
                except Exception as e:
                    st.error(f"형식 오류: {e} — JSON 형식인지 확인하거나 AI 자동 전송을 이용해주세요.")
            else:
                st.warning("AI 응답을 입력해주세요.")

    return False
