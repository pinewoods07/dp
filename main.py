import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import numpy as np
from datetime import date
from pathlib import Path

# ─────────────────────────────────────────────
# Page config
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="기후 주민등록증",
    page_icon="🪪",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# 파일 경로 (main.py 기준)
BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"

# ─────────────────────────────────────────────
# Global CSS
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display:ital@0;1&family=IBM+Plex+Mono:wght@300;400;600&family=Noto+Sans+KR:wght@300;400;500;700;900&display=swap');

html, body, .stApp, [class*="st-"] {
    font-family: 'Noto Sans KR', sans-serif;
}
.stApp { background: #f0ece3; }
#MainMenu, footer, header { visibility: hidden; }

.hero { text-align: center; padding: 44px 24px 16px; }
.hero h1 {
    font-family: 'DM Serif Display', serif;
    font-size: 40px; letter-spacing: -1px; color: #0d1b2a; margin-bottom: 10px;
}
.hero p { color: #888; font-size: 14px; line-height: 1.8; margin: 0; }

.id-card {
    font-family: 'IBM Plex Mono', monospace;
    background: linear-gradient(160deg, #0d1b2a 0%, #152535 50%, #0a2d4a 100%);
    border-radius: 22px; padding: 36px 40px; color: white; margin: 24px 0 32px;
    position: relative; overflow: hidden;
    box-shadow: 0 30px 80px rgba(0,0,0,0.38), 0 0 0 1px rgba(212,175,55,0.22),
        inset 0 1px 0 rgba(255,255,255,0.09);
}
.id-card::before {
    content: 'CLIMATE ID'; position: absolute; top: 48%; left: 50%;
    transform: translate(-50%, -50%) rotate(-28deg); font-size: 90px; font-weight: 900;
    color: rgba(212,175,55,0.025); white-space: nowrap; pointer-events: none; letter-spacing: 12px;
}
.id-card::after {
    content: ''; position: absolute; top: 0; left: 0; right: 0; height: 4px;
    background: linear-gradient(90deg, #b8952a, #f5e07a, #d4af37, #f5e07a, #b8952a);
}
.card-header {
    display: flex; justify-content: space-between; align-items: flex-start;
    padding-bottom: 22px; margin-bottom: 24px; border-bottom: 1px solid rgba(212,175,55,0.2);
}
.card-title-text {
    font-size: 10px; letter-spacing: 4px; color: #d4af37;
    text-transform: uppercase; margin-bottom: 8px;
}
.card-name { font-size: 22px; font-weight: 600; color: #f5f0e8; letter-spacing: 2px; }
.card-meta { text-align: right; font-size: 10px; color: rgba(255,255,255,0.3); line-height: 2; letter-spacing: 0.5px; }
.grid-2 { display: grid; grid-template-columns: 1fr 1fr; gap: 12px; margin-bottom: 12px; }
.mblock {
    background: rgba(255,255,255,0.055); border: 1px solid rgba(212,175,55,0.14);
    border-radius: 14px; padding: 20px 22px;
}
.mlabel {
    font-size: 9px; letter-spacing: 3px; color: rgba(212,175,55,0.65);
    text-transform: uppercase; margin-bottom: 12px;
}
.temp-big { font-size: 62px; font-weight: 300; line-height: 1; color: #f5f0e8; letter-spacing: -3px; }
.temp-unit { font-size: 24px; color: rgba(255,255,255,0.45); }
.day-label { margin-top: 9px; font-size: 12px; color: rgba(255,255,255,0.58); font-family: 'Noto Sans KR', sans-serif; }
.year-num { font-size: 34px; font-weight: 300; color: #f5f0e8; margin: 6px 0 12px; letter-spacing: -1px; }
.gold-pill {
    display: inline-block; padding: 5px 15px; background: rgba(212,175,55,0.13);
    border: 1px solid rgba(212,175,55,0.32); border-radius: 20px; font-size: 11px;
    color: #d4af37; font-family: 'Noto Sans KR', sans-serif; font-weight: 500;
}
.year-rank { margin-top: 10px; font-size: 10px; color: rgba(255,255,255,0.3); letter-spacing: 1px; }
.range-row { display: flex; gap: 28px; margin-top: 14px; }
.ri-label { font-size: 9px; letter-spacing: 2px; color: rgba(255,255,255,0.38); text-transform: uppercase; margin-bottom: 5px; }
.ri-val { font-size: 28px; font-weight: 300; letter-spacing: -1px; }
.pop-num { font-size: 40px; font-weight: 300; color: #f5f0e8; letter-spacing: -1px; margin: 10px 0; }
.gender-row { display: flex; gap: 10px; flex-wrap: wrap; margin-top: 12px; }
.gpill {
    background: rgba(255,255,255,0.07); border: 1px solid rgba(255,255,255,0.14);
    border-radius: 20px; padding: 5px 15px; font-size: 11px;
    color: rgba(255,255,255,0.72); font-family: 'Noto Sans KR', sans-serif;
}
.card-footer {
    display: flex; justify-content: space-between; align-items: flex-end;
    margin-top: 26px; padding-top: 18px; border-top: 1px solid rgba(212,175,55,0.14);
}
.serial { font-size: 10px; letter-spacing: 2px; color: rgba(255,255,255,0.18); }
.issuer { text-align: right; font-size: 9px; color: rgba(212,175,55,0.28); letter-spacing: 1px; line-height: 1.9; }
.section-title {
    font-size: 13px; font-weight: 700; color: #0d1b2a; margin: 28px 0 6px;
    letter-spacing: 0.3px; font-family: 'Noto Sans KR', sans-serif;
}
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# 인코딩을 자동으로 찾아서 CSV 읽기
# ─────────────────────────────────────────────
def read_csv_auto(path, **kwargs):
    """여러 인코딩을 차례로 시도해서 성공하는 것으로 읽는다."""
    encodings = ["utf-8-sig", "cp949", "euc-kr", "utf-8", "latin1"]
    last_err = None
    for enc in encodings:
        try:
            return pd.read_csv(path, encoding=enc, **kwargs), enc
        except Exception as e:
            last_err = e
            continue
    raise RuntimeError(f"어떤 인코딩으로도 읽지 못했습니다: {last_err}")


# ─────────────────────────────────────────────
# Data loading (cached)
# ─────────────────────────────────────────────
@st.cache_data
def load_weather() -> pd.DataFrame:
    df, _ = read_csv_auto(DATA_DIR / "ta_20260601093156.csv")
    df.columns = [c.strip() for c in df.columns]
    # 날짜 앞의 탭/따옴표/공백 정리
    df["날짜"] = df["날짜"].astype(str).str.replace('"', "").str.strip()
    df["날짜"] = pd.to_datetime(df["날짜"], errors="coerce")
    # 기온 컬럼 숫자형 변환
    for col in ["평균기온(℃)", "최저기온(℃)", "최고기온(℃)"]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")
    df = df.dropna(subset=["날짜"])
    return df


@st.cache_data
def load_population():
    df, used_enc = read_csv_auto(DATA_DIR / "202604_202604_연령별인구현황_월간.csv")
    df.columns = [str(c).strip() for c in df.columns]
    # 첫 컬럼(행정구역)을 제외한 나머지를 숫자로 변환
    for col in df.columns[1:]:
        df[col] = df[col].astype(str).str.replace(",", "").str.strip()
        df[col] = pd.to_numeric(df[col], errors="coerce")
    return df, used_enc


# ── 데이터 불러오기 ──
weather_df = load_weather()
pop_df, pop_enc = load_population()

# 첫 컬럼 이름 (행정구역)
region_col = pop_df.columns[0]
# '전국'이 들어간 행 찾기
nation_mask = pop_df[region_col].astype(str).str.contains("전국")
if nation_mask.any():
    national = pop_df[nation_mask].iloc[0]
else:
    national = pop_df.iloc[0]   # 못 찾으면 첫 행 사용


# ─────────────────────────────────────────────
# 디버그용 사이드바 (문제 생기면 여기서 컬럼명 확인)
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("### 🛠 디버그 정보")
    st.write("인구 파일 인코딩:", pop_enc)
    st.write("행정구역 컬럼:", region_col)
    if st.checkbox("인구 데이터 컬럼명 전체 보기"):
        st.write(pop_df.columns.tolist())


# ─────────────────────────────────────────────
# 나이별 인구 컬럼을 유연하게 찾는 함수
# ─────────────────────────────────────────────
def find_pop(gender_keyword: str, age: int):
    """
    성별 키워드('계','남','여')와 나이를 받아
    해당하는 인구 컬럼 값을 찾아 반환. 못 찾으면 0.
    컬럼명이 '2026년04월_계_30세' 형태든 조금 다르든 유연하게 매칭.
    """
    if age >= 100:
        age_patterns = ["100세 이상", "100세이상", "100세"]
    else:
        age_patterns = [f"{age}세"]

    for col in national.index:
        col_str = str(col)
        # 성별 키워드가 포함되고
        if gender_keyword not in col_str:
            continue
        # 나이 패턴이 정확히 끝부분에 맞는지 확인
        for ap in age_patterns:
            # '_30세'처럼 구분자 뒤에 오는 경우를 우선 매칭
            if col_str.endswith(ap):
                val = national[col]
                if pd.notna(val):
                    return int(val)
    return 0


# ─────────────────────────────────────────────
# Hero & input
# ─────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <h1>🪪 기후 주민등록증</h1>
    <p>생년월일을 입력하면, 서울이 기억하는 당신의 탄생 기록을 발급해드립니다<br>
       기상청 서울관측소 119년 데이터 × 전국 연령별 인구 통계</p>
</div>
""", unsafe_allow_html=True)

c1, c2 = st.columns([4, 1])
with c1:
    birth_date = st.date_input(
        "생년월일",
        value=date(1995, 6, 15),
        min_value=date(1907, 10, 1),
        max_value=date(2026, 5, 31),
        label_visibility="collapsed",
        format="YYYY.MM.DD",
    )
with c2:
    issued = st.button("발급하기", use_container_width=True, type="primary")

if not issued:
    st.markdown(
        "<p style='text-align:center;color:#bbb;font-size:13px;margin-top:14px'>"
        "1907.10.01 ~ 2026.05.31 범위의 날짜를 선택해주세요</p>",
        unsafe_allow_html=True,
    )
    st.stop()


# ─────────────────────────────────────────────
# Data processing
# ─────────────────────────────────────────────
birth_dt    = pd.Timestamp(birth_date)
birth_year  = birth_date.year
birth_month = birth_date.month
birth_day   = birth_date.day

row = weather_df[weather_df["날짜"] == birth_dt]
if row.empty:
    st.error("해당 날짜의 기상 데이터를 찾을 수 없습니다. 날짜를 다시 확인해주세요.")
    st.stop()

avg_temp = row["평균기온(℃)"].values[0]
min_temp = row["최저기온(℃)"].values[0]
max_temp = row["최고기온(℃)"].values[0]
has_temp = not pd.isna(avg_temp)

yearly_avg = (
    weather_df.groupby(weather_df["날짜"].dt.year)["평균기온(℃)"].mean().dropna()
)
total_yrs = len(yearly_avg)
year_val  = yearly_avg.get(birth_year)

if year_val is not None and not pd.isna(year_val):
    hot_rank = int((yearly_avg > year_val).sum()) + 1
    pct      = float((yearly_avg <= year_val).sum()) / total_yrs * 100
    if pct >= 80:   year_label = "🔥 역대 더운 해"
    elif pct >= 60: year_label = "☀️ 평년보다 더운 해"
    elif pct >= 40: year_label = "🌤️ 평년 수준"
    elif pct >= 20: year_label = "🌬️ 평년보다 서늘한 해"
    else:           year_label = "❄️ 역대 추운 해"
    year_val_str  = f"{year_val:.2f}℃"
    hot_rank_str  = f"더운 해 순위 : 역대 {hot_rank}위 / 전체 {total_yrs}년"
else:
    year_val      = float("nan")
    hot_rank      = 0
    year_label    = "—"
    year_val_str  = "—"
    hot_rank_str  = ""

if has_temp:
    if avg_temp >= 28:   day_emoji, day_lbl = "☀️", "무더운 날"
    elif avg_temp >= 20: day_emoji, day_lbl = "🌤️", "따뜻한 날"
    elif avg_temp >= 10: day_emoji, day_lbl = "🍂", "선선한 날"
    elif avg_temp >= 0:  day_emoji, day_lbl = "🌨️", "쌀쌀한 날"
    else:                day_emoji, day_lbl = "❄️", "추운 날"
    avg_str = f"{avg_temp:.1f}"
    min_str = f"{min_temp:.1f}" if not pd.isna(min_temp) else "—"
    max_str = f"{max_temp:.1f}" if not pd.isna(max_temp) else "—"
    min_col = "#5b86e5"
    max_col = "#ff6b35"
else:
    day_emoji, day_lbl = "❓", "기록 없음"
    avg_str = min_str = max_str = "—"
    min_col = max_col = "rgba(255,255,255,0.45)"

# 나이 계산 (2026년 기준 단순 나이)
age = 2026 - birth_year
if age < 0:
    age = 0
age_key = "100세 이상" if age >= 100 else f"{age}세"

total_pop  = find_pop("계", age)
male_pop   = find_pop("남", age)
female_pop = find_pop("여", age)


# ─────────────────────────────────────────────
# ID Card HTML
# ─────────────────────────────────────────────
st.markdown(f"""
<div class="id-card">
  <div class="card-header">
    <div>
      <div class="card-title-text">Korea Climate ID Card · 기후 주민등록증</div>
      <div class="card-name">{birth_date.strftime('%Y . %m . %d')} &nbsp;생</div>
    </div>
    <div class="card-meta">
      발급일 : 2026 . 06 . 01<br>
      발급기관 : 기상청 기후데이터센터<br>
      관측소 : 서울특별시 (지점 108)
    </div>
  </div>
  <div class="grid-2">
    <div class="mblock">
      <div class="mlabel">Birth Day Temp · 탄생일 평균기온</div>
      <div class="temp-big">{avg_str}<span class="temp-unit">℃</span></div>
      <div class="day-label">{day_emoji}&nbsp; {day_lbl}</div>
    </div>
    <div class="mblock">
      <div class="mlabel">Birth Year · {birth_year}년 연평균 기온</div>
      <div class="year-num">{year_val_str}</div>
      <div class="gold-pill">{year_label}</div>
      <div class="year-rank">{hot_rank_str}</div>
    </div>
  </div>
  <div class="mblock" style="margin-bottom:12px">
    <div class="mlabel">Temperature Range · 탄생일 기온 범위</div>
    <div class="range-row">
      <div><div class="ri-label">최저 Low</div><div class="ri-val" style="color:{min_col}">{min_str}℃</div></div>
      <div><div class="ri-label">평균 Avg</div><div class="ri-val">{avg_str}℃</div></div>
      <div><div class="ri-label">최고 High</div><div class="ri-val" style="color:{max_col}">{max_str}℃</div></div>
    </div>
  </div>
  <div class="mblock">
    <div class="mlabel">Population · 전국 동갑 현황 (2026. 04 기준 · {age_key})</div>
    <div class="pop-num">{total_pop:,}<span style="font-size:16px;color:rgba(255,255,255,0.38);font-weight:300"> 명</span></div>
    <div class="gender-row">
      <span class="gpill">👨 남성 {male_pop:,}명</span>
      <span class="gpill">👩 여성 {female_pop:,}명</span>
      <span class="gpill">🇰🇷 전국 기준</span>
    </div>
  </div>
  <div class="card-footer">
    <div class="serial">ID · {birth_date.strftime('%Y%m%d')} · KR · STA-108 · 2026</div>
    <div class="issuer">
      KOREA METEOROLOGICAL ADMINISTRATION<br>
      MINISTRY OF THE INTERIOR AND SAFETY
    </div>
  </div>
</div>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# Shared plot style
# ─────────────────────────────────────────────
NAVY  = "#0d1b2a"
GOLD  = "#d4af37"
BLUE  = "rgba(80,130,210,0.7)"
RED_D = "rgba(200,70,70,0.6)"
PGRID = "rgba(180,168,150,0.28)"
BASE  = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(240,236,228,0.55)",
    font=dict(family="IBM Plex Mono, monospace", color=NAVY, size=11),
    margin=dict(l=8, r=8, t=20, b=8),
    xaxis=dict(showgrid=True, gridcolor=PGRID, zeroline=False),
    yaxis=dict(showgrid=True, gridcolor=PGRID, zeroline=False, title="℃"),
    hovermode="x unified",
)


# ── Chart 1 ──
st.markdown(
    "<div class='section-title'>📈 서울 119년 연평균 기온 — 당신의 탄생 연도는 어디?</div>",
    unsafe_allow_html=True,
)
z1   = np.polyfit(yearly_avg.index.astype(int), yearly_avg.values, 1)
trd1 = np.poly1d(z1)(yearly_avg.index.astype(int))

f1 = go.Figure()
f1.add_trace(go.Scatter(
    x=yearly_avg.index, y=yearly_avg.values, mode="lines", name="연평균 기온",
    line=dict(color=BLUE, width=1.5), fill="tozeroy", fillcolor="rgba(80,130,210,0.06)",
    hovertemplate="%{x}년 : %{y:.2f}℃<extra></extra>",
))
f1.add_trace(go.Scatter(
    x=yearly_avg.index, y=trd1, mode="lines", name="기온 추세선",
    line=dict(color=RED_D, width=2, dash="dash"), hoverinfo="skip",
))
if not pd.isna(year_val):
    f1.add_trace(go.Scatter(
        x=[birth_year], y=[year_val], mode="markers+text",
        marker=dict(color=GOLD, size=15, symbol="star", line=dict(color="white", width=1.5)),
        text=[f"  {birth_year}년"], textposition="top right",
        textfont=dict(color=GOLD, size=12, family="IBM Plex Mono"),
        name="나의 탄생 연도",
        hovertemplate=f"{birth_year}년 : {year_val:.2f}℃<extra></extra>",
    ))
f1.update_layout(
    **BASE, height=320,
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1,
                bgcolor="rgba(0,0,0,0)", font=dict(size=10)),
)
st.plotly_chart(f1, use_container_width=True)


# ── Chart 2 ──
st.markdown(
    f"<div class='section-title'>🗓️ {birth_year}년 서울의 월별 기온 — 태어난 해의 사계절</div>",
    unsafe_allow_html=True,
)
yr_data = weather_df[weather_df["날짜"].dt.year == birth_year]
monthly = yr_data.groupby(yr_data["날짜"].dt.month)["평균기온(℃)"].mean().dropna()
months_kr = ["1월","2월","3월","4월","5월","6월","7월","8월","9월","10월","11월","12월"]

def month_color(t):
    if t < 0:  return "#5b86e5"
    if t < 10: return "#84aad6"
    if t < 20: return "#4ecdc4"
    return "#ff6b35"

if len(monthly) > 0:
    bar_colors = [month_color(t) for t in monthly.values]
    f2 = go.Figure()
    f2.add_trace(go.Bar(
        x=[months_kr[m - 1] for m in monthly.index], y=monthly.values,
        marker_color=bar_colors, name="월평균 기온",
        hovertemplate="%{x} 평균 : %{y:.1f}℃<extra></extra>",
    ))
    if birth_month in monthly.index:
        f2.add_vline(
            x=months_kr[birth_month - 1], line_dash="dot", line_color=GOLD, line_width=2.5,
            annotation_text=f"탄생월 ({avg_str}℃)",
            annotation_font=dict(color=GOLD, size=11, family="IBM Plex Mono"),
            annotation_position="top",
        )
    f2.update_layout(**BASE, height=290, xaxis=dict(showgrid=False), showlegend=False, hovermode="x")
    st.plotly_chart(f2, use_container_width=True)
else:
    st.info("해당 연도의 월별 데이터가 충분하지 않습니다.")


# ── Chart 3 ──
st.markdown(
    f"<div class='section-title'>🎂 매년 {birth_month}월 {birth_day}일의 서울 기온 — 내 생일, 점점 더워지고 있을까?</div>",
    unsafe_allow_html=True,
)
bday = (
    weather_df[
        (weather_df["날짜"].dt.month == birth_month) &
        (weather_df["날짜"].dt.day == birth_day)
    ].dropna(subset=["평균기온(℃)"]).copy()
)
bday["year"] = bday["날짜"].dt.year

if len(bday) >= 5:
    bz   = np.polyfit(bday["year"], bday["평균기온(℃)"], 1)
    btrd = np.poly1d(bz)(bday["year"])
    btrd = np.asarray(btrd)
    delta = float(btrd[-1] - btrd[0])
    delta_str   = f"+{delta:.1f}℃" if delta >= 0 else f"{delta:.1f}℃"
    delta_color = "#e05a3a" if delta >= 0 else "#5b86e5"
    birth_bday = bday[bday["year"] == birth_year]

    f3 = go.Figure()
    f3.add_trace(go.Scatter(
        x=bday["year"], y=bday["평균기온(℃)"], mode="markers",
        marker=dict(
            color=bday["평균기온(℃)"],
            colorscale=[[0, "#5b86e5"], [0.45, "#4ecdc4"], [1, "#ff6b35"]],
            size=7, opacity=0.8, line=dict(color="white", width=0.5), showscale=False,
        ),
        name="해당 날 기온",
        hovertemplate=f"{birth_month}월 {birth_day}일 %{{x}}년 : %{{y:.1f}}℃<extra></extra>",
    ))
    f3.add_trace(go.Scatter(
        x=bday["year"], y=btrd, mode="lines", name=f"추세 ({delta_str})",
        line=dict(color=RED_D, width=2, dash="dash"), hoverinfo="skip",
    ))
    if not birth_bday.empty:
        by_t = birth_bday["평균기온(℃)"].values[0]
        f3.add_trace(go.Scatter(
            x=[birth_year], y=[by_t], mode="markers+text",
            marker=dict(color=GOLD, size=17, symbol="star", line=dict(color="white", width=2)),
            text=["  탄생 연도"], textposition="top right",
            textfont=dict(color=GOLD, size=12, family="IBM Plex Mono"),
            name="나의 탄생 연도",
            hovertemplate=f"{birth_year}년 : {by_t:.1f}℃<extra></extra>",
        ))
    f3.update_layout(
        **BASE, height=320,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1,
                    bgcolor="rgba(0,0,0,0)", font=dict(size=10)),
        annotations=[dict(
            x=0.01, y=0.97, xref="paper", yref="paper",
            text=f"과거 → 현재 생일 기온 변화 : <b>{delta_str}</b>",
            showarrow=False, align="left",
            font=dict(size=12, color=delta_color, family="IBM Plex Mono"),
            bgcolor="rgba(240,236,228,0.85)", borderpad=7,
            bordercolor=delta_color, borderwidth=1.2,
        )],
    )
    st.plotly_chart(f3, use_container_width=True)
else:
    st.info("해당 날짜의 연도별 과거 데이터가 충분하지 않습니다.")


# ── Footer ──
st.caption(
    "📊 기상 데이터: 기상청 기후데이터센터, 서울 기상관측소 지점 108 (1907~2026) · "
    "인구 데이터: 행정안전부 주민등록 인구통계 (2026년 4월)"
)
