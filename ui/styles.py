import streamlit as st

_CSS = """
<link rel="stylesheet"
  href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard/dist/web/static/pretendard.css">
<style>
*, *::before, *::after {
  font-family: 'Pretendard', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif !important;
  letter-spacing: -0.01em;
}
body { background: #fafafa; }

.main .block-container {
  max-width: 800px;
  padding-top: 1rem;
  padding-bottom: 5rem;
}

/* ── Stepper (progress bar) — 인라인 스타일로 렌더링, CSS 불필요 ── */

/* ── Cards ── */
.coach-card {
  background: #fff;
  border: 1px solid #e5e7eb;
  border-radius: 12px;
  padding: 24px;
  margin-bottom: 16px;
  box-shadow: 0 1px 3px rgba(0,0,0,.04);
}

/* ── Roadmap timeline ── */
.roadmap-item {
  display: flex; gap: 16px; margin-bottom: 20px; position: relative;
}
.roadmap-line {
  display: flex; flex-direction: column; align-items: center;
}
.roadmap-dot {
  width: 36px; height: 36px; border-radius: 50%;
  background: #3b82f6; color: #fff;
  display: flex; align-items: center; justify-content: center;
  font-weight: 700; font-size: 14px; flex-shrink: 0;
}
.roadmap-connector {
  width: 2px; flex: 1; background: #e5e7eb; margin: 4px 0;
  min-height: 24px;
}
.roadmap-content {
  flex: 1; padding-bottom: 8px;
}
.roadmap-goal { font-size: 15px; font-weight: 700; color: #111827; margin-bottom: 6px; }
.roadmap-meta { font-size: 12px; color: #6b7280; }

/* ── Resource cards ── */
.resource-card {
  background: #fff; border: 1px solid #e5e7eb; border-radius: 10px;
  padding: 16px; margin-bottom: 10px;
  transition: transform .15s, box-shadow .15s;
}
.resource-card:hover { transform: translateY(-2px); box-shadow: 0 4px 12px rgba(0,0,0,.08); }
.badge { display: inline-block; padding: 2px 9px; border-radius: 20px; font-size: 11px; font-weight: 700; }
.badge-책    { background: #dbeafe; color: #1d4ed8; }
.badge-사이트 { background: #d1fae5; color: #065f46; }
.badge-논문  { background: #ede9fe; color: #5b21b6; }
.badge-영상  { background: #fef3c7; color: #92400e; }
.badge-기타  { background: #f3f4f6; color: #374151; }

/* ── News cards ── */
.news-card {
  background: #fff; border: 1px solid #e5e7eb; border-radius: 10px;
  padding: 14px 18px; margin-bottom: 10px;
}
.news-headline { font-size: 15px; font-weight: 600; color: #111827; text-decoration: none; line-height: 1.5; }
.news-headline:hover { color: #3b82f6; }
.news-meta { font-size: 12px; color: #9ca3af; margin-top: 4px; }
.news-summary-box {
  background: #f0f9ff; border-left: 3px solid #3b82f6;
  border-radius: 0 8px 8px 0; padding: 10px 14px;
  font-size: 13px; color: #374151; line-height: 1.6; margin-top: 10px;
}

/* ── Score bars ── */
.score-bar-bg { background: #f3f4f6; border-radius: 999px; height: 8px; overflow: hidden; margin-top: 4px; }
.score-bar-fill { height: 100%; border-radius: 999px; transition: width .5s ease; }

/* ── Section headings ── */
.section-header    { font-size: 22px; font-weight: 800; color: #111827; margin-bottom: 4px; }
.section-subheader { font-size: 14px; color: #6b7280; margin-bottom: 20px; }

/* ── Type cards ── */
.type-card {
  background: #fff; border: 2px solid #e5e7eb; border-radius: 12px;
  padding: 18px; cursor: pointer;
  transition: transform .15s, box-shadow .15s, border-color .15s;
}
.type-card:hover { transform: translateY(-2px); box-shadow: 0 4px 12px rgba(0,0,0,.09); }
.type-card.selected { border-width: 2px; }

/* ── Streamlit overrides ── */
div[data-testid="stButton"] button { border-radius: 8px; font-weight: 600; transition: transform .1s; }
div[data-testid="stButton"] button:hover { transform: translateY(-1px); }
div[data-testid="stTextArea"] textarea { border-radius: 8px; border-color: #e5e7eb; font-size: 14px; }

#MainMenu, footer { visibility: hidden; }
</style>
"""


def inject_css():
    st.markdown(_CSS, unsafe_allow_html=True)
