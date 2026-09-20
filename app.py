from pathlib import Path

import pandas as pd
import streamlit as st
import geopandas as gpd
import altair as alt
import pydeck as pdk

# 페이지 기본 설정
st.set_page_config(
    page_title="골목상권 매출 하락 조기경보",
    layout="wide",
    initial_sidebar_state="expanded",
)
# 대시보드 디자인
st.markdown(
    """
<style>
:root {
    --black: #111111;
    --red: #BF0404;
    --gray: #E5E5E5;
    --white: #FFFFFF;
    --text-gray: #6F6F6F;
}

/* 전체 배경 */
.stApp {
    background: var(--gray);
    color: var(--black);
}

[data-testid="stHeader"] {
    background: transparent;
    height: 3rem;
}

[data-testid="stToolbar"],
#MainMenu,
footer {
    visibility: hidden;
}

/* 대시보드 본체 */
.block-container {
    max-width: 1180px;
    margin-top: 25px;
    margin-bottom: 25px;
    padding: 34px 40px 40px;

    background: var(--white);
    border-radius: 22px;

    box-shadow: 0 18px 45px rgba(17, 17, 17, 0.10);
}

html,
body,
[class*="css"] {
    font-family:
        "Malgun Gothic",
        "Apple SD Gothic Neo",
        sans-serif;
}

/* 단순한 상단 제목 */
.simple-header {
    display: flex;
    justify-content: space-between;
    align-items: flex-end;
    gap: 25px;

    padding: 6px 3px 19px;
    border-bottom: 1px solid var(--gray);
}

.simple-title {
    margin: 0 0 7px;

    color: var(--black);
    font-size: 28px;
    font-weight: 800;
    letter-spacing: -1.2px;
}

.simple-title .highlight {
    color: var(--red);
}

.simple-description {
    margin: 0;

    color: var(--text-gray);
    font-size: 13px;
}

.simple-period {
    flex-shrink: 0;
    padding-bottom: 2px;

    color: var(--text-gray);
    font-size: 12px;
    text-align: right;
}

.simple-period strong {
    display: block;
    margin-top: 4px;

    color: var(--black);
    font-size: 17px;
}

/* 아이콘 메뉴를 중앙에 배치 */
div[data-testid="stElementContainer"]:has(
    div[data-testid="stButtonGroup"]
),
div[data-testid="stElementContainer"]:has(
    div[data-testid="stSegmentedControl"]
) {
    display: flex !important;
    justify-content: center !important;

    margin: 17px 0 27px !important;
}

/* 메뉴 공통 배경 제거 */
div[data-testid="stButtonGroup"],
div[data-testid="stSegmentedControl"] {
    width: auto !important;
    min-width: 0 !important;
    max-width: none !important;

    margin: 0 !important;
    padding: 0 !important;

    background: transparent !important;
    border: none !important;
    box-shadow: none !important;
}

/* 버튼 한 줄 정렬 */
div[data-testid="stButtonGroup"] div[role="radiogroup"],
div[data-testid="stSegmentedControl"] div[role="radiogroup"] {
    display: flex !important;
    flex-wrap: nowrap !important;
    gap: 10px !important;
}

/* 각각 분리된 메뉴 버튼 */
div[data-testid="stButtonGroup"] button,
div[data-testid="stSegmentedControl"] button {
    flex: 0 0 42px !important;

    width: 42px !important;
    min-width: 42px !important;
    max-width: 42px !important;
    height: 42px !important;
    min-height: 42px !important;

    margin: 0 !important;
    padding: 0 !important;

    display: flex !important;
    align-items: center !important;
    justify-content: center !important;

    background: #F4F4F4 !important;
    border: 1px solid #D7D7D7 !important;
    border-radius: 11px !important;

    color: #555555 !important;

    box-shadow: none !important;
}

div[data-testid="stButtonGroup"] button p,
div[data-testid="stSegmentedControl"] button p {
    margin: 0 !important;

    color: inherit !important;
    font-size: 18px !important;
    line-height: 1 !important;
    text-align: center !important;
}

/* 마우스 오버 */
div[data-testid="stButtonGroup"] button:hover,
div[data-testid="stSegmentedControl"] button:hover {
    background: #EAEAEA !important;
    border-color: #BBBBBB !important;
    color: var(--black) !important;
}

/* 선택된 메뉴 */
div[data-testid="stButtonGroup"] button[aria-pressed="true"],
div[data-testid="stSegmentedControl"] button[aria-pressed="true"],
button[data-testid="stBaseButton-segmented_controlActive"] {
    background: var(--red) !important;
    border-color: var(--red) !important;
    color: var(--white) !important;

    box-shadow: 0 5px 13px rgba(191, 4, 4, 0.22) !important;
}

/* 핵심 지표 */
.kpi-grid {
    display: grid;
    grid-template-columns: repeat(4, minmax(0, 1fr));
    gap: 13px;
    margin: 17px 0 24px;
}

.kpi-card {
    min-height: 128px;
    padding: 19px;

    background: var(--white);
    border: 1px solid var(--gray);
    border-radius: 14px;
}

.kpi-label {
    margin-bottom: 12px;

    color: var(--text-gray);
    font-size: 12px;
    font-weight: 700;
}

.kpi-value {
    color: var(--black);
    font-size: 29px;
    font-weight: 800;
    letter-spacing: -1px;
}

.kpi-unit {
    margin-left: 3px;
    font-size: 16px;
}

.kpi-note {
    margin-top: 8px;

    color: #929292;
    font-size: 11px;
}

/* 시나리오 타격액 강조 */
.kpi-card.impact {
    background: var(--red);
    border-color: var(--red);
}

.kpi-card.impact .kpi-label,
.kpi-card.impact .kpi-note {
    color: rgba(255, 255, 255, 0.76);
}

.kpi-card.impact .kpi-value {
    color: var(--white);
}

/* 평균 위험점수 강조 */
.kpi-card.risk {
    background: var(--black);
    border-color: var(--black);
}

.kpi-card.risk .kpi-label,
.kpi-card.risk .kpi-note {
    color: #BDBDBD;
}

.kpi-card.risk .kpi-value {
    color: var(--white);
}

/* 상세 페이지 지표 */
[data-testid="stMetric"] {
    padding: 16px 18px;

    background: var(--white);
    border: 1px solid var(--gray);
    border-top: 3px solid var(--red);
    border-radius: 12px;
}

[data-testid="stMetricLabel"] {
    color: var(--text-gray);
}

[data-testid="stMetricValue"] {
    color: var(--black);
    font-weight: 800;
}

/* 표와 입력창 */
[data-testid="stDataFrame"] {
    overflow: hidden;

    border: 1px solid var(--gray);
    border-radius: 12px;
}

[data-testid="stSelectbox"] > div > div {
    background: var(--white);
    border-radius: 9px;
}

/* 안내 영역 */
[data-testid="stAlert"] {
    background: #F5F5F5;
    border: 1px solid var(--gray);
    border-left: 4px solid var(--red);
    border-radius: 9px;
}

h2,
h3,
h4 {
    color: var(--black);
    font-weight: 800;
    letter-spacing: -0.5px;
}

hr {
    border-color: var(--gray);
}

@media (max-width: 800px) {
    .block-container {
        margin-top: 10px;
        padding: 23px 19px;
        border-radius: 16px;
    }

    .simple-header {
        align-items: flex-start;
        flex-direction: column;
    }

    .simple-period {
        text-align: left;
    }

    .kpi-grid {
        grid-template-columns: 1fr 1fr;
    }
}

@media (max-width: 500px) {
    .simple-title {
        font-size: 23px;
    }

    .kpi-grid {
        grid-template-columns: 1fr;
    }
}
/* 전체 화면 여백 축소 */
.block-container {
    margin-top: 14px !important;
    margin-bottom: 14px !important;
    padding: 23px 30px 28px !important;
}

/* 제목 영역을 조금 더 компакт하게 */
.simple-header {
    padding-top: 2px !important;
    padding-bottom: 14px !important;
}

/* 아이콘 메뉴 주변 여백 축소 */
div[data-testid="stElementContainer"]:has(
    div[data-testid="stButtonGroup"]
),
div[data-testid="stElementContainer"]:has(
    div[data-testid="stSegmentedControl"]
) {
    margin-top: 12px !important;
    margin-bottom: 17px !important;
}

/* 관리 현황 제목 여백 */
h2,
h3 {
    margin-top: 4px !important;
    margin-bottom: 7px !important;
}

/* KPI 카드 간격 */
.kpi-grid {
    gap: 12px !important;
    margin-top: 10px !important;
    margin-bottom: 18px !important;
}

/* KPI 카드 크기 */
.kpi-card {
    min-height: 145px !important;
    padding: 22px 20px !important;

    display: flex;
    flex-direction: column;
    justify-content: center;
}

/* 카드 제목 확대 */
.kpi-label {
    margin-bottom: 14px !important;

    font-size: 14px !important;
    font-weight: 800 !important;
    line-height: 1.35 !important;
}

/* 핵심 숫자 확대 */
.kpi-value {
    font-size: 36px !important;
    font-weight: 900 !important;
    line-height: 1 !important;
    letter-spacing: -1.3px !important;
}

/* 단위 확대 */
.kpi-unit {
    margin-left: 4px !important;
    font-size: 19px !important;
    font-weight: 800 !important;
}

/* 카드 설명 확대 */
.kpi-note {
    margin-top: 13px !important;

    font-size: 12px !important;
    line-height: 1.45 !important;
}
.action-card {
    min-height: 58px;
    padding: 17px 18px;

    display: flex;
    align-items: center;

    background: #F5F5F5;
    border: 1px solid #E5E5E5;
    border-left: 4px solid #BF0404;
    border-radius: 9px;

    color: #111111;
    font-size: 14px;
    font-weight: 600;
    line-height: 1.5;
}
/* 우선관리 TOP 5 표 */
.priority-table {
    width: 100%;
    table-layout: fixed;
    border-collapse: separate;
    border-spacing: 0;

    overflow: hidden;

    background: #FFFFFF;
    border: 1px solid #E5E5E5;
    border-radius: 11px;

    color: #111111;
    font-size: 13px;
}

.priority-table th {
    padding: 10px 8px;

    background: #F4F4F4;
    border-bottom: 1px solid #D8D8D8;

    color: #666666;
    font-size: 12px;
    font-weight: 700;
    text-align: left;
}

.priority-table td {
    padding: 10px 8px;

    border-bottom: 1px solid #E5E5E5;

    vertical-align: middle;
    line-height: 1.35;
}

.priority-table tbody tr:last-child td {
    border-bottom: none;
}

/* 순위 열 */
.priority-table th:nth-child(1),
.priority-table td:nth-child(1) {
    width: 42px;
    padding-left: 4px;
    padding-right: 4px;
    text-align: center;
}

/* 상권명 열 */
.priority-table th:nth-child(2),
.priority-table td:nth-child(2) {
    width: auto;

    white-space: normal;
    word-break: keep-all;
}

/* 위험점수 열 */
.priority-table th:nth-child(3),
.priority-table td:nth-child(3) {
    width: 72px;
    text-align: right;
}

.priority-table td:nth-child(3) {
    color: #BF0404;
    font-weight: 800;
}

/* 타격액 열 */
.priority-table th:nth-child(4),
.priority-table td:nth-child(4) {
    width: 76px;
    text-align: right;
    white-space: nowrap;
}

.priority-table tbody tr:hover {
    background: #FAF2F2;
}
/* TOP 5 표 최종 정렬 */
.priority-table {
    width: 100% !important;
    table-layout: fixed !important;
}

.priority-table th,
.priority-table td {
    box-sizing: border-box !important;
    height: 40px;
    padding: 9px 9px !important;

    vertical-align: middle !important;
    line-height: 1.35 !important;
}

/* 순위 */
.priority-table th:nth-child(1),
.priority-table td:nth-child(1) {
    width: 40px !important;
    padding-left: 3px !important;
    padding-right: 3px !important;
    text-align: center !important;
}

/* 상권명 */
.priority-table th:nth-child(2),
.priority-table td:nth-child(2) {
    width: auto !important;
    text-align: left !important;

    white-space: normal !important;
    word-break: keep-all !important;
    overflow-wrap: anywhere !important;
}

/* 위험점수 */
.priority-table th:nth-child(3),
.priority-table td:nth-child(3) {
    width: 72px !important;
    text-align: right !important;
}

/* 타격액 */
.priority-table th:nth-child(4),
.priority-table td:nth-child(4) {
    width: 92px !important;
    text-align: right !important;
    white-space: nowrap !important;
}

/* 행 구분 */
.priority-table tbody tr:nth-child(even) {
    background: #F8F8F8;
}

.priority-table tbody tr:hover {
    background: #FAEEEE;
}

/* 전체 화면 반응형 레이아웃 */
.stApp {
    background: #FFFFFF;
}

.block-container {
    width: 100% !important;
    max-width: none !important;
    min-height: 100vh;

    margin: 0 !important;
    padding: 24px clamp(20px, 3vw, 54px) 36px !important;

    border-radius: 0 !important;
    box-shadow: none !important;
}

@media (max-width: 800px) {
    .block-container {
        padding: 18px 16px 28px !important;
    }
}

/* 접힌 사이드바의 펼치기 버튼은 표시 */
[data-testid="stExpandSidebarButton"] {
    visibility: visible !important;
}

/* 큰 메뉴를 세로 풀페이지로 전환 */
[data-testid="stMain"] {
    scroll-snap-type: y mandatory;
    scroll-behavior: smooth;
    overscroll-behavior-y: contain;
}

/* 1페이지: 상권 상세 분석 */
[data-testid="stLayoutWrapper"]:has(.st-key-slide_detail) {
    order: 1;
    min-height: 100vh;

    scroll-snap-align: start;
    scroll-snap-stop: always;
    scroll-margin-top: 0;
}

/* 2페이지: 종합 현황 */
[data-testid="stLayoutWrapper"]:has(.st-key-slide_overview) {
    order: 2;
    min-height: 100vh;

    scroll-snap-align: start;
    scroll-snap-stop: always;
}

/* 3페이지: 우선관리 상권 */
[data-testid="stLayoutWrapper"]:has(.st-key-slide_priority) {
    order: 3;
    min-height: 100vh;

    scroll-snap-align: start;
    scroll-snap-stop: always;
}

/* 작은 모바일 화면에서는 내용이 잘리지 않도록 일반 스크롤 */
@media (max-width: 700px) {
    [data-testid="stMain"] {
        scroll-snap-type: none;
    }

    [data-testid="stLayoutWrapper"]:has(.st-key-slide_detail),
    [data-testid="stLayoutWrapper"]:has(.st-key-slide_overview),
    [data-testid="stLayoutWrapper"]:has(.st-key-slide_priority) {
        min-height: auto;
        scroll-snap-align: none;
        scroll-margin-top: 0;
    }
}

.slide-heading {
    padding: 12px 0 20px;
    margin-bottom: 26px;
    border-bottom: 1px solid #E5E7EB;
}

.slide-number {
    color: #D00000;
    font-size: 14px;
    font-weight: 800;
    letter-spacing: 0.16em;
}

.slide-main-title {
    margin-top: 6px;
    color: #111111;
    font-size: clamp(34px, 4vw, 58px);
    font-weight: 900;
    line-height: 1.08;
}

.slide-description {
    margin-top: 10px;
    color: #6B7280;
    font-size: clamp(14px, 1.2vw, 17px);
}

/* 원래 대시보드 제목 고정 */
[data-testid="stElementContainer"]:has(.simple-header) {
    position: sticky;
    top: 0;
    z-index: 9999;

    padding: 0 !important;
    min-height: 132px;

    background: #FFFFFF !important;
    box-shadow: 0 1px 0 #E5E7EB;
}

/* 제목 영역 자체도 완전히 불투명하게 */
.simple-header {
    background: #FFFFFF !important;
}

/* 화면 제목이 고정 헤더에 가려지지 않게 */
[data-testid="stMain"] {
    scroll-padding-top: 144px !important;
}

/* 종합 현황 왼쪽 KPI 카드 2×2 배치 */
.st-key-slide_overview .kpi-grid {
    grid-template-columns: repeat(2, minmax(0, 1fr)) !important;
    gap: 14px !important;
    margin: 12px 0 14px !important;
}

.st-key-slide_overview .kpi-card {
    aspect-ratio: 1 / 1;
    min-height: 0 !important;
    padding: 18px !important;
}

@media (min-width: 701px) and (max-width: 1100px) {
    [data-testid="stMain"] {
        scroll-padding-top: 196px !important;
    }
}

/* 고정 프레임: 프로젝트 제목은 원래 크기로 유지 */
[data-testid="stElementContainer"]:has(.simple-header) {
    position: sticky;
    top: 0;
    z-index: 9999;

    min-height: 138px !important;
    background: #FFFFFF !important;
    box-shadow: 0 1px 0 #E5E7EB;
}

html body .simple-header {
    padding: 2px 3px 14px !important;
    align-items: flex-end !important;
    background: #FFFFFF !important;
}

html body .simple-header .simple-title {
    margin: 0 0 7px !important;
    padding: 20px 0 16px !important;

    font-size: 44px !important;
    line-height: 1.2 !important;
}

html body .simple-header .simple-description {
    font-size: 16px !important;
    line-height: 1.6 !important;
}

/* 고정 제목 아래에서 페이지 시작 */
[data-testid="stMain"] {
    scroll-padding-top: 152px !important;
}

/* 페이지 높이를 억지로 늘리지 않음 */
[data-testid="stLayoutWrapper"]:has(.st-key-slide_detail),
[data-testid="stLayoutWrapper"]:has(.st-key-slide_overview),
[data-testid="stLayoutWrapper"]:has(.st-key-slide_priority) {
    height: auto !important;
    min-height: 0 !important;
    overflow: visible !important;
}

/* 프로젝트 헤더 위쪽 공간 확보 */
html body [data-testid="stElementContainer"]:has(.simple-header) {
    min-height: 150px !important;
}

html body .simple-header {
    padding: 14px 3px !important;
}

/* 상권 상세 분석·종합 현황 등의 페이지 제목 축소 */
html body .slide-heading {
    padding: 6px 0 12px !important;
    margin-bottom: 12px !important;
}

html body .slide-number {
    font-size: 11px !important;
}

html body .slide-main-title {
    margin-top: 3px !important;
    font-size: 32px !important;
    line-height: 1.1 !important;
}

html body .slide-description {
    margin-top: 4px !important;
    font-size: 13px !important;
    line-height: 1.3 !important;
}

/* 고정 프로젝트 헤더 아래에 페이지 정렬 */
html body [data-testid="stMain"] {
    scroll-padding-top: 150px !important;
}

/* 상세 페이지는 정확히 남은 화면만 사용 */
@media (min-width: 1200px) and (min-height: 740px) {
    html body
    [data-testid="stLayoutWrapper"]:has(.st-key-slide_detail) {
        height: calc(100dvh - 164px) !important;
        min-height: calc(100dvh - 164px) !important;
        overflow: hidden !important;
    }

    /* 남는 공간을 내용 사이에 분배 */
    html body .st-key-slide_detail {
        height: 100% !important;
        justify-content: space-between !important;
        gap: 0 !important;
    }
}

/* 종합 현황 왼쪽 KPI 카드 압축 */
html body .st-key-slide_overview .kpi-grid {
    gap: 10px !important;
    margin: 8px 0 10px !important;
}

html body .st-key-slide_overview .kpi-card {
    padding: 14px !important;
}

html body .st-key-slide_overview .kpi-label {
    margin-bottom: 8px !important;
    font-size: 12px !important;
}

html body .st-key-slide_overview .kpi-note {
    font-size: 11px !important;
    line-height: 1.35 !important;
}

/* 종합 현황 내부의 불필요한 제목 여백 제거 */
html body .st-key-slide_overview h3 {
    margin: 0 0 4px !important;
    padding: 0 !important;

    font-size: 24px !important;
    line-height: 1.2 !important;
}

html body .st-key-slide_overview h4 {
    margin: 0 0 4px !important;
    padding: 0 !important;

    font-size: 20px !important;
    line-height: 1.2 !important;
}

/* 종합 현황 안의 요소 사이 기본 간격 축소 */
html body
.st-key-slide_overview [data-testid="stVerticalBlock"] {
    gap: 8px !important;
}

/* 종합 현황을 화면 한 장에 정확히 맞춤 */
@media (min-width: 1200px) and (min-height: 740px) {
    html body
    [data-testid="stLayoutWrapper"]:has(.st-key-slide_overview) {
        height: calc(100dvh - 166px) !important;
        min-height: calc(100dvh - 166px) !important;
        overflow: hidden !important;
    }

    /* 화면 높이에 따라 지도도 남은 공간을 채움 */
    html body
    .st-key-slide_overview [data-testid="stDeckGlJsonChart"],
    html body
    .st-key-slide_overview [data-testid="stDeckGlJsonChart"] > div:last-child {
        height: clamp(
            500px,
            calc(100dvh - 330px),
            620px
        ) !important;

        min-height: clamp(
            500px,
            calc(100dvh - 330px),
            620px
        ) !important;
    }
}

/* 종합 현황의 콘텐츠 높이를 실제 내용에 맞춤.
   좁은 왼쪽 열에서 정사각형 비율과 뷰포트 고정 높이가 함께 적용되면
   KPI 설명과 다음 섹션이 겹치므로 이 화면에 한해 두 제약을 해제한다. */
html body .st-key-slide_overview .kpi-card {
    aspect-ratio: auto !important;
    height: auto !important;
    min-height: 176px !important;
    padding: 18px !important;

    display: flex !important;
    flex-direction: column !important;
    justify-content: center !important;
}

html body .st-key-slide_overview .kpi-value {
    font-size: clamp(28px, 2.2vw, 36px) !important;
    line-height: 1.08 !important;
    white-space: nowrap;
}

html body .st-key-slide_overview .kpi-unit {
    font-size: clamp(14px, 1.3vw, 19px) !important;
}

html body .st-key-slide_overview .kpi-label,
html body .st-key-slide_overview .kpi-note {
    white-space: normal !important;
    word-break: keep-all !important;
    overflow-wrap: anywhere !important;
}

html body .st-key-slide_overview .kpi-note {
    margin-top: 12px !important;
}

html body .st-key-slide_overview [data-testid="stCaptionContainer"] {
    margin: 4px 0 18px !important;
    line-height: 1.65 !important;
    white-space: normal !important;
}

html body .st-key-slide_overview {
    padding-bottom: 44px !important;
}

@media (min-width: 1200px) and (min-height: 740px) {
    html body
    [data-testid="stLayoutWrapper"]:has(.st-key-slide_overview) {
        height: auto !important;
        min-height: 0 !important;
        overflow: visible !important;
    }
}

@media (max-width: 1100px) {
    /* 좁은 데스크톱에서는 종합 현황의 3열 구성을 세로로 쌓아
       지도·범례와 다음 제목이 화면 밖으로 밀리지 않게 한다. */
    html body .st-key-slide_overview [data-testid="stHorizontalBlock"] {
        flex-direction: column !important;
        align-items: stretch !important;
    }

    html body .st-key-slide_overview [data-testid="stColumn"] {
        width: 100% !important;
        flex: 1 1 auto !important;
    }

    html body .st-key-slide_overview .kpi-grid {
        grid-template-columns: repeat(2, minmax(0, 1fr)) !important;
    }

    html body .st-key-slide_overview .kpi-card {
        min-height: 148px !important;
    }
}

@media (max-width: 700px) {
    html body .st-key-slide_overview .kpi-grid {
        grid-template-columns: 1fr !important;
    }
}

</style>
""",
    unsafe_allow_html=True,
)

