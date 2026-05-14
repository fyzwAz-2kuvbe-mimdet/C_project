import json
from prompts.mentoring_prompts import STEP04_RESOURCES, SYSTEM_COACH


def build_prompt(topic: str, roadmap: list) -> tuple:
    roadmap_text = json.dumps(roadmap, ensure_ascii=False, indent=2)
    user = STEP04_RESOURCES.format(topic=topic, roadmap=roadmap_text)
    return SYSTEM_COACH, user
