import streamlit as st
from core.step07_core_questions import build_prompt
from utils.ai_runner import prompt_panel


def render():
    if st.button("← 이전"):
        st.session_state.current_step = 6
        st.rerun()

    st.markdown('<div class="section-header">핵심 탐구 질문</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-subheader">질문에 하나씩 답하면 결과물 작성의 뼈대가 됩니다.</div>', unsafe_allow_html=True)

    grade = st.session_state.get("grade", "고1")
    lt = st.session_state.get("learning_type", "hana")
    refined = st.session_state.get("refined_topic") or {}
    topic = refined.get("refined_topic", st.session_state.get("interest_text", ""))
    keywords = refined.get("key_concepts", [])

    # ── 1단계: 핵심 질문 생성 ──────────────────────────
    questions = st.session_state.get("core_questions")
    if not questions:
        st.markdown("**AI가 탐구 주제에 맞는 핵심 질문을 생성합니다.**")
        system, prompt = build_prompt(topic, keywords, grade, lt)
        if not prompt_panel(system, prompt, "core_questions",
                            spinner_text="AI가 핵심 질문을 생성하고 있어요...",
                            btn_label="핵심 질문 생성하기"):
            return
        st.session_state.q7_idx = 0
        st.session_state.question_answers = {}
        questions = st.session_state.core_questions

    # dict {"questions": [...]} 형태로 저장된 경우 리스트로 정규화
    if isinstance(questions, dict):
        questions = questions.get("questions", [])
        st.session_state.core_questions = questions

    if not questions:
        st.warning("질문을 불러오지 못했어요. 다시 생성해주세요.")
        st.session_state.core_questions = None
        st.rerun()

    # ── 2단계: 한 번에 하나씩 답변 ────────────────────
    _render_one_by_one(questions)


def _render_one_by_one(questions: list):
    answers = st.session_state.get("question_answers") or {}
    total = len(questions)
    idx = min(st.session_state.get("q7_idx", 0), total)

    if idx < total:
        # 진행률
        st.markdown(
            f'<div style="background:#dff0ec;border-radius:999px;height:6px;margin-bottom:16px;">'
            f'<div style="background:#0d9488;width:{int(idx/total*100)}%;height:100%;border-radius:999px;"></div>'
            f'</div>',
            unsafe_allow_html=True,
        )
        st.markdown(
            f'<div style="font-size:12px;color:#4b7772;margin-bottom:8px;">핵심 질문 {idx+1} / {total}</div>',
            unsafe_allow_html=True,
        )

        q = questions[idx]
        st.markdown(
            f'<div style="background:#f0faf8;border-left:5px solid #0d9488;border-radius:0 12px 12px 0;'
            f'padding:16px 20px;margin-bottom:12px;">'
            f'<div style="font-size:12px;font-weight:700;color:#0d9488;margin-bottom:6px;">핵심 질문 {idx+1}</div>'
            f'<div style="font-size:16px;font-weight:600;color:#0a5c52;">{q}</div>'
            f'</div>',
            unsafe_allow_html=True,
        )

        saved = answers.get(str(idx), "")
        answer = st.text_area(
            "답변",
            value=saved,
            height=140,
            key=f"q7_ans_{idx}",
            placeholder="자신의 생각을 자유롭게 써보세요. 완벽하지 않아도 괜찮아요.",
            label_visibility="collapsed",
        )
        answers[str(idx)] = answer
        st.session_state.question_answers = answers

        col_skip, col_next = st.columns([1, 2])
        with col_skip:
            if st.button("건너뛰기", use_container_width=True):
                st.session_state.q7_idx = idx + 1
                st.rerun()
        with col_next:
            if st.button(
                "다음 질문 →" if idx < total - 1 else "답변 완료 ✓",
                type="primary",
                use_container_width=True,
                disabled=not answer.strip(),
            ):
                st.session_state.q7_idx = idx + 1
                st.rerun()
        return

    # 모든 질문 완료 → 답변 요약
    st.markdown("**내 답변 요약**")
    for i, q in enumerate(questions):
        a = answers.get(str(i), "").strip()
        st.markdown(
            f'<div style="background:#fff;border:1px solid #c9e6e1;border-radius:10px;padding:12px 16px;margin-bottom:8px;">'
            f'<div style="font-size:11px;font-weight:700;color:#4b7772;margin-bottom:4px;">Q{i+1}. {q}</div>'
            f'<div style="font-size:13px;color:#374151;">{a if a else "(미작성)"}</div>'
            f'</div>',
            unsafe_allow_html=True,
        )

    if st.button("답변 다시하기", use_container_width=False):
        st.session_state.q7_idx = 0
        st.session_state.question_answers = {}
        st.rerun()

    st.markdown("")
    any_answered = any(answers.get(str(i), "").strip() for i in range(len(questions)))
    if st.button("결과물 작성하기", type="primary", use_container_width=True, disabled=not any_answered):
        st.session_state.current_step = 8
        st.rerun()
