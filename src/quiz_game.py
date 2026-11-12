"""게임 전체를 관리하는 QuizGame 클래스."""

import json
import random
from datetime import datetime
from pathlib import Path

from default_quizzes import get_default_quizzes
from quiz import Quiz

# 프로젝트 루트(src 폴더의 상위 폴더)의 state.json
STATE_FILE = Path(__file__).resolve().parent.parent / "state.json"

LINE = "=" * 40
SUB_LINE = "-" * 40
HISTORY_VIEW_COUNT = 10   # 기록 보기에서 보여줄 최근 게임 수


class CancelInput(Exception):
    """입력 도중 사용자가 취소했을 때 사용하는 예외."""


def read_int(prompt, low, high, extras=()):
    """low~high 사이 정수를 받을 때까지 다시 묻는다.

    extras에 문자열(예: "q")을 주면 그 입력은 소문자 문자열 그대로 돌려준다.
    Ctrl+C / EOF는 그대로 올려서 호출한 쪽(run)에서 안전 종료한다.
    """
    while True:
        text = input(prompt).strip()
        if text == "":
            print("⚠️ 빈 입력입니다. 숫자를 입력하세요.")
            continue
        if text.lower() in extras:
            return text.lower()
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
    """빈 입력이 아닌 문자열을 받는다. '/q' 를 입력하면 CancelInput 을 발생시킨다."""
    while True:
        text = input(prompt).strip()
        if text.lower() == "/q":
            raise CancelInput
        if text == "":
            print("⚠️ 빈 입력입니다. 내용을 입력하세요.")
            continue
        return text


def validate_history_item(item):
    """게임 기록 한 건의 형식을 검사한다. 잘못되면 ValueError."""
    if not isinstance(item, dict):
        raise ValueError("history 항목 형식 오류")
    if not isinstance(item["played_at"], str):
        raise ValueError("played_at 형식 오류")
    for key in ("total", "correct", "hints", "score"):
        value = item[key]
        if isinstance(value, bool) or not isinstance(value, int) or value < 0:
            raise ValueError(f"{key} 형식 오류")
    return {key: item[key] for key in ("played_at", "total", "correct", "hints", "score")}


