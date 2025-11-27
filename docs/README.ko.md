# 데이터 분석 프로젝트
Python으로 CSV 데이터를 분석하고, Next.js(React)로 분석 결과를 대시보드 형태로 시각화하는 프로젝트입니다.

백엔드는 CSV 데이터를 로딩한 뒤 전처리 및 통계 지표 분석을 수행하고,
프론트엔드에서 바로 활용할 수 있도록 구조화된 JSON 아티팩트를 생성하여
`artifacts/` 디렉토리에 저장합니다.

프론트엔드는 이 JSON 데이터를 불러와 차트·테이블 형태로 시각화된 대시보드를 제공합니다.

## 리포지토리 바로가기
[front](/front) | [backend](/back)

## 폴더 구조
```text
final-project-data-analysis/
│
├─ backend/              # Python 데이터 분석 파이프라인
│   ├─ README.md         # 백엔드(분석 파이프라인) 전용 설명서
│   ├─ requirements.txt  # Python 의존성 목록
│   ├─ data/             # 입력 데이터(CSV 등)
│   ├─ artifacts/        # 분석 결과물(JSON, 차트, 요약 파일 등)
│   └─ src/              # 분석 코드 (app/domain/infrastructure/presentation)
│
├─ frontend/             # Next.js 기반 웹 대시보드
│   ├─ README.md         # 프론트엔드 전용 설명서
│   ├─ package.json
│   ├─ public/           # 정적 파일 (예: summary.json)
│   └─ src/              # React/Next.js 코드
│
├─ docs/                 # 문서 모음
│   ├─ README.ko.md              # 전체 한국어 문서 버전
│   ├─ requirements-analysis.md  # 요구사항 분석
│   ├─ io-design.md              # 입출력/화면 설계
│   └─ system-architecture.md    # 시스템/레이어 구조 설명
│
└─ video/                # 시연 영상
    └─ demo.mp4
```

## 라이선스 (KO)

이 프로젝트는 **MIT 라이선스**로 배포됩니다.

다음과 같은 행위가 허용됩니다.
- 소프트웨어의 사용, 복사, 수정, 병합
- 배포, 재배포
- 상업적 이용

단, 원저작자 표기(저작권 표시)는 필수입니다.  
출처를 밝히지 않은 무단 사용, 특히 학술적 사용 
(이 프로젝트 내용을 논문/과제/발표에 무단 포함 등)은  
명백한 저작권 침해이며 법적 책임이 발생할 수 있습니다.

자세한 내용은 `LICENSE` 파일을 참고하십시오.