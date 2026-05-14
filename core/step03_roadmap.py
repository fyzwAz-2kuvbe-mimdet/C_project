from prompts.mentoring_prompts import STEP03_ROADMAP, SYSTEM_COACH


def build_prompt(topic: str, curiosity: str, current_level: str) -> tuple:
    user = STEP03_ROADMAP.format(
        topic=topic,
        curiosity=curiosity or "(없음)",
        current_level=current_level or "(없음)",
    )
    return SYSTEM_COACH, user
