import streamlit as st
from core.step05_resources import recommend
import urllib.parse


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
    learning_type = st.session_state.get("learning_type", "hana")
    refined = st.session_state.get("refined_topic") or {}
    topic = refined.get("refined_topic", st.session_state.get("interest_text", ""))
    roadmap = st.session_state.get("roadmap") or []

    resources = st.session_state.get("resources")
    if not resources:
        with st.spinner("AI가 단계별 자료를 추천하고 있어요..."):
            try:
                resources = recommend(roadmap, topic, grade, learning_type)
                st.session_state.resources = resources
            except Exception as e:
                st.error(f"자료 추천 중 오류: {e}")
                return

    _render_resources(resources, roadmap)

    st.markdown("")
    if st.button("📰 뉴스·동향 보기 →", type="primary", use_container_width=True):
        st.session_state.current_step = 6
        st.rerun()


def _render_resources(resources: dict, roadmap: list):
    per_step = resources.get("per_step", {})
    general = resources.get("general", [])

    for i, step in enumerate(roadmap):
        step_num = str(step.get("step_number", i + 1))
        step_title = step.get("step_title", f"단계 {i+1}")
        step_items = per_step.get(step_num, per_step.get(str(i+1), []))

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
    desc = item.get("description", "")
    url = item.get("url", "")
    is_search = item.get("is_search_link", False)

    bg, fg = _TYPE_COLORS.get(rtype, _TYPE_COLORS["기타"])
    badge = f'<span class="badge" style="background:{bg};color:{fg};">{rtype}</span>'
    caveat = (
        ' <span style="font-size:10px;color:#9ca3af;">(검색 링크 — 실존 확인 필요)</span>'
        if is_search else ""
    )

    if not url:
        url = _auto_url(rtype, title, author)
        is_search = True

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
