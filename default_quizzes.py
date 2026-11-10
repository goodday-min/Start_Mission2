"""기본 퀴즈 데이터: 주제는 '파이썬/Git 기초'. Quiz 인스턴스로 생성한다."""

from quiz import Quiz


def get_default_quizzes():
    return [
        Quiz("파이썬에서 변수 x에 숫자 5를 저장하는 올바른 문장은?",
             ["x == 5", "let x = 5", "x = 5", "int x = 5"], 3,
             "= 는 '대입', == 는 '비교'예요."),
        Quiz("'hello' 처럼 따옴표로 감싼 값의 자료형은?",
             ["int", "str", "bool", "dict"], 2,
             "string(문자열)의 줄임말이에요."),
        Quiz("'이름': '철수' 처럼 키와 값을 짝지어 저장하는 자료형은?",
             ["list", "tuple", "dict", "str"], 3,
             "JSON 객체와 모양이 거의 같아요."),
        Quiz("반복 횟수를 모르고 '조건이 참인 동안' 반복할 때 알맞은 문법은?",
             ["for", "while", "if", "def"], 2,
             "'~하는 동안'이라는 뜻의 영어 단어예요."),
        Quiz("파이썬에서 함수를 정의할 때 사용하는 키워드는?",
             ["func", "define", "def", "function"], 3,
             "define의 앞 3글자예요."),
        Quiz("객체가 만들어질 때 자동으로 호출되어 속성을 초기화하는 메서드는?",
             ["__start__", "__init__", "__new_obj__", "__main__"], 2,
             "initialize(초기화)의 줄임말이에요."),
        Quiz("클래스 메서드의 첫 번째 매개변수 self가 가리키는 것은?",
             ["클래스의 이름", "현재 객체 자기 자신", "부모 클래스", "파일 경로"], 2),
        Quiz("JSON 파일 객체에서 데이터를 읽어 파이썬 객체로 바꾸는 함수는?",
             ["json.load()", "json.write()", "json.open()", "json.read()"], 1),
        Quiz("오류가 발생해도 프로그램이 멈추지 않도록 처리하는 구문은?",
             ["if / else", "try / except", "for / while", "import / from"], 2),
        Quiz("원격 저장소를 내 컴퓨터로 복제하는 Git 명령어는?",
             ["git init", "git commit", "git clone", "git push"], 3),
        Quiz("git add 명령어가 하는 일은?",
             ["변경된 파일을 커밋 대상(스테이징)에 올린다",
              "커밋을 원격 저장소에 업로드한다",
              "두 브랜치를 병합한다",
              "저장소를 삭제한다"], 1),
        Quiz("다른 브랜치로 이동(전환)할 때 사용하는 Git 명령어는?",
             ["git checkout", "git pull", "git init", "git add"], 1),
    ]
