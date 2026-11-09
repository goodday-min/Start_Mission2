
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