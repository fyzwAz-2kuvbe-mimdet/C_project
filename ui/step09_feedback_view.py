import streamlit as st
from config.learning_types import get_criteria
from core.step09_feedback import build_prompt
from utils.ai_runner import prompt_panel


def render():
    if st.button("← 이전"):
        st.session_state.current_step = 8
        st.rerun()

    st.markdown('<div class="section-header">🤖 AI 첨삭</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-subheader">학습 유형 기준으로 결과물을 평가하고 개선 방향을 알려드려요.</div>', unsafe_allow_html=True)

    grade = st.session_state.get("grade", "고1")
    lt = st.session_state.get("learning_type", "hana")
    student_text = st.session_state.get("student_text", "")
    format_type = st.session_state.get("format_type", "에세이")

    system, prompt = build_prompt(student_text, format_type, grade, lt)
    if not prompt_panel(system, prompt, "feedback",
                        spinner_text="AI가 결과물을 분석하고 있어요...",
                        btn_label="🤖 AI 첨삭 시작"):
        return

    feedback = st.session_state.feedback
    if not isinstance(feedback, dict):
        st.warning("첨삭 데이터가 올바르지 않아요. 다시 시도해주세요.")
        if st.button("다시 시도"):
            st.session_state.feedback = None
            st.rerun()
        return

    _render_feedback(feedback, lt)

    st.markdown("")
    if st.button("🌱 성찰·다음 방향 →", type="primary", use_container_width=True):
        st.session_state.current_step = 10
        st.rerun()


def _render_feedback(fb: dict, lt: str):
    overall = fb.get("overall_score", 0)
    strengths = fb.get("strengths", [])
    weaknesses = fb.get("weaknesses", [])
    per_criterion = fb.get("per_criterion", fb.get("criteria_scores", {}))
    before_after = fb.get("before_after", fb.get("rewrite_suggestions", []))
    overall_comment = fb.get("overall_comment", fb.get("format_specific_advice", ""))

    pct = min(max(overall, 0), 100)
    bar_color = "#10b981" if pct >= 70 else ("#f59e0b" if pct >= 50 else "#ef4444")
    st.markdown(
        f'<div style="background:#fff;border:1px solid #e5e7eb;border-radius:12px;padding:20px 24px;margin-bottom:20px;">'
        f'  <div style="font-size:12px;font-weight:700;color:#6b7280;margin-bottom:6px;">종합 점수</div>'
        f'  <div style="font-size:40px;font-weight:800;color:{bar_color};">{overall}<span style="font-size:18px;color:#9ca3af;">/100</span></div>'
        f'  <div class="score-bar-bg" style="margin-top:10px;">'
        f'    <div class="score-bar-fill" style="width:{pct}%;background:{bar_color};"></div>'
        f'  </div>'
        f'  {"<div style=\"font-size:13px;color:#374151;margin-top:10px;\">" + overall_comment + "</div>" if overall_comment else ""}'
        f'</div>',
        unsafe_allow_html=True,
    )

    criteria = get_criteria(lt)
    if criteria and per_criterion:
        st.markdown("**항목별 평가**")
        for cr in criteria:
            key = cr["key"]
            score = per_criterion.get(key, 0)
            pct_c = min(max(score, 0), 100)
            bar_c = "#10b981" if pct_c >= 70 else ("#f59e0b" if pct_c >= 50 else "#ef4444")
            st.markdown(
                f'<div style="margin-bottom:12px;">'
                f'  <div style="display:flex;justify-content:space-between;margin-bottom:4px;">'
                f'    <span style="font-size:13px;color:#374151;">{cr["label"]}</span>'
                f'    <span style="font-size:13px;font-weight:700;color:{bar_c};">{score}점</span>'
                f'  </div>'
                f'  <div class="score-bar-bg">'
                f'    <div class="score-bar-fill" style="width:{pct_c}%;background:{bar_c};"></div>'
                f'  </div>'
                f'</div>',
                unsafe_allow_html=True,
            )

    col1, col2 = st.columns(2)
    with col1:
        if strengths:
            st.markdown("**강점**")
            for s in strengths:
                point = s.get("point", s) if isinstance(s, dict) else s
                st.markdown(
                    f'<div style="background:#d1fae5;border-radius:8px;padding:10px 14px;margin-bottom:6px;font-size:13px;color:#065f46;">✅ {point}</div>',
                    unsafe_allow_html=True,
                )
    with col2:
        if weaknesses:
            st.markdown("**개선 사항**")
            for w in weaknesses:
                point = w.get("point", w) if isinstance(w, dict) else w
                st.markdown(
                    f'<div style="background:#fef3c7;border-radius:8px;padding:10px 14px;margin-bottom:6px;font-size:13px;color:#92400e;">💡 {point}</div>',
                    unsafe_allow_html=True,
                )

    if before_after:
        st.markdown("**Before → After 예시**")
        for item in before_after:
            before = item.get("before", "")
            after = item.get("after", "")
            reason = item.get("reason", "")
            st.markdown(
                f'<div style="background:#fff;border:1px solid #e5e7eb;border-radius:10px;padding:14px;margin-bottom:10px;">'
                f'  <div style="font-size:12px;font-weight:700;color:#ef4444;margin-bottom:4px;">Before</div>'
                f'  <div style="font-size:13px;color:#374151;margin-bottom:8px;">{before}</div>'
                f'  <div style="font-size:12px;font-weight:700;color:#10b981;margin-bottom:4px;">After</div>'
                f'  <div style="font-size:13px;color:#374151;margin-bottom:8px;">{after}</div>'
                f'  {"<div style=\"font-size:12px;color:#6b7280;\">💬 " + reason + "</div>" if reason else ""}'
                f'</div>',
                unsafe_allow_html=True,
            )
