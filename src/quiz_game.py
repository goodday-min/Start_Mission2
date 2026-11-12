"""게임 전체를 관리하는 QuizGame 클래스."""

import json
from pathlib import Path

from default_quizzes import get_default_quizzes
from quiz import Quiz

# 프로젝트 루트(이 파일이 있는 폴더)의 state.json
STATE_FILE = Path(__file__).resolve().parent / "state.json"

LINE = "=" * 40
SUB_LINE = "-" * 40


def read_int(prompt, low, high):
    """low~high 사이 정수를 받을 때까지 다시 묻는다."""
    while True:
        text = input(prompt).strip()
        if text == "":
            print("⚠️ 빈 입력입니다. 숫자를 입력하세요.")
            continue
        try:
            number = int(text)
        except ValueError:
            print(f"⚠️ 숫자만 입력할 수 있습니다. {low}-{high} 사이의 숫자를 입력하세요.")
            continue
        if not low <= number <= high:
            print(f"⚠️ 잘못된 입력입니다. {low}-{high} 사이의 숫자를 입력하세요.")
            continue
        return number


def read_text(prompt):
    """빈 입력이 아닌 문자열을 받을 때까지 다시 묻는다."""
    while True:
        text = input(prompt).strip()
        if text == "":
            print("⚠️ 빈 입력입니다. 내용을 입력하세요.")
            continue
        return text


class QuizGame:
    def __init__(self, state_file=STATE_FILE):
        self.state_file = Path(state_file)
        self.quizzes = []          # 퀴즈 목록
        self.best_score = None     # 최고 점수 (아직 안 풀었으면 None)

    # ---------- 저장 / 불러오기 ----------
    def use_default_data(self):
        self.quizzes = get_default_quizzes()
        self.best_score = None

    def load_state(self):
        """state.json을 읽는다. 없으면 기본 데이터, 손상되었으면 안내 후 초기화."""
        if not self.state_file.exists():
            self.use_default_data()
            print("📂 저장된 데이터가 없어 기본 퀴즈로 시작합니다.")
            return
        try:
            with open(self.state_file, "r", encoding="utf-8") as f:
                data = json.load(f)
            quizzes = [Quiz.from_dict(item) for item in data["quizzes"]]
            best_score = data.get("best_score")
            if best_score is not None and (
                isinstance(best_score, bool) or not isinstance(best_score, int)
            ):
                raise ValueError("best_score 형식 오류")
        except (OSError, ValueError, KeyError, TypeError, AttributeError) as e:
            # JSONDecodeError, UnicodeDecodeError는 ValueError의 하위 클래스
            print(f"⚠️ 데이터 파일을 읽을 수 없습니다. ({type(e).__name__}) 기본 데이터로 초기화합니다.")
            self.use_default_data()
            self.save_state()
            return
        self.quizzes = quizzes
        self.best_score = best_score
        score_text = f"{best_score}점" if best_score is not None else "없음"
        print(f"📂 저장된 데이터를 불러왔습니다. (퀴즈 {len(quizzes)}개, 최고점수 {score_text})")

    def save_state(self):
        """퀴즈와 최고 점수를 state.json에 UTF-8로 저장한다. 성공하면 True."""
        data = {
            "quizzes": [q.to_dict() for q in self.quizzes],
            "best_score": self.best_score,
        }
        try:
            with open(self.state_file, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            return True
        except OSError as e:
            print(f"⚠️ 파일 저장에 실패했습니다: {e}")
            return False

    # ---------- 메뉴 ----------

    def show_menu(self):
        print(LINE)
        print(" 🎯 파이썬/Git 기초 퀴즈 게임 🎯")
        print(LINE)
        print(" 1. 퀴즈 풀기")
        print(" 2. 퀴즈 추가")
        print(" 3. 퀴즈 목록")
        print(" 4. 점수 확인")
        print(" 5. 종료")
        print(LINE)

    def play_quiz(self):
        if not self.quizzes:
            print("⚠️ 등록된 퀴즈가 없습니다. 먼저 퀴즈를 추가해 주세요.")
            return

        total = len(self.quizzes)
        print(f"📝 퀴즈를 시작합니다! (총 {total}문제)")
        correct = 0
        for number, quiz in enumerate(self.quizzes, start=1):
            print(SUB_LINE)
            quiz.display(number)
            user_answer = read_int("정답 입력: ", 1, 4)
            if quiz.is_correct(user_answer):
                print("✅ 정답입니다!")
                correct += 1
            else:
                print(f"❌ 오답입니다. 정답은 {quiz.answer}번입니다.")

        score = correct * 100 // total
        print(LINE)
        print(f"🏆 결과: {total}문제 중 {correct}문제 정답! ({score}점)")
        if self.best_score is None or score > self.best_score:
            self.best_score = score
            print("🎉 새로운 최고 점수입니다!")
            self.save_state()
        print(LINE)

    def add_quiz(self):
        print("📌 새로운 퀴즈를 추가합니다.")
        question = read_text("문제를 입력하세요: ")
        choices = [read_text(f"선택지 {i}: ") for i in range(1, 5)]
        answer = read_int("정답 번호 (1-4): ", 1, 4)
        self.quizzes.append(Quiz(question, choices, answer))
        if self.save_state():
            print("✅ 퀴즈가 추가되었습니다!")

    def list_quizzes(self):
        if not self.quizzes:
            print("⚠️ 등록된 퀴즈가 없습니다.")
            return
        print(f"📋 등록된 퀴즈 목록 (총 {len(self.quizzes)}개)")
        print(SUB_LINE)
        for i, quiz in enumerate(self.quizzes, start=1):
            print(f" [{i}] {quiz.question}")
        print(SUB_LINE)

    def show_score(self):
        if self.best_score is None:
            print("⚠️ 아직 퀴즈를 풀지 않았습니다. 퀴즈를 풀고 다시 확인해 주세요.")
            return
        print(f"🏆 최고 점수: {self.best_score}점")

    def run(self):
        self.load_state()
        actions = {
            1: self.play_quiz,
            2: self.add_quiz,
            3: self.list_quizzes,
            4: self.show_score,
        }
        try:
            while True:
                print()
                self.show_menu()
                choice = read_int("선택: ", 1, 5)
                if choice == 5:
                    self.save_state()
                    print("👋 프로그램을 종료합니다. 데이터가 저장되었습니다.")
                    return
                print()
                actions[choice]()
        except (KeyboardInterrupt, EOFError):
            print("\n\n⚠️ 입력이 중단되었습니다. 데이터를 저장하고 종료합니다.")
            self.save_state()