import streamlit as st
from core.step03_refine_interest import build_questions_prompt, build_refine_prompt
from utils.ai_runner import prompt_panel


def render():
    if st.button("← 이전"):
        st.session_state.current_step = 2
        st.rerun()

    st.markdown('<div class="section-header">주제 구체화</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-subheader">질문에 하나씩 답하면 나만의 탐구 방향이 잡혀요.</div>', unsafe_allow_html=True)

    grade = st.session_state.get("grade", "고1")
    lt = st.session_state.get("learning_type", "hana")
    interest = st.session_state.get("interest_text", "")
    analysis = st.session_state.get("initial_analysis") or {}
    subtopic = analysis.get("estimated_subtopic", interest)

    questions = st.session_state.get("follow_up_questions")
    if not questions:
        st.markdown("**AI가 탐구 방향을 파악하기 위한 질문을 생성합니다.**")
        system, prompt = build_questions_prompt(interest, subtopic, grade, lt)
        if not prompt_panel(system, prompt, "follow_up_questions",
                            spinner_text="AI가 질문을 생성하고 있어요...",
                            btn_label="질문 생성하기"):
            return
        st.session_state.q3_idx = 0
        st.session_state.user_answers = {}
        questions = st.session_state.follow_up_questions

    if isinstance(questions, dict):
        questions = questions.get("questions", [])
        st.session_state.follow_up_questions = questions

    if not questions:
        st.warning("질문을 불러오지 못했어요. 다시 생성해주세요.")
        st.session_state.follow_up_questions = None
        st.rerun()

    refined = st.session_state.get("refined_topic")
    if not refined:
        _render_one_by_one(questions, interest, grade, lt)
        return

    _render_refined(refined)


def _render_one_by_one(questions: list, interest: str, grade: str, lt: str):
    answers = st.session_state.get("user_answers") or {}
    total = len(questions)
    idx = min(st.session_state.get("q3_idx", 0), total)

    if idx < total:
        st.markdown(
            f'<div style="background:#dff0ec;border-radius:999px;height:6px;margin-bottom:16px;">'
            f'<div style="background:#0d9488;width:{int(idx/total*100)}%;height:100%;border-radius:999px;"></div>'
            f'</div>',
            unsafe_allow_html=True,
        )
        st.markdown(
            f'<div style="font-size:12px;color:#4b7772;margin-bottom:8px;">질문 {idx+1} / {total}</div>',
            unsafe_allow_html=True,
        )

        q = questions[idx]
        st.markdown(
            f'<div style="background:#f0faf8;border-left:5px solid #0d9488;border-radius:0 12px 12px 0;'
            f'padding:16px 20px;margin-bottom:12px;">'
            f'<div style="font-size:13px;font-weight:700;color:#0d9488;margin-bottom:6px;">Q{idx+1}</div>'
            f'<div style="font-size:16px;font-weight:600;color:#0a5c52;">{q}</div>'
            f'</div>',
            unsafe_allow_html=True,
        )

        saved = answers.get(str(idx), "")
        answer = st.text_area(
            "답변",
            value=saved,
            height=120,
            key=f"q3_ans_{idx}",
            placeholder="자유롭게 생각을 적어보세요. 짧아도 괜찮아요.",
            label_visibility="collapsed",
        )
        answers[str(idx)] = answer
        st.session_state.user_answers = answers

        col_skip, col_next = st.columns([1, 2])
        with col_skip:
            if st.button("건너뛰기", use_container_width=True):
                st.session_state.q3_idx = idx + 1
                st.rerun()
        with col_next:
            if st.button(
                "다음 질문" if idx < total - 1 else "답변 완료",
                type="primary",
                use_container_width=True,
                disabled=not answer.strip(),
            ):
                st.session_state.q3_idx = idx + 1
                st.rerun()
        return

    st.markdown("**답변 요약**")
    for i, q in enumerate(questions):
        a = answers.get(str(i), "").strip()
        if a:
            st.markdown(
                f'<div style="background:#fff;border:1px solid #c9e6e1;border-radius:10px;padding:12px 16px;margin-bottom:8px;">'
                f'<div style="font-size:11px;font-weight:700;color:#4b7772;margin-bottom:4px;">Q{i+1}. {q}</div>'
                f'<div style="font-size:13px;color:#374151;">{a}</div>'
                f'</div>',
                unsafe_allow_html=True,
            )

    if st.button("답변 다시하기", use_container_width=False):
        st.session_state.q3_idx = 0
        st.session_state.user_answers = {}
        st.rerun()

    st.markdown("---")
    st.markdown("**AI가 답변을 바탕으로 탐구 주제를 정제합니다.**")
    system, prompt = build_refine_prompt(interest, questions, answers, grade, lt)
    prompt_panel(system, prompt, "refined_topic",
                 spinner_text="AI가 탐구 주제를 정제하고 있어요...",
                 btn_label="주제 정제하기")


def _render_refined(refined: dict):
    topic = refined.get("refined_topic", "")
    angle = refined.get("specific_angle", "")
    goal = refined.get("learning_goal", "")
    keywords = refined.get("key_concepts", [])

    st.markdown("---")
    st.markdown("**정제된 탐구 주제**")
    st.markdown(
        f'<div style="background:#f0faf8;border-left:5px solid #0d9488;border-radius:0 12px 12px 0;padding:16px 20px;">'
        f'<div style="font-size:11px;font-weight:700;color:#0d9488;margin-bottom:4px;">확정 주제</div>'
        f'<div style="font-size:18px;font-weight:800;color:#0a5c52;">{topic}</div>'
        f'</div>',
        unsafe_allow_html=True,
    )

    col1, col2 = st.columns(2)
    with col1:
        if angle:
            st.markdown(
                f'<div style="background:#fff;border:1px solid #c9e6e1;border-radius:10px;padding:14px;margin-top:10px;">'
                f'<div style="font-size:11px;font-weight:700;color:#4b7772;margin-bottom:4px;">탐구 각도</div>'
                f'<div style="font-size:14px;color:#374151;">{angle}</div></div>',
                unsafe_allow_html=True,
            )
    with col2:
        if goal:
            st.markdown(
                f'<div style="background:#fff;border:1px solid #c9e6e1;border-radius:10px;padding:14px;margin-top:10px;">'
                f'<div style="font-size:11px;font-weight:700;color:#4b7772;margin-bottom:4px;">학습 목표</div>'
                f'<div style="font-size:14px;color:#374151;">{goal}</div></div>',
                unsafe_allow_html=True,
            )

    if keywords:
        tags = "".join(
            f'<span style="background:#ccede9;color:#0a5c52;border-radius:20px;padding:3px 10px;'
            f'font-size:12px;font-weight:600;margin:2px;display:inline-block;">{kw}</span>'
            for kw in keywords
        )
        st.markdown(f'<div style="margin-top:10px;">{tags}</div>', unsafe_allow_html=True)

    st.markdown("")
    col_yes, col_no = st.columns(2)
    with col_yes:
        if st.button("확정, 로드맵 보기", type="primary", use_container_width=True):
            st.session_state.step3_confirmed = True
            st.session_state.current_step = 4
            for k in ["roadmap", "resources", "news_items", "extra_resources",
                      "news_summaries", "core_questions", "question_answers",
                      "student_text", "feedback", "next_step_result"]:
                st.session_state[k] = None if k not in ("news_summaries", "question_answers") else {}
            st.rerun()
    with col_no:
        if st.button("다시 정제", use_container_width=True):
            st.session_state.refined_topic = None
            st.rerun()
