[EN](../README.md) | [KO](README.ko.md)

# 백엔드 - Python 데이터 분석 파이프라인
이 백엔드 모듈은 CSV 데이터를 로딩하고 전처리한 뒤, 
통계 지표를 계산하여 구조화된 JSON 아티팩트로 생성하는 역할을 수행합니다.  

생성된 JSON 파일은 프론트엔드(Next.js)에서 대시보드를 렌더링하는 데 사용됩니다.

전체 코드는 계층형 아키텍처(app → domain → infrastructure → presentation)를 기반으로 작성되어 유지보수성과 확장성을 고려했습니다.

## 백엔드 구조 요약
```text
backend/
├─ data/                 # 입력 CSV 파일
├─ artifacts/            # 생성된 JSON/차트 등 결과물
│   └─ summaries/
│       └─ summary.json
└─ src/
    ├─ app/              # 실행 엔트리포인트
    ├─ domain/           # 분석 로직
    ├─ infrastructure/   # 파일 입출력
    └─ presentation/     # (선택적) 출력/시각화
```

## 종속성 (Dependencies)
| 패키지            | 버전     | 용도                      |
| -------------- | ------ | ----------------------- |
| **pandas**     | latest | 데이터 로드/정제/변환/분석         |
| **openpyxl**   | latest | Excel(.xlsx) 파일 읽기·쓰기   |
| **matplotlib** | latest | 차트 생성 및 시각화             |
| **seaborn**    | latest | 고급 통계 시각화               |
| **jupyter**    | latest | Notebook 기반 인터랙티브 분석 환경 |

## 설치 방법 (Installation)
### backend 디렉토리로 이동
```bash
cd back
```

### 가상 환경 생성 (Virtual Environment)
```bash
py -3 -m venv .venv
```

### 가상 환경 활성화 (Windows PowerShell)
```bash
.\.venv\Scripts\activate
```

## 의존성 설치 (Install Dependencies)
가상 환경이 활성화된 상태에서 다음 명령 중 하나를 실행합니다.

```bash
pip install -r requirements.txt
```

OR

```bash
python -m pip install -r requirements.txt
```

### Python 명령어가 인식되지 않는 경우
전체 경로를 사용하세요.
```bash
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

## 실행 방법 (How to Run)
```bash
python src/app/main.py
```

## 출력 (Artifacts)
분석 결과는 아래 디렉토리에 저장됩니다.
```text
artifacts/
  ├─ charts/      # 시각화 이미지
  └─ summaries/   # 통계 요약, 엑셀 파일 등
```