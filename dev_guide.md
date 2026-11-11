# 퀴즈 게임 개발 순서 가이드 (커밋하면서 따라 하기)

실제로 개발하는 순서대로 **코드 → 실행 확인 → 커밋** 을 반복합니다. 이 폴더(`start_mission2`)의 `_완성본_참고`에 완성본이 있지만, 막힐 때만 보세요.

> 이 가이드의 코드는 단계별로 실제 실행 테스트를 거쳤습니다. 한 단계가 끝날 때마다 **반드시 실행해서 확인한 뒤** 커밋하세요.

## 전체 순서 한눈에 보기

| 단계 | 커밋 메시지 | 사용하는 Git 명령 | 만드는 파일 |
|---|---|---|---|
| 0 | (준비) | `config` | GitHub 저장소 생성, 폴더 준비 |
| 1 | `Docs: 프로젝트 초기 설정` | `init` `add` `commit` `push` | `.gitignore`, `README.md` |
| 2 | `Feat: 메뉴 기능 구현` | `add` `commit` | `main.py` |
| 3 | `Feat: Quiz 클래스 작성` | | `quiz.py` |
| 4 | `Feat: 기본 퀴즈 데이터 작성` | | `default_quizzes.py` |
| 5 | `Feat: 퀴즈 풀기 기능 구현` | **`checkout -b`**, **`merge`** | `main.py` 수정 |
| 6 | `Feat: 퀴즈 추가 기능 구현` | | `main.py` 수정 |
| 7 | `Feat: 퀴즈 목록 기능 구현` | | `main.py` 수정 |
| 8 | `Feat: 점수 확인 기능 구현` | | `main.py` 수정 |
| 9 | `Refactor: QuizGame 클래스로 구조 정리` | | `quiz_game.py` 신규, `main.py` 축소 |
| 10 | `Feat: Quiz 딕셔너리 변환 추가` | | `quiz.py` 수정 |
| 11 | `Feat: state.json 저장/불러오기 구현` | | `quiz_game.py` 수정 |
| 12 | `Docs: README 작성` | `push` | `README.md` |
| 13 | (clone/pull 실습) | **`clone`**, **`pull`** | |
| 14 | (제출물 캡처) | `log --oneline --graph` | |

커밋은 브랜치 병합 포함 14개 이상이 되어 요구사항(10개 이상)을 채웁니다. Git 명령어 7종(`init` `add` `commit` `push` `pull` `checkout` `clone`)도 모두 쓰게 됩니다.

**작업 순서가 이런 이유:** 처음에는 함수로 빠르게 동작하는 버전을 만들고(2~8단계), 기능이 다 모이면 `QuizGame` 클래스로 정리(9단계)한 다음, 마지막에 파일 저장(10~11단계)을 붙입니다. 과제의 Git 체크포인트 순서와 같아요.

---

## 0단계. 준비

1. GitHub에서 **New repository** 를 만듭니다. 이름은 예: `python-quiz-game`, Public. **README, .gitignore 추가 옵션은 모두 끄세요**(로컬에서 만들 거라 충돌합니다).
2. 터미널(PowerShell 또는 VSCode 터미널)에서 폴더를 만들고 이동합니다.
   ```bash
   cd C:\Users\user\codyssey\allinone\start_mission2
   mkdir quiz-game
   cd quiz-game
   ```
3. Git 사용자 정보를 한 번만 설정합니다(이미 했다면 건너뛰기).
   ```bash
   git config --global user.name "내 이름"
   git config --global user.email "GitHub 이메일"
   ```
4. 환경 확인(제출 스크린샷용으로 이 화면을 캡처해 두세요).
   ```bash
   python --version
   git --version
   ```
   `python`이 안 되면 `py --version`, `py main.py` 로 대신 실행합니다.

---

## 1단계. Git 저장소 설정 → 첫 commit + push

폴더(`quiz-game`) 안에서 파일 2개를 만듭니다.

**`.gitignore`**
```
__pycache__/
*.pyc
.vscode/
.idea/
```

**`README.md`** (일단 제목만, 12단계에서 완성)
```markdown
# 파이썬/Git 기초 퀴즈 게임

작성 중입니다.
```

