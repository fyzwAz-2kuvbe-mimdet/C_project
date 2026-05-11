from core.llm_client import ask
from config.learning_types import get_type

_GRADE_INFO = {
    "초4": ("elementary", "초등학교 4학년"),
    "초5": ("elementary", "초등학교 5학년"),
    "초6": ("elementary", "초등학교 6학년"),
    "중1": ("middle", "중학교 1학년"),
    "중2": ("middle", "중학교 2학년"),
    "중3": ("middle", "중학교 3학년"),
    "고1": ("high", "고등학교 1학년"),
    "고2": ("high", "고등학교 2학년"),
    "고3": ("high", "고등학교 3학년"),
}

_VOCAB_GUIDE = {
    "elementary": "친근하고 쉬운 표현을 사용하고, 어려운 단어는 괄호로 설명을 덧붙이세요. 학생이 재미있게 느낄 수 있도록 격려해주세요.",
    "middle": "교과서 수준의 어휘를 사용하되, 전문 용어는 간략히 설명하세요.",
    "high": "학술적 용어와 개념을 자연스럽게 사용하세요. 비판적 사고를 자극하는 질문을 포함하세요.",
}

_SYSTEM_TEMPLATE = """당신은 {grade_name} 학생을 위한 친절한 AI 학습 코치입니다.
학습 유형: {type_name} ({type_core})
언어 수준 지침: {vocab_guide}

학생이 관심사를 처음 접하는 입문자일 수 있습니다. 어렵거나 전문적인 질문은 절대 하지 마세요.

[후속 질문 목적]
1. 이 관심사가 어떤 분야(과학/예술/사회/기술/스포츠 등)에 속하는지 스스로 인식하게 돕기
2. 관심사와 연결된 주변 키워드·개념을 자연스럽게 확장하기
3. 학생이 이미 알고 있는 것과 더 알고 싶은 것을 파악하기

[질문 작성 규칙]
- 정답이 없는 열린 질문으로 작성하세요.
- "왜", "어떻게", "무엇이" 같은 탐색적 표현으로 시작하세요.
- 전문 용어, 수식, 심화 개념이 들어간 질문은 금지입니다.
- 학생이 일상 언어로 편하게 답할 수 있어야 합니다.
- 예시: "이 주제 중에서 특히 어떤 부분이 가장 신기하거나 궁금했나요?"
- 예시: "이 주제가 우리 일상생활과 어떻게 연결될 것 같나요?"
- 예시: "비슷하거나 관련 있다고 생각하는 다른 분야나 주제가 있나요?"

반드시 아래 JSON 형식으로만 응답하세요:
{{
  "follow_up_questions": ["질문1", "질문2", "질문3"],
  "estimated_subtopic": "추정 세부 주제 (15자 이내)",
  "depth_level": "초급 또는 중급 또는 고급"
}}"""


def diagnose(interest_text: str, grade: str, learning_type_id: str) -> dict:
    level, grade_name = _GRADE_INFO.get(grade, ("high", grade))
    type_info = get_type(learning_type_id)

    system_prompt = _SYSTEM_TEMPLATE.format(
        grade_name=grade_name,
        type_name=type_info.get("name", ""),
        type_core=type_info.get("core", ""),
        question_style=type_info.get("question_style", ""),
        vocab_guide=_VOCAB_GUIDE[level],
    )

    result = ask(
        system_prompt,
        f"학생의 관심사: {interest_text}",
        max_tokens=8192,
        json_mode=True,
    )

    questions = result.get("follow_up_questions", [])
    if len(questions) < 3:
        questions += ["이 주제에서 가장 궁금한 점이 무엇인가요?"] * (3 - len(questions))
    result["follow_up_questions"] = questions[:5]
    return result
