"""개별 퀴즈 한 문제를 표현하는 Quiz 클래스."""


class Quiz:
    """문제(question), 선택지 4개(choices), 정답 번호 1~4(answer), 힌트(hint)를 가진다."""

    def __init__(self, question, choices, answer, hint=""):
        self.question = question
        self.choices = choices
        self.answer = answer  # 1~4 중 하나의 번호
        self.hint = hint      # 보너스: 힌트 (없으면 빈 문자열)

    def display(self, number=None):
        """문제와 선택지를 화면에 출력한다."""
        title = f"[문제 {number}]" if number is not None else "[문제]"
        print(title)
        print(self.question)
        for i, choice in enumerate(self.choices, start=1):
            print(f" {i}. {choice}")

    def is_correct(self, user_answer):
        """사용자가 고른 번호가 정답이면 True."""
        return user_answer == self.answer

    def to_dict(self):
        """JSON 저장을 위해 딕셔너리로 바꾼다."""
        return {
            "question": self.question,
            "choices": self.choices,
            "answer": self.answer,
            "hint": self.hint,
        }

    @staticmethod
    def from_dict(data):
        """딕셔너리에서 Quiz 객체를 만든다. 형식이 잘못되면 ValueError를 낸다."""
        question = data["question"]
        choices = data["choices"]
        answer = data["answer"]
        hint = data.get("hint", "")   # 힌트가 없는 예전 데이터도 읽을 수 있게 기본값 사용
        if not isinstance(question, str) or not question.strip():
            raise ValueError("question 형식 오류")
        if not isinstance(choices, list) or len(choices) != 4:
            raise ValueError("choices는 4개여야 합니다")
        if not all(isinstance(c, str) and c.strip() for c in choices):
            raise ValueError("choices 형식 오류")
        if isinstance(answer, bool) or not isinstance(answer, int) or not 1 <= answer <= 4:
            raise ValueError("answer는 1~4여야 합니다")
        if not isinstance(hint, str):
            raise ValueError("hint 형식 오류")
        return Quiz(question, choices, answer, hint)