```bash
git init
git add .gitignore README.md
git commit -m "Docs: 프로젝트 초기 설정 (.gitignore, README 생성)"
git branch -M main
git remote add origin https://github.com/<내아이디>/python-quiz-game.git
git push -u origin main
```
- `git init` : 이 폴더를 Git 저장소로 만듭니다.
- `git add` : 커밋에 포함할 파일을 올려둡니다(스테이징).
- `git commit` : 올려둔 변경을 하나의 기록으로 저장합니다.
- `git push` : 내 커밋을 GitHub로 올립니다. 처음 push 때 GitHub 로그인 창이 뜨면 로그인하세요.

GitHub 페이지를 새로고침해서 파일 2개가 보이면 성공입니다.

---

## 2단계. 메뉴 기능

`main.py` 를 만들고 아래를 그대로 입력합니다. 이 단계에서 **입력 처리 함수 `read_int`** 와 **메뉴 반복 흐름**, **Ctrl+C 처리**까지 만듭니다. 나머지 기능은 일단 "(준비 중)" 이라고만 출력하는 빈 함수(스텁)로 두고, 이후 단계에서 하나씩 진짜 코드로 교체합니다.

```python
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
```

**실행해서 확인**
```bash
python main.py
```
- `1` 입력 → "(준비 중) 퀴즈 풀기" 출력 후 메뉴 복귀
- 그냥 Enter / `abc` / `9` → 각각 안내 메시지 후 다시 입력
- `5` → 종료
- 실행 중 `Ctrl+C` → 에러 없이 안내 메시지 후 종료

```bash
git add main.py
git commit -m "Feat: 메뉴 기능 구현 (입력 검증, 종료 처리)"
git push
```

**개념 메모:** `while True` 는 "종료를 고를 때까지 반복"에 쓰고, `for` 는 "정해진 횟수/목록을 돌 때" 씁니다(5단계에서 `for`가 나옵니다). `try/except` 로 `int("abc")` 같은 오류를 잡아 프로그램이 죽지 않게 합니다.

---

## 3단계. Quiz 클래스

`quiz.py` 파일을 새로 만듭니다.

```python
"""개별 퀴즈 한 문제를 표현하는 Quiz 클래스."""


class Quiz:
    """문제(question), 선택지 4개(choices), 정답 번호 1~4(answer)를 가진다."""

    def __init__(self, question, choices, answer):
        self.question = question
        self.choices = choices
        self.answer = answer  # 1~4 중 하나의 번호

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
```

**실행해서 확인** (터미널에서 한 줄로 테스트)
```bash
python -c "from quiz import Quiz; q=Quiz('테스트',['a','b','c','d'],2); q.display(1); print(q.is_correct(2), q.is_correct(1))"
```
선택지 4개가 출력되고 마지막 줄이 `True False` 이면 성공입니다.

```bash
git add quiz.py
git commit -m "Feat: Quiz 클래스 작성 (문제 출력, 정답 확인)"
git push
```

**개념 메모:** `__init__` 은 객체가 만들어질 때 자동 실행되어 속성을 채우고, `self` 는 "지금 만들어지는/사용 중인 그 객체 자신"입니다.

---

## 4단계. 기본 퀴즈 데이터

`default_quizzes.py` 를 새로 만듭니다. 문제는 8개로 시작하지만, **본인이 직접 더 추가하거나 문제를 바꿔도 좋아요**(요구사항은 5개 이상, 직접 작성).

```python
"""기본 퀴즈 데이터: 주제는 '파이썬/Git 기초'."""

from quiz import Quiz


def get_default_quizzes():
    return [
        Quiz("파이썬에서 변수 x에 숫자 5를 저장하는 올바른 문장은?",
             ["x == 5", "let x = 5", "x = 5", "int x = 5"], 3),
        Quiz("'hello' 처럼 따옴표로 감싼 값의 자료형은?",
             ["int", "str", "bool", "dict"], 2),
        Quiz("'이름': '철수' 처럼 키와 값을 짝지어 저장하는 자료형은?",
             ["list", "tuple", "dict", "str"], 3),
        Quiz("파이썬에서 함수를 정의할 때 사용하는 키워드는?",
             ["func", "define", "def", "function"], 3),
        Quiz("객체가 만들어질 때 자동으로 호출되어 속성을 초기화하는 메서드는?",
             ["__start__", "__init__", "__new_obj__", "__main__"], 2),
        Quiz("오류가 발생해도 프로그램이 멈추지 않도록 처리하는 구문은?",
             ["if / else", "try / except", "for / while", "import / from"], 2),
        Quiz("원격 저장소를 내 컴퓨터로 복제하는 Git 명령어는?",
             ["git init", "git commit", "git clone", "git push"], 3),
        Quiz("다른 브랜치로 이동(전환)할 때 사용하는 Git 명령어는?",
             ["git checkout", "git pull", "git init", "git add"], 1),
    ]
```

