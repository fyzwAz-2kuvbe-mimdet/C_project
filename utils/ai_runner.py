import json
import streamlit as st

from core.llm_client import _extract_json, ask


def _done_key(result_key: str) -> str:
    return f"_done_{result_key}"


def is_done(result_key: str) -> bool:
    """result_key 결과가 이미 저장됐는지 확인 (빈 값도 완료로 간주)."""
    return st.session_state.get(_done_key(result_key), False)


def reset_result(result_key: str):
    """result와 완료 플래그를 모두 초기화해 패널을 다시 표시할 수 있게 한다."""
    st.session_state[result_key] = None
    st.session_state[_done_key(result_key)] = False


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
    - 이미 완료된 경우 즉시 True 반환 (빈 결과도 완료 취급, 재호출 없음).
    - Tab 1: Gemini 자동 전송.
    - Tab 2: 프롬프트 복사 후 수동 붙여넣기.
    """
    # sentinel 패턴: 완료 플래그로 체크 → 빈 결과여도 재호출 방지
    if is_done(result_key):
        return True

    show_key = f"_show_{result_key}"
    if show_key not in st.session_state:
        st.session_state[show_key] = False
    if st.button("프롬프트 보기 / 숨기기", key=f"_toggle_{result_key}"):
        st.session_state[show_key] = not st.session_state[show_key]
    if st.session_state[show_key]:
        st.caption("아래 내용을 복사해서 ChatGPT, Claude 등 다른 AI에도 사용할 수 있어요.")
        st.code(prompt, language="text")

    tab_auto, tab_manual = st.tabs(["AI 자동 전송", "직접 붙여넣기"])

    with tab_auto:
        st.caption("Gemini AI가 자동으로 분석합니다.")
        if st.button(btn_label, key=f"_auto_{result_key}", type="primary", use_container_width=True):
            with st.spinner(spinner_text):
                try:
                    result = ask(system, prompt, json_mode=json_mode)
                    st.session_state[result_key] = result
                    st.session_state[_done_key(result_key)] = True
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
                    parsed = json.loads(_extract_json(manual)) if json_mode else manual.strip()
                    st.session_state[result_key] = parsed
                    st.session_state[_done_key(result_key)] = True
                    st.rerun()
                except Exception as e:
                    st.error(f"형식 오류: {e} — JSON 형식인지 확인하거나 AI 자동 전송을 이용해주세요.")
            else:
                st.warning("AI 응답을 입력해주세요.")

    return False
