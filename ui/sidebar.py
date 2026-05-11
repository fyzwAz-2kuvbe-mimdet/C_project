import streamlit as st
from config.learning_types import get_all_types

_GRADES = ["초4", "초5", "초6", "중1", "중2", "중3", "고1", "고2", "고3"]
_STEP_NAMES = {
    1: "유형 선택", 2: "관심사 입력", 3: "주제 구체화",
    4: "로드맵", 5: "자료 추천", 6: "뉴스·동향",
    7: "핵심 질문", 8: "결과물 작성", 9: "AI 첨삭", 10: "성찰·저장",
}


def render_sidebar():
    st.markdown(
        "<div style='font-size:20px;font-weight:800;color:#111827;margin-bottom:2px;'>🎓 AI 학습 멘토</div>"
        "<div style='font-size:12px;color:#6b7280;margin-bottom:12px;'>10단계 탐구 멘토링</div>",
        unsafe_allow_html=True,
    )
    st.divider()

    # ── 학년 ──
    st.markdown("**학년**")
    grade = st.selectbox("학년", _GRADES,
                         index=_GRADES.index(st.session_state.get("grade", "고1")),
                         label_visibility="collapsed")
    if grade != st.session_state.get("grade"):
        st.session_state.grade = grade

    st.divider()

    # ── 학습 유형 ──
    st.markdown("**학습 유형**")
    types = get_all_types()
    type_ids = list(types.keys())
    labels = [f"{v['icon']} {v['name']}" for v in types.values()]
    cur = st.session_state.get("learning_type", "hana")
    sel = st.radio("유형", labels, index=type_ids.index(cur), label_visibility="collapsed")
    sel_id = type_ids[labels.index(sel)]
    if sel_id != cur:
        st.session_state.learning_type = sel_id

    # ── 유형 카드 ──
    info = types[sel_id]
    c = info["color"]
    criteria_li = "".join(
        f"<li style='font-size:11px;color:#374151;margin-bottom:3px;'>{cr['label']}</li>"
        for cr in info["evaluation_criteria"]
    )
    st.markdown(
        f"""<div style="border-left:4px solid {c};background:{c}11;border-radius:0 10px 10px 0;padding:12px 14px;margin-top:8px;">
          <div style="font-size:13px;font-weight:700;color:{c};margin-bottom:3px;">{info['icon']} {info['name']}</div>
          <div style="font-size:11px;color:#374151;margin-bottom:6px;">{info['description']}</div>
          <div style="font-size:10px;font-weight:700;color:#9ca3af;margin-bottom:3px;">평가 기준</div>
          <ul style="margin:0;padding-left:13px;">{criteria_li}</ul>
        </div>""",
        unsafe_allow_html=True,
    )

    st.divider()

    # ── 진행 상태 ──
    step = st.session_state.get("current_step", 1)
    st.markdown(
        f"<div style='font-size:12px;color:#6b7280;margin-bottom:8px;'>"
        f"진행 단계: <strong style='color:#111827;'>{step}/10 — {_STEP_NAMES[step]}</strong></div>",
        unsafe_allow_html=True,
    )
    if step > 1:
        if st.button("🔄 처음부터 다시", use_container_width=True):
            from utils.session import reset_all
            reset_all()
            st.rerun()
