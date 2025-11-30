[EN](../README.md) | [KO](README.ko.md)

# 백엔드 - Python 데이터 분석 파이프라인
Kaggle Coding Questions 데이터를 로딩/전처리하고 통계 지표를 계산해 JSON·엑셀·차트 아티팩트를 생성합니다. `back/src` 아래 단일 파이썬 패키지(`backend`)로 구성되어 있으며 계층형 아키텍처(app → domain → infrastructure → presentation)를 유지합니다.

## 백엔드 구조 요약
```text
back/
├─ data/                     # 입력 CSV 파일
├─ artifacts/                # 생성된 JSON/차트/엑셀 결과물
│   ├─ charts/
│   ├─ json/
│   ├─ summaries/
│   └─ xlsx/
└─ src/                      # 패키지 루트 (backend)
   ├─ app/                   # 실행 엔트리포인트, 파이프라인 오케스트레이션
   ├─ domain/                # 분석 로직 & 엔티티
   ├─ infrastructure/        # 설정, 로깅, 파일 I/O
   └─ presentation/          # 출력/시각화(Exporter)
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
### back 디렉토리로 이동
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
py -3 -m pip install -r requirements.txt
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
`src` 폴더를 `PYTHONPATH`에 추가한 뒤 `backend` 패키지를 모듈 형태로 실행합니다.

`--data-file` 옵션은 선택 사항이며, 기본값은 `backend.infrastructure.config.DATA_FILE` 상수를 따릅니다.

```bash
# back/ 폴더 안으로 이동 후 실행합니다.
cd back
# Venv 활성화 후 실행
.\.venv\Scripts\activate
python -m src.app.main --data-file data/coding-questions-dataset/questions_dataset.csv
```

## 출력 (Artifacts)
분석 결과는 아래 디렉토리에 저장되며, 탭 전용 JSON은 `front/src/shared/data`에도 동기화되어 Next.js 앱에서 바로 사용됩니다.

```text
artifacts/
  ├─ summaries/   # 통계 요약, 엑셀 파일 등
  ├─ charts/      # 시각화 이미지
  ├─ json/        # 탭별 JSON (overview/difficulty/tags/structure/raw)
  └─ xlsx/        # 탭별 Excel 파일
```