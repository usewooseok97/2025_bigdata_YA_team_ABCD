import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import statsmodels.api as sm

# 전역 변수
sidebar_image = "./smart_guro.png"
csv_path = "./서울시_부동산_실거래가_정보_구로구.csv"
pages = ["Home", "연/월 추세", "면적 체감효과", "연식 코호트", "반복매매 지수", "가격 분포 (수염차트)"]

# 데이터 읽기
def load_data(path):
    df = pd.read_csv(path, encoding="euc-kr", low_memory=False)
    
    df['계약일자'] = pd.to_datetime(df['계약일'], format='%Y%m%d')
    # df['계약일자'] = df['계약일자'].dt.date
    df['계약연'] = df['계약일자'].dt.year
    df['계약월'] = df['계약일자'].dt.month
    df['계약일'] = df['계약일자'].dt.day
    
    df['건물면적(평)'] = df['건물면적(㎡)'] * 0.3025
    
    df['물건금액(원)'] = df['물건금액(만원)'] * 10000
    
    df['평단가'] = df['물건금액(원)'] / df['건물면적(평)']
    
    return df

df = load_data(csv_path)

# st 기본 설정
st.set_page_config(page_title="구로구 부동산 실거래가 분석", layout="wide")

# st 사이드바
st.sidebar.image(sidebar_image, width='stretch')

st.sidebar.markdown("<hr>", unsafe_allow_html=True)

selected_page = st.sidebar.selectbox("목록", options=pages, index=0)

st.sidebar.markdown("<hr>", unsafe_allow_html=True)

st.sidebar.markdown("### Filter Options")

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

# 데이터 필터링
q = df[
    (df['건물용도'].isin(selected_uses)) &
    ((df['법정동명'].isin(selected_dongs)) if selected_dongs else True) &
    (df['계약연'] >= selected_years[0]) & (df['계약연'] <= selected_years[1]) &
    (df['건물면적(평)'] >= selected_area[0]) & (df['건물면적(평)'] <= selected_area[1]) &
    (df['물건금액(원)'] >= selected_price[0]) & (df['물건금액(원)'] <= selected_price[1])
].copy()

# st 메인 페이지
def Home():
    st.title("구로구 실거래가 분석: 2006 ~ 2025 인사이트")
    st.markdown("### 서울시 구로구 실거래 데이터를 기반으로 한 탐색형 대시보드 <hr>", unsafe_allow_html=True)
    
    c1, c2, c3 = st.columns(3)
    with c1: st.metric("표본 수", f"{len(q):,}")
    with c2: st.metric("평균 거래 가격(원)", f"{q['물건금액(원)'].mean():,.0f}")
    with c3: st.metric("평단가 평균(원)", f"{q['평단가'].mean():,.0f}")
    
    st.subheader("연도별 평당 단가(중앙값)")
    if len(q):
        ts = q.groupby(['건물용도', '계약연'])['평단가'].median().reset_index()
        fig = px.line(ts, x='계약연', y='평단가', color='건물용도', markers=True)
        fig.update_layout(yaxis_title='원/평')
        st.plotly_chart(fig, width='stretch')
    else:
        st.info("필터 조건에 맞는 데이터가 없습니다.")
    
    colA, colB, colC = st.columns(3)
    with colA:
        st.subheader("용도별 거래 비중")
        if len(q):
            pie = q['건물용도'].value_counts().reset_index()
            pie.columns = ['건물용도','건수']
            fig = px.pie(pie, names='건물용도', values='건수', hole=0.4)
            st.plotly_chart(fig, width='stretch')
    with colB:
        st.subheader("동별 중앙 평단가 TOP 10")
        if len(q):
            top = (q.groupby('법정동명')['평단가'].median()
                   .sort_values(ascending=False).head(10).reset_index())
            fig = px.bar(top, x='평단가', y='법정동명', orientation='h', color='법정동명')
            fig.update_layout(xaxis_title='원/㎡', yaxis_title='법정동')
            st.plotly_chart(fig, width='stretch')
    with colC:
        st.subheader("동별 거래량 TOP 10")
        if len(q):
            top_count = (q['법정동명'].value_counts().head(10).reset_index())
            top_count.columns = ['법정동명','건수']
            fig = px.bar(top_count, x='건수', y='법정동명', orientation='h', color='법정동명')
            fig.update_layout(xaxis_title='거래 건수', yaxis_title='법정동')
            st.plotly_chart(fig, width='stretch')

    st.subheader("최근 거래 30건")
    
    cols = ['계약일자', '법정동명', '건물용도', '건물면적(평)', '물건금액(원)', '평단가']
    show_cols = [c for c in cols if c in q.columns]
    if len(q) and show_cols:
        st.dataframe(q.sort_values('계약일자', ascending=False)[show_cols].head(30), width='stretch')

def 연월_추세():
    st.header("연/월별 평당 실거래가 추세")
    mv = st.radio("이동평균", options=[None,'3개월','6개월','12개월'], horizontal=True, index=0)
    show_cnt = st.checkbox("거래건수 보조축 표시", value=False)

    if not len(q): st.info("데이터 없음"); st.stop()
    
    g = q.groupby(['계약월','건물용도']).agg(중앙단가=('평단가','median'), 건수=('평단가','count')).reset_index()
    if mv:
        win = int(mv.replace('개월',''))
        g['중앙단가_MA'] = g.groupby('건물용도')['중앙단가'].transform(lambda s: s.rolling(win, min_periods=1).mean())

    ycol = '중앙단가_MA' if mv else '중앙단가'
    fig = px.line(g, x='계약월', y=ycol, color='건물용도', markers=True)
    fig.update_layout(yaxis_title='원/평', title="평당 실거래가 추세")
    st.plotly_chart(fig, width='stretch')

    if show_cnt:
        fig2 = px.line(g, x='계약월', y='건수', color='건물용도', markers=True, title="거래건수(보조)")
        st.plotly_chart(fig2, width='stretch')

    st.subheader("월별 요약 테이블")
    st.dataframe(g.head(2000), width='stretch')