# 데이터 경로
BASE_DIR = Path(__file__).resolve().parent
DATA_PATH = (
    BASE_DIR
    / "data"
    / "processed"
    / "priority_top5_20261.csv"
)
FULL_DATA_PATH = (
    BASE_DIR
    / "data"
    / "processed"
    / "coffee_risk_analysis_data_v2.csv"
)
AREA_SHAPE_PATH = (
    BASE_DIR
    / "data"
    / "raw"
    / "commercial_area_boundary"
    / "서울시 상권분석서비스(영역-상권).shp"
)

@st.cache_data
def load_data():
    return pd.read_csv(DATA_PATH, encoding="utf-8-sig")
@st.cache_data
def load_full_data():
    return pd.read_csv(
        FULL_DATA_PATH,
        encoding="utf-8-sig",
    )
@st.cache_data
def load_commercial_area_coordinates():
    area_gdf = gpd.read_file(
        AREA_SHAPE_PATH,
        encoding="cp949",
    )

    # 상권 코드를 숫자형으로 통일
    area_gdf["상권_코드"] = pd.to_numeric(
        area_gdf["TRDAR_CD"],
        errors="coerce",
    ).astype("Int64")

    # 거리 계산용 좌표계로 통일
    if area_gdf.crs is None:
        area_gdf = area_gdf.set_crs(epsg=5181)
    else:
        area_gdf = area_gdf.to_crs(epsg=5181)

    # 각 상권 영역의 중심점 계산
    center_gdf = gpd.GeoDataFrame(
        {
            "상권_코드": area_gdf["상권_코드"],
        },
        geometry=area_gdf.geometry.centroid,
        crs=area_gdf.crs,
    )

    # 지도용 위·경도로 변환
    center_gdf = center_gdf.to_crs(epsg=4326)

    center_gdf["위도"] = center_gdf.geometry.y
    center_gdf["경도"] = center_gdf.geometry.x

    return (
        center_gdf[
            ["상권_코드", "위도", "경도"]
        ]
        .dropna()
        .drop_duplicates("상권_코드")
    )

