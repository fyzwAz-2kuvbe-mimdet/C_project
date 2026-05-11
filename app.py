import streamlit as st

st.set_page_config(
    page_title="AI 학습 코치",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)

from ui.styles import inject_css, render_step_indicator  # noqa: E402 — after set_page_config
from ui.sidebar import render_sidebar
from ui.step1_interest import render_step1
from ui.step2_resources import render_step2
from ui.step3_news import render_step3
from ui.step4_feedback import render_step4
from utils.session import init_session, generate_download_report

# ── CSS must be first ──
inject_css()

# ── API key guard ──
if "GEMINI_API_KEY" not in st.secrets:
    st.error("⚠️ GEMINI_API_KEY가 설정되지 않았습니다. .streamlit/secrets.toml을 확인하세요.")
    st.info(
        """**설정 방법**
1. `.streamlit/secrets.toml.example` 파일을 복사해 `.streamlit/secrets.toml`로 저장하세요.
2. 파일 안의 `your_gemini_api_key_here`를 실제 키로 교체하세요.
3. API 키는 [Google AI Studio](https://aistudio.google.com/app/apikey)에서 무료 발급받을 수 있습니다."""
    )
    st.stop()

# ── Session state ──
init_session()

# ── Sidebar ──
with st.sidebar:
    render_sidebar()

# ── Step indicator ──
render_step_indicator(st.session_state.current_step)

# ── Step routing ──
step = st.session_state.current_step
if step == 1:
    render_step1()
elif step == 2:
    render_step2()
elif step == 3:
    render_step3()
elif step == 4:
    render_step4()

# ── Download report (available from step 2 onwards after resources loaded) ──
if st.session_state.get("step2_complete") or st.session_state.get("feedback"):
    st.markdown("---")
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        report = generate_download_report()
        safe_name = st.session_state.get("interest_text", "학습")[:20].replace(" ", "_")
        st.download_button(
            label="📄 전체 학습 리포트 다운로드 (.md)",
            data=report,
            file_name=f"학습리포트_{safe_name}.md",
            mime="text/markdown",
            use_container_width=True,
        )
