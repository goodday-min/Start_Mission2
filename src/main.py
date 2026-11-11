"""파이썬/Git 기초 퀴즈 게임 (함수 버전)"""

import sys

from default_quizzes import get_default_quizzes

from quiz import Quiz

LINE = "=" * 40
SUB_LINE = "-" * 40

quizzes = get_default_quizzes()   # 전체 퀴즈 목록 (프로그램이 켜져 있는 동안 메모리에 보관)

def read_int(prompt, low, high):
    """low~high 사이 정수를 받을 때까지 다시 묻는다."""
    while True:
        text = input(prompt).strip()          # 앞뒤 공백 제거
        if text == "":                        # 빈 입력
            print("⚠️ 빈 입력입니다. 숫자를 입력하세요.")
            continue
        try:
            number = int(text)                # 숫자 변환 실패 처리
        except ValueError:
            print(f"⚠️ 숫자만 입력할 수 있습니다. {low}-{high} 사이의 숫자를 입력하세요.")
            continue
        if not low <= number <= high:         # 범위 밖 숫자
            print(f"⚠️ 잘못된 입력입니다. {low}-{high} 사이의 숫자를 입력하세요.")
            continue
        return number


def show_menu():
    print(LINE)
    print(" 🎯 파이썬/Git 기초 퀴즈 게임 🎯")
    print(LINE)
    print(" 1. 퀴즈 풀기")
    print(" 2. 퀴즈 추가")
    print(" 3. 퀴즈 목록")
    print(" 4. 점수 확인")
    print(" 5. 종료")
    print(LINE)

def read_text(prompt):
    """빈 입력이 아닌 문자열을 받을 때까지 다시 묻는다."""
    while True:
        text = input(prompt).strip()
        if text == "":
            print("⚠️ 빈 입력입니다. 내용을 입력하세요.")
            continue
        return text



# --- 아직 구현하지 않은 기능 (이후 단계에서 하나씩 진짜 함수로 교체) ---
def play_quiz():
    
    if not quizzes:                                   # 퀴즈가 없는 경우
        print("⚠️ 등록된 퀴즈가 없습니다. 먼저 퀴즈를 추가해 주세요.")
        return

    total = len(quizzes)
    print(f"📝 퀴즈를 시작합니다! (총 {total}문제)")
    correct = 0
    for number, quiz in enumerate(quizzes, start=1):
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
    print(LINE)


def add_quiz():
    print("📌 새로운 퀴즈를 추가합니다.")
    question = read_text("문제를 입력하세요: ")
    choices = [read_text(f"선택지 {i}: ") for i in range(1, 5)]
    answer = read_int("정답 번호 (1-4): ", 1, 4)
    quizzes.append(Quiz(question, choices, answer))
    print("✅ 퀴즈가 추가되었습니다!")


def list_quizzes():
    if not quizzes:
        print("⚠️ 등록된 퀴즈가 없습니다.")
        return
    print(f"📋 등록된 퀴즈 목록 (총 {len(quizzes)}개)")
    print(SUB_LINE)
    for i, quiz in enumerate(quizzes, start=1):
        print(f" [{i}] {quiz.question}")
    print(SUB_LINE)

def show_score():
    print("(준비 중) 점수 확인")
# ------------------------------------------------------------------


def main():
    # 윈도우 콘솔에서도 한글/이모지가 깨지지 않도록 UTF-8 출력 설정
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8")
        except (AttributeError, ValueError):
            pass

    actions = {1: play_quiz, 2: add_quiz, 3: list_quizzes, 4: show_score}
    try:
        while True:
            print()
            show_menu()
            choice = read_int("선택: ", 1, 5)
            if choice == 5:
                print("👋 프로그램을 종료합니다.")
                return
            print()
            actions[choice]()
    except (KeyboardInterrupt, EOFError):
        # Ctrl+C 또는 입력 스트림 종료 시 비정상 종료하지 않고 안내 후 종료
        print("\n\n⚠️ 입력이 중단되었습니다. 프로그램을 종료합니다.")


if __name__ == "__main__":
    main()