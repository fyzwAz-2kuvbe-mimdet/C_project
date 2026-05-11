import streamlit as st
from core.step07_core_questions import generate_core_questions


def render():
    if st.button("← 이전"):
        st.session_state.current_step = 6
        st.rerun()

    st.markdown('<div class="section-header">❓ 핵심 탐구 질문</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-subheader">이 질문들에 자신의 생각을 써보세요. 결과물 작성의 뼈대가 됩니다.</div>', unsafe_allow_html=True)

    grade = st.session_state.get("grade", "고1")
    learning_type = st.session_state.get("learning_type", "hana")
    refined = st.session_state.get("refined_topic") or {}
    topic = refined.get("refined_topic", st.session_state.get("interest_text", ""))
    keywords = refined.get("key_concepts", [])

    questions = st.session_state.get("core_questions")
    if not questions:
        with st.spinner("AI가 핵심 탐구 질문을 생성하고 있어요..."):
            try:
                questions = generate_core_questions(topic, keywords, grade, learning_type)
                st.session_state.core_questions = questions
            except Exception as e:
                st.error(f"질문 생성 중 오류: {e}")
                return

    q_answers = st.session_state.get("question_answers") or {}
    new_answers = {}

    for i, q in enumerate(questions):
        st.markdown(
            f'<div style="background:#eff6ff;border-left:5px solid #3b82f6;border-radius:0 10px 10px 0;'
            f'padding:12px 16px;margin-bottom:6px;">'
            f'<div style="font-size:12px;font-weight:700;color:#3b82f6;margin-bottom:4px;">핵심 질문 {i+1}</div>'
            f'<div style="font-size:15px;font-weight:600;color:#1e40af;">{q}</div>'
            f'</div>',
            unsafe_allow_html=True,
        )
        new_answers[str(i)] = st.text_area(
            f"답변 {i+1}", value=q_answers.get(str(i), ""),
            height=100, key=f"cq_{i}", label_visibility="collapsed",
            placeholder="자유롭게 생각을 적어보세요...",
        )
        st.markdown("")

    st.session_state.question_answers = new_answers
    any_answered = any(v.strip() for v in new_answers.values())

    if st.button("✍️ 결과물 작성하기 →", type="primary", use_container_width=True, disabled=not any_answered):
        st.session_state.current_step = 8
        st.rerun()
