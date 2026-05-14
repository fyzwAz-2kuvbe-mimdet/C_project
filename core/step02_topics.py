from prompts.mentoring_prompts import STEP02_TOPICS, SYSTEM_COACH


def build_prompt(refined_keyword: str, student_context: str) -> tuple:
    user = STEP02_TOPICS.format(
        refined_keyword=refined_keyword,
        student_context=student_context or "(없음)",
    )
    return SYSTEM_COACH, user
