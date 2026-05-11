import streamlit as st
from config.learning_types import get_type

_DEFAULTS = {
    "current_step": 1,
    "grade": "고1",
    "learning_type": "hana",
    "interest_text": "",
    "follow_up_questions": [],
    "user_answers": {},
    "diagnosis": {},
    "resources": None,
    "news_items": None,
    "student_text": "",
    "feedback": None,
    "step1_complete": False,
    "step2_complete": False,
    "step3_complete": False,
}


def init_session():
    for key, value in _DEFAULTS.items():
        if key not in st.session_state:
            st.session_state[key] = value


def reset_from_step(step: int):
    if step <= 1:
        st.session_state.interest_text = ""
        st.session_state.follow_up_questions = []
        st.session_state.user_answers = {}
        st.session_state.diagnosis = {}
        st.session_state.step1_complete = False
    if step <= 2:
        st.session_state.resources = None
        st.session_state.step2_complete = False
    if step <= 3:
        st.session_state.news_items = None
        st.session_state.step3_complete = False
    if step <= 4:
        st.session_state.student_text = ""
        st.session_state.feedback = None


def generate_download_report() -> str:
    grade = st.session_state.get("grade", "")
    type_info = get_type(st.session_state.get("learning_type", "hana"))
    diagnosis = st.session_state.get("diagnosis", {})

    lines = [
        "# AI 학습 코치 리포트",
        "",
        f"**학년:** {grade}",
        f"**학습 유형:** {type_info.get('name', '')} ({type_info.get('core', '')})",
        "",
        "---",
        "",
        "## 1. 관심 주제",
        st.session_state.get("interest_text", ""),
        "",
    ]

    if diagnosis.get("estimated_subtopic"):
        lines += [
            f"**세부 주제:** {diagnosis['estimated_subtopic']}",
            f"**깊이 수준:** {diagnosis.get('depth_level', '')}",
            "",
        ]

    questions = st.session_state.get("follow_up_questions", [])
    answers = st.session_state.get("user_answers", {})
    if questions and answers:
        lines += ["## 2. 탐구 질문 & 답변", ""]
        for i, q in enumerate(questions):
            lines.append(f"**Q{i+1}. {q}**")
            lines.append(f"A: {answers.get(str(i), '')}")
            lines.append("")

    resources = st.session_state.get("resources") or []
    if resources:
        lines += ["## 3. 추천 학습 자료", ""]
        for r in resources:
            lines += [
                f"### {r.get('title', '')}",
                f"- **유형:** {r.get('type', '')} | **수준:** {r.get('level', '')}",
                f"- **추천 이유:** {r.get('why', '')}",
                f"- **출처:** {r.get('source_url', '')}",
                f"- **예상 학습 시간:** {r.get('duration', '')}",
                "",
            ]

    news_items = st.session_state.get("news_items") or []
    if news_items:
        lines += ["## 4. 최신 뉴스", ""]
        for n in news_items:
            lines.append(
                f"- [{n.get('headline', '')}]({n.get('link', '')}) — {n.get('press', '')} ({n.get('date', '')})"
            )
        lines.append("")

    feedback = st.session_state.get("feedback")
    if feedback:
        lines += [
            "## 5. AI 첨삭 결과",
            "",
            f"**종합 점수:** {feedback.get('overall_score', '')}/10",
            "",
            "### 강점",
        ]
        for s in feedback.get("strengths", []):
            lines.append(f"- {s}")
        lines += ["", "### 개선 사항"]
        for w in feedback.get("weaknesses", []):
            lines.append(f"- {w}")
        next_step = feedback.get("next_step", "")
        if next_step:
            lines += ["", "### 다음 학습 방향", next_step]

    return "\n".join(lines)
