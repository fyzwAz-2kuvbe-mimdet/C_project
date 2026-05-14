import streamlit as st
from core.step10_next_step import build_prompt
from utils.ai_runner import prompt_panel
from utils.markdown_export import build_markdown


def render():
    if st.button("← 이전"):
        st.session_state.current_step = 9
        st.rerun()

    st.markdown('<div class="section-header">성찰·저장</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-subheader">탐구 여정을 마무리하고 다음 방향을 확인해요.</div>', unsafe_allow_html=True)

    grade = st.session_state.get("grade", "고1")
    lt = st.session_state.get("learning_type", "hana")
    refined = st.session_state.get("refined_topic") or {}
    topic = refined.get("refined_topic", st.session_state.get("interest_text", ""))
    feedback = st.session_state.get("feedback") or {}
    overall_score = feedback.get("overall_score", 0)

    system, prompt = build_prompt(topic, overall_score, grade, lt)
    if not prompt_panel(system, prompt, "next_step_result",
                        spinner_text="AI가 다음 탐구 방향을 제안하고 있어요...",
                        btn_label="다음 방향 제안받기"):
        return

    next_result = st.session_state.next_step_result
    if next_result:
        _render_next(next_result)

    st.divider()
    _render_reflection()
    st.divider()
    _render_download(topic)


def _render_next(nr: dict):
    next_dir = nr.get("next_direction", nr.get("next_topic", ""))
    expansion = nr.get("expansion_topics", [])
    activities = nr.get("suggested_activities", [])

    if next_dir:
        st.markdown("**다음 탐구 방향**")
        st.markdown(
            f'<div style="background:#f0faf8;border-left:5px solid #0d9488;border-radius:0 12px 12px 0;'
            f'padding:16px 20px;margin-bottom:12px;">'
            f'<div style="font-size:15px;font-weight:600;color:#0a5c52;line-height:1.6;">{next_dir}</div>'
            f'</div>',
            unsafe_allow_html=True,
        )

    if expansion:
        st.markdown("**확장 주제**")
        tags_html = ""
        for t in expansion:
            if isinstance(t, dict):
                label = t.get("topic", "")
                conn = t.get("connection", "")
                tags_html += (
                    f'<span title="{conn}" style="background:#ccede9;color:#0a5c52;border-radius:20px;'
                    f'padding:4px 12px;font-size:13px;font-weight:600;margin:3px;display:inline-block;'
                    f'cursor:default;">{label}</span>'
                )
            else:
                tags_html += (
                    f'<span style="background:#ccede9;color:#0a5c52;border-radius:20px;'
                    f'padding:4px 12px;font-size:13px;font-weight:600;margin:3px;display:inline-block;">{t}</span>'
                )
        st.markdown(f'<div style="margin-bottom:12px;">{tags_html}</div>', unsafe_allow_html=True)

    if activities:
        st.markdown("**추천 활동**")
        for act in activities:
            st.markdown(
                f'<div style="background:#f8fafc;border-radius:8px;padding:10px 14px;margin-bottom:6px;'
                f'font-size:13px;color:#374151;">→ {act}</div>',
                unsafe_allow_html=True,
            )


def _render_reflection():
    st.markdown("**자기 성찰 노트**")
    reflection = st.text_area(
        "성찰",
        value=st.session_state.get("reflection_text", ""),
        height=150,
        placeholder="이번 탐구에서 무엇을 배웠나요? 어떤 점이 어려웠고, 무엇이 흥미로웠나요?",
        label_visibility="collapsed",
    )
    st.session_state.reflection_text = reflection


def _render_download(topic: str):
    st.markdown("**전체 학습 기록 다운로드**")
    md = build_markdown()
    fname = f"학습기록_{topic[:20].replace(' ', '_')}.md"
    st.download_button(
        label="마크다운으로 내보내기",
        data=md.encode("utf-8"),
        file_name=fname,
        mime="text/markdown",
        use_container_width=True,
    )
    st.caption("마크다운(.md) 파일은 Notion, Obsidian, VS Code 등에서 바로 열 수 있어요.")
