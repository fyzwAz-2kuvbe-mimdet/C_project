import streamlit as st

_DEFAULTS = {
    "current_step": 1,
    "grade": "고1",
    "learning_type": "hana",
    # step 2
    "interest_text": "",
    "initial_analysis": None,
    "step2_confirmed": False,
    # step 3
    "follow_up_questions": None,
    "user_answers": {},
    "q3_idx": 0,
    "refined_topic": None,
    "step3_confirmed": False,
    # step 4
    "roadmap": None,
    # step 5
    "resources": None,
    # step 6
    "news_items": None,
    "extra_resources": None,
    "news_summaries": {},
    # step 7
    "core_questions": None,
    "question_answers": {},
    "q7_idx": 0,
    # step 8
    "student_text": "",
    "format_type": "에세이",
    # step 9
    "feedback": None,
    # step 10
    "next_step_result": None,
    "reflection_text": "",
}


def init_session():
    for key, val in _DEFAULTS.items():
        if key not in st.session_state:
            st.session_state[key] = val


def reset_all():
    for key, val in _DEFAULTS.items():
        st.session_state[key] = val
