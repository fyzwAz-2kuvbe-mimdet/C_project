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

_SYSTEM_TEMPLATE = """당신은 {grade_name} 학생을 위한 AI 학습 코치입니다.
학습 유형: {type_name} ({type_core})
질문 스타일 힌트: {question_style}
언어 수준 지침: {vocab_guide}

학생의 관심사를 분석하고 학습을 더 깊이 있게 만들기 위한 후속 질문 3~5개를 생성하세요.
- 관심사가 막연하면 범위를 좁히는 질문을 하세요.
- 관심사가 구체적이면 원리·맥락·응용까지 파고드는 질문을 하세요.
- 학습 유형의 핵심 역량({type_core})과 연결되는 질문을 포함하세요.

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
        max_tokens=800,
        json_mode=True,
    )

    questions = result.get("follow_up_questions", [])
    if len(questions) < 3:
        questions += ["이 주제에서 가장 궁금한 점이 무엇인가요?"] * (3 - len(questions))
    result["follow_up_questions"] = questions[:5]
    return result
