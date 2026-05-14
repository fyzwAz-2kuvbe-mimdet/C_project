from prompts.mentoring_prompts import STEP08_FEEDBACK, SYSTEM_COACH


def build_prompt(topic: str, student_draft: str, ai_abstract: str) -> tuple:
    user = STEP08_FEEDBACK.format(
        topic=topic,
        student_draft=student_draft or "(없음)",
        ai_abstract=ai_abstract or "(없음)",
    )
    return SYSTEM_COACH, user
