import streamlit as st

_STEPS = {
    1: "유형선택", 2: "관심입력", 3: "주제구체화",
    4: "로드맵",   5: "자료추천", 6: "뉴스·동향",
    7: "핵심질문", 8: "결과작성", 9: "AI첨삭",   10: "성찰저장",
}

_PHASES = [
    (1, "Phase 1 진단", [1, 2, 3]),
    (2, "Phase 2 학습", [4, 5, 6]),
    (3, "Phase 3 탐구", [7, 8]),
    (4, "Phase 4 성찰", [9, 10]),
]

_PHASE_COLORS = {1: "#3b82f6", 2: "#8b5cf6", 3: "#10b981", 4: "#f59e0b"}


def render_progress(current_step: int):
    ph_row: list[str] = []
    circ_row: list[str] = []
    name_row: list[str] = []

    for idx, (phase_num, phase_name, phase_steps) in enumerate(_PHASES):
        pc = _PHASE_COLORS[phase_num]
        min_s, max_s = min(phase_steps), max(phase_steps)

        if current_step > max_s:
            ph_c = "#10b981"
        elif current_step >= min_s:
            ph_c = pc
        else:
            ph_c = "#d1d5db"

        span = 2 * len(phase_steps) - 1
        ph_row.append(
            f'<td colspan="{span}" style="text-align:center;padding:0 4px 6px;'
            f'border-bottom:2px solid {ph_c};font-size:9px;font-weight:700;'
            f'color:{ph_c};letter-spacing:.04em;">{phase_name}</td>'
        )

        for i, step_num in enumerate(phase_steps):
            name = _STEPS[step_num]

            if step_num < current_step:
                cbg, cfg, ct = "#10b981", "#fff", "✓"
                lc, lw = "#10b981", "600"
            elif step_num == current_step:
                cbg, cfg, ct = pc, "#fff", str(step_num)
                lc, lw = pc, "700"
            else:
                cbg, cfg, ct = "#f3f4f6", "#9ca3af", str(step_num)
                lc, lw = "#9ca3af", "400"

            shadow = f"box-shadow:0 0 0 4px {pc}22;" if step_num == current_step else ""

            circ_row.append(
                f'<td style="padding:6px 3px 0;text-align:center;vertical-align:middle;">'
                f'<div style="width:30px;height:30px;border-radius:50%;background:{cbg};color:{cfg};'
                f'display:flex;align-items:center;justify-content:center;'
                f'font-size:12px;font-weight:700;margin:0 auto;{shadow}">{ct}</div></td>'
            )
            name_row.append(
                f'<td style="padding:4px 3px 0;text-align:center;vertical-align:top;">'
                f'<span style="font-size:9px;color:{lc};font-weight:{lw};'
                f'white-space:nowrap;">{name}</span></td>'
            )

            # 페이즈 내 연결선
            if i < len(phase_steps) - 1:
                nxt = phase_steps[i + 1]
                cline = "#10b981" if nxt <= current_step else "#e5e7eb"
                circ_row.append(
                    f'<td style="padding:6px 0 0;vertical-align:middle;">'
                    f'<div style="height:2px;background:{cline};min-width:16px;"></div></td>'
                )
                name_row.append('<td></td>')

        # 페이즈 간 연결선 (마지막 페이즈 제외)
        if idx < len(_PHASES) - 1:
            next_first = _PHASES[idx + 1][2][0]
            cline = "#10b981" if next_first <= current_step else "#e5e7eb"
            circ_row.append(
                f'<td style="padding:6px 2px 0;vertical-align:middle;">'
                f'<div style="height:2px;background:{cline};min-width:10px;'
                f'border-left:3px solid #fff;border-right:3px solid #fff;"></div></td>'
            )
            name_row.append('<td></td>')
            ph_row.append(
                f'<td style="padding:0 2px 6px;border-bottom:2px solid #e5e7eb;min-width:10px;"></td>'
            )

    html = (
        '<div style="background:#fff;border-bottom:1px solid #e5e7eb;'
        'padding:12px 16px 10px;margin-bottom:20px;overflow-x:auto;">'
        '<table cellspacing="0" cellpadding="0" '
        'style="border-collapse:collapse;margin:0 auto;">'
        f'<tr>{"".join(ph_row)}</tr>'
        f'<tr>{"".join(circ_row)}</tr>'
        f'<tr>{"".join(name_row)}</tr>'
        '</table></div>'
    )
    st.markdown(html, unsafe_allow_html=True)
