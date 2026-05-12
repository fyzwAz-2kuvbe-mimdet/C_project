import streamlit as st
from core.step04_roadmap import build_prompt
from utils.ai_runner import prompt_panel, reset_result


def render():
    if st.button("← 이전"):
        st.session_state.current_step = 3
        st.rerun()

    st.markdown('<div class="section-header">🗺️ 학습 로드맵</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-subheader">AI가 설계한 단계별 탐구 여정이에요.</div>', unsafe_allow_html=True)

    grade = st.session_state.get("grade", "고1")
    lt = st.session_state.get("learning_type", "hana")
    refined = st.session_state.get("refined_topic") or {}
    topic = refined.get("refined_topic", st.session_state.get("interest_text", ""))
    keywords = refined.get("key_concepts", [])

    system, prompt = build_prompt(topic, keywords, grade, lt)
    if not prompt_panel(system, prompt, "roadmap",
                        spinner_text="AI가 학습 로드맵을 설계하고 있어요...",
                        btn_label="🗺️ 로드맵 생성하기"):
        return

    roadmap = st.session_state.roadmap
    if not isinstance(roadmap, list) or not roadmap:
        st.warning("로드맵 데이터가 올바르지 않아요. 다시 생성해주세요.")
        if st.button("다시 생성"):
            reset_result("roadmap")
            st.rerun()
        return

    _render_roadmap(roadmap)

    st.markdown("")
    if st.button("📚 학습 자료 추천받기 →", type="primary", use_container_width=True):
        st.session_state.current_step = 5
        st.rerun()


def _render_roadmap(roadmap: list):
    items = []
    for i, step in enumerate(roadmap):
        title = step.get("step_title") or step.get("goal", f"단계 {i+1}")
        goal = step.get("goal", "")
        duration = step.get("estimated_hours", step.get("duration", ""))
        activities = step.get("activities", [])
        prereq = step.get("prerequisite", "")
        is_last = i == len(roadmap) - 1

        connector = "" if is_last else '<div class="roadmap-connector"></div>'
        act_html = "".join(f'<li style="font-size:13px;color:#6b7280;margin-bottom:2px;">{a}</li>' for a in activities)
        acts = f'<ul style="margin:6px 0 0 0;padding-left:18px;">{act_html}</ul>' if activities else ""
        pre_html = (
            f'<div style="font-size:11px;color:#9ca3af;margin-top:4px;">사전 지식: {prereq}</div>'
            if prereq and prereq != "없음" else ""
        )

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
            f'    {pre_html}'
            f'    {acts}'
            f'  </div>'
            f'</div>'
        )

    st.markdown("".join(items), unsafe_allow_html=True)
