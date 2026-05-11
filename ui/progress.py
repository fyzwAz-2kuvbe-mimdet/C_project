import streamlit as st

_PHASES = [
    ("Phase 1 진단", [1, 2, 3]),
    ("Phase 2 학습", [4, 5, 6]),
    ("Phase 3 탐구", [7, 8]),
    ("Phase 4 성찰", [9, 10]),
]


def render_progress(current_step: int):
    parts = []
    for phase_idx, (label, steps) in enumerate(_PHASES):
        # phase label
        step_nodes = ""
        for i, s in enumerate(steps):
            if s < current_step:
                cls, txt = "done", "✓"
            elif s == current_step:
                cls, txt = "active", str(s)
            else:
                cls, txt = "", str(s)
            step_nodes += f'<div class="step-node {cls}">{txt}</div>'
            if i < len(steps) - 1:
                line_cls = "done" if steps[i + 1] <= current_step else ""
                step_nodes += f'<div class="step-line {line_cls}"></div>'

        parts.append(
            f'<div class="phase-group">'
            f'  <div class="phase-label">{label}</div>'
            f'  <div class="phase-steps">{step_nodes}</div>'
            f"</div>"
        )
        if phase_idx < len(_PHASES) - 1:
            parts.append('<div class="phase-sep"></div>')

    html = (
        '<div class="progress-outer">'
        '<div class="progress-inner">'
        + "".join(parts)
        + "</div></div>"
    )
    st.markdown(html, unsafe_allow_html=True)
