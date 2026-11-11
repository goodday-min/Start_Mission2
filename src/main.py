"""파이썬/Git 기초 퀴즈 게임 (함수 버전)"""

import sys

LINE = "=" * 40


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


# --- 아직 구현하지 않은 기능 (이후 단계에서 하나씩 진짜 함수로 교체) ---
def play_quiz():
    print("(준비 중) 퀴즈 풀기")


def add_quiz():
    print("(준비 중) 퀴즈 추가")


def list_quizzes():
    print("(준비 중) 퀴즈 목록")


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