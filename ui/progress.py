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

_PC = {1: "#3b82f6", 2: "#8b5cf6", 3: "#10b981", 4: "#f59e0b"}
_STEP_PC = {s: _PC[pn] for pn, _, steps in _PHASES for s in steps}

STEP_W = 52   # px — each step cell width
CONN_W = 18   # px — connector cell width


def render_progress(current_step: int):
    ph_row: list[str] = []
    data_row: list[str] = []

    for idx, (pn, pname, psteps) in enumerate(_PHASES):
        pc = _PC[pn]
        done_ph  = current_step > max(psteps)
        active_ph = min(psteps) <= current_step <= max(psteps)
        ph_c = "#10b981" if done_ph else (pc if active_ph else "#d1d5db")

        span = 2 * len(psteps) - 1
        ph_row.append(
            f'<td colspan="{span}" style="border:0;text-align:center;padding:0 0 6px;'
            f'border-bottom:2px solid {ph_c} !important;font-size:9px;font-weight:700;'
            f'color:{ph_c};white-space:nowrap;letter-spacing:.03em;">{pname}</td>'
        )

        for i, sn in enumerate(psteps):
            name = _STEPS[sn]
            done   = sn < current_step
            active = sn == current_step

            if done:
                cbg, cfg, ct = "#10b981", "#fff", "✓"
                lc, lw = "#10b981", "600"
                shadow = "filter:drop-shadow(0 1px 3px #10b98155);"
            elif active:
                cbg, cfg, ct = pc, "#fff", str(sn)
                lc, lw = pc, "700"
                shadow = f"box-shadow:0 0 0 4px {pc}28;"
            else:
                cbg, cfg, ct = "#f3f4f6", "#9ca3af", str(sn)
                lc, lw = "#9ca3af", "400"
                shadow = ""

            circle = (
                f'<div style="width:34px;height:34px;border-radius:50%;'
                f'background:{cbg};color:{cfg};{shadow}'
                f'display:flex;align-items:center;justify-content:center;'
                f'font-size:13px;font-weight:700;margin:0 auto;">{ct}</div>'
            )
            label = (
                f'<div style="font-size:9px;color:{lc};font-weight:{lw};'
                f'white-space:nowrap;text-align:center;margin-top:5px;">{name}</div>'
            )

            inner = (
                f'<div onclick="window.parent.location.href=window.parent.location.pathname+\'?nav_to={sn}\'"'
                f' style="cursor:pointer;" title="{sn}단계 · {name}으로 이동">'
                f'{circle}{label}</div>'
            )

            data_row.append(
                f'<td style="border:0;width:{STEP_W}px;padding:8px 4px 10px;'
                f'text-align:center;vertical-align:top;">{inner}</td>'
            )

            # Within-phase connector
            if i < len(psteps) - 1:
                nxt = psteps[i + 1]
                cline = "#10b981" if nxt <= current_step else "#e5e7eb"
                data_row.append(
                    f'<td style="border:0;width:{CONN_W}px;padding:0;vertical-align:middle;">'
                    f'<div style="height:2px;background:{cline};"></div></td>'
                )

        # Phase-boundary connector
        if idx < len(_PHASES) - 1:
            next_first = _PHASES[idx + 1][2][0]
            cline = "#10b981" if next_first <= current_step else "#e5e7eb"
            data_row.append(
                f'<td style="border:0;width:{CONN_W}px;padding:0;vertical-align:middle;">'
                f'<div style="height:2px;background:{cline};'
                f'border-left:4px solid #fafafa;border-right:4px solid #fafafa;"></div></td>'
            )
            ph_row.append(
                f'<td style="border:0;border-bottom:2px solid #e5e7eb !important;'
                f'width:{CONN_W}px;padding:0 0 6px;"></td>'
            )

    html = (
        '<div style="background:#fff;border-bottom:1px solid #e5e7eb;'
        'padding:12px 0 0;margin-bottom:20px;overflow-x:auto;">'
        '<table cellspacing="0" cellpadding="0" '
        'style="border-collapse:collapse;border:0;margin:0 auto;">'
        f'<tr>{"".join(ph_row)}</tr>'
        f'<tr>{"".join(data_row)}</tr>'
        '</table></div>'
    )
    st.markdown(html, unsafe_allow_html=True)
