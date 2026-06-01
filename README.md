# 🪪 기후 주민등록증

> 생년월일을 입력하면, **서울이 기억하는 당신의 탄생 기록**을 발급해드립니다.

기상청 서울관측소 119년(1907~2026) 기상 데이터와 행정안전부 2026년 4월 연령별 인구 통계를 결합한 인터랙티브 웹앱입니다.

---

## 📋 발급 내용

| 항목 | 내용 |
|------|------|
| 탄생일 기온 | 평균 / 최저 / 최고 기온, 날씨 유형 |
| 탄생 연도 기온 특성 | 연평균 기온, 역대 더운 해 순위 |
| 전국 동갑 현황 | 같은 나이 인구수 (남/여 포함) |

## 📈 차트 3종

1. **서울 119년 연평균 기온** — 탄생 연도 하이라이트 + 기온 추세선
2. **탄생 연도의 월별 기온** — 태어난 해의 사계절, 탄생월 강조
3. **매년 내 생일날의 서울 기온** — "내 생일, 점점 더워지고 있을까?" (가장 독특한 차트!)

---

## 🚀 실행 방법

### 1. 저장소 클론 & 데이터 준비

```bash
git clone https://github.com/<your-username>/<repo-name>.git
cd <repo-name>
```

`data/` 폴더를 만들고 CSV 파일 두 개를 넣어주세요:

```
project/
├── app.py
├── requirements.txt
├── README.md
└── data/
    ├── ta_20260601093156.csv               ← 서울 기상 데이터 (기상청)
    └── 202604_202604_연령별인구현황_월간.csv  ← 인구 데이터 (행정안전부)
```

### 2. 패키지 설치 & 실행

```bash
pip install -r requirements.txt
streamlit run app.py
```

브라우저에서 `http://localhost:8501` 접속!

---

## ☁️ Streamlit Cloud 배포

1. GitHub에 레포 업로드 (data/ 폴더 포함)
2. [share.streamlit.io](https://share.streamlit.io) 접속 후 GitHub 연결
3. `app.py` 선택 → Deploy!

---

## 📊 데이터 출처

- **기상 데이터**: 기상청 기후데이터센터, 서울 기상관측소 (지점 108), 1907~2026
- **인구 데이터**: 행정안전부 주민등록 인구통계, 2026년 4월

---

## 🛠 기술 스택

- **Frontend**: [Streamlit](https://streamlit.io)
- **시각화**: [Plotly](https://plotly.com/python/)
- **데이터 처리**: Pandas, NumPy
- **폰트**: DM Serif Display, IBM Plex Mono (Google Fonts)
