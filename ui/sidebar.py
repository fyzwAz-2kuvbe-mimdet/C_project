import streamlit as st
from config.learning_types import get_all_types

_GRADES = ["초4", "초5", "초6", "중1", "중2", "중3", "고1", "고2", "고3"]
_STEP_NAMES = {
    1: "유형선택", 2: "관심입력", 3: "주제구체화",
    4: "로드맵",   5: "자료추천", 6: "뉴스·동향",
    7: "핵심질문", 8: "결과작성", 9: "AI첨삭",   10: "성찰저장",
}
_PHASES = [
    ("Phase 1", "#0d9488", [1, 2, 3]),
    ("Phase 2", "#0891b2", [4, 5, 6]),
    ("Phase 3", "#059669", [7, 8]),
    ("Phase 4", "#0a5c52", [9, 10]),
]
_STEP_COLOR = {s: c for _, c, steps in _PHASES for s in steps}


def render_sidebar():
    st.markdown(
        "<div style='font-size:20px;font-weight:800;color:#0a5c52;margin-bottom:2px;'>AI 학습 멘토</div>"
        "<div style='font-size:12px;color:#4b7772;margin-bottom:12px;'>10단계 탐구 멘토링</div>",
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
    labels = [v['name'] for v in types.values()]
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
          <div style="font-size:13px;font-weight:700;color:{c};margin-bottom:3px;">{info['name']}</div>
          <div style="font-size:11px;color:#374151;margin-bottom:6px;">{info['description']}</div>
          <div style="font-size:10px;font-weight:700;color:#9ca3af;margin-bottom:3px;">평가 기준</div>
          <ul style="margin:0;padding-left:13px;">{criteria_li}</ul>
        </div>""",
        unsafe_allow_html=True,
    )

    st.divider()

    # ── 단계 이동 (원형 버튼 그리드) ──
    current = st.session_state.get("current_step", 1)
    st.markdown("**단계 이동**")
    _render_phase_labels()
    _render_step_buttons(current, 1, 5)
    _render_step_buttons(current, 6, 10)

    st.divider()

    # ── 진행 상태 ──
    st.markdown(
        f"<div style='font-size:12px;color:#6b7280;'>"
        f"현재: <strong style='color:#0a5c52;'>{current}단계 — {_STEP_NAMES[current]}</strong></div>",
        unsafe_allow_html=True,
    )
    if current > 1:
        if st.button("처음부터 다시", use_container_width=True):
            from utils.session import reset_all
            reset_all()
            st.rerun()


def _render_phase_labels():
    parts = []
    for name, color, steps in _PHASES:
        flex = len(steps)
        parts.append(
            f'<div style="flex:{flex};text-align:center;font-size:9px;font-weight:700;'
            f'color:{color};border-bottom:2px solid {color};padding-bottom:3px;'
            f'white-space:nowrap;overflow:hidden;">{name}</div>'
        )
    html = f'<div style="display:flex;gap:2px;margin-bottom:6px;">{"".join(parts)}</div>'
    st.markdown(html, unsafe_allow_html=True)


def _render_step_buttons(current: int, start: int, end: int):
    cols = st.columns(end - start + 1)
    for i, col in enumerate(cols):
        sn = start + i
        done = sn < current
        active = sn == current
        lbl = "✓" if done else str(sn)
        btn_type = "primary" if active else "secondary"
        with col:
            if st.button(
                lbl,
                key=f"_nav_{sn}",
                type=btn_type,
                use_container_width=True,
                help=f"{sn}. {_STEP_NAMES[sn]}",
            ):
                st.session_state.current_step = sn
                st.rerun()
