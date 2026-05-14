import streamlit as st
from config.learning_types import get_all_types


def render():
    st.markdown('<div class="section-header">학습 유형 선택</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-subheader">유형을 클릭해서 선택하세요</div>', unsafe_allow_html=True)

    types = get_all_types()
    current = st.session_state.get("learning_type", "hana")

    for tid, info in types.items():
        c = info["color"]
        is_sel = tid == current

        # 버튼을 카드처럼 보이게 하는 CSS — 마커 바로 다음 버튼만 타겟
        st.markdown(
            f"<style>"
            f".element-container:has(#tm-{tid}) + .element-container button{{"
            f"  border-left:5px solid {c} !important;"
            f"  border-radius:0 10px 10px 0 !important;"
            f"  white-space:pre-line !important;"
            f"  text-align:left !important;"
            f"  height:auto !important;"
            f"  min-height:88px !important;"
            f"  padding:14px 18px !important;"
            f"  line-height:1.6 !important;"
            f"  font-size:14px !important;"
            f"  font-weight:400 !important;"
            f"}}"
            f".element-container:has(#tm-{tid}) + .element-container button b{{"
            f"  font-size:15px !important;"
            f"  font-weight:700 !important;"
            f"}}"
            f"</style>"
            f'<span id="tm-{tid}"></span>',
            unsafe_allow_html=True,
        )

        # 버튼 라벨: 이름(굵게) + 핵심 / 줄바꿈 / 설명
        label = f"{info['name']}  ·  {info['core']}\n{info['description']}"
        if st.button(
            label,
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
