import json
from prompts.mentoring_prompts import STEP01_KEYWORD, SYSTEM_COACH


def build_prompt(keyword: str) -> tuple:
    user = STEP01_KEYWORD.format(keyword=keyword)
    return SYSTEM_COACH, user