# 데이터 불러오기
df = load_data()

전체_원본_df = load_full_data()

기준_분기 = int(
    df["기준_년분기_코드"].iloc[0]
)

전체_원본_df["기준_년분기_코드"] = pd.to_numeric(
    전체_원본_df["기준_년분기_코드"],
    errors="coerce",
)

전체_원본_df["2차_위험신호지수"] = pd.to_numeric(
    전체_원본_df["2차_위험신호지수"],
    errors="coerce",
)

전체_df = 전체_원본_df.loc[
    전체_원본_df["기준_년분기_코드"]
    == 기준_분기
].copy()

전체_df = 전체_df.dropna(
    subset=["2차_위험신호지수"]
)

전체_df["전체_위험순위"] = (
    전체_df["2차_위험신호지수"]
    .rank(
        method="min",
        ascending=False,
    )
    .astype(int)
)

전체_df = 전체_df.sort_values(
    "전체_위험순위"
).reset_index(drop=True)

# 상세페이지용 객단가 증감률 계산
매출비율 = (
    1
    + pd.to_numeric(
        전체_df["현재_매출_YoY_%"],
        errors="coerce",
    ) / 100
)

건수비율 = (
    1
    + pd.to_numeric(
        전체_df["현재_매출건수_YoY_%"],
        errors="coerce",
    ) / 100
)