**실행해서 확인**
```bash
python -c "from default_quizzes import get_default_quizzes as g; qs=g(); print(len(qs)); qs[0].display(1)"
```

```bash
git add default_quizzes.py
git commit -m "기본 퀴즈 데이터 작성 (파이썬/Git 기초 8문제)"
git push
```

---

## 5단계. 퀴즈 풀기 (브랜치 만들어서 작업 → 병합)

이번 기능만 **별도 브랜치**에서 작업합니다.

```bash
git checkout -b feature/play-quiz
```

`main.py` 를 수정합니다.

**(1)** 파일 맨 위의 `import sys` 와 `LINE = "=" * 40` 두 줄(사이 빈 줄 포함)을 아래로 **교체**:
```python
import sys

from default_quizzes import get_default_quizzes

LINE = "=" * 40
SUB_LINE = "-" * 40

quizzes = get_default_quizzes()   # 전체 퀴즈 목록 (프로그램이 켜져 있는 동안 메모리에 보관)
```

**(2)** 스텁 `def play_quiz(): print("(준비 중) 퀴즈 풀기")` 를 지우고, 그 자리에 아래 함수를 넣습니다.
```python
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
```

**실행해서 확인:** 메뉴 `1` 선택 → 8문제가 차례로 나오고, 정답/오답 안내와 마지막 결과 점수가 나오는지 확인합니다. 잘못된 입력(`0`, `5`, `abc`, 빈 입력)도 넣어 보세요.

```bash
git add main.py
git commit -m "Feat: 퀴즈 풀기 기능 구현 (출제, 채점, 결과 표시)"
git checkout main
git merge --no-ff feature/play-quiz -m "Merge: 퀴즈 풀기 브랜치 병합"
git push
git branch -d feature/play-quiz
```
- `checkout -b` : 새 브랜치를 만들고 이동합니다. `checkout main` : 다시 main으로 이동합니다.
- `merge --no-ff` : 병합 기록(merge commit)을 반드시 남깁니다. 이 옵션이 없으면 "빨리 감기" 병합이 되어 `git log --graph` 에 갈라졌다 합쳐지는 모양이 안 보여요. 제출 캡처에 필요하니 꼭 붙이세요.
- 병합 후 `git branch` 로 현재 `main` 위에 있는지 확인하세요.

---

## 6단계. 퀴즈 추가

(이제부터는 main 브랜치에서 바로 작업해도 됩니다.) `main.py` 수정:

**(1)** 위쪽 import에 한 줄 추가:
```python
from quiz import Quiz
```
(`from default_quizzes import get_default_quizzes` 바로 아래에 두면 됩니다.)

**(2)** 스텁 `add_quiz` 를 지우고, `show_menu` 아래쪽 아무 곳(예: `play_quiz` 위)에 아래를 넣습니다.
```python
def read_text(prompt):
    """빈 입력이 아닌 문자열을 받을 때까지 다시 묻는다."""
    while True:
        text = input(prompt).strip()
        if text == "":
            print("⚠️ 빈 입력입니다. 내용을 입력하세요.")
            continue
        return text


def add_quiz():
    print("📌 새로운 퀴즈를 추가합니다.")
    question = read_text("문제를 입력하세요: ")
    choices = [read_text(f"선택지 {i}: ") for i in range(1, 5)]
    answer = read_int("정답 번호 (1-4): ", 1, 4)
    quizzes.append(Quiz(question, choices, answer))
    print("✅ 퀴즈가 추가되었습니다!")
```

