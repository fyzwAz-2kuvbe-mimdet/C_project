import streamlit as st
from core.step04_roadmap import build_roadmap


def render():
    if st.button("← 이전"):
        st.session_state.current_step = 3
        st.rerun()

    st.markdown('<div class="section-header">🗺️ 학습 로드맵</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-subheader">AI가 설계한 단계별 탐구 여정이에요.</div>', unsafe_allow_html=True)

    grade = st.session_state.get("grade", "고1")
    learning_type = st.session_state.get("learning_type", "hana")
    refined = st.session_state.get("refined_topic") or {}
    topic = refined.get("refined_topic", st.session_state.get("interest_text", ""))
    keywords = refined.get("key_concepts", [])

    roadmap = st.session_state.get("roadmap")
    if not roadmap:
        with st.spinner("AI가 학습 로드맵을 설계하고 있어요..."):
            try:
                roadmap = build_roadmap(topic, keywords, grade, learning_type)
                st.session_state.roadmap = roadmap
            except Exception as e:
                st.error(f"로드맵 생성 중 오류: {e}")
                return

    _render_roadmap(roadmap)

    st.markdown("")
    if st.button("📚 학습 자료 추천받기 →", type="primary", use_container_width=True):
        st.session_state.current_step = 5
        st.rerun()


def _render_roadmap(roadmap: list):
    items = []
    for i, step in enumerate(roadmap):
        title = step.get("step_title", f"단계 {i+1}")
        goal = step.get("goal", "")
        duration = step.get("duration", "")
        activities = step.get("activities", [])
        is_last = i == len(roadmap) - 1

        connector = "" if is_last else '<div class="roadmap-connector"></div>'
        act_html = "".join(f'<li style="font-size:13px;color:#6b7280;margin-bottom:2px;">{a}</li>' for a in activities)
        acts = f'<ul style="margin:6px 0 0 0;padding-left:18px;">{act_html}</ul>' if activities else ""

        items.append(
            f'<div class="roadmap-item">'
            f'  <div class="roadmap-line">'
            f'    <div class="roadmap-dot">{i+1}</div>'
            f'    {connector}'
            f'  </div>'
            f'  <div class="roadmap-content">'
            f'    <div class="roadmap-goal">{title}</div>'
            f'    <div class="roadmap-meta">{goal}'
            f'      {"&nbsp;·&nbsp;<strong>" + duration + "</strong>" if duration else ""}'
            f'    </div>'
            f'    {acts}'
            f'  </div>'
            f'</div>'
        )

    st.markdown("".join(items), unsafe_allow_html=True)