전체_df["추정_객단가_YoY_%"] = (
    (
        매출비율
        / 건수비율.where(건수비율 != 0)
    )
    - 1
) * 100


# 관측된 지표에 따른 신호와 확인 조치
def 관측신호_생성(매출증감, 거래증감, 객단가증감):
    거래하락 = (
        pd.notna(거래증감)
        and 거래증감 <= -10
    )

    객단가하락 = (
        pd.notna(객단가증감)
        and 객단가증감 <= -5
    )

    매출하락 = (
        pd.notna(매출증감)
        and 매출증감 <= -10
    )

    if 거래하락 and 객단가하락:
        return (
            "[거래건수·객단가 동반 하락]",
            "방문 전환과 세트·추가구매 운영 상태를 함께 확인",
        )

    if 거래하락:
        return (
            "[거래건수 감소]",
            "유입·구매전환·재방문 지표를 추가로 확인",
        )

    if 객단가하락:
        return (
            "[객단가 하락]",
            "상품 구성과 세트·추가구매 운영 상태를 확인",
        )

    if 매출하락:
        return (
            "[매출 감소]",
            "거래건수와 상품 구성별 매출을 추가로 확인",
        )

    return (
        "[누적 위험 신호]",
        "최근 분기 추이와 현장 운영 상태를 함께 확인",
    )


# 전체 상권용 상세 진단 생성
def 상세진단_생성(행):
    위험수준값 = 행.get("2차_위험신호_구간")

    if pd.isna(위험수준값):
        return pd.Series(
            {
                "위험_상태_태그": "[판단 불가]",
                "주요_원인_태그": "[위험수준 미산정]",
                "권장_조치": "원천 데이터 확인 후 다시 평가",
                "보조_상황_태그": "[데이터 확인 필요]",
            }
        )

    위험수준 = str(위험수준값)
    매출증감 = 행.get("현재_매출_YoY_%")
    거래증감 = 행.get("현재_매출건수_YoY_%")
    객단가증감 = 행.get("추정_객단가_YoY_%")
    하락점수 = 행.get("하락지속_위험점수")

    매출개선 = (
        pd.notna(매출증감)
        and 매출증감 >= 0
    )

    거래개선 = (
        pd.notna(거래증감)
        and 거래증감 >= 0
    )

    강한하락신호 = (
        (
            pd.notna(매출증감)
            and 매출증감 <= -10
        )
        or (
            pd.notna(거래증감)
            and 거래증감 <= -10
        )
        or (
            pd.notna(객단가증감)
            and 객단가증감 <= -5
        )
    )

    # 위험수준을 먼저 기준으로 상태 결정
    if 위험수준 == "낮음":
        if 매출개선 and 거래개선:
            위험상태 = "[안정]"
            관측신호 = "[핵심 하락 신호 없음]"
            권장조치 = "정기 모니터링을 유지하고 다음 분기 변화를 확인"
        elif not 강한하락신호:
            위험상태 = "[관찰]"
            관측신호 = "[경미한 지표 변동]"
            권장조치 = "즉각적인 조치보다 다음 분기 지표를 재확인"
        else:
            위험상태 = "[관찰]"
            관측신호, 권장조치 = 관측신호_생성(
                매출증감,
                거래증감,
                객단가증감,
            )

    elif 위험수준 == "보통":
        위험상태 = "[주의 관찰]"
        관측신호, 권장조치 = 관측신호_생성(
            매출증감,
            거래증감,
            객단가증감,
        )

    elif 위험수준 in ["높음", "매우 높음"]:
        if pd.notna(하락점수) and 하락점수 >= 75:
            위험상태 = "[하락 장기화]"
        elif pd.notna(하락점수) and 하락점수 >= 50:
            위험상태 = "[하락 반복]"
        else:
            위험상태 = "[신규 위험 신호]"

        관측신호, 권장조치 = 관측신호_생성(
            매출증감,
            거래증감,
            객단가증감,
        )

    else:
        위험상태 = "[판단 불가]"
        관측신호 = "[위험수준 확인 필요]"
        권장조치 = "위험점수와 원천 데이터를 다시 확인"

    # 참고 신호 생성
    보조태그 = []

    if (
        pd.notna(객단가증감)
        and 객단가증감 <= -5
    ):
        보조태그.append(
            "[객단가 하락] 상품 구성 확인"
        )

    점포차이 = 행.get("점포수_전년차이")

    if (
        pd.notna(점포차이)
        and 점포차이 >= 2
    ):
        보조태그.append(
            "[경쟁 증가] 주변 점포 변화 확인"
        )

    유동인구증감 = 행.get("오후_유동인구_YoY_%")

    if (
        pd.notna(유동인구증감)
        and 유동인구증감 <= -7.92
    ):
        보조태그.append(
            "[상권 유입 감소] 피크시간 운영 확인"
        )

    if 보조태그:
        보조상황 = " / ".join(보조태그[:2])
    elif 위험상태 == "[안정]":
        보조상황 = "[개선 확인] 매출과 거래건수 모두 증가"
    elif 위험수준 == "낮음":
        보조상황 = "[정기 관찰] 다음 분기 변화 확인"
    else:
        보조상황 = "[현장 확인] 운영 상태와 점주 의견 확인"

    return pd.Series(
        {
            "위험_상태_태그": 위험상태,
            "주요_원인_태그": 관측신호,
            "권장_조치": 권장조치,
            "보조_상황_태그": 보조상황,
        }
    )


전체_df[
    [
        "위험_상태_태그",
        "주요_원인_태그",
        "권장_조치",
        "보조_상황_태그",
    ]
] = 전체_df.apply(
    상세진단_생성,
    axis=1,
)

# 공통 계산
전체_df["당월_매출_금액"] = pd.to_numeric(
    전체_df["당월_매출_금액"],
    errors="coerce",
)

전체_분기_상권_수 = len(
    전체_원본_df.loc[
        전체_원본_df["기준_년분기_코드"] == 기준_분기
    ]
)

