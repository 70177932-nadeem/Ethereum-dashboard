"""filters.py — Data loading, cleaning, and all filter logic."""

import pandas as pd
import numpy as np

DATA_PATH = "data/ETH-USD.csv"


def load_data() -> pd.DataFrame:
    df = pd.read_csv(DATA_PATH)

    # Parse dates, drop unparseable
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
    df.dropna(subset=["Date"], inplace=True)

    # Drop full duplicates
    df.drop_duplicates(inplace=True)

    # Fix numeric types & fill missing with median
    num_cols = ["Open", "High", "Low", "Close", "Adj Close", "Volume"]
    for col in num_cols:
        df[col] = pd.to_numeric(df[col], errors="coerce")
        df[col] = df[col].fillna(df[col].median())

    # Derived features
    df = df.sort_values("Date").reset_index(drop=True)
    df["Year"]         = df["Date"].dt.year
    df["Month"]        = df["Date"].dt.month
    df["Month_Name"]   = df["Date"].dt.strftime("%b")
    df["Quarter"]      = "Q" + df["Date"].dt.quarter.astype(str)
    df["Daily_Return"] = df["Close"].pct_change() * 100
    df["Price_Range"]  = df["High"] - df["Low"]
    df["Volume_B"]     = df["Volume"] / 1e9

    return df


def apply_filters(df, date_range, selected_years, price_min, price_max, search_text):
    f = df.copy()

    if date_range and len(date_range) == 2:
        f = f[(f["Date"] >= pd.Timestamp(date_range[0])) &
              (f["Date"] <= pd.Timestamp(date_range[1]))]

    if selected_years:
        f = f[f["Year"].isin(selected_years)]

    f = f[(f["Close"] >= price_min) & (f["Close"] <= price_max)]

    if search_text.strip():
        f = f[f["Date"].astype(str).str.contains(search_text.strip(), case=False, na=False)]

    return f


def kpi_summary(df):
    ret = df["Daily_Return"].dropna()
    return {
        "total_records":   len(df),
        "avg_close":       df["Close"].mean(),
        "max_close":       df["Close"].max(),
        "min_close":       df["Close"].min(),
        "avg_volume":      df["Volume_B"].mean(),
        "avg_daily_ret":   ret.mean(),
        "best_day":        ret.max(),
        "worst_day":       ret.min(),
    }