def 면적_체감효과():
    st.header("면적의 체감효과(규모의 경제)")
    scale = st.radio("회귀 스케일", options=['선형','로그-로그'], horizontal=True)
    샘플 = st.slider("산점 샘플 수", 1000, 10000, 4000, step=500)
    
    if not len(q): st.info("데이터 없음"); st.stop()
    
    qq = q[['건물면적(평)','평단가','건물용도']].dropna().sample(min(샘플, len(q)), random_state=1)
    if scale == '로그-로그':
        qq = qq[(qq['건물면적(평)']>0) & (qq['평단가']>0)]
        qq['log_면적'] = np.log(qq['건물면적(평)'])
        qq['log_단가'] = np.log(qq['평단가'])
        fig = px.scatter(qq, x='log_면적', y='log_단가', color='건물용도', trendline='ols', opacity=0.5)
    else:
        fig = px.scatter(qq, x='건물면적(평)', y='평단가', color='건물용도', trendline='ols', opacity=0.5)
    st.plotly_chart(fig, width='stretch')
    st.dataframe(qq.head(100), width='stretch')
    
def 연식_코호트():
    st.header("연식 코호트 비교")
    단위 = st.radio("코호트 단위", options=['10년','5년'], horizontal=True)
    
    if not len(q): st.info("데이터 없음"); st.stop()
    
    def cohort_label(y):
        if pd.isna(y): return '미상'
        y = int(y)
        if 단위=='10년':
            s = (y//10)*10; e = s+9; return f'{s}s'
        else:
            s = (y//5)*5; e = s+4; return f'{s}-{e}'
    
    qq = q[['건축년도','평단가','계약월']].copy()
    qq['코호트'] = qq['건축년도'].apply(cohort_label)
    m = qq.groupby(['코호트','계약월'])['평단가'].median().reset_index()
    
    fig = px.line(m, x='계약월', y='평단가', color='코호트')
    st.plotly_chart(fig, width='stretch')
    st.dataframe(m.head(2000), width='stretch')
    
def 반복매매_지수():
    st.header("반복매매(Repeat Sales) 후보 & 지수")
    키구성 = st.multiselect("동일물건 판정 키", options=['법정동명','본번','부번','건물명'], default=['법정동명','본번','부번','건물명'])
    최소간격 = st.slider("최소 재거래 간격(개월)", 0, 60, 6)
    
    if not len(q): st.info("데이터 없음"); st.stop()
    
    # 간단 후보: 키 그룹에서 2건 이상
    key = [c for c in 키구성 if c in q.columns]
    if not key: st.info("키가 없습니다."); st.stop()
    
    cand = q.dropna(subset=key+['계약일자','평단가']).copy()
    gp = cand.groupby(key)
    pairs = gp.filter(lambda d: len(d)>=2).sort_values(key+['계약일자'])
    
    st.subheader("후보(상위 200)")
    cols = key + ['계약일자','평단가','건물면적(㎡)']
    st.dataframe(pairs[cols].head(200), width='stretch')
    st.caption("※ 지수/수익률 산출 로직은 사용자 구현 위치")

def 가격_분포_수염차트():
    st.header("기준별 가격 분포 (Box Plot)")
    
    # X축, Y축 선택 옵션
    c1, c2 = st.columns(2)
    with c1:
        x_axis_option = st.radio(
            "분석 기준 (X축)",
            options=['법정동명', '건물용도', '계약연'],
            horizontal=True,
            index=0
        )
    with c2:
        y_axis_option = st.radio(
            "분석 값 (Y축)",
            options=['평단가', '물건금액(원)', '건물면적(평)'],
            horizontal=True,
            index=0
        )
    
    st.subheader(f"{x_axis_option}별 {y_axis_option} 분포")

    if not len(q): 
        st.info("필터 조건에 맞는 데이터가 없습니다.")
        st.stop()
    
    # X축의 고유값이 너무 많으면 차트가 복잡해질 수 있음을 알림
    unique_count = len(q[x_axis_option].unique())
    if unique_count > 20:
        st.info(f"'{x_axis_option}'의 고유 항목이 {unique_count}개로 너무 많습니다. 사이드바 필터를 사용해 비교 대상을 줄이는 것을 권장합니다.")

    # 시각화를 위한 데이터 복사 및 처리
    plot_q = q.copy()
    
    # '계약연'은 숫자가 아닌 카테고리(문자열)로 다루어야 box plot이 올바르게 그려짐
    if x_axis_option == '계약연':
        plot_q[x_axis_option] = plot_q[x_axis_option].astype(str)

    # Plotly로 Box Plot 생성
    fig = px.box(plot_q, x=x_axis_option, y=y_axis_option, color=x_axis_option,
                 title=f"{x_axis_option}에 따른 {y_axis_option} 분포")
    
    # Y축 레이블 설정
    y_title_map = {
        '평단가': '원/평',
        '물건금액(원)': '원',
        '건물면적(평)': '평'
    }
    fig.update_layout(
        xaxis_title=x_axis_option,
        yaxis_title=y_title_map.get(y_axis_option, y_axis_option)
    )
    
    st.plotly_chart(fig, width='stretch')

    # 데이터 샘플 표시
    st.dataframe(plot_q[[x_axis_option, y_axis_option]].head(200), width='stretch')

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
