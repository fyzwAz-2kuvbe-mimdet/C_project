import streamlit as st
from config.learning_types import get_all_types

_GRADES = ["초4", "초5", "초6", "중1", "중2", "중3", "고1", "고2", "고3"]


def render_sidebar():
    st.markdown(
        "<div style='font-size:22px; font-weight:800; color:#111827; margin-bottom:4px;'>🎓 AI 학습 코치</div>"
        "<div style='font-size:13px; color:#6b7280; margin-bottom:16px;'>맞춤형 학습 경험을 시작하세요</div>",
        unsafe_allow_html=True,
    )
    st.divider()

    # ── Grade ──
    st.markdown("**학년**")
    grade = st.selectbox(
        "학년 선택",
        _GRADES,
        index=_GRADES.index(st.session_state.get("grade", "고1")),
        label_visibility="collapsed",
    )
    if grade != st.session_state.get("grade"):
        st.session_state.grade = grade

    st.divider()

    # ── Learning type ──
    st.markdown("**학습 유형**")

    types = get_all_types()
    type_ids = list(types.keys())
    type_labels = [f"{v['icon']} {v['name']}" for v in types.values()]

    current_type = st.session_state.get("learning_type", "hana")
    current_idx = type_ids.index(current_type) if current_type in type_ids else 0

    selected_label = st.radio(
        "학습 유형 선택",
        type_labels,
        index=current_idx,
        label_visibility="collapsed",
    )
    selected_id = type_ids[type_labels.index(selected_label)]
    if selected_id != st.session_state.get("learning_type"):
        st.session_state.learning_type = selected_id

    # ── Type detail card ──
    info = types[selected_id]
    c = info["color"]
    criteria_html = "".join(
        f"<li style='font-size:11px; color:#374151; margin-bottom:3px;'>{cr['label']}</li>"
        for cr in info["evaluation_criteria"]
    )
    st.markdown(
        f"""<div style="border-left:4px solid {c}; background:{c}11;
                        border-radius:0 10px 10px 0; padding:14px 16px; margin-top:10px;">
          <div style="font-size:13px; font-weight:700; color:{c}; margin-bottom:3px;">
            {info['icon']} {info['name']}
          </div>
          <div style="font-size:12px; color:#374151; margin-bottom:8px; line-height:1.5;">
            {info['description']}
          </div>
          <div style="font-size:11px; font-weight:700; color:#6b7280; margin-bottom:4px;">
            평가 기준
          </div>
          <ul style="margin:0; padding-left:14px;">{criteria_html}</ul>
        </div>""",
        unsafe_allow_html=True,
    )

    st.divider()

    # ── Progress ──
    step = st.session_state.get("current_step", 1)
    step_names = {1: "관심사 입력", 2: "자료 추천", 3: "뉴스", 4: "첨삭"}
    st.markdown(
        f"<div style='font-size:12px; color:#6b7280; margin-bottom:8px;'>"
        f"현재 단계: <strong style='color:#111827;'>{step}/4 — {step_names[step]}</strong></div>",
        unsafe_allow_html=True,
    )

    if step > 1:
        if st.button("🔄 처음부터 다시", use_container_width=True):
            from utils.session import reset_from_step
            reset_from_step(1)
            st.session_state.current_step = 1
            st.rerun()
