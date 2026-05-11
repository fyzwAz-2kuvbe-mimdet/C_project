import streamlit as st
from config.learning_types import get_all_types


def render():
    st.markdown('<div class="section-header">🎯 학습 유형 선택</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-subheader">나에게 맞는 유형을 선택하면 맞춤 멘토링이 시작됩니다</div>', unsafe_allow_html=True)

    types = get_all_types()
    type_ids = list(types.keys())
    current = st.session_state.get("learning_type", "hana")

    cols = st.columns(2)
    for idx, (tid, info) in enumerate(types.items()):
        c = info["color"]
        is_sel = tid == current
        border = f"2px solid {c}" if is_sel else "2px solid #e5e7eb"
        bg = f"{c}11" if is_sel else "#fff"
        with cols[idx % 2]:
            st.markdown(
                f"""<div class="type-card {'selected' if is_sel else ''}"
                         style="border-color:{c if is_sel else '#e5e7eb'};background:{bg};border-left:5px solid {c};">
                  <div style="font-size:24px;margin-bottom:6px;">{info['icon']}</div>
                  <div style="font-size:15px;font-weight:700;color:#111827;margin-bottom:3px;">{info['name']}</div>
                  <div style="font-size:12px;color:#6b7280;margin-bottom:8px;">{info['description']}</div>
                  <div style="font-size:11px;font-weight:700;color:{c};">{info['core']}</div>
                </div>""",
                unsafe_allow_html=True,
            )
            if st.button(f"{'✅ 선택됨' if is_sel else '선택'}", key=f"type_{tid}", use_container_width=True,
                         type="primary" if is_sel else "secondary"):
                st.session_state.learning_type = tid
                st.rerun()
        if idx % 2 == 1:
            st.markdown("")

    st.divider()

    # 평가기준 미리보기
    info = types[current]
    c = info["color"]
    st.markdown(f"**{info['icon']} {info['name']} 평가 기준**")
    for cr in info["evaluation_criteria"]:
        st.markdown(
            f'<div style="display:flex;justify-content:space-between;padding:8px 12px;'
            f'background:#f8fafc;border-radius:8px;margin-bottom:6px;">'
            f'<span style="font-size:13px;color:#374151;">{cr["label"]}</span>'
            f'<span style="font-size:12px;font-weight:700;color:{c};">{cr["weight"]}점</span></div>',
            unsafe_allow_html=True,
        )

    st.markdown("")
    if st.button("다음 단계 →", type="primary", use_container_width=True):
        st.session_state.current_step = 2
        st.rerun()
