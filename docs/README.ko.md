[KO](README.ko.md) | [EN](../README.md)

# 데이터 분석 프로젝트
Python으로 Kaggle **Coding Questions Dataset**을 분석하고, Next.js(React) 대시보드에서 시각화하는 프로젝트입니다.

백엔드는 CSV를 로딩·정제한 뒤 난이도 분포, 태그/카테고리 상위값, 문제 구조 버킷, 타임라인, 교차 매트릭스 등 통계 지표를 계산합니다. JSON/Excel/차트 아티팩트를 생성하고, 프론트엔드가 읽을 수 있도록 `front/src/shared/data`에도 동기화합니다.

프론트엔드는 생성된 JSON을 탭 기반 대시보드(Overview, Difficulty, Tags, Structure, Raw)로 렌더링합니다.

## 데이터셋 출처
이 프로젝트에서 사용하는 데이터셋은 Kaggle 자료를 기반으로 합니다.
총 600개 이상의 프로그래밍 문제가 포함되어 있으며 제목, 설명, 난이도, 예제, 제약 조건, 테스트 케이스 등으로 구성된 구조화된 데이터셋입니다.

[**Coding Questions Dataset**](https://www.kaggle.com/datasets/guitaristboy/coding-questions-dataset)

라이선스: MIT License  
원저작자: Kartikeya Pandey
> 이 저장소에는 원본 CSV 데이터셋이 포함되어 있으며,  
> MIT 라이선스 조건에 따라 재배포 및 가공이 허용됩니다.  
> 해당 데이터셋은 Python 분석 파이프라인의 입력 데이터로 사용됩니다.


## 리포지토리
[front](/front) | [backend](/back)

## 폴더 구조
```text
final-project-data-analysis/
│
├─ back/                  # Python 데이터 분석 파이프라인
│   ├─ README.md          # 백엔드 전용 문서
│   ├─ requirements.txt   # Python 의존성
│   ├─ data/              # 입력 CSV
│   ├─ artifacts/         # 결과물(JSON/차트/엑셀)
│   └─ src/               # app/domain/infrastructure/presentation 계층 코드
│
├─ front/                 # Next.js 기반 대시보드
│   ├─ README.md          # 프론트엔드 전용 문서
│   ├─ package.json
│   ├─ public/            # 정적 파일
│   └─ src/               # Feature-sliced React 코드 + 공유 데이터
│
├─ docs/                  # 문서 모음(KO/EN)
│   ├─ README.ko.md              # 한국어 개요
│   ├─ requirements-analysis/    # 요구사항 및 목표 분석
│   ├─ io-design/                # 입출력/데이터 계약 정리
│   └─ system-architecture/      # 시스템·레이어 구조 설명
│
└─ video/                # 시연 영상
    └─ demo.mp4
```

## 백엔드 요약 (back/)
- 엔트리: `back/src/app/main.py`
- 기본 데이터셋: `back/data/coding-questions-dataset/questions_dataset.csv`
- 산출물: `back/artifacts/json`(프론트용 JSON), `back/artifacts/charts`, `back/artifacts/xlsx`(엑셀 분할), `front/src/shared/data`(UI 동기화 JSON)
- 실행 예시 (`back` 폴더 기준):
  ```bash
  export PYTHONPATH="$(pwd)/src"
  python -m backend.app.main --data-file data/coding-questions-dataset/questions_dataset.csv
  ```

## 프론트엔드 요약 (front/)
- Next.js(App Router) 대시보드: Overview/Difficulty/Tags/Structure/Raw 탭 제공
- 사용 데이터: `front/src/shared/data`의 `overview.json`, `difficulty.json`, `summary-full.json` 등
- 개발 서버 실행 (`front` 폴더 기준):
  ```bash
  npm install
  npm run dev
  ```

## 라이선스
이 프로젝트는 **MIT License**로 배포됩니다. 자세한 내용은 `LICENSE` 파일을 참고하세요.