**실행해서 확인:** 메뉴 `2` → 문제/선택지 4개/정답 번호 입력 → 메뉴 `3`은 아직 준비 중이니 `1`번으로 풀어서 방금 추가한 문제가 9번째로 나오는지 확인합니다. 빈 입력, 정답 번호 `9`, `abc` 도 시도해 보세요. (아직 파일 저장은 없어서 종료하면 사라집니다. 11단계에서 해결해요.)

```bash
git add main.py
git commit -m "Feat: 퀴즈 추가 기능 구현 (입력 검증 포함)"
git push
```

---

## 7단계. 퀴즈 목록

스텁 `list_quizzes` 를 지우고 아래로 교체합니다.

```python
def list_quizzes():
    if not quizzes:
        print("⚠️ 등록된 퀴즈가 없습니다.")
        return
    print(f"📋 등록된 퀴즈 목록 (총 {len(quizzes)}개)")
    print(SUB_LINE)
    for i, quiz in enumerate(quizzes, start=1):
        print(f" [{i}] {quiz.question}")
    print(SUB_LINE)
```

**실행해서 확인:** 메뉴 `3` 에서 목록이 번호와 함께 나오는지, 퀴즈를 추가한 뒤 개수가 늘어나는지 확인합니다.

```bash
git add main.py
git commit -m "Feat: 퀴즈 목록 기능 구현"
git push
```

---

## 8단계. 점수 확인 (최고 점수 갱신)

**(1)** `quizzes = get_default_quizzes()` 줄 **바로 아래**에 추가:
```python
best_score = None                 # 최고 점수 (아직 안 풀었으면 None)
```

**(2)** `play_quiz` 함수 전체를 아래 버전으로 **교체**(최고 점수 비교/갱신이 추가됨, 바뀐 부분은 주석 표시):
```python
def play_quiz():
    global best_score                                 # 전역 변수 best_score를 이 함수에서 바꾸겠다는 선언
    if not quizzes:
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
    if best_score is None or score > best_score:      # 최고 점수와 비교 후 갱신
        best_score = score
        print("🎉 새로운 최고 점수입니다!")
    print(LINE)
```

**(3)** 스텁 `show_score` 를 지우고 아래로 교체:
```python
def show_score():
    if best_score is None:
        print("⚠️ 아직 퀴즈를 풀지 않았습니다. 퀴즈를 풀고 다시 확인해 주세요.")
        return
    print(f"🏆 최고 점수: {best_score}점")
```

**실행해서 확인**
1. 퀴즈를 풀기 전에 메뉴 `4` → "아직 퀴즈를 풀지 않았습니다"
2. 퀴즈를 한 번 풀고 → "새로운 최고 점수입니다!" 와 함께 메뉴 `4` 에 점수 표시
3. 일부러 다 틀리게 한 번 더 풀기 → 최고 점수가 그대로인지 확인

```bash
git add main.py
git commit -m "Feat: 점수 확인 및 최고 점수 갱신 기능 구현"
git push
```

**개념 메모:** 함수 안에서 바깥(전역) 변수를 바꾸려면 `global` 선언이 필요합니다. 이게 불편하다는 걸 느꼈다면 다음 단계의 클래스가 왜 필요한지 이해한 거예요.

---

## 9단계. QuizGame 클래스로 구조 정리 (리팩터링)

`main.py` 에 흩어진 변수(`quizzes`, `best_score`)와 함수들을 **하나의 클래스**로 묶습니다. 동작은 그대로이고 구조만 바뀝니다.

**(1)** `quiz_game.py` 새 파일:
```python
"""게임 전체를 관리하는 QuizGame 클래스."""

from default_quizzes import get_default_quizzes
from quiz import Quiz

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
    def __init__(self):
        self.quizzes = get_default_quizzes()   # 퀴즈 목록
        self.best_score = None                 # 최고 점수 (아직 안 풀었으면 None)

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
        print(LINE)

    def add_quiz(self):
        print("📌 새로운 퀴즈를 추가합니다.")
        question = read_text("문제를 입력하세요: ")
        choices = [read_text(f"선택지 {i}: ") for i in range(1, 5)]
        answer = read_int("정답 번호 (1-4): ", 1, 4)
        self.quizzes.append(Quiz(question, choices, answer))
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
                    print("👋 프로그램을 종료합니다.")
                    return
                print()
                actions[choice]()
        except (KeyboardInterrupt, EOFError):
            print("\n\n⚠️ 입력이 중단되었습니다. 프로그램을 종료합니다.")
```

