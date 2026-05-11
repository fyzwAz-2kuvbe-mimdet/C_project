import streamlit as st
from core.step03_refine_interest import generate_questions, refine_topic


def render():
    if st.button("← 이전"):
        st.session_state.current_step = 2
        st.rerun()

    st.markdown('<div class="section-header">🔎 주제 구체화</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-subheader">몇 가지 질문에 답하면 나만의 탐구 방향이 잡혀요.</div>', unsafe_allow_html=True)

    grade = st.session_state.get("grade", "고1")
    learning_type = st.session_state.get("learning_type", "hana")
    interest = st.session_state.get("interest_text", "")
    analysis = st.session_state.get("initial_analysis", {}) or {}
    subtopic = analysis.get("estimated_subtopic", interest)

    questions = st.session_state.get("follow_up_questions")
    if not questions:
        with st.spinner("AI가 탐구 방향 질문을 생성하고 있어요..."):
            try:
                questions = generate_questions(interest, subtopic, grade, learning_type)
                st.session_state.follow_up_questions = questions
            except Exception as e:
                st.error(f"질문 생성 중 오류: {e}")
                return

    answers = st.session_state.get("user_answers") or {}

    st.markdown("**아래 질문 중 하나 이상에 자유롭게 답해주세요.**")
    new_answers = {}
    for i, q in enumerate(questions):
        val = answers.get(str(i), "")
        new_answers[str(i)] = st.text_area(
            f"Q{i+1}. {q}", value=val, height=80, key=f"qa_{i}"
        )

    any_answered = any(v.strip() for v in new_answers.values())
    st.session_state.user_answers = new_answers

    if st.button("🧭 주제 정제하기", type="primary", use_container_width=True, disabled=not any_answered):
        with st.spinner("AI가 탐구 주제를 정제하고 있어요..."):
            try:
                result = refine_topic(interest, questions, new_answers, grade, learning_type)
                st.session_state.refined_topic = result
                st.session_state.step3_confirmed = False
                st.rerun()
            except Exception as e:
                st.error(f"주제 정제 중 오류: {e}")

    refined = st.session_state.get("refined_topic")
    if refined:
        _render_refined(refined)


def _render_refined(refined: dict):
    topic = refined.get("refined_topic", "")
    angle = refined.get("specific_angle", "")
    goal = refined.get("learning_goal", "")
    keywords = refined.get("key_concepts", [])

    st.markdown("---")
    st.markdown("**정제된 탐구 주제**")

    st.markdown(
        f'<div style="background:#eff6ff;border-left:5px solid #3b82f6;border-radius:0 12px 12px 0;padding:16px 20px;">'
        f'<div style="font-size:11px;font-weight:700;color:#3b82f6;margin-bottom:4px;">확정 주제</div>'
        f'<div style="font-size:18px;font-weight:800;color:#1e40af;">{topic}</div>'
        f'</div>',
        unsafe_allow_html=True,
    )

    col1, col2 = st.columns(2)
    with col1:
        if angle:
            st.markdown(
                f'<div style="background:#f8fafc;border-radius:10px;padding:14px;margin-top:10px;">'
                f'<div style="font-size:11px;font-weight:700;color:#6b7280;margin-bottom:4px;">탐구 각도</div>'
                f'<div style="font-size:14px;color:#374151;">{angle}</div></div>',
                unsafe_allow_html=True,
            )
    with col2:
        if goal:
            st.markdown(
                f'<div style="background:#f8fafc;border-radius:10px;padding:14px;margin-top:10px;">'
                f'<div style="font-size:11px;font-weight:700;color:#6b7280;margin-bottom:4px;">학습 목표</div>'
                f'<div style="font-size:14px;color:#374151;">{goal}</div></div>',
                unsafe_allow_html=True,
            )

    if keywords:
        tags = "".join(
            f'<span style="background:#dbeafe;color:#1d4ed8;border-radius:20px;padding:3px 10px;font-size:12px;font-weight:600;margin:2px;">{kw}</span>'
            for kw in keywords
        )
        st.markdown(
            f'<div style="margin-top:10px;">{tags}</div>',
            unsafe_allow_html=True,
        )

    st.markdown("")
    col_yes, col_no = st.columns(2)
    with col_yes:
        if st.button("✅ 확정, 로드맵 보기", type="primary", use_container_width=True):
            st.session_state.step3_confirmed = True
            st.session_state.current_step = 4
            for k in ["roadmap", "resources", "news_items", "extra_resources",
                      "news_summaries", "core_questions", "question_answers",
                      "student_text", "feedback", "next_step_result"]:
                st.session_state[k] = None if k not in ("news_summaries", "question_answers") else {}
            st.rerun()
    with col_no:
        if st.button("✏️ 다시 정제", use_container_width=True):
            st.session_state.refined_topic = None
            st.rerun()