위험점수_산정_수 = len(전체_df)

위험점수_기준 = 전체_df[
    "2차_위험신호지수"
].quantile(0.75)

매출액_중앙값 = 전체_df[
    "당월_매출_금액"
].median()

위험상위25_df = 전체_df.loc[
    전체_df["2차_위험신호지수"] >= 위험점수_기준
].copy()

위험상위25_수 = len(위험상위25_df)

관리_후보_df = 위험상위25_df.loc[
    위험상위25_df["당월_매출_금액"] >= 매출액_중앙값
].copy()

관리_후보_수 = len(관리_후보_df)

타격액_합계 = df[
    "상권_10%_하락_시나리오_타격액"
].sum()

평균_위험점수 = df[
    "2차_위험신호지수"
].mean()

예측_분기_열 = next(
    col for col in df.columns
    if "예측" in col and "분기" in col
)

예측_분기코드 = str(
    int(float(df[예측_분기_열].iloc[0]))
)

예측_분기 = (
    f"{예측_분기코드[:4]} "
    f"Q{예측_분기코드[4]}"
)


# 공통 제목
st.markdown(
    f"""
<div class="simple-header">
<div>
<h1 class="simple-title">골목상권 <span class="highlight">매출 하락</span> 조기경보</h1>
<p class="simple-description">프랜차이즈 본사 슈퍼바이저용 상권 우선관리 대시보드</p>
</div>
<div class="simple-period">
예측 대상 분기
<strong>{예측_분기}</strong>
</div>
</div>
""",
    unsafe_allow_html=True,
)

# 지도에서 선택한 상권을 상세페이지로 전달
# 지도에서 클릭한 상권 저장
def 지도_상권_클릭():
    지도상태 = st.session_state.get("상권_지도")

    if 지도상태 is None:
        return

    선택목록 = 지도상태.selection.objects.get(
        "risk-points",
        [],
    )

    if not 선택목록:
        return

    st.session_state["지도_선택_상권"] = (
        선택목록[0]["상권_코드_명"]
    )


# 오른쪽 버튼으로 상세페이지 이동
def 선택상권_상세이동():
    선택상권명 = st.session_state.get(
        "지도_선택_상권"
    )

    if not 선택상권명:
        return

    st.session_state["상세_상권_선택"] = 선택상권명
    st.session_state["페이지_메뉴"] = "상권 상세 분석"

메뉴_옵션 = [
    "상권 상세 분석",
    "종합 현황",
    "우선관리 상권",
]

# 기존 아이콘 메뉴값이 남아 있으면 상세 화면으로 초기화
if st.session_state.get("페이지_메뉴") not in 메뉴_옵션:
    st.session_state["페이지_메뉴"] = "상권 상세 분석"

with st.sidebar:
    st.markdown("## 상권 위험 관리")
    st.caption(f"{예측_분기} · 서울 골목상권 커피·음료")
    st.divider()

    메뉴 = st.radio(
        "화면 이동",
        options=메뉴_옵션,
        key="페이지_메뉴",
    )

    st.divider()
    st.caption(
        "위험점수는 하락 확률이 아니라 "
        "관리 우선순위를 위한 상대 점수입니다."
    )

    if True:  # 스크롤형 화면 전환을 위해 항상 준비
        st.divider()
        st.markdown("### 상권 찾기")

        검색용_df = 전체_df.sort_values(
            "상권_코드_명"
        ).reset_index(drop=True)

        상권목록 = 검색용_df["상권_코드_명"].tolist()

        if (
            st.session_state.get("상세_상권_선택")
            not in 상권목록
        ):
            st.session_state["상세_상권_선택"] = 상권목록[0]

        선택_상권명 = st.selectbox(
            "상권명 검색",
            options=상권목록,
            key="상세_상권_선택",
        )

        st.caption(
            f"전체 {len(검색용_df):,}개 상권을 검색할 수 있습니다."
        )


