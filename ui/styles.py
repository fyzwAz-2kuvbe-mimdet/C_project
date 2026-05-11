import streamlit as st

_CSS = """
<link rel="stylesheet"
  href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard/dist/web/static/pretendard.css">

<style>
/* ── Global ── */
*, *::before, *::after {
  font-family: 'Pretendard', -apple-system, BlinkMacSystemFont,
               'Segoe UI', sans-serif !important;
  letter-spacing: -0.01em;
}
body { background: #fafafa; }

/* ── Main container ── */
.main .block-container {
  max-width: 800px;
  padding-top: 1.5rem;
  padding-bottom: 5rem;
}

/* ── Step indicator ── */
.step-wrapper {
  display: flex;
  justify-content: center;
  padding: 20px 0 28px;
}
.step-row {
  display: flex;
  align-items: center;
}
.step-node {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 6px;
  min-width: 72px;
}
.step-circle {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 15px;
  font-weight: 700;
  background: #e5e7eb;
  color: #9ca3af;
  transition: background 0.25s, box-shadow 0.25s;
}
.step-node.active .step-circle {
  background: #3b82f6;
  color: #fff;
  box-shadow: 0 0 0 5px rgba(59,130,246,.15);
}
.step-node.done .step-circle {
  background: #10b981;
  color: #fff;
}
.step-label {
  font-size: 11px;
  font-weight: 600;
  color: #9ca3af;
  white-space: nowrap;
}
.step-node.active .step-label { color: #3b82f6; }
.step-node.done .step-label   { color: #10b981; }
.step-connector {
  width: 72px;
  height: 2px;
  background: #e5e7eb;
  margin-bottom: 22px;
  flex-shrink: 0;
}
.step-connector.done { background: #10b981; }

/* ── Cards ── */
.coach-card {
  background: #fff;
  border: 1px solid #e5e7eb;
  border-radius: 12px;
  padding: 24px;
  margin-bottom: 16px;
  box-shadow: 0 1px 3px rgba(0,0,0,.04), 0 1px 2px rgba(0,0,0,.06);
}

/* ── Resource cards ── */
.resource-card {
  background: #fff;
  border: 1px solid #e5e7eb;
  border-radius: 12px;
  padding: 20px;
  height: 100%;
  transition: transform .15s, box-shadow .15s;
}
.resource-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 14px rgba(0,0,0,.09);
}
.resource-badge {
  display: inline-block;
  padding: 3px 10px;
  border-radius: 20px;
  font-size: 11px;
  font-weight: 700;
  margin-bottom: 10px;
}
.badge-책    { background: #dbeafe; color: #1d4ed8; }
.badge-사이트 { background: #d1fae5; color: #065f46; }
.badge-논문  { background: #ede9fe; color: #5b21b6; }
.badge-영상  { background: #fef3c7; color: #92400e; }
.badge-기타  { background: #f3f4f6; color: #374151; }
.resource-title {
  font-size: 15px;
  font-weight: 700;
  color: #111827;
  margin-bottom: 8px;
  line-height: 1.45;
}
.resource-why {
  font-size: 13px;
  color: #374151;
  line-height: 1.55;
  margin-bottom: 10px;
}

/* ── News cards ── */
.news-card {
  background: #fff;
  border: 1px solid #e5e7eb;
  border-radius: 10px;
  padding: 16px 20px;
  margin-bottom: 10px;
  transition: box-shadow .15s;
}
.news-card:hover { box-shadow: 0 2px 10px rgba(0,0,0,.08); }
.news-headline {
  font-size: 15px;
  font-weight: 600;
  color: #111827;
  text-decoration: none;
  line-height: 1.5;
}
.news-headline:hover { color: #3b82f6; }
.news-meta    { font-size: 12px; color: #9ca3af; margin-top: 4px; }
.news-summary { font-size: 13px; color: #6b7280; margin-top: 8px; line-height: 1.55; }

/* ── Score bars ── */
.score-bar-bg {
  background: #f3f4f6;
  border-radius: 999px;
  height: 8px;
  overflow: hidden;
  margin-top: 4px;
}
.score-bar-fill {
  height: 100%;
  border-radius: 999px;
  transition: width .5s ease;
}

/* ── Section headings ── */
.section-header    { font-size: 22px; font-weight: 800; color: #111827; margin-bottom: 4px; }
.section-subheader { font-size: 14px; color: #6b7280; margin-bottom: 20px; }

/* ── Streamlit widget tweaks ── */
div[data-testid="stButton"] button {
  border-radius: 8px;
  font-weight: 600;
  transition: transform .1s;
}
div[data-testid="stButton"] button:hover { transform: translateY(-1px); }
div[data-testid="stTextArea"] textarea {
  border-radius: 8px;
  border-color: #e5e7eb;
  font-size: 14px;
  line-height: 1.6;
}
div[data-testid="stTextArea"] textarea:focus {
  border-color: #3b82f6;
  box-shadow: 0 0 0 3px rgba(59,130,246,.1);
}

#MainMenu { visibility: hidden; }
footer    { visibility: hidden; }
</style>
"""


def inject_css():
    st.markdown(_CSS, unsafe_allow_html=True)


def render_step_indicator(current_step: int):
    steps = [("1", "관심사"), ("2", "자료"), ("3", "뉴스"), ("4", "첨삭")]
    html_parts = []

    for i, (num, label) in enumerate(steps):
        if i + 1 < current_step:
            cls, circle = "done", "✓"
        elif i + 1 == current_step:
            cls, circle = "active", num
        else:
            cls, circle = "", num

        html_parts.append(
            f'<div class="step-node {cls}">'
            f'  <div class="step-circle">{circle}</div>'
            f'  <div class="step-label">{label}</div>'
            f"</div>"
        )
        if i < len(steps) - 1:
            conn_cls = "done" if i + 1 < current_step else ""
            html_parts.append(f'<div class="step-connector {conn_cls}"></div>')

    st.markdown(
        f'<div class="step-wrapper"><div class="step-row">{"".join(html_parts)}</div></div>',
        unsafe_allow_html=True,
    )
