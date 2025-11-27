# Project Name?
주제 고민중

## Language
[EN](../README.md) | [KO](README.ko.md)

---

## 프로젝트 개요 (Project Overview)
이 프로젝트는 Python 기반 데이터 분석을 수행하기 위한 구조화된 분석 시스템입니다. CSV 또는 Excel 데이터를 불러오고, 필요에 따라 전처리/분석/시각화를 수행하며 최종 결과물(차트, 통계 요약 등)을 artifacts 디렉토리에 저장합니다.

## 프로젝트 구조 (Project Structure)
```text
final-project-data-analysis/
│
├─ README.md                        # 메인 영어 문서
├─ requirements.txt                 # Python 종속성 목록
├─ .gitignore
│
├─ data/                            # 입력 데이터 (CSV, Excel 등)
│   └─ ...logs.csv
│
├─ artifacts/                       # 생성된 분석 산출물 (차트, summary 등)
│   ├─ charts/
│   └─ summaries/
│
├─ docs/                            # 프로젝트 문서 (한국어 포함)
│   ├─ README.ko.md                 # 한국어 README
│   ├─ requirements-analysis.md     # 요구사항 분석 문서
│   ├─ io-design.md                 # 입출력(화면) 설계
│   └─ system-architecture.md       # 계층 구조 및 시스템 설계
│
├─ video/                           # 시연 영상
│   └─ demo.mp4
│
└─ src/                             # 소스 코드 (계층 기반 구조)
    ├─ app/                         # 애플리케이션 계층 (엔트리 포인트, 파이프라인)
    │   ├─ main.py
    │   └─ config.py
    │
    ├─ domain/                      # 도메인 계층 (엔티티, 비즈니스 로직)
    │   ├─ entities/
    │   │   └─ ...log.py
    │   └─ services/
    │       └─ metrics.py
    │
    ├─ infrastructure/              # 인프라 계층 (I/O, 저장, 로깅 등)
    │   ├─ io/
    │   │   ├─ csv_loader.py
    │   │   └─ artifact_writer.py
    │   └─ logging/
    │       └─ logger.py
    │
    └─ presentation/                # 프레젠테이션 계층 (시각화, 보고서 생성)
        ├─ charts/
        │   ├─ stage_chart.py
        │   └─ daily_chart.py
        └─ reports/
            └─ console_report.py
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
```bash
pip install -r requirements.txt
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

## 라이선스 (KO)

이 프로젝트는 **MIT 라이선스**로 배포됩니다.

다음과 같은 행위가 허용됩니다.
- 소프트웨어의 사용, 복사, 수정, 병합
- 배포, 재배포
- 상업적 이용

단, **원저작자 표기(저작권 표시)**는 필수입니다.  
출처를 밝히지 않은 무단 사용, 특히 학술적 사용 
(이 프로젝트 내용을 논문/과제/발표에 무단 포함 등)은  
명백한 저작권 침해이며 법적 책임이 발생할 수 있습니다.

자세한 내용은 `LICENSE` 파일을 참고하십시오.