# 1. 대시보드 홈
def 슬라이드_제목(번호, 제목, 설명):
    st.markdown(
        f"""
        <div class="slide-heading">
            <div class="slide-number">{번호}</div>
            <div class="slide-main-title">{제목}</div>
            <div class="slide-description">{설명}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with st.container(key="slide_overview"):
    슬라이드_제목(
        "02",
        "종합 현황",
        "서울 골목상권의 전체 위험 분포와 관리 현황",
    )

    요약영역, 위험현황영역 = st.columns(
        [0.74, 2.40],
        gap="large",
    )
    
with 요약영역:
    st.subheader(f"{예측_분기} 관리 현황")

    st.markdown(
    f"""
<div class="kpi-grid">
<div class="kpi-card">
<div class="kpi-label">선정 조건 충족 상권</div>
<div class="kpi-value">{관리_후보_수}<span class="kpi-unit">곳</span></div>
<div class="kpi-note">위험 상위 25% · 매출액 중앙값 이상</div>
</div>

<div class="kpi-card">
<div class="kpi-label">최종 우선관리 상권</div>
<div class="kpi-value">{len(df)}<span class="kpi-unit">곳</span></div>
<div class="kpi-note">매출 영향 규모를 반영한 TOP 5</div>
</div>

<div class="kpi-card impact">
<div class="kpi-label">TOP 5 시나리오 타격액</div>
<div class="kpi-value">{타격액_합계 / 100_000_000:.2f}<span class="kpi-unit">억원</span></div>
<div class="kpi-note">현재 매출의 10% 하락 가정</div>
</div>

<div class="kpi-card risk">
<div class="kpi-label">TOP 5 평균 위험점수</div>
<div class="kpi-value">{평균_위험점수:.1f}<span class="kpi-unit">점</span></div>
<div class="kpi-note">2차 위험신호지수 기준</div>
</div>
</div>
""",
    unsafe_allow_html=True,
)

    st.caption(
        f"선정 과정: 해당 분기 {전체_분기_상권_수:,}곳"
        f" → 위험점수 산정 {위험점수_산정_수:,}곳"
        f" → 위험 상위 25% {위험상위25_수:,}곳"
        f" → 매출액 중앙값 이상 {관리_후보_수:,}곳"
        f" → 최종 TOP {len(df)}"
    )

    st.subheader("전체 상권 위험도 현황")
    
    st.markdown(
        f"""
<div style="border:1px solid #E1E1E1;border-left:4px solid #BF0404;border-radius:10px;padding:14px 16px;background:#FAFAFA;margin:4px 0 0 0;">
<div style="color:#111111;font-size:14px;font-weight:800;margin-bottom:8px;">같은 ‘매우 높음’인데 왜 TOP 5가 따로 있나요?</div>
<div style="color:#444444;font-size:13px;line-height:1.8;">
<span style="display:inline-block;min-width:110px;color:#BF0404;font-weight:800;">위험수준</span>매출 하락 신호가 얼마나 강한지를 나타냅니다.<br>
<span style="display:inline-block;min-width:110px;color:#111111;font-weight:800;">TOP 5 우선관리</span>위험 상위 25%이면서 매출액 중앙값 이상인 {관리_후보_수:,}곳 중, 매출 10% 하락 시 타격액이 큰 5곳입니다.
</div>
</div>
""",
        unsafe_allow_html=True,
    )

with 위험현황영역:
    
    좌표_df = load_commercial_area_coordinates()

    지도_df = 전체_df.copy()

    지도_df["상권_코드"] = pd.to_numeric(
        지도_df["상권_코드"],
        errors="coerce",
    ).astype("Int64")

    지도_df = 지도_df.merge(
        좌표_df,
        on="상권_코드",
        how="left",
    )

    지도_df = 지도_df.dropna(
        subset=["위도", "경도"]
    ).copy()

    # 최종 TOP 5의 관리 순위 연결
    top5_순위_df = df[
        ["상권_코드", "관리_순위"]
    ].copy()

    top5_순위_df["상권_코드"] = pd.to_numeric(
        top5_순위_df["상권_코드"],
        errors="coerce",
    ).astype("Int64")

    지도_df = 지도_df.merge(
        top5_순위_df,
        on="상권_코드",
        how="left",
    )

    지도_df["TOP5여부"] = (
        지도_df["관리_순위"].notna()
    )

    # 위험수준별 지도 색상
    위험색상 = {
        "매우 높음": [191, 4, 4, 235],
        "높음": [232, 105, 38, 230],
        "보통": [222, 174, 48, 220],
        "낮음": [54, 139, 121, 210],
    }

    지도_df["표시색상"] = (
        지도_df["2차_위험신호_구간"]
        .map(위험색상)
    )

    # 경고등 바깥 후광
    # 단계별 후광 색상
    지도_df["후광색상_바깥"] = 지도_df["표시색상"].apply(
        lambda 색상: [색상[0], 색상[1], 색상[2], 12]
    )

    지도_df["후광색상_중간"] = 지도_df["표시색상"].apply(
        lambda 색상: [색상[0], 색상[1], 색상[2], 25]
    )

    지도_df["후광색상_안쪽"] = 지도_df["표시색상"].apply(
        lambda 색상: [색상[0], 색상[1], 색상[2], 48]
    )


    # 위험도 분포표
    위험순서 = [
        "매우 높음",
        "높음",
        "보통",
        "낮음",
    ]

    위험도_분포 = (
        지도_df["2차_위험신호_구간"]
        .value_counts()
        .reindex(
            위험순서,
            fill_value=0,
        )
        .rename_axis("위험수준")
        .reset_index(name="상권수")
    )

    위험도_분포["비율(%)"] = (
        위험도_분포["상권수"]
        .div(len(지도_df))
        .mul(100)
        .round(1)
    )

    전체행 = pd.DataFrame(
        {
            "위험수준": ["전체"],
            "상권수": [len(지도_df)],
            "비율(%)": [100.0],
        }
    )

    위험도_분포 = pd.concat(
        [전체행, 위험도_분포],
        ignore_index=True,
    )

    지도영역, 분포영역 = st.columns(
        [2.7, 1.25],
        gap="large",
    )

    # 오른쪽 위험도 분포표
    with 분포영역:
        st.markdown("#### 선택 상권")

        지도_선택_상권명 = st.session_state.get(
            "지도_선택_상권"
        )

        if 지도_선택_상권명:
            지도_선택결과 = 지도_df.loc[
                지도_df["상권_코드_명"]
                == 지도_선택_상권명
            ]

        else:
            지도_선택결과 = pd.DataFrame()

        if not 지도_선택결과.empty:
            지도_선택행 = 지도_선택결과.iloc[0]

            if pd.notna(지도_선택행["관리_순위"]):
                관리문구 = (
                    f"우선관리 순위 "
                    f"{int(지도_선택행['관리_순위'])}위"
                )
            else:
                관리문구 = "위험도 모니터링"

            st.markdown(
                f"""
<div style="border:1px solid #D9D9D9;border-left:4px solid #BF0404;border-radius:10px;padding:13px 14px;background:#FFFFFF;box-shadow:0 4px 14px rgba(0,0,0,0.06);margin-bottom:9px;">
<div style="color:#BF0404;font-size:11px;font-weight:700;margin-bottom:5px;">{관리문구}</div>
<div style="color:#111111;font-size:15px;font-weight:700;line-height:1.35;margin-bottom:11px;">{지도_선택행['상권_코드_명']}</div>
<div style="display:grid;grid-template-columns:1fr auto;gap:6px 10px;font-size:12px;">
<span style="color:#777777;">전체 위험점수 순위</span>
<strong>{int(지도_선택행['전체_위험순위']):,}위</strong>
<span style="color:#777777;">위험점수</span>
<strong>{지도_선택행['2차_위험신호지수']:.1f}점</strong>
<span style="color:#777777;">위험수준</span>
<strong style="color:#BF0404;">{지도_선택행['2차_위험신호_구간']}</strong>
</div>
</div>
""",
                unsafe_allow_html=True,
            )

            st.button(
                "상세 분석 보기",
                key="선택상권_상세보기",
                width="stretch",
                on_click=선택상권_상세이동,
            )

        else:
            st.markdown(
                """
<div style="
    border: 1px dashed #CCCCCC;
    border-radius: 10px;
    padding: 18px 12px;
    color: #777777;
    font-size: 12px;
    text-align: center;
    background: #FAFAFA;
">
    지도에서 상권을 선택하세요.
</div>
""",
                unsafe_allow_html=True,
            )

        st.markdown("#### 위험도 분포")

        위험도_선택표 = 위험도_분포.copy()

        위험도_선택표["위험도"] = (
            위험도_선택표.apply(
                lambda 행: (
                    f"{행['위험수준']} · "
                    f"{int(행['상권수']):,}개 · "
                    f"{행['비율(%)']:.1f}%"
                ),
                axis=1,
            )
        )

        위험도_선택표 = 위험도_선택표[
            ["위험도"]
        ]

        선택결과 = st.dataframe(
            위험도_선택표,
            width="stretch",
            hide_index=True,
            height=280,
            row_height=45,
            on_select="rerun",
            selection_mode="single-row",
            key="위험도_분포표",
            column_config={
                "위험도": st.column_config.TextColumn(
                    "위험수준 · 상권수 · 비율",
                    width="large",
                ),
            },
        )

        선택된_행 = 선택결과.selection.rows

        if 선택된_행:
            선택_위험수준 = 위험도_분포.iloc[
                선택된_행[0]
            ]["위험수준"]
        else:
            선택_위험수준 = "매우 높음"

        st.caption(
            "표의 행을 클릭하면 해당 위험수준만 "
            "지도에 표시됩니다."
        )

        st.markdown(
            f"**현재 표시:** {선택_위험수준}"
        )

    # 선택 위험수준에 맞춰 지도 필터링
    if 선택_위험수준 == "전체":
        필터_지도_df = 지도_df.copy()
    else:
        필터_지도_df = 지도_df.loc[
            지도_df["2차_위험신호_구간"]
            == 선택_위험수준
        ].copy()

    # 지도 설명창 표시용 데이터
    필터_지도_df["위험점수_표시"] = (
        pd.to_numeric(
            필터_지도_df["2차_위험신호지수"],
            errors="coerce",
        )
        .round(1)
        .map(lambda 값: f"{값:.1f}점")
    )

    필터_지도_df["위험순위_표시"] = (
        필터_지도_df["전체_위험순위"]
        .astype(int)
        .map(lambda 값: f"{값:,}위")
    )

    필터_지도_df["관리구분"] = (
        필터_지도_df["TOP5여부"]
        .map(
            {
                True: "TOP 5 우선관리",
                False: "위험도 모니터링",
            }
        )
    )

    # 전체 화면은 TOP 5, 필터 화면은 위험순위 상위 8개 라벨
    def 지도용_상권명(상권명):
        상권명 = str(상권명)

        if len(상권명) <= 10:
            return 상권명

        return 상권명[:10] + "…"

    # 지도에서 선택된 상권
    선택된_상권명 = st.session_state.get(
        "지도_선택_상권"
    )

    if 선택된_상권명:
        선택_지도_df = 필터_지도_df.loc[
            필터_지도_df["상권_코드_명"]
            == 선택된_상권명
        ].copy()
    else:
        선택_지도_df = 필터_지도_df.head(0).copy()
        
    if 선택_위험수준 == "전체":
        라벨_df = 필터_지도_df.loc[
            필터_지도_df["TOP5여부"]
        ].copy()

        라벨_df["지도라벨"] = 라벨_df.apply(
            lambda 행:
            f"{int(행['관리_순위'])}위 "
            f"{지도용_상권명(행['상권_코드_명'])}",
            axis=1,
        )

    else:
        라벨_df = (
            필터_지도_df
            .nsmallest(
                8,
                "전체_위험순위",
            )
            .copy()
        )

        라벨_df["지도라벨"] = 라벨_df.apply(
            lambda 행:
            f"{int(행['전체_위험순위'])}위 "
            f"{지도용_상권명(행['상권_코드_명'])}",
            axis=1,
        )

    # 일반 상권 그라데이션 후광
    후광_바깥레이어 = pdk.Layer(
        "ScatterplotLayer",
        id="risk-halo-outer",
        data=필터_지도_df,
        get_position="[경도, 위도]",
        get_fill_color="후광색상_바깥",
        get_radius=1,
        radius_min_pixels=10,
        radius_max_pixels=10,
        stroked=False,
        pickable=False,
    )

    후광_중간레이어 = pdk.Layer(
        "ScatterplotLayer",
        id="risk-halo-middle",
        data=필터_지도_df,
        get_position="[경도, 위도]",
        get_fill_color="후광색상_중간",
        get_radius=1,
        radius_min_pixels=8,
        radius_max_pixels=8,
        stroked=False,
        pickable=False,
    )

    후광_안쪽레이어 = pdk.Layer(
        "ScatterplotLayer",
        id="risk-halo-inner",
        data=필터_지도_df,
        get_position="[경도, 위도]",
        get_fill_color="후광색상_안쪽",
        get_radius=1,
        radius_min_pixels=6,
        radius_max_pixels=6,
        stroked=False,
        pickable=False,
    )

    # 일반 상권은 작고 단정한 점으로 표시
    기본상권레이어 = pdk.Layer(
        "ScatterplotLayer",
        id="risk-points",
        data=필터_지도_df,
        get_position="[경도, 위도]",
        get_fill_color="표시색상",
        get_radius=1,
        radius_min_pixels=4,
        radius_max_pixels=4,
        stroked=False,
        pickable=True,
        auto_highlight=True,
    )

    # 현재 필터에 포함된 TOP 5
    TOP5_지도_df = 필터_지도_df.loc[
        필터_지도_df["TOP5여부"]
    ].copy()

    TOP5_지도_df["관리번호"] = (
        TOP5_지도_df["관리_순위"]
        .astype(int)
        .astype(str)
    )

    # TOP5 전용 강조 후광
    # TOP5 그라데이션 후광
    TOP5_후광_바깥레이어 = pdk.Layer(
        "ScatterplotLayer",
        id="top5-halo-outer",
        data=TOP5_지도_df,
        get_position="[경도, 위도]",
        get_fill_color=[191, 4, 4, 15],
        get_radius=1,
        radius_min_pixels=19,
        radius_max_pixels=19,
        stroked=False,
        pickable=False,
    )

    TOP5_후광_중간레이어 = pdk.Layer(
        "ScatterplotLayer",
        id="top5-halo-middle",
        data=TOP5_지도_df,
        get_position="[경도, 위도]",
        get_fill_color=[191, 4, 4, 30],
        get_radius=1,
        radius_min_pixels=16,
        radius_max_pixels=16,
        stroked=False,
        pickable=False,
    )

    TOP5_후광_안쪽레이어 = pdk.Layer(
        "ScatterplotLayer",
        id="top5-halo-inner",
        data=TOP5_지도_df,
        get_position="[경도, 위도]",
        get_fill_color=[191, 4, 4, 55],
        get_radius=1,
        radius_min_pixels=13,
        radius_max_pixels=13,
        stroked=False,
        pickable=False,
    )

    # TOP 5 빨간 중심 표시
    TOP5_중심레이어 = pdk.Layer(
        "ScatterplotLayer",
        id="top5-center",
        data=TOP5_지도_df,
        get_position="[경도, 위도]",
        get_fill_color=[191, 4, 4, 255],
        get_radius=1,
        radius_min_pixels=11,
        radius_max_pixels=11,
        stroked=False,
        pickable=False,
    )

    # TOP 5 순위 숫자
        # 숫자를 세 번 겹쳐 굵게 표현
    TOP5_번호왼쪽레이어 = pdk.Layer(
        "TextLayer",
        id="top5-number-left",
        data=TOP5_지도_df,
        get_position="[경도, 위도]",
        get_text="관리번호",
        get_size=16,
        get_color=[255, 255, 255, 255],
        get_text_anchor="'middle'",
        get_alignment_baseline="'center'",
        get_pixel_offset=[-0.7, 0],
        pickable=False,
    )

    TOP5_번호레이어 = pdk.Layer(
        "TextLayer",
        id="top5-number-center",
        data=TOP5_지도_df,
        get_position="[경도, 위도]",
        get_text="관리번호",
        get_size=16,
        get_color=[255, 255, 255, 255],
        get_text_anchor="'middle'",
        get_alignment_baseline="'center'",
        get_pixel_offset=[0, 0],
        pickable=False,
    )

    TOP5_번호오른쪽레이어 = pdk.Layer(
        "TextLayer",
        id="top5-number-right",
        data=TOP5_지도_df,
        get_position="[경도, 위도]",
        get_text="관리번호",
        get_size=16,
        get_color=[255, 255, 255, 255],
        get_text_anchor="'middle'",
        get_alignment_baseline="'center'",
        get_pixel_offset=[0.7, 0],
        pickable=False,
    )

    # 선택 지점 흰색 외곽 링
    선택_외곽레이어 = pdk.Layer(
        "ScatterplotLayer",
        id="selected-point-outer",
        data=선택_지도_df,
        get_position="[경도, 위도]",
        get_fill_color=[255, 255, 255, 0],
        get_radius=1,
        radius_min_pixels=20,
        radius_max_pixels=20,
        stroked=True,
        get_line_color=[255, 255, 255, 255],
        line_width_min_pixels=5,
        pickable=False,
    )

    # 선택 지점 빨간 강조 링
    선택_링레이어 = pdk.Layer(
        "ScatterplotLayer",
        id="selected-point-ring",
        data=선택_지도_df,
        get_position="[경도, 위도]",
        get_fill_color=[255, 255, 255, 0],
        get_radius=1,
        radius_min_pixels=18,
        radius_max_pixels=18,
        stroked=True,
        get_line_color=[191, 4, 4, 255],
        line_width_min_pixels=3,
        pickable=False,
    )
    # 위험도가 매우 높은 상권에 경고 표시
    긴급경고_df = 필터_지도_df.loc[
        필터_지도_df["2차_위험신호_구간"]
        == "매우 높음"
    ].copy()

    경고문자레이어 = pdk.Layer(
        "TextLayer",
        data=긴급경고_df,
        get_position="[경도, 위도]",
        get_text="'!'",
        get_size=10,
        get_color=[255, 255, 255, 255],
        get_text_anchor="'middle'",
        get_alignment_baseline="'center'",
        pickable=False,
    )

    # 주요 상권 이름
    라벨레이어 = pdk.Layer(
        "TextLayer",
        id="area-labels",
        data=라벨_df,
        get_position="[경도, 위도]",
        get_text="지도라벨",
        get_size=13,
        get_color=[17, 17, 17, 255],
        get_text_anchor="'middle'",
        get_alignment_baseline="'bottom'",
        get_pixel_offset=[0, -15],
        pickable=False,
    )

    지도중심 = pdk.ViewState(
        latitude=float(
            필터_지도_df["위도"].mean()
        ),
        longitude=float(
            필터_지도_df["경도"].mean()
        ),
        zoom=10.2,
        pitch=0,
    )

    지도 = pdk.Deck(
        map_style=(
            "https://basemaps.cartocdn.com/gl/"
            "voyager-gl-style/style.json"
        ),
        initial_view_state=지도중심,
        layers=[
            후광_바깥레이어,
            후광_중간레이어,
            후광_안쪽레이어,
            기본상권레이어,

            TOP5_후광_바깥레이어,
            TOP5_후광_중간레이어,
            TOP5_후광_안쪽레이어,
            TOP5_중심레이어,

            TOP5_번호왼쪽레이어,
            TOP5_번호레이어,
            TOP5_번호오른쪽레이어,

            선택_외곽레이어,
            선택_링레이어,
            라벨레이어,
        ],
        
    )

    # 왼쪽 지도
    with 지도영역:
        st.markdown("#### 서울 골목상권 위험 분포")

        st.pydeck_chart(
            지도,
            width="stretch",
            height=550,
            key="상권_지도",
            on_select=지도_상권_클릭,
            selection_mode="single-object",
        )

        st.caption(
            f"현재 지도에 "
            f"{len(필터_지도_df):,}개 상권을 "
            "표시하고 있습니다."
        )
# 2. 우선관리 TOP 5
with st.container(key="slide_priority"):
    슬라이드_제목(
        "03",
        "우선관리 상권",
        "위험도와 예상 타격액을 함께 고려한 관리 우선순위",
    )

    st.subheader(f"{예측_분기} 우선관리 TOP 5")

    st.caption(
        f"가장 위험한 5곳이 아니라, 선정 조건을 충족한 "
        f"{관리_후보_수:,}곳 중 매출 하락 시 예상 손실이 큰 5곳입니다."
    )


    # 차트용 데이터
    차트_df = df[
        [
            "관리_순위",
            "상권_코드_명",
            "2차_위험신호지수",
            "상권_10%_하락_시나리오_타격액",
        ]
    ].copy()

    차트_df = 차트_df.rename(
        columns={
            "관리_순위": "관리순위",
            "상권_코드_명": "상권명",
            "2차_위험신호지수": "위험점수",
            "상권_10%_하락_시나리오_타격액":
                "시나리오 타격액",
        }
    )

    차트_df["시나리오 타격액(억원)"] = (
        차트_df["시나리오 타격액"]
        / 100_000_000
    )

    최대_타격액 = (
        차트_df["시나리오 타격액(억원)"].max()
    )

    차트_df["차트용 상권명"] = (
    차트_df["상권명"]
    .apply(
        lambda 이름:
        이름 if len(이름) <= 11
        else 이름[:11] + "…"
    )
)

    left, right = st.columns([0.9, 1.4])

    # 왼쪽 그래프
    with left:
        st.markdown("#### 10% 하락 시나리오 영향 규모")
        st.caption(
            f"선정 조건을 충족한 {관리_후보_수:,}곳 중 "
            "매출 10% 하락 시 타격액이 큰 순서입니다."
        )

        막대 = (
            alt.Chart(차트_df)
            .mark_bar(
                cornerRadiusEnd=4,
                size=19,
)
            .encode(
                y=alt.Y(
                    "차트용 상권명:N",
                    sort=alt.SortField(
                        field="관리순위",
                        order="ascending",
                    ),
                    title=None,
                    axis=alt.Axis(
                        labelLimit=155,
                        labelFontSize=12,
                        grid=True,
                        gridColor="#E5E5E5",
                        gridWidth=1,
                        tickBand="extent",
                        ticks=False,
                        domain=False,
                    ),
                ),
                x=alt.X(
                    "시나리오 타격액(억원):Q",
                    title="10% 시나리오 타격액(억원)",
                    scale=alt.Scale(
                        domain=[
                            0,
                            최대_타격액 * 1.18,
                        ]
                    ),
                    axis=alt.Axis(
                        grid=True,
                        tickCount=4,
                    ),
                ),
                color=alt.Color(
                    "관리순위:O",
                    scale=alt.Scale(
                        domain=[1, 2, 3, 4, 5],
                        range=[
                          "#8D0000",
                          "#AB1717",
                          "#C64343",
                          "#D87575",
                          "#E5A3A3",
                        ],
                    ),
                    legend=None,
                ),
                tooltip=[
                    alt.Tooltip(
                        "관리순위:Q",
                        title="우선관리 순위",
                    ),
                    alt.Tooltip(
                        "상권명:N",
                        title="상권명",
                    ),
                    alt.Tooltip(
                        "위험점수:Q",
                        title="위험점수",
                        format=".1f",
                    ),
                    alt.Tooltip(
                        "시나리오 타격액(억원):Q",
                        title="타격액",
                        format=".2f",
                    ),
                ],
            )
        )

        금액표시 = 막대.mark_text(
            align="left",
            baseline="middle",
            dx=5,
            color="#111111",
            fontSize=11,
        ).encode(
            text=alt.Text(
                "시나리오 타격액(억원):Q",
                format=".2f",
            )
        )

        st.altair_chart(
            막대 + 금액표시,
            width="stretch",
        )

    # 오른쪽 TOP 5 표
    with right:
        st.markdown("#### 전체 상권 위험점수 순위")
        st.caption(
            f"전체 {위험점수_산정_수:,}곳을 위험점수만으로 정렬한 순위입니다. "
            f"왼쪽 TOP 5는 후보 {관리_후보_수:,}곳 중 "
            "시나리오 타격액이 큰 순서입니다."
        )

        검색어 = st.text_input(
            "상권 검색",
            placeholder="상권명을 입력하세요",
            label_visibility="collapsed",
            key="전체_순위_검색",
        )

        전체_순위표 = 전체_df[
            [
                "전체_위험순위",
                "상권_코드_명",
                "2차_위험신호지수",
                "2차_위험신호_구간",
            ]
        ].copy()

        전체_순위표[
            "2차_위험신호지수"
        ] = 전체_순위표[
            "2차_위험신호지수"
        ].round(1)

        전체_순위표 = 전체_순위표.rename(
            columns={
                "전체_위험순위": "순위",
                "상권_코드_명": "상권명",
                "2차_위험신호지수": "위험점수",
                "2차_위험신호_구간": "위험수준",
            }
        )

        if 검색어:
            전체_순위표 = 전체_순위표.loc[
                전체_순위표["상권명"]
                .str.contains(
                    검색어,
                    case=False,
                    na=False,
                    regex=False,
                )
            ]

        st.dataframe(
            전체_순위표,
            width="stretch",
            hide_index=True,
            height=330,
            column_config={
                "순위": st.column_config.NumberColumn(
                    width="small",
                    format="%d",
                ),
                "상권명": st.column_config.TextColumn(
                    width="medium",
                ),
                "위험점수": st.column_config.NumberColumn(
                    width="small",
                    format="%.1f",
                ),
                "위험수준": st.column_config.TextColumn(
                    width="small",
                ),
            },
        )

    st.caption(
        "시나리오 타격액은 예측액이 아니라 현재 매출의 "
        "10% 하락을 가정한 관리 우선순위 참고 금액입니다."
    )


# 3. 상권 상세
with st.container(key="slide_detail"):
    슬라이드_제목(
        "01",
        "상권 상세 분석",
        "선택한 상권의 위험 신호와 슈퍼바이저 권장 조치",
    )

    st.subheader("선택 상권 상세")

    선택행 = 검색용_df.loc[
        검색용_df["상권_코드_명"] == 선택_상권명
    ].iloc[0]

    def 퍼센트_표시(열이름):
        값 = 선택행.get(열이름)

        if pd.isna(값):
            return "-"

        return f"{float(값):+.1f}%"

    def 텍스트_표시(열이름):
        값 = 선택행.get(열이름)

        if pd.isna(값):
            return "정보 없음"

        return str(값)

    st.markdown(
        f"### {선택_상권명} "
        f"— 위험점수 "
        f"{선택행['2차_위험신호지수']:.1f}점"
    )
    선택_TOP5행 = df.loc[
        df["상권_코드_명"] == 선택_상권명
    ]

    if not 선택_TOP5행.empty:
        우선관리_문구 = (
            f" · 우선관리 순위 "
            f"{int(선택_TOP5행['관리_순위'].iloc[0])}위"
        )
    else:
        우선관리_문구 = ""

    st.caption(
        f"전체 위험점수 순위 "
        f"{int(선택행['전체_위험순위']):,}위"
        f"{우선관리_문구} · "
        f"위험 수준 {텍스트_표시('2차_위험신호_구간')}"
    )

    detail1, detail2, detail3, detail4 = st.columns(4)

    detail1.metric(
        "현재 매출 YoY",
        퍼센트_표시("현재_매출_YoY_%"),
    )

    detail2.metric(
        "매출건수 YoY",
        퍼센트_표시("현재_매출건수_YoY_%"),
    )

    detail3.metric(
        "추정 객단가 YoY",
        퍼센트_표시("추정_객단가_YoY_%"),
    )

    detail4.metric(
        "오후 유동인구 YoY",
        퍼센트_표시("오후_유동인구_YoY_%"),
    )

    left, right = st.columns(2)

    with left:
        st.markdown("#### 위험 신호 해석")

        st.write(
            "**위험 상태:**",
            텍스트_표시("위험_상태_태그"),
        )

        st.write(
            "**관측 신호:**",
            텍스트_표시("주요_원인_태그"),
        )

        st.write(
            "**추가 확인:**",
            텍스트_표시("보조_상황_태그"),
        )

    with right:
        st.markdown("#### 슈퍼바이저 권장 조치")

        권장_조치_내용 = 텍스트_표시("권장_조치")

        st.markdown(
            f"""
<div class="action-card">
{권장_조치_내용}
</div>
""",
            unsafe_allow_html=True,
        )


    # 공통 하단 안내
    st.markdown(
        """
<div style="
    margin-top: 22px;
    padding-top: 14px;
    border-top: 1px solid #E5E5E5;
    color: #777777;
    font-size: 12px;
">
본 결과는 상권 단위 위험 선별 결과이며, 개별 가맹점의 매출 예측이 아닙니다.
</div>
""",
        unsafe_allow_html=True,
    )
