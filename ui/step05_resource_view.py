import streamlit as st
import urllib.parse
from core.step05_resources import build_prompt
from utils.ai_runner import prompt_panel, reset_result

_TYPE_COLORS = {
    "책": ("#dbeafe", "#1d4ed8"),
    "사이트": ("#d1fae5", "#065f46"),
    "논문": ("#ede9fe", "#5b21b6"),
    "영상": ("#fef3c7", "#92400e"),
    "기타": ("#f3f4f6", "#374151"),
}


def render():
    if st.button("← 이전"):
        st.session_state.current_step = 4
        st.rerun()

    st.markdown('<div class="section-header">📚 학습 자료 추천</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-subheader">로드맵 단계별 맞춤 자료를 모았어요.</div>', unsafe_allow_html=True)

    grade = st.session_state.get("grade", "고1")
    lt = st.session_state.get("learning_type", "hana")
    refined = st.session_state.get("refined_topic") or {}
    topic = refined.get("refined_topic", st.session_state.get("interest_text", ""))
    roadmap = st.session_state.get("roadmap") or []

    system, prompt = build_prompt(roadmap, topic, grade, lt)
    if not prompt_panel(system, prompt, "resources",
                        spinner_text="AI가 단계별 자료를 추천하고 있어요...",
                        btn_label="📚 자료 추천받기"):
        return

    resources = st.session_state.resources
    if not isinstance(resources, dict):
        st.warning("자료 데이터가 올바르지 않아요. 다시 생성해주세요.")
        if st.button("다시 생성"):
            reset_result("resources")
            st.rerun()
        return

    _render_resources(resources, roadmap)

    st.markdown("")
    if st.button("📰 뉴스·동향 보기 →", type="primary", use_container_width=True):
        st.session_state.current_step = 6
        st.rerun()


def _render_resources(resources: dict, roadmap: list):
    per_step = resources.get("per_step", {})
    general = resources.get("general", [])

    # AI가 단계별로 키를 숫자 문자열로 반환하면 그대로 사용, 없으면 로드맵 순서 기준
    for i, step in enumerate(roadmap):
        step_num = str(step.get("step_number", i + 1))
        step_title = step.get("step_title") or step.get("goal", f"단계 {i+1}")
        step_items = per_step.get(step_num, per_step.get(str(i + 1), []))

        with st.expander(f"**{i+1}단계: {step_title}**  ({len(step_items)}개)", expanded=(i == 0)):
            if step_items:
                for item in step_items:
                    _render_card(item)
            else:
                st.caption("추천 자료가 없습니다.")

    if general:
        with st.expander("**공통 추천 자료**", expanded=False):
            for item in general:
                _render_card(item)


def _render_card(item: dict):
    rtype = item.get("type", "기타")
    title = item.get("title", "")
    author = item.get("author", "")
    desc = item.get("description", item.get("why", ""))
    url = item.get("url", item.get("source_url", ""))

    bg, fg = _TYPE_COLORS.get(rtype, _TYPE_COLORS["기타"])
    badge = f'<span class="badge" style="background:{bg};color:{fg};">{rtype}</span>'

    is_search = not url or url == "출처 미확인"
    if is_search:
        url = _auto_url(rtype, title, author)
    caveat = (
        ' <span style="font-size:10px;color:#9ca3af;">(검색 링크)</span>'
        if is_search and url else ""
    )
    link_html = (
        f'<a href="{url}" target="_blank" style="color:#3b82f6;font-weight:600;font-size:13px;">'
        f'🔗 바로가기{caveat}</a>'
        if url else ""
    )

    st.markdown(
        f'<div class="resource-card">'
        f'  {badge}'
        f'  <div style="font-size:15px;font-weight:700;color:#111827;margin:6px 0 2px;">{title}</div>'
        f'  {"<div style=\"font-size:12px;color:#6b7280;margin-bottom:4px;\">" + author + "</div>" if author else ""}'
        f'  {"<div style=\"font-size:13px;color:#374151;margin-bottom:6px;\">" + desc + "</div>" if desc else ""}'
        f'  {link_html}'
        f'</div>',
        unsafe_allow_html=True,
    )


def _auto_url(rtype: str, title: str, author: str) -> str:
    q = urllib.parse.quote(f"{title} {author}".strip())
    if rtype == "책":
        return f"https://www.aladin.co.kr/search/wsearchresult.aspx?SearchWord={q}"
    if rtype == "논문":
        return f"https://scholar.google.com/scholar?q={q}"
    if rtype == "영상":
        return f"https://www.youtube.com/results?search_query={q}"
    if rtype == "사이트":
        return f"https://www.google.com/search?q={q}"
    return ""