class QuizGame:
    def __init__(self, state_file=STATE_FILE):
        self.state_file = Path(state_file)
        self.quizzes = []          # 퀴즈 목록
        self.best_score = None     # 최고 점수 (아직 안 풀었으면 None)
        self.history = []          # 보너스: 게임 기록 목록

    # ---------- 저장 / 불러오기 ----------
    def use_default_data(self):
        self.quizzes = get_default_quizzes()
        self.best_score = None
        self.history = []

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
            # history가 없는 예전 파일도 읽을 수 있게 기본값은 빈 리스트
            history = [validate_history_item(item) for item in data.get("history", [])]
        except (OSError, ValueError, KeyError, TypeError, AttributeError) as e:
            # JSONDecodeError, UnicodeDecodeError는 ValueError의 하위 클래스
            print(f"⚠️ 데이터 파일을 읽을 수 없습니다. ({type(e).__name__}) 기본 데이터로 초기화합니다.")
            self.use_default_data()
            self.save_state()
            return
        self.quizzes = quizzes
        self.best_score = best_score
        self.history = history
        score_text = f"{best_score}점" if best_score is not None else "없음"
        print(f"📂 저장된 데이터를 불러왔습니다. (퀴즈 {len(quizzes)}개, 최고점수 {score_text}, 기록 {len(history)}건)")

    def save_state(self):
        """퀴즈, 최고 점수, 게임 기록을 state.json에 UTF-8로 저장한다. 성공하면 True."""
        data = {
            "quizzes": [q.to_dict() for q in self.quizzes],
            "best_score": self.best_score,
            "history": self.history,
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
        print(" 5. 퀴즈 삭제")
        print(" 6. 게임 기록 보기")
        print(" 7. 종료")
        print(LINE)

    # ---------- 퀴즈 풀기 ----------
    def play_quiz(self):
        if not self.quizzes:
            print("⚠️ 등록된 퀴즈가 없습니다. 먼저 퀴즈를 추가해 주세요.")
            return

        available = len(self.quizzes)
        count = read_int(f"몇 문제를 풀까요? (1-{available}, 취소: 0): ", 0, available)
        if count == 0:
            print("퀴즈 풀기를 취소했습니다.")
            return
        questions = random.sample(self.quizzes, count)   # 보너스: 랜덤 순서로 count개 출제

        print(f"\n📝 퀴즈를 시작합니다! (총 {count}문제)")
        correct = 0     # 정답 수
        hints = 0       # 힌트를 쓴 문제 수
        points = 0      # 정답 2점, 힌트 쓴 정답 1점, 오답 0점
        for number, quiz in enumerate(questions, start=1):
            print(SUB_LINE)
            quiz.display(number)
            result = self.ask_answer(quiz)
            if result is None:      # 중단
                print("⏹️ 퀴즈를 중단하고 메뉴로 돌아갑니다. (점수는 기록되지 않습니다)")
                return
            is_correct, hint_used = result
            if hint_used:
                hints += 1
            if is_correct:
                correct += 1
                points += 1 if hint_used else 2

        score = points * 100 // (2 * count)
        print(LINE)
        print(f"🏆 결과: {count}문제 중 {correct}문제 정답! ({score}점)")
        if hints:
            print(f"💡 힌트 {hints}회 사용 (힌트를 쓴 정답은 절반 점수로 계산)")
        if self.best_score is None or score > self.best_score:
            self.best_score = score
            print("🎉 새로운 최고 점수입니다!")
        print(LINE)

        self.history.append({
            "played_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "total": count,
            "correct": correct,
            "hints": hints,
            "score": score,
        })
        self.save_state()

    def ask_answer(self, quiz):
        """한 문제를 묻고 (정답 여부, 힌트 사용 여부)를 돌려준다. 중단(q)하면 None."""
        if quiz.hint:
            prompt = "정답 입력 (힌트: 0, 중단: q): "
            low = 0
        else:
            prompt = "정답 입력 (중단: q): "
            low = 1
        hint_used = False
        while True:
            answer = read_int(prompt, low, 4, extras=("q",))
            if answer == "q":
                return None
            if answer == 0:
                print(f"💡 힌트: {quiz.hint}")
                hint_used = True
                continue
            break

        if quiz.is_correct(answer):
            if hint_used:
                print("✅ 정답입니다! (힌트를 사용해 절반 점수)")
            else:
                print("✅ 정답입니다!")
            return True, hint_used
        print(f"❌ 오답입니다. 정답은 {quiz.answer}번입니다.")
        return False, hint_used

    # ---------- 퀴즈 추가 ----------
    def add_quiz(self):
        print("📌 새로운 퀴즈를 추가합니다. (입력 도중 취소: /q)")
        try:
            question = read_text("문제를 입력하세요: ")
            choices = [read_text(f"선택지 {i}: ") for i in range(1, 5)]
            answer = read_int("정답 번호 (1-4, 취소: 0): ", 0, 4)
            if answer == 0:
                raise CancelInput
            hint = input("힌트 (없으면 Enter): ").strip()
        except CancelInput:
            print("퀴즈 추가를 취소했습니다.")
            return
        self.quizzes.append(Quiz(question, choices, answer, hint))
        if self.save_state():
            print("✅ 퀴즈가 추가되었습니다!")

    # ---------- 퀴즈 목록 ----------
    def list_quizzes(self):
        if not self.quizzes:
            print("⚠️ 등록된 퀴즈가 없습니다.")
            return
        print(f"📋 등록된 퀴즈 목록 (총 {len(self.quizzes)}개)")
        print(SUB_LINE)
        for i, quiz in enumerate(self.quizzes, start=1):
            print(f" [{i}] {quiz.question}")
        print(SUB_LINE)

    # ---------- 점수 확인 ----------
    def show_score(self):
        if self.best_score is None:
            print("⚠️ 아직 퀴즈를 풀지 않았습니다. 퀴즈를 풀고 다시 확인해 주세요.")
            return
        print(f"🏆 최고 점수: {self.best_score}점")

    # ---------- 퀴즈 삭제 ----------
    def delete_quiz(self):
        if not self.quizzes:
            print("⚠️ 삭제할 퀴즈가 없습니다.")
            return
        self.list_quizzes()
        number = read_int(f"삭제할 퀴즈 번호 (1-{len(self.quizzes)}, 취소: 0): ", 0, len(self.quizzes))
        if number == 0:
            print("삭제를 취소했습니다.")
            return
        removed = self.quizzes.pop(number - 1)
        if self.save_state():
            print(f"🗑️ 삭제되었습니다: {removed.question}")

    # ---------- 게임 기록 ----------
    def show_history(self):
        if not self.history:
            print("⚠️ 아직 게임 기록이 없습니다. 퀴즈를 풀고 다시 확인해 주세요.")
            return
        recent = self.history[-HISTORY_VIEW_COUNT:]
        print(f"📜 게임 기록 (총 {len(self.history)}회 중 최근 {len(recent)}회)")
        print(SUB_LINE)
        for item in reversed(recent):   # 최신 기록이 위로
            print(f" {item['played_at']} | {item['total']}문제 중 {item['correct']}정답"
                  f" | 힌트 {item['hints']}회 | {item['score']}점")
        print(SUB_LINE)

    # ---------- 실행 ----------
    def run(self):
        self.load_state()
        actions = {
            1: self.play_quiz,
            2: self.add_quiz,
            3: self.list_quizzes,
            4: self.show_score,
            5: self.delete_quiz,
            6: self.show_history,
        }
        try:
            while True:
                print()
                self.show_menu()
                choice = read_int("선택: ", 1, 7)
                if choice == 7:
                    self.save_state()
                    print("👋 프로그램을 종료합니다. 데이터가 저장되었습니다.")
                    return
                print()
                actions[choice]()
        except (KeyboardInterrupt, EOFError):
            print("\n\n⚠️ 입력이 중단되었습니다. 데이터를 저장하고 종료합니다.")
            self.save_state()
