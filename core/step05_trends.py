from prompts.mentoring_prompts import STEP05_TRENDS, SYSTEM_COACH


def build_prompt(topic: str, current_level: str) -> tuple:
    user = STEP05_TRENDS.format(
        topic=topic,
        current_level=current_level or "(없음)",
    )
    return SYSTEM_COACH, user
