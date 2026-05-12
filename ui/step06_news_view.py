import streamlit as st
from core.step06_news import (
    build_extra_resources_prompt, build_summarize_prompt,
    get_extra_resources, search_news, summarize_news,
)
from utils.ai_runner import prompt_panel


def render():
    if st.button("← 이전"):
        st.session_state.current_step = 5
        st.rerun()

    st.markdown('<div class="section-header">📰 뉴스·동향</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-subheader">주제와 관련된 최신 뉴스와 추가 자료예요.</div>', unsafe_allow_html=True)

    grade = st.session_state.get("grade", "고1")
    lt = st.session_state.get("learning_type", "hana")
    refined = st.session_state.get("refined_topic") or {}
    topic = refined.get("refined_topic", st.session_state.get("interest_text", ""))

    # 뉴스 크롤링 (AI 불필요, 웹 스크래핑)
    news_items = st.session_state.get("news_items")
    if news_items is None:
        with st.spinner("최신 뉴스를 가져오고 있어요..."):
            news_items = search_news(topic, max_results=10)
            st.session_state.news_items = news_items

    summaries = st.session_state.get("news_summaries") or {}

    if news_items:
        st.markdown("**최신 뉴스**")
        for idx, item in enumerate(news_items):
            _render_news_card(idx, item, summaries, grade, lt)
    else:
        st.info("관련 뉴스를 찾지 못했어요.")

    st.markdown("---")
    _render_extra(topic, grade, lt)

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

    if str(idx) not in summaries:
        col_btn, _ = st.columns([1, 3])
        with col_btn:
            # 3줄 요약도 dual mode 지원
            with st.expander("📋 3줄 요약", expanded=False):
                system, prompt = build_summarize_prompt(
                    headline, item.get("summary", ""), grade, lt
                )
                summary_key = f"news_sum_{idx}"
                if prompt_panel(system, prompt, summary_key,
                                json_mode=False,
                                spinner_text="요약 중...",
                                btn_label="요약하기"):
                    summaries[str(idx)] = st.session_state[summary_key]
                    st.session_state.news_summaries = summaries
    else:
        st.markdown(
            f'<div class="news-summary-box">{summaries[str(idx)]}</div>',
            unsafe_allow_html=True,
        )


def _render_extra(topic: str, grade: str, lt: str):
    st.markdown("**유형별 추가 자료**")

    system, prompt = build_extra_resources_prompt(topic, grade, lt)
    if not prompt_panel(system, prompt, "extra_resources",
                        spinner_text="추가 자료를 불러오는 중...",
                        btn_label="추가 자료 불러오기"):
        return

    items = (st.session_state.extra_resources or {}).get("items", [])
    if not items:
        st.caption("추가 자료가 없습니다.")
        return

    for item in items:
        name = item.get("name", item.get("title", ""))
        desc = item.get("description", "")
        url = item.get("url", "")
        link_html = (
            f' &nbsp;<a href="{url}" target="_blank" style="font-size:12px;color:#3b82f6;">🔗 바로가기</a>'
            if url and url != "출처 미확인" else ""
        )
        st.markdown(
            f'<div style="background:#f8fafc;border-radius:8px;padding:12px 14px;margin-bottom:8px;">'
            f'  <div style="font-size:14px;font-weight:700;color:#111827;">{name}{link_html}</div>'
            f'  {"<div style=\"font-size:13px;color:#6b7280;margin-top:4px;\">" + desc + "</div>" if desc else ""}'
            f'</div>',
            unsafe_allow_html=True,
        )
