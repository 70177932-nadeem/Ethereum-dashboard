import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns

# ── EDUMIN-style palette ──────────────────────────────────────────────────────
BG      = "#FFFFFF"
CARD_BG = "#F4F7FE"
ETH     = "#4318FF"   # deep indigo
BLUE    = "#2196F3"
ORANGE  = "#FF9800"
PURPLE  = "#9C27B0"
GREEN   = "#05CD99"
RED     = "#EE5D50"
MUTED   = "#A3AED0"
GRID    = "#EFF4FB"
TEXT    = "#1B2559"
TEXT2   = "#68769F"

PALETTE = [ETH, BLUE, ORANGE, PURPLE, GREEN, RED, "#00BCD4", "#FF5722"]


def _style(fig, axes=None):
    fig.patch.set_facecolor(BG)
    for ax in (axes or fig.get_axes()):
        ax.set_facecolor(CARD_BG)
        ax.tick_params(colors=TEXT2, labelsize=9)
        ax.xaxis.label.set_color(TEXT2)
        ax.yaxis.label.set_color(TEXT2)
        ax.title.set_color(TEXT)
        for spine in ax.spines.values():
            spine.set_edgecolor("#E9EDF7")
            spine.set_linewidth(0.8)
        ax.grid(color=GRID, linewidth=0.8, linestyle="-", alpha=1)
        ax.set_axisbelow(True)


def fig_line_chart(df):
    fig, ax = plt.subplots(figsize=(9, 3.8))
    ax.plot(df["Date"], df["Close"], color=ETH, linewidth=2.2, zorder=3)
    ax.fill_between(df["Date"], df["Close"], alpha=0.10, color=ETH)
    ax.set_xlabel("Date", fontweight="600"); ax.set_ylabel("Price (USD)", fontweight="600")
    ax.set_title("ETH Close Price Over Time", fontsize=12, fontweight="bold", pad=10, color=TEXT)
    _style(fig)
    plt.tight_layout(pad=1.2)
    return fig


def fig_area_chart(df):
    fig, ax = plt.subplots(figsize=(9, 3.8))
    ax.fill_between(df["Date"], df["Volume_B"], color=BLUE, alpha=0.30, zorder=2)
    ax.plot(df["Date"], df["Volume_B"], color=BLUE, linewidth=1.8, zorder=3)
    ax.set_xlabel("Date", fontweight="600"); ax.set_ylabel("Volume (Billions USD)", fontweight="600")
    ax.set_title("Trading Volume Over Time", fontsize=12, fontweight="bold", pad=10, color=TEXT)
    _style(fig)
    plt.tight_layout(pad=1.2)
    return fig


def fig_bar_chart(df):
    yearly = df.groupby("Year")["Close"].mean().reset_index()
    fig, ax = plt.subplots(figsize=(7, 3.8))
    bars = ax.bar(yearly["Year"].astype(str), yearly["Close"],
                  color=[PALETTE[i % len(PALETTE)] for i in range(len(yearly))],
                  edgecolor="white", linewidth=1.2, width=0.6, zorder=3,
                  capstyle="round")
    for bar in bars:
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 20,
                f"${bar.get_height():,.0f}", ha="center", va="bottom",
                color=TEXT2, fontsize=7.5, fontweight="700")
    ax.set_xlabel("Year", fontweight="600"); ax.set_ylabel("Avg Close (USD)", fontweight="600")
    ax.set_title("Avg Close Price by Year", fontsize=12, fontweight="bold", pad=10, color=TEXT)
    _style(fig)
    plt.tight_layout(pad=1.2)
    return fig


def fig_histogram(df):
    fig, ax = plt.subplots(figsize=(7, 3.8))
    ax.hist(df["Close"], bins=55, color=PURPLE, edgecolor="white",
            linewidth=0.5, alpha=0.85, zorder=3)
    ax.axvline(df["Close"].mean(), color=ORANGE, linestyle="--",
               linewidth=2, label=f"Mean: ${df['Close'].mean():,.0f}", zorder=4)
    ax.set_xlabel("Close Price (USD)", fontweight="600"); ax.set_ylabel("Frequency", fontweight="600")
    ax.set_title("Close Price Distribution", fontsize=12, fontweight="bold", pad=10, color=TEXT)
    ax.legend(fontsize=9, framealpha=0.95, edgecolor="#E9EDF7")
    _style(fig)
    plt.tight_layout(pad=1.2)
    return fig


def fig_scatter_plot(df):
    sample = df.sample(min(len(df), 700), random_state=42)
    fig, ax = plt.subplots(figsize=(7, 3.8))
    sc = ax.scatter(sample["Volume_B"], sample["Close"],
                    c=sample["Close"], cmap="cool",
                    alpha=0.65, s=18, edgecolors="none", zorder=3)
    cb = plt.colorbar(sc, ax=ax)
    cb.ax.tick_params(labelsize=8, color=MUTED)
    plt.setp(cb.ax.yaxis.get_ticklabels(), color=TEXT2, fontsize=8)
    cb.set_label("Close Price", color=TEXT2, fontsize=9)
    ax.set_xlabel("Volume (Billions USD)", fontweight="600"); ax.set_ylabel("Close Price (USD)", fontweight="600")
    ax.set_title("Volume vs Close Price", fontsize=12, fontweight="bold", pad=10, color=TEXT)
    _style(fig)
    plt.tight_layout(pad=1.2)
    return fig


