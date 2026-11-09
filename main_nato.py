import json
import random

class Quiz:
    def __init__(self, question, answer):
        self.question = question
        self.answer = answer

class QuizGame:
    def __init__(self):
        self.quizzes = []
        self.score = 0
        self.load()

    def load(self):
        try:
            with open("quizzes.json", "r", encoding="utf-8") as f:
                data = json.load(f)
                self.quizzes = data.get("quizzes", [])
                self.score = data.get("score", 0)
        except FileNotFoundError:
            self.quizzes = []
            self.score = 0

    def save(self):
        data = {
            "quizzes": self.quizzes,
            "score": self.score
        }
        with open("quizzes.json", "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

    def play(self):
        if len(self.quizzes) == 0:
            print("퀴즈가 없습니다.")
            return

        quiz = random.choice(self.quizzes)

        print(f"\nQ. {quiz['question']}")
        answer = input("정답: ")

        if answer == quiz['answer']:
            print("정답입니다! 🎉")
            self.score += 1
        else:
            print(f"틀렸습니다. 정답은 {quiz['answer']} 입니다.")

        self.save()

    def add_quiz(self):
        print("\n=== 퀴즈 추가 ===")

        question = input("문제를 입력하세요: ")
        answer = input("정답을 입력하세요: ")

        if question == "" or answer == "":
            print("문제와 정답을 모두 입력해주세요.")
            return

        new_quiz = {
            "question": question,
            "answer": answer
        }

        self.quizzes.append(new_quiz)
        self.save()
        print("퀴즈가 추가되었습니다! ✅")

    def run(self):
        while True:
            print("\n=== 퀴즈 게임 ===")
            print("1. 퀴즈 풀기")
            print("2. 퀴즈 추가")
            print("3. 점수 확인")
            print("4. 종료")

            choice = input("선택: ")

            if choice == "1":
                self.play()
            elif choice == "2":
                self.add_quiz()
            elif choice == "3":
                print(f"\n현재 점수: {self.score}점")
            elif choice == "4":
                print("게임을 종료합니다. 👋")
                break
            else:
                print("1~4 중에서 선택해주세요.")

# 실행
game = QuizGame()
game.run()