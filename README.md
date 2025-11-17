
# Guro Real Estate Insight Dashboard  
> 서울시 **구로구 부동산 실거래가 빅데이터 분석** / Streamlit 대시보드

---

## Table of Contents
- [1. 프로젝트 개요](#1-프로젝트-개요)  
  - [1-1. 주제](#1-1-주제)  
  - [1-2. 주제 선택 이유](#1-2-주제-선택-이유)  
  - [1-3. 분석 목표 & 핵심 질문](#1-3-분석-목표--핵심-질문)
- [2. 데이터 소개](#2-데이터-소개)  
  - [2-1. 데이터 출처](#2-1-데이터-출처)  
  - [2-2. 주요 컬럼](#2-2-주요-컬럼)  
  - [2-3. 전처리 및 파생 변수](#2-3-전처리-및-파생-변수)
- [3. 기술 스택](#3-기술-스택)
- [4. 프로젝트 구조](#4-프로젝트-구조)  
  - [4-1. 폴더 구조](#4-1-폴더-구조)  
  - [4-2. 주요 파일 설명](#4-2-주요-파일-설명)
- [5. 코드 설명 (Business Logic)](#5-코드-설명-business-logic)  
  - [5-1. 전역 설정 및 공통 필터링 로직](#5-1-전역-설정-및-공통-필터링-로직)  
  - [5-2. 페이지 공통 구조](#5-2-페이지-공통-구조)  
  - [5-3. Home 페이지](#5-3-home-페이지)  
  - [5-4. 연월_추세 페이지](#5-4-연월_추세-페이지)  
  - [5-5. 면적_체감효과 페이지](#5-5-면적_체감효과-페이지)  
  - [5-6. 연식_코호트 페이지](#5-6-연식_코호트-페이지)  
  - [5-7. 반복매매_지수 페이지](#5-7-반복매매-지수-페이지)  
  - [5-8. 가격_분포_수염차트 페이지](#5-8-가격_분포_수염차트-페이지)
- [6. 분석 내용 요약](#6-분석-내용-요약)
- [7. 실행 방법](#7-실행-방법)
- [8. 시연 동영상](#8-시연-동영상)
- [9. 팀원 소개](#9-팀원-소개)
- [10. 외부 URL & 참고 자료](#10-외부-url--참고-자료)

---

## 1. 프로젝트 개요

### 1-1. 주제
**서울시 구로구 부동산 실거래가 데이터를 활용한 시계열·공간·특성별 가격 분석 및 대시보드 구현**

- 서울 열린데이터 광장에서 제공하는 **구로구 실거래가 데이터**를 기반으로,  
  거래 연도·면적·건축 연식·지역(동)·용도에 따른 가격 패턴을 인터랙티브하게 탐색할 수 있는 Streamlit 대시보드입니다.

---

### 1-2. 주제 선택 이유

1. **생활 밀착형 주제**  
   - 부동산 가격은 실제 거주, 투자, 이사 등 대학생에게도 직접적으로 영향을 주는 데이터입니다.
2. **구로구의 특수성**  
   - 구로 디지털단지, 주거지역, 상업·업무시설이 혼재되어 있어  
     **용도별·지역별 가격 차이**를 살펴보기에 적합한 구입니다.
3. **빅데이터·시각화 연습**  
   - 수만 건 이상의 거래 데이터를 **전처리, 집계, 시각화, 대시보드화**까지 경험해 볼 수 있어  
     데이터 분석 프로젝트 포트폴리오로 활용하기에 좋다고 판단했습니다.

---

### 1-3. 분석 목표 & 핵심 질문

**분석 목표**

- 구로구 실거래가 데이터를 바탕으로 **시간, 면적, 연식, 위치**에 따른 가격 구조를 이해하고  
  이를 누구나 쉽게 탐색할 수 있는 **웹 대시보드 형태로 제공**하는 것.

**핵심 질문**

1. **연도·월에 따라 평당 실거래가는 어떻게 변화했는가?**  
2. **주거/상업/업무 등 건물용도에 따라 가격 수준과 변동성이 어떻게 다른가?**  
3. **면적이 커질수록 평당 가격은 떨어지는가(규모의 경제/체감효과)?**  
4. **건축 연식이 다른 코호트(예: 1990년대 vs 2010년대)는 어떤 가격 패턴을 보이는가?**  
5. **같은 동(법정동) 안에서도 가격 분포는 얼마나 넓게 퍼져 있는가?**  
6. **반복 매매(같은 물건의 재거래) 후보를 찾을 수 있는가, 향후 수익률 분석까지 확장 가능한가?**

---

## 2. 데이터 소개

### 2-1. 데이터 출처

- **데이터명**: 서울시 부동산 실거래가 정보 (구로구)  
- **출처**: 서울 열린데이터 광장  
- **파일명(본 프로젝트)**: `서울시_부동산_실거래가_정보_구로구.csv`  

> 실제 프로젝트에서는 학교에서 제공한 CSV를 사용하였으며,  
> 공개 포트폴리오에서는 민감 정보가 포함되지 않도록 주의합니다.

---

### 2-2. 주요 컬럼

프로젝트에서 핵심적으로 사용한 컬럼은 다음과 같습니다. (컬럼명은 CSV 기준)

- **계약일**: 거래 계약일 (예: `20060101`)  
- **법정동명**: 거래가 발생한 법정동명 (예: 구로동, 오류동 등)  
- **건물용도**: 아파트, 다세대, 오피스텔, 상가, 업무시설 등  
- **건물면적(㎡)**: 건물 면적 (제곱미터)  
- **물건금액(만원)**: 거래 금액 (만원 단위)  
- **건축년도**: 건물 준공 연도  

파생 변수로 다음을 추가 계산하였습니다.

- **계약일자**: `datetime` 형태의 계약일  
- **계약연 / 계약월 / 계약일**: 연/월/일 단위로 분해된 날짜 정보  
- **건물면적(평)**: `건물면적(㎡) * 0.3025`  
- **물건금액(원)**: `물건금액(만원) * 10,000`  
- **평단가**: `물건금액(원) / 건물면적(평)`  

---

### 2-3. 전처리 및 파생 변수

```python
df = pd.read_csv(path, encoding="euc-kr", low_memory=False)

df['계약일자'] = pd.to_datetime(df['계약일'], format='%Y%m%d')
df['계약연'] = df['계약일자'].dt.year
df['계약월'] = df['계약일자'].dt.month
df['계약일'] = df['계약일자'].dt.day

df['건물면적(평)'] = df['건물면적(㎡)'] * 0.3025
df['물건금액(원)'] = df['물건금액(만원)'] * 10000
df['평단가'] = df['물건금액(원)'] / df['건물면적(평)']
```

- **날짜 파싱**: `계약일` 정수형을 `datetime`으로 변환한 뒤 연/월/일 컬럼으로 분리  
- **단위 변환**: 실제 생활에서 많이 쓰는 “**평**” 단위를 사용하기 위해 면적 변환  
- **가격 단위 통일**: 만원 → 원 단위로 변환 후 평당 가격 계산  

---

## 3. 기술 스택

- **언어 / 런타임**
  - Python 3.x

- **데이터 처리**
  - `pandas` : 데이터프레임 처리 및 전처리
  - `numpy` : 수치 계산 및 로그 변환

- **시각화**
  - `plotly.express` : 인터랙티브 라인 차트, 산점도, 파이차트, 박스플롯
  - `statsmodels` : Plotly `trendline="ols"` 사용 시 선형 회귀(OLS) 백엔드로 활용

- **웹 대시보드**
  - `streamlit` : 사이드바 필터, 페이지 전환, 레이아웃 구성

---

## 4. 프로젝트 구조

### 4-1. 폴더 구조

```bash
📦guro-real-estate-streamlit
 ┣ 📂data
 ┃ ┗ 서울시_부동산_실거래가_정보_구로구.csv
 ┣ 📂assets
 ┃ ┗ smart_guro.png
 ┣ 📄app.py              # 본 프로젝트의 Streamlit 메인 앱
 ┣ 📄requirements.txt    # (선택) 의존성 패키지 목록
 ┗ 📄README.md
```

> 실제 과제 제출 시에는 최소한 `app.py`, `data/…csv`, `assets/smart_guro.png`, `README.md`만 있어도 동작하며,  
> `requirements.txt`는 배포/재현을 위해 추가하는 것을 권장합니다.

---

### 4-2. 주요 파일 설명

- **`app.py`**
  - Streamlit 기반 **단일 페이지 앱** 파일  
  - 페이지 라우팅, 사이드바 필터, 데이터 로딩, 그래프 그리기를 모두 포함  
- **`data/서울시_부동산_실거래가_정보_구로구.csv`**
  - 분석 대상 원천 데이터(csv)  
- **`assets/smart_guro.png`**
  - 사이드바 상단에 표시되는 대시보드 로고 / 이미지  
- **`requirements.txt` (선택)**
  - `streamlit`, `pandas`, `numpy`, `plotly`, `statsmodels` 등 의존성 명시

---

## 5. 코드 설명 (Business Logic)

### 5-1. 전역 설정 및 공통 필터링 로직

```python
sidebar_image = "./smart_guro.png"
csv_path = "./서울시_부동산_실거래가_정보_구로구.csv"
pages = ["Home", "연/월 추세", "면적 체감효과", "연식 코호트", "반복매매 지수", "가격 분포 (수염차트)"]
```

- **`sidebar_image`**  
  - Streamlit 사이드바 상단에 표시할 이미지 경로
- **`csv_path`**  
  - 분석에 사용할 CSV 파일 경로
- **`pages`**  
  - 화면 상단/사이드바에서 선택할 수 있는 페이지 목록

```python
df = load_data(csv_path)
st.set_page_config(page_title="구로구 부동산 실거래가 분석", layout="wide")
```

- 앱 시작 시 **데이터를 한 번만 로딩**하고, 페이지 레이아웃은 `wide`로 설정

#### 사이드바 필터

```python
st.sidebar.image(sidebar_image, width='stretch')

selected_page = st.sidebar.selectbox("목록", options=pages, index=0)

use_all = sorted(df['건물용도'].dropna().unique().tolist())
selected_uses = st.sidebar.multiselect("건물용도(표준)", options=use_all, default=use_all)

dong_all = sorted(df['법정동명'].dropna().unique().tolist())
selected_dongs = st.sidebar.multiselect("법정동(복수 선택)", options=dong_all, default=[])

ymin, ymax = int(df['계약연'].min()), int(df['계약연'].max())
selected_years = st.sidebar.slider("계약연 범위", ymin, ymax, (ymin, ymax))

area_min, area_max = float(df['건물면적(평)'].min()), float(df['건물면적(평)'].max())
selected_area = st.sidebar.slider("건물면적(평)", area_min, area_max, (area_min, area_max))

price_min, price_max = int(df['물건금액(원)'].min()), int(df['물건금액(원)'].max())
selected_price = st.sidebar.slider("가격(원)", price_min, price_max, (price_min, price_max))
```

- **건물용도 필터**: 아파트/다세대/상가 등 선택  
- **법정동 필터**: 특정 동만 보고 싶을 때 복수 선택  
- **계약연 범위**: 분석할 연도 구간 지정  
- **면적 구간**: 평 단위 면적 범위 설정  
- **가격 구간**: 원 단위 가격 범위 설정  

#### 공통 필터링 DataFrame `q`

```python
q = df[
    (df['건물용도'].isin(selected_uses)) &
    ((df['법정동명'].isin(selected_dongs)) if selected_dongs else True) &
    (df['계약연'] >= selected_years[0]) & (df['계약연'] <= selected_years[1]) &
    (df['건물면적(평)'] >= selected_area[0]) & (df['건물면적(평)'] <= selected_area[1]) &
    (df['물건금액(원)'] >= selected_price[0]) & (df['물건금액(원)'] <= selected_price[1])
].copy()
```

- 모든 페이지는 이 **필터링된 DataFrame `q`** 를 공통으로 사용  
- 필터 조건을 변경하면 **모든 페이지의 분석 결과가 동시에 반영**되도록 설계  

---

### 5-2. 페이지 공통 구조

맨 아래에서 선택한 페이지에 따라 각 함수를 호출합니다.

```python
if selected_page == "Home":
    Home()
if selected_page == "연/월 추세":
    연월_추세()
if selected_page == "면적 체감효과":
    면적_체감효과()
if selected_page == "연식 코호트":
    연식_코호트()
if selected_page == "반복매매 지수":
    반복매매_지수()
if selected_page == "가격 분포 (수염차트)":
    가격_분포_수염차트()
```

---

### 5-3. `Home` 페이지

```python
def Home():
    st.title("구로구 실거래가 분석: 2006 ~ 2025 인사이트")
    st.markdown("### 서울시 구로구 실거래 데이터를 기반으로 한 탐색형 대시보드 <hr>", unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    with c1: st.metric("표본 수", f"{len(q):,}")
    with c2: st.metric("평균 거래 가격(원)", f"{q['물건금액(원)'].mean():,.0f}")
    with c3: st.metric("평단가 평균(원)", f"{q['평단가'].mean():,.0f}")
```

- **전반적인 요약 지표**를 한눈에 보여주는 대시보드 메인 화면
  - 필터링된 데이터 기준 표본 수, 평균 거래액, 평균 평단가

```python
ts = q.groupby(['건물용도', '계약연'])['평단가'].median().reset_index()
fig = px.line(ts, x='계약연', y='평단가', color='건물용도', markers=True)
```

- 연도별 **건물용도에 따른 평단가 중앙값 추세** 시각화

```python
pie = q['건물용도'].value_counts().reset_index()
top = (q.groupby('법정동명')['평단가'].median().sort_values(ascending=False).head(10).reset_index())
top_count = (q['법정동명'].value_counts().head(10).reset_index())
```

- **용도별 거래 비중 파이차트**
- **동별 평단가 Top 10 바 차트**
- **동별 거래량 Top 10 바 차트**

```python
st.subheader("최근 거래 30건")
cols = ['계약일자', '법정동명', '건물용도', '건물면적(평)', '물건금액(원)', '평단가']
st.dataframe(q.sort_values('계약일자', ascending=False)[show_cols].head(30))
```

- 필터 조건에 맞는 **최근 거래 30건**을 테이블로 제공

---

### 5-4. `연월_추세` 페이지

```python
def 연월_추세():
    st.header("연/월별 평당 실거래가 추세")
    mv = st.radio("이동평균", options=[None,'3개월','6개월','12개월'], horizontal=True, index=0)
    show_cnt = st.checkbox("거래건수 보조축 표시", value=False)
```

- 이동평균(3/6/12개월)을 선택하여 **단기 변동성을 완화한 추세**를 확인할 수 있도록 설계
- 거래건수를 보조 그래프로 함께 볼 수 있음

```python
g = q.groupby(['계약월','건물용도']).agg(중앙단가=('평단가','median'), 건수=('평단가','count')).reset_index()
...
fig = px.line(g, x='계약월', y=ycol, color='건물용도', markers=True)
```

- 월 단위, 용도별 평단가 중앙값/거래 건수 집계  
- **Time series 형태의 가격 흐름**을 시각적으로 파악

---

### 5-5. `면적_체감효과` 페이지

```python
def 면적_체감효과():
    st.header("면적의 체감효과(규모의 경제)")
    scale = st.radio("회귀 스케일", options=['선형','로그-로그'], horizontal=True)
    샘플 = st.slider("산점 샘플 수", 1000, 10000, 4000, step=500)
```

- **면적이 커질수록 평당 가격이 어떻게 변하는지**를 보기 위한 페이지
- 회귀 스케일:
  - `선형`: 원래 축 기준 산점도 + OLS 회귀선
  - `로그-로그`: log(면적) vs log(평단가)로, 탄력성(β)을 해석하기 쉬운 형태

```python
qq = q[['건물면적(평)','평단가','건물용도']].dropna().sample(min(샘플, len(q)), random_state=1)
if scale == '로그-로그':
    qq['log_면적'] = np.log(qq['건물면적(평)'])
    qq['log_단가'] = np.log(qq['평단가'])
    fig = px.scatter(qq, x='log_면적', y='log_단가', color='건물용도', trendline='ols', opacity=0.5)
else:
    fig = px.scatter(qq, x='건물면적(평)', y='평단가', color='건물용도', trendline='ols', opacity=0.5)
```

- `trendline='ols'` 옵션을 통해 **statsmodels 기반 선형 회귀선**을 자동으로 그려줌
- 시각적으로 **규모의 경제 / 체감효과 여부**를 확인 가능

---

### 5-6. `연식_코호트` 페이지

```python
def 연식_코호트():
    st.header("연식 코호트 비교")
    단위 = st.radio("코호트 단위", options=['10년','5년'], horizontal=True)
```

- 건축연도를 기준으로 **10년/5년 단위 코호트**를 나누어  
  건물 연식에 따른 가격 패턴을 비교하는 페이지

```python
def cohort_label(y):
    if pd.isna(y): return '미상'
    y = int(y)
    if 단위=='10년':
        s = (y//10)*10; return f'{s}s'
    else:
        s = (y//5)*5; e = s+4; return f'{s}-{e}'
```

- `건축년도` → `코호트` 라벨 변환 함수

```python
qq = q[['건축년도','평단가','계약월']].copy()
qq['코호트'] = qq['건축년도'].apply(cohort_label)
m = qq.groupby(['코호트','계약월'])['평단가'].median().reset_index()
fig = px.line(m, x='계약월', y='평단가', color='코호트')
```

- 코호트별 월 단위 평단가 중앙값 라인 차트  
- **“신축일수록 비싼가?”**, “어느 코호트 구간이 가장 안정적인가?”와 같은 질문 탐색

---

### 5-7. `반복매매_지수` 페이지

```python
def 반복매매_지수():
    st.header("반복매매(Repeat Sales) 후보 & 지수")
    키구성 = st.multiselect("동일물건 판정 키", options=['법정동명','본번','부번','건물명'],
                            default=['법정동명','본번','부번','건물명'])
    최소간격 = st.slider("최소 재거래 간격(개월)", 0, 60, 6)
```

- 동일 물건을 식별하기 위한 **Key 컬럼 조합**을 사용자가 직접 선택
- 이론적으로는 동일 물건의 반복매매를 이용하여 **Repeat Sales Index** (지수)를 만들 수 있는 기반

```python
key = [c for c in 키구성 if c in q.columns]
cand = q.dropna(subset=key+['계약일자','평단가']).copy()
gp = cand.groupby(key)
pairs = gp.filter(lambda d: len(d)>=2).sort_values(key+['계약일자'])
```

- 같은 키 조합으로 **2회 이상 거래된 물건**만 필터링하여 후보 추출  
- 현재 버전에서는 **후보 리스트 및 기본 정보만 표시**하고,  
  실제 지수/수익률 계산 로직은 추후 확장 포인트로 남겨두었습니다.

---

### 5-8. `가격_분포_수염차트` 페이지

```python
def 가격_분포_수염차트():
    st.header("기준별 가격 분포 (Box Plot)")
    ...
    x_axis_option = st.radio("분석 기준 (X축)", options=['법정동명', '건물용도', '계약연'])
    y_axis_option = st.radio("분석 값 (Y축)", options=['평단가', '물건금액(원)', '건물면적(평)'])
```

- X축 기준:
  - **법정동명**: 동별 분포
  - **건물용도**: 용도별 분포
  - **계약연**: 연도별 분포
- Y축 값:
  - 평단가, 전체 금액, 면적 중 선택

```python
fig = px.box(plot_q, x=x_axis_option, y=y_axis_option, color=x_axis_option,
             title=f"{x_axis_option}에 따른 {y_axis_option} 분포")
```

- Box Plot(수염차트)을 통해 **중앙값, 사분위수, 이상치** 등 분포 특성을 직관적으로 파악

---

## 6. 분석 내용 요약

- **시간(연/월) 분석**
  - 특정 시기(예: 저금리/고금리 기간)에 평단가가 어떻게 변화했는지 추세 확인
  - 용도별로 가격 사이클의 **상승·하락 타이밍이 다름**을 확인

- **공간(법정동) 분석**
  - 동별 평단가 Top 10, 거래량 Top 10을 통해  
    **핫스팟 지역**과 **거래가 활발한 지역**을 분리해서 볼 수 있음

- **면적·규모 효과**
  - 면적이 큰 물건일수록 평당 가격이 일관되게 떨어지는지,  
    혹은 일정 면적 구간에서만 체감효과가 나타나는지 시각적으로 확인

- **연식 코호트 효과**
  - 신축 코호트(예: 2010년대 이후) vs 구축 코호트(1990년대 이전) 간 가격대 및 변동성 비교
  - 건축년도 미상(`미상`) 데이터가 어느 정도 비중을 차지하는지도 파악

- **가격 분포**
  - Box Plot을 통해 동/용도/연도별로 **편향된 분포, 긴 꼬리(이상치) 존재 여부** 확인

---

## 7. 실행 방법

### 7-1. 가상환경 생성 (선택)

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

### 7-2. 패키지 설치

```bash
pip install -r requirements.txt
# 또는
pip install streamlit pandas numpy plotly statsmodels
```

### 7-3. Streamlit 앱 실행

```bash
streamlit run app.py
```

- 브라우저가 자동으로 열리지 않을 경우, 콘솔에 표시되는 `Local URL`을 복사하여 접속합니다.
- 예: `http://localhost:8501`

---

## 8. 시연 동영상

- YouTube 시연 영상: **[구로구 실거래가 대시보드 데모](https://youtu.be/your-demo-link)**  

> 실제 제출 시 `your-demo-link` 부분을 팀의 실제 YouTube 링크로 교체해주세요.

---

## 9. 팀원 소개

> 팀원 전체가 같은 저장소를 fork해서 사용했지만, GitHub 제출은 **개인 계정 기준**입니다.

- **장현진** – 데이터 전처리, 대시보드 설계, 전체 코드 구조 설계  
- **강예솔** – 지표 정의, 시각화 아이디어, 결과 해석  
- **박세린** – 데이터 이해 및 도메인 리서치, README 정리  
- **강우석** – 코드 리팩토링, 실험 파라미터 튜닝, 발표 자료 지원  

(역할 분담은 과제 제출 형식에 맞추어 자유롭게 수정 가능합니다.)

---

## 10. 외부 URL & 참고 자료

- **데이터 출처**
  - 서울 열린데이터 광장: <https://data.seoul.go.kr>

- **사용 라이브러리 문서**
  - Streamlit: <https://docs.streamlit.io>  
  - Plotly Express: <https://plotly.com/python/plotly-express/>  
  - pandas: <https://pandas.pydata.org/docs/>  
  - statsmodels: <https://www.statsmodels.org/>

- **기타 참고**
  - Python 공식 문서: <https://docs.python.org/3/>

---

> 본 프로젝트는 대학 **빅데이터 분석 실습** 수업의 과제 목적으로 수행되었으며,  
> 구로구 실거래가 데이터를 통해 **실제 생활과 연결된 인사이트를 얻는 것**을 목표로 합니다.
