from prompts.mentoring_prompts import STEP07_ABSTRACT, SYSTEM_COACH


def build_prompt(topic: str, study_notes: str, motivation: str, key_findings: str, limits_and_next: str) -> tuple:
    user = STEP07_ABSTRACT.format(
        topic=topic,
        study_notes=study_notes or "(없음)",
        motivation=motivation or "(없음)",
        key_findings=key_findings or "(없음)",
        limits_and_next=limits_and_next or "(없음)",
    )
    return SYSTEM_COACH, user
