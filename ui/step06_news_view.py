import streamlit as st
from core.step06_news import get_extra_resources, search_news, summarize_news


def render():
    if st.button("← 이전"):
        st.session_state.current_step = 5
        st.rerun()

    st.markdown('<div class="section-header">📰 뉴스·동향</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-subheader">주제와 관련된 최신 뉴스와 추가 자료예요.</div>', unsafe_allow_html=True)

    grade = st.session_state.get("grade", "고1")
    learning_type = st.session_state.get("learning_type", "hana")
    refined = st.session_state.get("refined_topic") or {}
    topic = refined.get("refined_topic", st.session_state.get("interest_text", ""))

    news_items = st.session_state.get("news_items")
    if news_items is None:
        with st.spinner("최신 뉴스를 가져오고 있어요..."):
            news_items = search_news(topic, max_results=10)
            st.session_state.news_items = news_items

    summaries = st.session_state.get("news_summaries") or {}

    if news_items:
        st.markdown("**최신 뉴스**")
        for idx, item in enumerate(news_items):
            _render_news_card(idx, item, summaries, grade, learning_type)
    else:
        st.info("관련 뉴스를 찾지 못했어요. 검색어를 바꿔 시도해보세요.")

    st.markdown("---")
    _render_extra(topic, grade, learning_type)

    st.markdown("")
    if st.button("❓ 핵심 질문 보기 →", type="primary", use_container_width=True):
        st.session_state.current_step = 7
        st.rerun()


def _render_news_card(idx: int, item: dict, summaries: dict, grade: str, lt: str):
    headline = item.get("headline", "")
    link = item.get("link", "#")
    press = item.get("press", "")
    date = item.get("date", "")
    meta = "  ·  ".join(filter(None, [press, date]))

    st.markdown(
        f'<div class="news-card">'
        f'  <a class="news-headline" href="{link}" target="_blank">{headline}</a>'
        f'  {"<div class=\"news-meta\">" + meta + "</div>" if meta else ""}'
        f'</div>',
        unsafe_allow_html=True,
    )

    col_btn, _ = st.columns([1, 3])
    with col_btn:
        btn_key = f"summarize_{idx}"
        if str(idx) not in summaries:
            if st.button("📋 3줄 요약", key=btn_key, use_container_width=True):
                with st.spinner("요약 중..."):
                    try:
                        s = summarize_news(headline, item.get("summary", ""), grade, lt)
                        summaries[str(idx)] = s
                        st.session_state.news_summaries = summaries
                        st.rerun()
                    except Exception as e:
                        st.error(f"요약 오류: {e}")

    if str(idx) in summaries:
        st.markdown(
            f'<div class="news-summary-box">{summaries[str(idx)]}</div>',
            unsafe_allow_html=True,
        )


def _render_extra(topic: str, grade: str, lt: str):
    extra = st.session_state.get("extra_resources")
    if extra is None:
        with st.spinner("추가 자료를 불러오는 중..."):
            try:
                extra = get_extra_resources(topic, grade, lt)
                st.session_state.extra_resources = extra
            except Exception as e:
                st.error(f"추가 자료 오류: {e}")
                return

    items = extra.get("items", [])
    if not items:
        return

    st.markdown("**유형별 추가 자료**")
    for item in items:
        name = item.get("name", "")
        desc = item.get("description", "")
        url = item.get("url", "")
        link_html = f' &nbsp;<a href="{url}" target="_blank" style="font-size:12px;color:#3b82f6;">🔗 바로가기</a>' if url else ""
        st.markdown(
            f'<div style="background:#f8fafc;border-radius:8px;padding:12px 14px;margin-bottom:8px;">'
            f'  <div style="font-size:14px;font-weight:700;color:#111827;">{name}{link_html}</div>'
            f'  {"<div style=\"font-size:13px;color:#6b7280;margin-top:4px;\">" + desc + "</div>" if desc else ""}'
            f'</div>',
            unsafe_allow_html=True,
        )