**(2)** `main.py` 는 **전체를 지우고** 아래로 교체(짧아집니다):
```python
"""퀴즈 게임 실행 파일: python main.py"""

import sys

from quiz_game import QuizGame


def main():
    # 윈도우 콘솔에서도 한글/이모지가 깨지지 않도록 UTF-8 출력 설정
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8")
        except (AttributeError, ValueError):
            pass
    QuizGame().run()


if __name__ == "__main__":
    main()
```

**실행해서 확인:** 2~8단계에서 해본 것(메뉴, 풀기, 추가, 목록, 점수, 잘못된 입력, Ctrl+C)이 똑같이 동작해야 합니다.

```bash
git add main.py quiz_game.py
git commit -m "Refactor: QuizGame 클래스로 게임 로직 분리"
git push
```

**개념 메모:** `self.quizzes`, `self.best_score` 가 **속성**, `play_quiz` 등이 **메서드**입니다. 전역 변수와 `global` 이 사라진 점을 비교해 보세요. `Quiz`(문제 1개)와 `QuizGame`(게임 전체)로 역할이 나뉜 것도 과제의 핵심입니다.

---

## 10단계. Quiz를 JSON으로 저장할 수 있게 하기

JSON에는 파이썬 객체를 그대로 넣을 수 없어서, `Quiz` ↔ 딕셔너리 변환 메서드가 필요합니다. `quiz.py` 를 아래 **전체 내용으로 교체**합니다(3단계 코드 + 변환 메서드 2개).

```python
"""개별 퀴즈 한 문제를 표현하는 Quiz 클래스."""


class Quiz:
    """문제(question), 선택지 4개(choices), 정답 번호 1~4(answer)를 가진다."""

    def __init__(self, question, choices, answer):
        self.question = question
        self.choices = choices
        self.answer = answer  # 1~4 중 하나의 번호

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
        }

    @staticmethod
    def from_dict(data):
        """딕셔너리에서 Quiz 객체를 만든다. 형식이 잘못되면 ValueError를 낸다."""
        question = data["question"]
        choices = data["choices"]
        answer = data["answer"]
        if not isinstance(question, str) or not question.strip():
            raise ValueError("question 형식 오류")
        if not isinstance(choices, list) or len(choices) != 4:
            raise ValueError("choices는 4개여야 합니다")
        if not all(isinstance(c, str) and c.strip() for c in choices):
            raise ValueError("choices 형식 오류")
        if isinstance(answer, bool) or not isinstance(answer, int) or not 1 <= answer <= 4:
            raise ValueError("answer는 1~4여야 합니다")
        return Quiz(question, choices, answer)
```

**실행해서 확인**
```bash
python -c "from quiz import Quiz; q=Quiz('q',['a','b','c','d'],2); d=q.to_dict(); print(d); print(Quiz.from_dict(d).answer)"
```
딕셔너리가 출력되고 `2` 가 나오면 성공. 잘못된 데이터(예: answer 9)는 `ValueError` 가 납니다.

```bash
git add quiz.py
git commit -m "Feat: Quiz 딕셔너리 변환(to_dict/from_dict) 추가"
git push
```

---

## 11단계. state.json 저장/불러오기

`quiz_game.py` 를 아래 **전체 내용으로 교체**합니다. 9단계 코드에서 달라지는 점:
- `json`, `Path` import와 `STATE_FILE` 상수
- `load_state()` / `save_state()` / `use_default_data()` 메서드 추가
- 퀴즈 추가, 최고 점수 갱신, 종료, Ctrl+C/EOF 때 저장
- 시작할 때 `load_state()` 호출 (파일 없음 → 기본 퀴즈, 손상 → 안내 후 복구)

```python
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
```

