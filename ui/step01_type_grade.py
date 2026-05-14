import streamlit as st
from config.learning_types import get_all_types


def render():
    st.markdown('<div class="section-header">학습 유형 선택</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-subheader">유형을 선택하면 상세 내용이 표시됩니다</div>', unsafe_allow_html=True)

    types = get_all_types()
    current = st.session_state.get("learning_type", "hana")

    for tid, info in types.items():
        c = info["color"]
        is_sel = tid == current

        # CSS: 각 타입 버튼에 유형 색상 왼쪽 테두리 적용 (has() 셀렉터)
        st.markdown(
            f'<style>'
            f'.element-container:has(#type-marker-{tid}) + .element-container button'
            f'{{ border-left: 5px solid {c} !important;'
            f'   border-radius: 0 8px 8px 0 !important;'
            f'   text-align: left !important;'
            f'   height: 48px !important;'
            f'   padding-left: 16px !important; }}'
            f'</style>'
            f'<span id="type-marker-{tid}"></span>',
            unsafe_allow_html=True,
        )

        if st.button(
            info["name"],
            key=f"type_{tid}",
            use_container_width=True,
            type="primary" if is_sel else "secondary",
        ):
            st.session_state.learning_type = tid
            st.rerun()

        if is_sel:
            st.markdown(
                f'<div style="background:#f0faf8;'
                f'border:1px solid #c9e6e1;border-top:none;border-left:5px solid {c};'
                f'border-radius:0 0 10px 0;padding:14px 18px;margin-top:-6px;margin-bottom:12px;">'
                f'<div style="font-size:13px;color:#374151;line-height:1.7;margin-bottom:8px;">'
                f'{info["description"]}</div>'
                f'<div style="font-size:11px;font-weight:700;color:{c};">{info["core"]}</div>'
                f'</div>',
                unsafe_allow_html=True,
            )
        else:
            st.markdown('<div style="height:6px;"></div>', unsafe_allow_html=True)

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
