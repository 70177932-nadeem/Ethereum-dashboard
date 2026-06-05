"""
ETH-USD Data Visualization Dashboard
Course : Exploratory Data Analysis
Instructor : Ali Hassan Sherazi
"""

import streamlit as st
import pandas as pd
import numpy as np
from filters import load_data, apply_filters, kpi_summary
from charts import (
    fig_line_chart, fig_area_chart, fig_bar_chart,
    fig_histogram, fig_scatter_plot, fig_box_plot,
    fig_pie_chart, fig_heatmap, fig_count_plot, fig_violin_plot,
)

st.set_page_config(
    page_title="ETH-USD Dashboard",
    page_icon="⟠",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700;800&family=DM+Mono:wght@400;500&display=swap');

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    background-color: #F4F7FE;
    color: #1B2559;
}
.stApp { background-color: #F4F7FE; }
* { box-sizing: border-box; }

/* ── Sidebar ── */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0B1437 0%, #111C44 100%) !important;
    border-right: none !important;
    width: 250px !important;
}
section[data-testid="stSidebar"] > div { padding-top: 0 !important; }
section[data-testid="stSidebar"] * { color: #A3AED0 !important; font-family: 'DM Sans', sans-serif !important; }
section[data-testid="stSidebar"] h1,
section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3 { color: #ffffff !important; }

/* ── Sidebar brand ── */
.sidebar-brand {
    display: flex; align-items: center; gap: 10px;
    padding: 26px 20px 20px;
    border-bottom: 1px solid rgba(255,255,255,0.07);
    margin-bottom: 16px;
}
.brand-icon {
    width: 40px; height: 40px; border-radius: 12px;
    background: linear-gradient(135deg, #4318FF, #868CFF);
    display: flex; align-items: center; justify-content: center;
    font-size: 20px; flex-shrink: 0;
    box-shadow: 0 4px 15px rgba(67,24,255,0.4);
}
.brand-name { color: #ffffff !important; font-size: 20px; font-weight: 800; letter-spacing: -0.5px; }
.brand-sub  { color: #A3AED0 !important; font-size: 10px; font-weight: 500; letter-spacing: 1px; text-transform: uppercase; }

/* ── Nav ── */
.nav-section { padding: 0 12px; margin-bottom: 6px; }
.nav-label {
    font-size: 10px; font-weight: 700; text-transform: uppercase;
    letter-spacing: 1.5px; color: #3D4A6B !important;
    padding: 8px 8px 4px; display: block;
}
.nav-item {
    display: flex; align-items: center; gap: 10px;
    padding: 10px 12px; border-radius: 12px;
    color: #6B7DB3 !important; font-size: 13px; font-weight: 600;
    margin-bottom: 3px; cursor: pointer; transition: all 0.15s;
}
.nav-item:hover { background: rgba(255,255,255,0.06); color: #e2e8f0 !important; }
.nav-item.active {
    background: linear-gradient(135deg, rgba(67,24,255,0.25), rgba(67,24,255,0.10));
    color: #ffffff !important;
    border-left: 3px solid #4318FF;
}
.nav-icon { font-size: 15px; width: 22px; text-align: center; }

/* ── Filter header ── */
.filter-header {
    font-size: 10px; font-weight: 700; text-transform: uppercase;
    letter-spacing: 1.5px; color: #3D4A6B !important;
    padding: 16px 20px 8px; border-top: 1px solid rgba(255,255,255,0.06); margin-top: 8px;
}
.filter-label {
    font-size: 12px; font-weight: 600; color: #A3AED0 !important;
    padding: 0 20px 4px; display: block;
}

/* ── Sidebar widgets ── */
section[data-testid="stSidebar"] input {
    background: rgba(255,255,255,0.07) !important;
    color: #e2e8f0 !important;
    border: 1px solid rgba(255,255,255,0.10) !important;
    border-radius: 10px !important; font-size: 12px !important;
}
section[data-testid="stSidebar"] .stButton button {
    background: linear-gradient(135deg, rgba(67,24,255,0.25), rgba(67,24,255,0.15)) !important;
    color: #868CFF !important;
    border: 1px solid rgba(67,24,255,0.35) !important;
    border-radius: 12px !important; font-size: 12px !important; font-weight: 700 !important;
    transition: all 0.2s !important;
}
section[data-testid="stSidebar"] .stButton button:hover {
    background: linear-gradient(135deg, rgba(67,24,255,0.4), rgba(67,24,255,0.25)) !important;
    color: #ffffff !important;
}

/* ── Topbar ── */
.topbar {
    display: flex; align-items: center; justify-content: space-between;
    padding: 22px 4px 18px;
    border-bottom: 1px solid #E9EDF7;
    margin-bottom: 26px;
}
.topbar-title { font-size: 24px; font-weight: 800; color: #1B2559; letter-spacing: -0.5px; }
.topbar-sub   { font-size: 13px; color: #A3AED0; font-weight: 500; margin-top: 2px; }
.topbar-right { display: flex; align-items: center; gap: 10px; }
.topbar-badge {
    background: white; border-radius: 12px; padding: 8px 16px;
    font-size: 12px; font-weight: 700; color: #4318FF;
    border: 1px solid #E9EDF7; box-shadow: 0 2px 6px rgba(0,0,0,0.05);
}
.topbar-record {
    background: linear-gradient(135deg, #4318FF, #868CFF);
    color: white; border-radius: 12px; padding: 8px 16px;
    font-size: 12px; font-weight: 700;
    box-shadow: 0 4px 12px rgba(67,24,255,0.35);
}

/* ── KPI Cards ── */
.kpi-card {
    background: white; border-radius: 20px;
    padding: 20px 22px;
    box-shadow: 0 2px 10px rgba(112,144,176,0.12);
    border: 1px solid #F0F3FF;
    position: relative; overflow: hidden;
    transition: transform 0.2s, box-shadow 0.2s;
}
.kpi-card:hover { transform: translateY(-3px); box-shadow: 0 8px 24px rgba(112,144,176,0.20); }
.kpi-icon {
    width: 42px; height: 42px; border-radius: 12px;
    display: flex; align-items: center; justify-content: center;
    font-size: 18px; margin-bottom: 14px;
    box-shadow: 0 4px 14px rgba(0,0,0,0.12);
}
.kpi-label { font-size: 11px; font-weight: 700; text-transform: uppercase; letter-spacing: 1px; color: #A3AED0; }
.kpi-value { font-family: 'DM Mono', monospace; font-size: 26px; font-weight: 500; color: #1B2559; margin-top: 4px; line-height: 1.1; }
.kpi-sub   { font-size: 11px; color: #A3AED0; margin-top: 5px; }
.kpi-pos   { color: #05CD99; font-weight: 700; }
.kpi-neg   { color: #EE5D50; font-weight: 700; }

/* ── Chart Cards ── */
.chart-card {
    background: white; border-radius: 20px;
    padding: 22px 20px 14px;
    box-shadow: 0 2px 10px rgba(112,144,176,0.10);
    border: 1px solid #F0F3FF;
    margin-bottom: 22px;
}
.chart-card-title {
    font-size: 14px; font-weight: 800; color: #1B2559;
    letter-spacing: -0.2px; margin-bottom: 3px;
}
.chart-card-sub { font-size: 11px; color: #A3AED0; margin-bottom: 14px; }

/* ── Section titles ── */
.section-title {
    font-size: 11px; font-weight: 800; text-transform: uppercase;
    letter-spacing: 2px; color: #4318FF;
    margin: 28px 0 14px;
    display: flex; align-items: center; gap: 10px;
}
.section-title::after {
    content: ''; flex: 1; height: 1px;
    background: linear-gradient(90deg, #E9EDF7, transparent);
}

/* ── Streamlit metric override ── */
[data-testid="stMetric"] {
    background: white !important; border-radius: 20px !important;
    padding: 18px !important; border: 1px solid #F0F3FF !important;
    box-shadow: 0 2px 10px rgba(112,144,176,0.10) !important;
}
[data-testid="stMetricLabel"] { font-size: 11px !important; font-weight: 700 !important; color: #A3AED0 !important; text-transform: uppercase !important; letter-spacing: 0.8px !important; }
[data-testid="stMetricValue"] { font-family: 'DM Mono', monospace !important; font-size: 22px !important; color: #1B2559 !important; font-weight: 500 !important; }

/* ── Expander ── */
.streamlit-expanderHeader {
    background: white !important; border-radius: 14px !important;
    font-size: 13px !important; font-weight: 700 !important; color: #1B2559 !important;
    border: 1px solid #F0F3FF !important;
}

/* ── Dataframe ── */
.stDataFrame { border-radius: 14px !important; overflow: hidden; }

hr { border: none !important; border-top: 1px solid #E9EDF7 !important; margin: 8px 0 !important; }

/* ── Footer ── */
.footer { text-align: center; color: #A3AED0; font-size: 11px; padding: 28px 0 10px; font-weight: 500; }
</style>
""", unsafe_allow_html=True)


# ── Load data ──────────────────────────────────────────────────────────────────
@st.cache_data
def get_data():
    return load_data()

df_full = get_data()

# ── Sidebar ────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div class="sidebar-brand">
        <div class="brand-icon">⟠</div>
        <div>
            <div class="brand-name">ETH Dash</div>
            <div class="brand-sub">Analytics</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="nav-section">
        <span class="nav-label">Main Menu</span>
        <div class="nav-item active"><span class="nav-icon">📊</span> Dashboard</div>
        <div class="nav-item"><span class="nav-icon">📈</span> Price Charts</div>
        <div class="nav-item"><span class="nav-icon">💹</span> Volume</div>
        <div class="nav-item"><span class="nav-icon">🔁</span> Returns</div>
        <div class="nav-item"><span class="nav-icon">⚙️</span> Settings</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="filter-header">Filters</div>', unsafe_allow_html=True)

    st.markdown('<span class="filter-label">📅 Date Range</span>', unsafe_allow_html=True)
    min_date = df_full["Date"].min().date()
    max_date = df_full["Date"].max().date()
    date_range = st.date_input("Date", value=(min_date, max_date),
                                min_value=min_date, max_value=max_date,
                                label_visibility="collapsed")

    st.markdown('<span class="filter-label">📆 Year</span>', unsafe_allow_html=True)
    all_years = sorted(df_full["Year"].unique().tolist())
    selected_years = st.multiselect("Year", options=all_years,
                                     default=all_years, label_visibility="collapsed")

    st.markdown('<span class="filter-label">💲 Price Range (USD)</span>', unsafe_allow_html=True)
    p_min = float(df_full["Close"].min())
    p_max = float(df_full["Close"].max())
    price_range = st.slider("Price", min_value=p_min, max_value=p_max,
                             value=(p_min, p_max), step=1.0, label_visibility="collapsed")

    st.markdown('<span class="filter-label">🔍 Search Date</span>', unsafe_allow_html=True)
    search_text = st.text_input("Search", value="", label_visibility="collapsed",
                                 placeholder="e.g. 2021-01")
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🔄  Reset All Filters", use_container_width=True):
        st.rerun()

# ── Apply filters ──────────────────────────────────────────────────────────────
dr = date_range if (isinstance(date_range, tuple) and len(date_range) == 2) else (min_date, max_date)
df  = apply_filters(df_full, dr, selected_years if selected_years else all_years,
                    price_range[0], price_range[1], search_text)
kpi = kpi_summary(df)

# ── Topbar ─────────────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="topbar">
    <div>
        <div class="topbar-title">Dashboard</div>
        <div class="topbar-sub">Ethereum · ETH/USD · Exploratory Data Analysis</div>
    </div>
    <div class="topbar-right">
        <div class="topbar-badge">⟠ ETH-USD</div>
        <div class="topbar-record">{len(df):,} records</div>
    </div>
</div>
""", unsafe_allow_html=True)

# ── KPI Cards ──────────────────────────────────────────────────────────────────
ret_class = "kpi-pos" if kpi['avg_daily_ret'] >= 0 else "kpi-neg"
ret_arrow  = "▲" if kpi['avg_daily_ret'] >= 0 else "▼"

k1, k2, k3, k4, k5, k6 = st.columns(6)
k1.metric("📊 Total Records",    f"{kpi['total_records']:,}")
k2.metric("💲 Avg Close",        f"${kpi['avg_close']:,.2f}")
k3.metric("🔺 All-Time High",    f"${kpi['max_close']:,.2f}")
k4.metric("🔻 All-Time Low",     f"${kpi['min_close']:,.4f}")
k5.metric("📦 Avg Volume",       f"${kpi['avg_volume']:.2f}B")
k6.metric("📈 Avg Daily Return", f"{kpi['avg_daily_ret']:.3f}%")

# ── Row 1: Trends ──────────────────────────────────────────────────────────────
st.markdown('<div class="section-title">Price & Volume Trends</div>', unsafe_allow_html=True)
c1, c2 = st.columns(2)
with c1:
    st.markdown('<div class="chart-card"><div class="chart-card-title">Close Price Over Time</div><div class="chart-card-sub">Historical ETH/USD closing price from 2015 to 2021</div>', unsafe_allow_html=True)
    st.pyplot(fig_line_chart(df), use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
with c2:
    st.markdown('<div class="chart-card"><div class="chart-card-title">Trading Volume Over Time</div><div class="chart-card-sub">Daily trading volume in billions USD</div>', unsafe_allow_html=True)
    st.pyplot(fig_area_chart(df), use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ── Row 2: Distributions ───────────────────────────────────────────────────────
st.markdown('<div class="section-title">Price Distributions</div>', unsafe_allow_html=True)
c3, c4 = st.columns(2)
with c3:
    st.markdown('<div class="chart-card"><div class="chart-card-title">Close Price Histogram</div><div class="chart-card-sub">Frequency distribution of ETH closing prices</div>', unsafe_allow_html=True)
    st.pyplot(fig_histogram(df), use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
with c4:
    st.markdown('<div class="chart-card"><div class="chart-card-title">Price Spread by Year</div><div class="chart-card-sub">Median, IQR and outliers per year</div>', unsafe_allow_html=True)
    st.pyplot(fig_box_plot(df), use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ── Row 3: Categorical ─────────────────────────────────────────────────────────
st.markdown('<div class="section-title">Categorical & Proportional</div>', unsafe_allow_html=True)
c5, c6, c7 = st.columns(3)
with c5:
    st.markdown('<div class="chart-card"><div class="chart-card-title">Avg Price by Year</div><div class="chart-card-sub">Year-over-year average close price</div>', unsafe_allow_html=True)
    st.pyplot(fig_bar_chart(df), use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
with c6:
    st.markdown('<div class="chart-card"><div class="chart-card-title">Volume Share by Year</div><div class="chart-card-sub">Proportional trading volume per year</div>', unsafe_allow_html=True)
    st.pyplot(fig_pie_chart(df), use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
with c7:
    st.markdown('<div class="chart-card"><div class="chart-card-title">Trading Days per Year</div><div class="chart-card-sub">Count of active ETH trading days</div>', unsafe_allow_html=True)
    st.pyplot(fig_count_plot(df), use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ── Row 4: Relationships ───────────────────────────────────────────────────────
st.markdown('<div class="section-title">Relationships & Correlations</div>', unsafe_allow_html=True)
c8, c9 = st.columns(2)
with c8:
    st.markdown('<div class="chart-card"><div class="chart-card-title">Volume vs Price</div><div class="chart-card-sub">Scatter of volume against closing price</div>', unsafe_allow_html=True)
    st.pyplot(fig_scatter_plot(df), use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
with c9:
    st.markdown('<div class="chart-card"><div class="chart-card-title">Correlation Matrix</div><div class="chart-card-sub">Feature-level correlation heatmap</div>', unsafe_allow_html=True)
    st.pyplot(fig_heatmap(df), use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ── Row 5: Volatility ──────────────────────────────────────────────────────────
st.markdown('<div class="section-title">Volatility & Returns</div>', unsafe_allow_html=True)
st.markdown('<div class="chart-card"><div class="chart-card-title">Daily Return Distribution by Year</div><div class="chart-card-sub">Violin plot — return density and spread per year</div>', unsafe_allow_html=True)
st.pyplot(fig_violin_plot(df), use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)

# ── Data Table ─────────────────────────────────────────────────────────────────
st.markdown('<div class="section-title">Raw Data</div>', unsafe_allow_html=True)
with st.expander("📋  Show Filtered Data Table"):
    st.dataframe(
        df[["Date","Open","High","Low","Close","Volume","Daily_Return","Price_Range"]]
          .rename(columns={"Daily_Return":"Daily Return %","Price_Range":"Price Range"}),
        use_container_width=True, height=300)

st.markdown('<div class="footer">ETH-USD Dashboard · Exploratory Data Analysis · Instructor: Ali Hassan Sherazi</div>', unsafe_allow_html=True)
