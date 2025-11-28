# PyCharm (Professional) 인터랙티브 모드 설정 가이드
questionary / prompt_toolkit 기반 CLI 사용 시 필수 설정

이 문서는 PyCharm Professional 환경에서 questionary 기반 인터랙티브 CLI를 정상적으로 실행하기 위한 설정 방법을 설명합니다.

PyCharm의 기본 Run/Debug 콘솔은 완전한 TTY 환경을 제공하지 않기 때문에, 다음 오류가 발생할 수 있습니다.

```lua
prompt_toolkit.output.win32.NoConsoleScreenBufferError:
No Windows console found. Are you running cmd.exe?
```

## 1. Run Configuration 열기
PyCharm 상단 메뉴 -> Run → Edit Configurations…

## 2. 인터랙티브 실행 구성 선택
- main_interactive 
- main 
- 기타 Python Script 실행 구성

## 3. 터미널 에뮬레이션 옵션 활성화 (필수)
PyCharm Professional의 Run Configuration에서 Modify options 메뉴를 열고 아래 설정을 체크해야 합니다.

### 출력 콘솔에서 터미널을 에뮬레이션 처리
영문: Emulate terminal in output console

이 옵션을 켜야 PyCharm 콘솔이 TTY처럼 동작하여 questionary UI가 정상적으로 표시됩니다.

## 참고
이 설정은 PyCharm Professional에서만 제공됩니다. (Community Edition은 이 옵션이 기본적으로 없습니다.)

VSCode, Windows CMD, PowerShell 등에서는 기본 TTY 환경이므로 추가 설정이 필요 없습니다.
```bash
python app/main_interactive.py --interactive
```