"""
The Second Rent -- shared data prep and visual system.

One module so every figure in every medium draws on the same cleaned frame,
the same palette, and the same type scale. Imported by build_figures.py and
build_map.py.

David Jorgensen | DSC 640 Term Project
"""

from pathlib import Path

import matplotlib as mpl
import matplotlib.font_manager as fm
import numpy as np
import pandas as pd

# ---------------------------------------------------------------- paths

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data" / "nationaldatabaseofchildcareprices.xlsx"
FONTS = ROOT.parent / "tsa" / "fonts"
FIGURES = ROOT / "figures"
GEO = ROOT / "geo"
BUILD = ROOT / "build"

# ---------------------------------------------------------------- constants

BENCHMARK = 7.0                      # HHS affordability standard, % of income
CPI = {2008: 215.303, 2018: 251.107}  # CPI-U annual averages
WEEKS = 52                            # full-time, year-round annualization

# Sequential teal ramp carrying magnitude, plus one reserved warm accent.
RAMP = ["#e9eef1", "#c3d4da", "#93b3bd", "#5c8a9b", "#2f6d82", "#163a48"]
BINS = [0, 10, 13, 16, 19, 21, 100]
BIN_LABELS = ["<10%", "10-13%", "13-16%", "16-19%", "19-21%", ">21%"]

INK = "#163a48"       # deepest teal, doubles as body ink
MID = "#5c8a9b"
MUTED = "#93b3bd"
PAPER = "#faf9f7"
RULE = "#d9dedd"
ACCENT = "#bf5a3f"    # terracotta, reserved for the benchmark and the highlight
NODATA = "#eef0ee"

SERIF = "Merriweather"
SANS = "Source Sans 3"

# ---------------------------------------------------------------- fonts


def register_fonts():
    """Load the project's TTFs into matplotlib without installing them."""
    for ttf in sorted(FONTS.glob("*.ttf")):
        fm.fontManager.addfont(str(ttf))
    mpl.rcParams.update(
        {
            "font.family": SANS,
            "font.size": 11,
            "text.color": INK,
            "axes.edgecolor": RULE,
            "axes.labelcolor": INK,
            "axes.titlecolor": INK,
            "xtick.color": INK,
            "ytick.color": INK,
            "figure.facecolor": PAPER,
            "axes.facecolor": PAPER,
            "savefig.facecolor": PAPER,
            "axes.grid": False,
            "axes.spines.top": False,
            "axes.spines.right": False,
            "figure.dpi": 200,
            "savefig.dpi": 200,
            "savefig.bbox": "tight",
            "savefig.pad_inches": 0.08,
        }
    )


def serif(size, weight="bold"):
    return {"family": SERIF, "fontsize": size, "fontweight": weight}


# ---------------------------------------------------------------- data


def load():
    """Return the raw NDCP frame with the burden ratio attached."""
    df = pd.read_excel(DATA)
    df["County_FIPS_Code"] = df["County_FIPS_Code"].astype(int).astype(str).str.zfill(5)
    df["annual_infant"] = df["MCInfant"] * WEEKS
    df["burden"] = df["annual_infant"] / df["MHI"] * 100
    return df


def priced(df):
    """County-years where both the infant price and income exist."""
    return df.dropna(subset=["MCInfant", "MHI"]).copy()


def deflate(price, from_year, to_year=2018):
    """Restate a nominal price in `to_year` dollars using CPI-U."""
    return price * CPI[to_year] / CPI[from_year]


def real_series(df):
    """National median center-based infant price by year, in 2018 dollars.

    Each year is deflated on its own CPI-U index, interpolated linearly
    between the 2008 and 2018 anchors the project documents.
    """
    yearly = df.dropna(subset=["MCInfant"]).groupby("StudyYear")["MCInfant"].median()
    years = yearly.index.to_numpy()
    idx = np.interp(years, [2008, 2018], [CPI[2008], CPI[2018]])
    return pd.Series(yearly.to_numpy() * CPI[2018] / idx, index=years, name="real")


def state_2018(df):
    """State-level 2018 medians: burden, price, income, and both ranks."""
    d18 = priced(df[df.StudyYear == 2018])
    st = d18.groupby("State_Abbreviation").agg(
        state=("State_Name", "first"),
        burden=("burden", "median"),
        price=("MCInfant", "median"),
        mhi=("MHI", "median"),
        counties=("burden", "size"),
    )
    # Break the handful of exact price ties by burden so ranks stay unique and
    # the slope chart never stacks two state labels on one row.
    st = st.sort_values(["price", "burden"], ascending=False)
    st["price_rank"] = st["price"].rank(ascending=False, method="first").astype(int)
    st["burden_rank"] = st["burden"].rank(ascending=False, method="first").astype(int)
    st["shift"] = st["price_rank"] - st["burden_rank"]
    return st.sort_values("burden", ascending=False)


def headline(df):
    """The numbers every medium quotes, computed once."""
    d = priced(df)
    d18 = priced(df[df.StudyYear == 2018])
    age = df.dropna(subset=["MCInfant", "MCPreschool"])
    setting = df.dropna(subset=["MCInfant", "MFCCInfant"])
    real = real_series(df)
    two = d18.dropna(subset=["MCPreschool"])

    return {
        "n_county_years": len(d),
        "n_total_rows": len(df),
        "n_counties": df["County_FIPS_Code"].nunique(),
        "median_burden": d["burden"].median(),
        "pct_over_7": (d["burden"] > 7).mean() * 100,
        "pct_over_15": (d["burden"] > 15).mean() * 100,
        "age_premium": (age["MCInfant"].median() / age["MCPreschool"].median() - 1) * 100,
        "setting_premium": (
            setting["MCInfant"].median() / setting["MFCCInfant"].median() - 1
        )
        * 100,
        "real_growth": (real.loc[2018] / real.loc[2008] - 1) * 100,
        "real_2008": real.loc[2008],
        "real_2018": real.loc[2018],
        "two_child_burden": ((two["MCInfant"] + two["MCPreschool"]) * WEEKS / two["MHI"] * 100).median(),
        "suppressed_2018": int(df[df.StudyYear == 2018]["MCInfant"].isna().sum()),
        "counties_2018": int((df.StudyYear == 2018).sum()),
        "flfp_corr": df.dropna(subset=["MCInfant", "FLFPR_20to64_Under6"])["MCInfant"].corr(
            df["FLFPR_20to64_Under6"]
        ),
    }


def threshold_shares(df):
    """Share of reporting counties above each burden threshold, by year."""
    d = priced(df)
    out = {}
    for thr in (10, 15, 20):
        out[thr] = d.groupby("StudyYear")["burden"].apply(lambda s, t=thr: (s > t).mean() * 100)
    out["median"] = d.groupby("StudyYear")["burden"].median()
    return pd.DataFrame(out)


def bin_burden(values):
    """Map burden percentages onto the shared six-step ramp."""
    return pd.cut(values, bins=BINS, labels=BIN_LABELS, include_lowest=True)
