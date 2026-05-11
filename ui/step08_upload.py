import streamlit as st
from utils.file_loader import load_text_from_file

_FORMATS = ["에세이", "보고서", "발표자료 개요", "연구계획서", "자유 서술"]


def render():
    if st.button("← 이전"):
        st.session_state.current_step = 7
        st.rerun()

    st.markdown('<div class="section-header">✍️ 결과물 작성</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-subheader">탐구한 내용을 정리해서 올려주세요. AI가 꼼꼼히 첨삭해줄 거예요.</div>', unsafe_allow_html=True)

    fmt = st.selectbox(
        "결과물 형식",
        _FORMATS,
        index=_FORMATS.index(st.session_state.get("format_type", "에세이")) if st.session_state.get("format_type") in _FORMATS else 0,
    )
    st.session_state.format_type = fmt

    st.markdown("**작성 방식**")
    tab_text, tab_file = st.tabs(["직접 입력", "파일 업로드 (PDF / DOCX / TXT)"])

    with tab_text:
        text_val = st.session_state.get("student_text", "")
        new_text = st.text_area(
            "결과물 내용",
            value=text_val,
            height=300,
            placeholder="탐구 과정에서 작성한 내용을 붙여넣거나 여기서 바로 작성하세요.",
            label_visibility="collapsed",
        )
        if new_text != text_val:
            st.session_state.student_text = new_text

    with tab_file:
        uploaded = st.file_uploader("파일 선택", type=["pdf", "docx", "txt"], label_visibility="collapsed")
        if uploaded:
            try:
                file_text = load_text_from_file(uploaded)
                st.session_state.student_text = file_text
                st.success(f"파일 로드 완료 ({len(file_text):,}자)")
                st.text_area("미리보기", value=file_text[:500] + ("..." if len(file_text) > 500 else ""),
                             height=150, disabled=True, label_visibility="collapsed")
            except Exception as e:
                st.error(f"파일 로드 오류: {e}")

    student_text = st.session_state.get("student_text", "")
    char_count = len(student_text.strip())
    st.caption(f"현재 {char_count:,}자 입력됨")

    if st.button("🤖 AI 첨삭 받기 →", type="primary", use_container_width=True, disabled=char_count < 50):
        if char_count < 50:
            st.warning("최소 50자 이상 작성해주세요.")
        else:
            st.session_state.feedback = None
            st.session_state.current_step = 9
            st.rerun()