**실행해서 확인** (여기가 중요합니다)
1. `python main.py` → "저장된 데이터가 없어 기본 퀴즈로 시작합니다"
2. 퀴즈 하나 추가 + 퀴즈 풀기 → 종료
3. 폴더에 `state.json` 이 생겼는지 열어 보기(한글이 정상으로 보여야 함)
4. 다시 `python main.py` → "저장된 데이터를 불러왔습니다 (퀴즈 9개, 최고점수 ...)" 및 목록/점수 유지 확인
5. `state.json` 내용을 일부러 망가뜨리기(예: `{ broken` 으로 덮어쓰기) → 실행 시 안내 메시지가 뜨고 기본 퀴즈로 복구되는지 확인
6. `state.json` 삭제 후 실행 → 정상 시작

```bash
git add quiz_game.py
git commit -m "Feat: state.json 저장/불러오기 구현 (파일 없음/손상 처리)"
git push
```

> `state.json` 을 GitHub에 올릴지는 선택입니다. 올려도 되고, 올리기 싫으면 `.gitignore` 에 `state.json` 을 한 줄 추가하세요.

**개념 메모:** `with open(..., encoding="utf-8")` 로 파일을 열고 읽고 쓰며, `json.dump` / `json.load` 가 파이썬 객체와 JSON 사이를 변환합니다. `try/except` 로 파일이 없거나 깨진 경우에도 프로그램이 죽지 않게 했습니다.

---

## 12단계. README 작성 후 최종 push

`README.md` 를 아래 내용으로 교체합니다. `<...>` 부분은 본인 정보로 바꾸세요.

```markdown
# 파이썬/Git 기초 퀴즈 게임

## 프로젝트 개요
터미널에서 동작하는 콘솔 퀴즈 게임입니다. 메뉴에서 번호를 선택해 퀴즈 풀기, 퀴즈 추가, 퀴즈 목록, 점수 확인을 할 수 있고, 프로그램을 종료해도 추가한 퀴즈와 최고 점수가 `state.json`에 저장되어 유지됩니다.

- Python 3.10 이상, 외부 라이브러리 없이 표준 라이브러리만 사용
- `Quiz`, `QuizGame` 두 클래스로 역할 분리
- Git/GitHub로 기능 단위 커밋, 브랜치 작업 후 병합

## 퀴즈 주제와 선정 이유
**주제: 파이썬/Git 기초**

(본인 말로 2~3줄. 예: 입학 연수에서 배우는 변수, 자료형, 조건문/반복문, 클래스, JSON, Git 명령어를 문제로 만들면 퀴즈를 만들고 푸는 과정이 곧 복습이 되기 때문에 이 주제를 골랐습니다.)

## 실행 방법
    git clone <저장소 URL>
    cd python-quiz-game
    python main.py

Python 3.10 이상이 필요합니다. (`python --version` 으로 확인)

## 기능 목록
| 메뉴 | 기능 |
|---|---|
| 1. 퀴즈 풀기 | 등록된 퀴즈를 출제하고 정답/오답을 알려주며, 끝나면 결과와 최고 점수 갱신 여부를 표시 |
| 2. 퀴즈 추가 | 문제, 선택지 4개, 정답 번호를 입력받아 저장 |
| 3. 퀴즈 목록 | 등록된 퀴즈 목록 출력 |
| 4. 점수 확인 | 최고 점수 확인 (아직 안 풀었으면 안내) |
| 5. 종료 | 저장 후 종료 |

입력 처리: 앞뒤 공백 제거, 빈 입력/숫자 아님/범위 밖 숫자는 안내 후 재입력, Ctrl+C/EOF 시 저장 후 안전 종료, `state.json` 이 없거나 손상되면 기본 퀴즈로 시작/복구.

## 파일 구조
    .
    ├── main.py              # 실행 진입점
    ├── quiz.py              # Quiz 클래스 (문제 1개)
    ├── quiz_game.py         # QuizGame 클래스 (메뉴, 게임 진행, 저장/불러오기)
    ├── default_quizzes.py   # 기본 퀴즈 데이터
    ├── state.json           # 실행 후 생성되는 저장 데이터
    ├── .gitignore
    └── README.md

## 데이터 파일 설명 (`state.json`)
- 경로: 프로젝트 루트의 `state.json` (UTF-8)
- 역할: 퀴즈 목록과 최고 점수를 저장해 재실행 후에도 유지

    {
      "quizzes": [
        {
          "question": "원격 저장소를 내 컴퓨터로 복제하는 Git 명령어는?",
          "choices": ["git init", "git commit", "git clone", "git push"],
          "answer": 3
        }
      ],
      "best_score": 80
    }

| 필드 | 설명 |
|---|---|
| `quizzes` | 퀴즈 목록 |
| `quizzes[].question` | 문제 문장 |
| `quizzes[].choices` | 선택지 4개 |
| `quizzes[].answer` | 정답 번호 (1~4) |
| `best_score` | 최고 점수 (0~100, 아직 안 풀었으면 `null`) |
```

