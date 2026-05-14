import streamlit as st
from config.learning_types import get_all_types


def render():
    st.markdown('<div class="section-header">학습 유형 선택</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-subheader">나에게 맞는 유형을 선택하면 맞춤 멘토링이 시작됩니다</div>', unsafe_allow_html=True)

    types = get_all_types()
    current = st.session_state.get("learning_type", "hana")

    for tid, info in types.items():
        c = info["color"]
        is_sel = tid == current
        border_color = "#0d9488" if is_sel else "#c9e6e1"
        bg = "#f0faf8" if is_sel else "#fff"
        shadow = "0 0 0 3px rgba(13,148,136,.15)" if is_sel else "0 2px 6px rgba(13,148,136,.04)"

        col_card, col_btn = st.columns([5, 1])
        with col_card:
            st.markdown(
                f'<div style="background:{bg};border:1.5px solid {border_color};border-left:5px solid {c};'
                f'border-radius:0 12px 12px 0;padding:16px 18px;box-shadow:{shadow};">'
                f'<div style="font-size:15px;font-weight:700;color:#111827;margin-bottom:3px;">{info["name"]}</div>'
                f'<div style="font-size:12px;color:#6b7280;margin-bottom:6px;">{info["description"]}</div>'
                f'<div style="font-size:11px;font-weight:700;color:{c};">{info["core"]}</div>'
                f'</div>',
                unsafe_allow_html=True,
            )
        with col_btn:
            st.markdown('<div style="height:16px;"></div>', unsafe_allow_html=True)
            if st.button(
                "선택됨" if is_sel else "선택",
                key=f"type_{tid}",
                use_container_width=True,
                type="primary" if is_sel else "secondary",
            ):
                st.session_state.learning_type = tid
                st.rerun()
        st.markdown('<div style="height:4px;"></div>', unsafe_allow_html=True)

    st.divider()

    info = types[current]
    c = info["color"]
    st.markdown(f"**{info['name']} 평가 기준**")
    for cr in info["evaluation_criteria"]:
        st.markdown(
            f'<div style="display:flex;justify-content:space-between;padding:10px 14px;'
            f'background:#f0faf8;border-radius:8px;margin-bottom:6px;border:1px solid #c9e6e1;">'
            f'<span style="font-size:13px;color:#374151;">{cr["label"]}</span>'
            f'<span style="font-size:12px;font-weight:700;color:#0d9488;">{cr["weight"]}점</span></div>',
            unsafe_allow_html=True,
        )

    st.markdown("")
    if st.button("다음 단계", type="primary", use_container_width=True):
        st.session_state.current_step = 2
        st.rerun()
