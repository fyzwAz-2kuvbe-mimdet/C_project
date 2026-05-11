import streamlit as st
from core.step02_initial_analysis import analyze


_PLACEHOLDERS = {
    "초": "예: 공룡이 왜 멸종했는지, 로봇이 움직이는 방법...",
    "중": "예: 인공지능의 원리, 환경 문제와 경제 성장...",
    "고": "예: 양자컴퓨팅 큐비트 원리, 빅데이터와 직업윤리...",
}


def render():
    if st.button("← 이전"):
        st.session_state.current_step = 1
        st.rerun()

    st.markdown('<div class="section-header">💡 관심 주제 입력</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-subheader">궁금한 주제를 자유롭게 적어주세요. 키워드 하나도 괜찮아요.</div>', unsafe_allow_html=True)

    grade = st.session_state.get("grade", "고1")
    placeholder = _PLACEHOLDERS.get(grade[:1], _PLACEHOLDERS["고"])
    interest = st.text_area("관심 주제", value=st.session_state.get("interest_text", ""),
                            placeholder=placeholder, height=120, label_visibility="collapsed")

    col1, col2 = st.columns([4, 1])
    with col1:
        analyze_btn = st.button("🔍 AI 분석", type="primary", use_container_width=True, disabled=not interest.strip())
    with col2:
        if st.button("초기화", use_container_width=True):
            st.session_state.interest_text = ""
            st.session_state.initial_analysis = None
            st.session_state.step2_confirmed = False
            st.rerun()

    if analyze_btn and interest.strip():
        with st.spinner("AI가 관심사를 분석하고 있어요..."):
            try:
                result = analyze(interest.strip(), grade, st.session_state.learning_type)
                st.session_state.interest_text = interest.strip()
                st.session_state.initial_analysis = result
                st.session_state.step2_confirmed = False
                st.rerun()
            except Exception as e:
                st.error(f"분석 중 오류: {e}")

    analysis = st.session_state.get("initial_analysis")
    if analysis:
        _render_analysis(analysis)


def _render_analysis(analysis: dict):
    subtopic = analysis.get("estimated_subtopic", "")
    depth = analysis.get("depth_level", "")
    rationale = analysis.get("rationale", "")

    depth_colors = {"초급": ("#d1fae5", "#065f46"), "중급": ("#fef3c7", "#92400e"), "고급": ("#ede9fe", "#5b21b6")}
    bg, text = depth_colors.get(depth, ("#f3f4f6", "#374151"))

    st.markdown("---")
    st.markdown("**AI 분석 결과**")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(
            f'<div style="background:#eff6ff;border-radius:10px;padding:14px;">'
            f'<div style="font-size:11px;font-weight:700;color:#3b82f6;margin-bottom:4px;">추정 세부 주제</div>'
            f'<div style="font-size:16px;font-weight:700;color:#1e40af;">{subtopic}</div></div>',
            unsafe_allow_html=True,
        )
    with col2:
        st.markdown(
            f'<div style="background:{bg};border-radius:10px;padding:14px;">'
            f'<div style="font-size:11px;font-weight:700;color:{text};margin-bottom:4px;">학습 깊이</div>'
            f'<div style="font-size:16px;font-weight:700;color:{text};">{depth}</div></div>',
            unsafe_allow_html=True,
        )
    if rationale:
        st.markdown(
            f'<div style="background:#f8fafc;border-radius:8px;padding:12px;font-size:13px;color:#6b7280;margin-top:10px;">💬 {rationale}</div>',
            unsafe_allow_html=True,
        )

    st.markdown("")
    col_yes, col_no = st.columns(2)
    with col_yes:
        if st.button("✅ 맞아요, 다음으로", type="primary", use_container_width=True):
            st.session_state.step2_confirmed = True
            st.session_state.current_step = 3
            # reset downstream
            for k in ["follow_up_questions","user_answers","refined_topic","roadmap",
                      "resources","news_items","extra_resources","news_summaries",
                      "core_questions","question_answers","student_text","feedback","next_step_result"]:
                st.session_state[k] = None if k not in ("user_answers","news_summaries","question_answers") else {}
            st.rerun()
    with col_no:
        if st.button("✏️ 수정할게요", use_container_width=True):
            st.session_state.initial_analysis = None
            st.rerun()