> README 안의 코드 블록은 위에서는 들여쓰기 4칸으로 표기했어요. 실제 README에는 ```` ``` ```` 코드 블록으로 감싸면 보기 좋습니다.
> 점수는 `정답 수 × 100 ÷ 문제 수`(정수)입니다.

```bash
git add README.md
git commit -m "Docs: README 작성 (개요, 실행 방법, 기능, 파일 구조, 데이터 설명)"
git push
```

---

## 13단계. clone / pull 실습

개발이 끝난 후 순서대로 진행합니다.

```bash
# 1) 다른 위치에 저장소를 복제
cd C:\Users\user\codyssey\allinone\start_mission2
git clone https://github.com/<내아이디>/python-quiz-game.git quiz-game-clone

# 2) 복제본에서 간단한 변경 → commit → push
cd quiz-game-clone
# README.md 맨 아래에 한 줄 추가 (예: "clone 실습용 수정")
git add README.md
git commit -m "Docs: clone 실습용 README 수정"
git push

# 3) 원래 작업 폴더에서 pull 로 가져오기
cd ..\quiz-game
git pull

# 4) 반영 확인
git log --oneline -3
```
`README.md` 맨 아래에 추가한 줄이 보이면 성공입니다. `git pull` 이 "Already up to date" 가 나오면 push가 안 된 거니 복제본에서 `git push` 결과를 확인하세요.

---

## 14단계. 제출물 정리

- [ ] GitHub 저장소 URL
- [ ] 개발 환경 스크린샷: `python --version`, `git --version`, `git config --list` 일부 또는 VSCode 화면
- [ ] 실행 결과 스크린샷: 메뉴, 퀴즈 풀기, 퀴즈 추가, 퀴즈 목록, 점수 확인, (선택) 잘못된 입력/재시작 후 데이터 유지
- [ ] `git log --oneline --graph` 스크린샷 (병합 모양이 보여야 함)

```bash
git log --oneline --graph
```
README 예시처럼 `docs/screenshots/` 폴더에 캡처를 넣고 README에 연결하면 더 좋아요(추가 커밋: `Docs: 실행 화면 스크린샷 추가`).

---

## 보너스 (필수 완료 후 선택)
각각 별도 커밋으로 추가하세요. 막히면 `_완성본_참고` 를 참고하세요.

1. **랜덤 출제** : `import random` 후 `random.shuffle` 또는 `random.sample`
2. **문제 수 선택** : 풀기 전에 `read_int` 로 몇 문제인지 입력받기
3. **퀴즈 삭제** : 목록을 보여주고 번호 입력 → `self.quizzes.pop(번호 - 1)` → 저장
4. **힌트** : `Quiz` 에 `hint` 속성 추가, 풀이 중 `0` 입력 시 표시 (사용 시 점수 차감까지 하면 만점)
5. **점수 기록 히스토리** : 날짜/시간(`datetime`), 푼 문제 수, 점수를 리스트로 저장

## 막혔을 때 체크리스트
- `ModuleNotFoundError` : `quiz.py` 등 파일이 `main.py` 와 **같은 폴더**에 있는지, 파일명 오타 없는지
- 한글이 깨져 보임 : 파일을 UTF-8로 저장했는지(VSCode 우측 하단 인코딩 확인)
- `git push` 거절 : GitHub 저장소를 README 포함으로 만들었다면 충돌합니다. `git pull --rebase origin main` 후 다시 push
- `git merge` 중 충돌 : 충돌 표시(`<<<<<<<`)를 직접 정리하고 `git add` → `git commit`
