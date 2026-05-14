from prompts.mentoring_prompts import STEP06_REFLECTION, SYSTEM_COACH


def build_prompt(topic: str, what_i_studied: str, most_interesting: str, stuck_points: str) -> tuple:
    user = STEP06_REFLECTION.format(
        topic=topic,
        what_i_studied=what_i_studied or "(없음)",
        most_interesting=most_interesting or "(없음)",
        stuck_points=stuck_points or "(없음)",
    )
    return SYSTEM_COACH, user