def fig_box_plot(df):
    years = sorted(df["Year"].unique())
    data_by_year = [df[df["Year"] == y]["Close"].values for y in years]
    fig, ax = plt.subplots(figsize=(9, 3.8))
    bp = ax.boxplot(data_by_year, labels=[str(y) for y in years],
                    patch_artist=True, notch=False,
                    medianprops=dict(color=ORANGE, linewidth=2.2),
                    whiskerprops=dict(color=MUTED, linewidth=1.2),
                    capprops=dict(color=MUTED, linewidth=1.2),
                    flierprops=dict(marker="o", color=MUTED, markersize=3, alpha=0.4))
    for i, patch in enumerate(bp["boxes"]):
        patch.set_facecolor(PALETTE[i % len(PALETTE)])
        patch.set_alpha(0.55)
        patch.set_edgecolor("white")
    ax.set_xlabel("Year", fontweight="600"); ax.set_ylabel("Close Price (USD)", fontweight="600")
    ax.set_title("Price Distribution by Year", fontsize=12, fontweight="bold", pad=10, color=TEXT)
    _style(fig)
    plt.tight_layout(pad=1.2)
    return fig


def fig_pie_chart(df):
    vol_by_year = df.groupby("Year")["Volume"].sum()
    fig, ax = plt.subplots(figsize=(6, 4.6))
    wedges, texts, autotexts = ax.pie(
        vol_by_year.values,
        labels=vol_by_year.index.astype(str),
        autopct="%1.1f%%",
        colors=PALETTE[:len(vol_by_year)],
        startangle=140,
        wedgeprops=dict(edgecolor="white", linewidth=2.5),
        pctdistance=0.80,
    )
    for t in texts: t.set_color(TEXT); t.set_fontsize(9); t.set_fontweight("700")
    for at in autotexts: at.set_color("white"); at.set_fontsize(8); at.set_fontweight("bold")
    ax.set_title("Volume Share by Year", fontsize=12, fontweight="bold", pad=10, color=TEXT)
    fig.patch.set_facecolor(BG)
    ax.set_facecolor(BG)
    plt.tight_layout(pad=1.2)
    return fig


def fig_heatmap(df):
    num_cols = ["Open", "High", "Low", "Close", "Volume", "Daily_Return", "Price_Range"]
    corr = df[num_cols].corr()
    fig, ax = plt.subplots(figsize=(7, 5.2))
    sns.heatmap(corr, annot=True, fmt=".2f", cmap="coolwarm",
                ax=ax, linewidths=1.2, linecolor="white",
                annot_kws={"size": 8.5, "color": TEXT, "weight": "bold"},
                cbar_kws={"shrink": 0.8})
    ax.set_title("Feature Correlation Matrix", fontsize=12, fontweight="bold", pad=10, color=TEXT)
    ax.tick_params(axis="x", rotation=30, labelsize=9)
    ax.tick_params(axis="y", rotation=0, labelsize=9)
    _style(fig, [ax])
    plt.tight_layout(pad=1.2)
    return fig


def fig_count_plot(df):
    counts = df.groupby("Year").size().reset_index(name="Days")
    fig, ax = plt.subplots(figsize=(7, 3.8))
    bars = ax.bar(counts["Year"].astype(str), counts["Days"],
                  color=GREEN, edgecolor="white", linewidth=1.2, width=0.6, zorder=3)
    for bar in bars:
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 2,
                str(int(bar.get_height())), ha="center", va="bottom",
                color=TEXT2, fontsize=8, fontweight="700")
    ax.set_xlabel("Year", fontweight="600"); ax.set_ylabel("Trading Days", fontweight="600")
    ax.set_title("Trading Days per Year", fontsize=12, fontweight="bold", pad=10, color=TEXT)
    _style(fig)
    plt.tight_layout(pad=1.2)
    return fig


def fig_violin_plot(df):
    clean = df.dropna(subset=["Daily_Return"])
    clean = clean[clean["Daily_Return"].between(-30, 30)]
    years = sorted(clean["Year"].unique())
    data_by_year = [clean[clean["Year"] == y]["Daily_Return"].values for y in years]
    fig, ax = plt.subplots(figsize=(10, 3.8))
    parts = ax.violinplot(data_by_year, positions=range(len(years)),
                          showmedians=True, showextrema=True)
    for i, pc in enumerate(parts["bodies"]):
        pc.set_facecolor(PALETTE[i % len(PALETTE)])
        pc.set_alpha(0.65)
        pc.set_edgecolor("white")
    parts["cmedians"].set_color(ORANGE); parts["cmedians"].set_linewidth(2.2)
    parts["cmaxes"].set_color(MUTED); parts["cmins"].set_color(MUTED)
    parts["cbars"].set_color(MUTED)
    ax.set_xticks(range(len(years)))
    ax.set_xticklabels([str(y) for y in years])
    ax.axhline(0, color=RED, linestyle="--", linewidth=1.2, alpha=0.5)
    ax.set_xlabel("Year", fontweight="600"); ax.set_ylabel("Daily Return (%)", fontweight="600")
    ax.set_title("Daily Return Distribution by Year", fontsize=12, fontweight="bold", pad=10, color=TEXT)
    _style(fig)
    plt.tight_layout(pad=1.2)
    return fig
