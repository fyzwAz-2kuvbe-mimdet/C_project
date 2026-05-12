import streamlit as st

st.set_page_config(
    page_title="AI 학습 멘토",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)

from ui.styles import inject_css
from ui.progress import render_progress
from ui.sidebar import render_sidebar
from ui.step01_type_grade import render as step01
from ui.step02_interest_input import render as step02
from ui.step03_follow_up import render as step03
from ui.step04_roadmap_view import render as step04
from ui.step05_resource_view import render as step05
from ui.step06_news_view import render as step06
from ui.step07_question_view import render as step07
from ui.step08_upload import render as step08
from ui.step09_feedback_view import render as step09
from ui.step10_summary import render as step10
from utils.session import init_session

inject_css()

if "GEMINI_API_KEY" not in st.secrets:
    st.error("⚠️ GEMINI_API_KEY가 설정되지 않았습니다.")
    st.info(
        "Streamlit Cloud → Settings → Secrets에서 `GEMINI_API_KEY = \"your_key\"`를 추가하세요.\n\n"
        "API 키는 [Google AI Studio](https://aistudio.google.com/app/apikey)에서 무료 발급받을 수 있습니다."
    )
    st.stop()

init_session()

# ── Progress bar 클릭 → 단계 이동 ──────────────────────────────────
_nav = st.query_params.get("nav_to")
if _nav is not None:
    try:
        _target = int(_nav)
        _cur = st.session_state.get("current_step", 1)
        if 1 <= _target <= 10:
            st.session_state.current_step = _target
    except (ValueError, TypeError):
        pass
    st.query_params.clear()
    st.rerun()

with st.sidebar:
    render_sidebar()

step = st.session_state.get("current_step", 1)
render_progress(step)

_STEPS = {
    1: step01, 2: step02, 3: step03, 4: step04, 5: step05,
    6: step06, 7: step07, 8: step08, 9: step09, 10: step10,
}
_STEPS.get(step, step01)()
