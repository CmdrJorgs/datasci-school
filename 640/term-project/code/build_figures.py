"""
The Second Rent -- render the nine figures, three per medium.

Every medium gets its own set. No figure appears in more than one medium, and
no two figures in the package use the same mark.

    Medium 01 (print)       waffle, bullet, dumbbell
    Medium 02 (interactive) choropleth, iso-burden scatter, real-price lines
    Medium 03 (brief)       slope, ridgeline, threshold shares

David Jorgensen | DSC 640 Term Project
"""

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.patches import Rectangle
from matplotlib.lines import Line2D

sys.path.insert(0, str(Path(__file__).resolve().parent))
import secondrent as sr  # noqa: E402

sr.register_fonts()
OUT = sr.FIGURES
OUT.mkdir(exist_ok=True)

DF = sr.load()
H = sr.headline(DF)
D18 = sr.priced(DF[DF.StudyYear == 2018])


def save(fig, name):
    path = OUT / name
    fig.savefig(path, transparent=False)
    plt.close(fig)
    print(f"  wrote {path.relative_to(sr.ROOT)}")


# ===================================================== MEDIUM 01 | PRINT


def fig_waffle():
    """1,000 squares. One county in a thousand meets the federal standard."""
    cols, rows = 100, 10
    total = cols * rows
    n_pass = round(total * (100 - H["pct_over_7"]) / 100)      # 1
    n_over15 = round(total * H["pct_over_15"] / 100)           # 593
    n_mid = total - n_pass - n_over15                          # 406

    order = ([sr.NODATA] * n_pass) + ([sr.RAMP[2]] * n_mid) + ([sr.RAMP[5]] * n_over15)

    fig, ax = plt.subplots(figsize=(9.6, 1.85))
    for i, color in enumerate(order):
        r, c = divmod(i, cols)
        ax.add_patch(
            Rectangle(
                (c, rows - 1 - r),
                0.82,
                0.82,
                facecolor=color,
                edgecolor=sr.ACCENT if color == sr.NODATA else "none",
                linewidth=1.1 if color == sr.NODATA else 0,
            )
        )

    ax.annotate(
        "1 county in 1,000\nmeets the 7% standard",
        xy=(0.4, rows - 0.55),
        xytext=(2.4, rows + 1.4),
        color=sr.ACCENT,
        fontsize=9.6,
        fontweight=600,
        ha="left",
        va="bottom",
        arrowprops=dict(arrowstyle="-", color=sr.ACCENT, lw=1.1,
                        connectionstyle="angle,angleA=0,angleB=90,rad=4"),
    )

    ax.set_xlim(-1.0, cols + 0.6)
    ax.set_ylim(-5.4, rows + 6.2)
    ax.axis("off")
    ax.set_aspect("equal")

    legend = [
        (sr.RAMP[5], f"Over 15% of income  ({n_over15} counties)"),
        (sr.RAMP[2], f"7% to 15% of income  ({n_mid})"),
        (sr.NODATA, f"At or under 7%  ({n_pass})"),
    ]
    for j, (color, label) in enumerate(legend):
        x = j * 33.0
        ax.add_patch(
            Rectangle((x, -3.6), 1.5, 1.5, facecolor=color,
                      edgecolor=sr.ACCENT if color == sr.NODATA else "none", lw=1.1)
        )
        ax.text(x + 2.6, -2.85, label, fontsize=9.0, va="center", color=sr.INK)

    save(fig, "m01_waffle.png")


def fig_bullet():
    """Bullet chart: the typical county against the federal target."""
    d = sr.priced(DF)
    q25, med, q75, q90 = d["burden"].quantile([0.25, 0.5, 0.75, 0.90])

    fig, ax = plt.subplots(figsize=(9.6, 1.75))
    bands = [(0, 7, sr.RAMP[0]), (7, 13, sr.RAMP[1]), (13, 19, sr.RAMP[2]), (19, 26, sr.RAMP[3])]
    for lo, hi, color in bands:
        ax.add_patch(Rectangle((lo, 0.12), hi - lo, 0.76, facecolor=color, edgecolor="none"))

    ax.add_patch(Rectangle((0, 0.38), med, 0.24, facecolor=sr.INK, edgecolor="none", zorder=3))
    ax.plot([q25, q75], [0.5, 0.5], color=sr.PAPER, lw=0, zorder=4)
    for q, label in ((q25, "25th"), (q75, "75th")):
        ax.plot([q, q], [0.12, 0.34], color=sr.INK, lw=1.0, ls=(0, (2, 2)), zorder=5)
        ax.text(q, 0.06, f"{label} pct. {q:.1f}%", ha="center", va="top",
                fontsize=8.2, color=sr.INK)

    ax.plot([sr.BENCHMARK, sr.BENCHMARK], [0.06, 0.94], color=sr.ACCENT, lw=3.2, zorder=6,
            solid_capstyle="butt")
    ax.text(sr.BENCHMARK - 0.45, 1.02, "7%  federal target", ha="right", va="bottom",
            color=sr.ACCENT, fontsize=10, fontweight=600)
    ax.text(med + 0.45, 0.5, f"{med:.1f}%  typical county", ha="left", va="center",
            color=sr.INK, fontsize=11.5, fontweight=600)

    ax.set_xlim(0, 26)
    ax.set_ylim(-0.42, 1.32)
    ax.set_yticks([])
    ax.set_xticks(range(0, 27, 5))
    ax.set_xticklabels([f"{v}%" for v in range(0, 27, 5)], fontsize=9)
    for side in ("left", "bottom"):
        ax.spines[side].set_visible(False)
    ax.tick_params(length=0, pad=1)
    ax.set_xlabel("Center-based infant care as a share of median household income",
                  fontsize=9.4, labelpad=6)
    save(fig, "m01_bullet.png")


def fig_dumbbell():
    """Two premiums, two connected pairs: age and setting."""
    age = DF.dropna(subset=["MCInfant", "MCPreschool"])
    setting = DF.dropna(subset=["MCInfant", "MFCCInfant"])
    pairs = [
        ("Child's age", "Preschooler", age["MCPreschool"].median(),
         "Infant", age["MCInfant"].median(), H["age_premium"]),
        ("Care setting", "Home-based provider", setting["MFCCInfant"].median(),
         "Licensed center", setting["MCInfant"].median(), H["setting_premium"]),
    ]

    fig, ax = plt.subplots(figsize=(9.6, 2.15))
    for i, (group, lo_lab, lo, hi_lab, hi, prem) in enumerate(pairs):
        y = 1 - i
        ax.plot([lo, hi], [y, y], color=sr.RAMP[2], lw=7, solid_capstyle="round", zorder=1)
        ax.scatter([lo], [y], s=210, color=sr.RAMP[3], zorder=3, edgecolor=sr.PAPER, linewidth=1.6)
        ax.scatter([hi], [y], s=260, color=sr.INK, zorder=3, edgecolor=sr.PAPER, linewidth=1.6)

        ax.text(lo - 6, y, f"${lo:.0f}", ha="right", va="center", fontsize=11.5,
                fontweight=600, color=sr.RAMP[4])
        ax.text(hi + 6, y, f"${hi:.0f}", ha="left", va="center", fontsize=11.5,
                fontweight=600, color=sr.INK)
        ax.text(lo - 6, y - 0.27, lo_lab, ha="right", va="center", fontsize=9, color=sr.MID)
        ax.text(hi + 6, y - 0.27, hi_lab, ha="left", va="center", fontsize=9, color=sr.MID)
        ax.text((lo + hi) / 2, y + 0.28, f"+{prem:.0f}%", ha="center", va="bottom",
                fontsize=11, fontweight=700, color=sr.ACCENT)
        ax.text(72, y, " ".join(group.upper()), ha="left", va="center",
                fontsize=8.2, color=sr.MID)

    ax.set_xlim(70, 172)
    ax.set_ylim(-0.62, 1.62)
    ax.set_yticks([])
    ax.set_xticks([100, 110, 120, 130, 140, 150])
    ax.set_xticklabels([f"${v}" for v in (100, 110, 120, 130, 140, 150)], fontsize=9)
    for side in ("left", "bottom"):
        ax.spines[side].set_visible(False)
    ax.tick_params(length=0, pad=1)
    ax.set_xlabel("Median full-time weekly price, all reporting county-years",
                  fontsize=9.4, labelpad=6)
    save(fig, "m01_dumbbell.png")


# =============================================== MEDIUM 02 | INTERACTIVE


def _counties():
    import geopandas as gpd

    gdf = gpd.read_file(f"zip://{sr.GEO / 'cb_2018_us_county_20m.zip'}")
    states = gpd.read_file(f"zip://{sr.GEO / 'cb_2018_us_state_20m.zip'}")
    gdf["GEOID"] = gdf["GEOID"].astype(str).str.zfill(5)
    m = gdf.merge(D18[["County_FIPS_Code", "burden", "County_Name", "State_Abbreviation"]],
                  left_on="GEOID", right_on="County_FIPS_Code", how="left")
    m["bin"] = sr.bin_burden(m["burden"])
    return m, states


def fig_choropleth():
    """County choropleth of the 2018 burden, with Alaska and Hawaii insets."""
    counties, states = _counties()
    cmap = dict(zip(sr.BIN_LABELS, sr.RAMP))
    counties["color"] = counties["bin"].astype(object).map(cmap).fillna(sr.NODATA)

    fig = plt.figure(figsize=(8.8, 5.6))
    ax = fig.add_axes([0.0, 0.10, 1.0, 0.90])
    ax_ak = fig.add_axes([0.015, 0.10, 0.20, 0.24])
    ax_hi = fig.add_axes([0.205, 0.10, 0.10, 0.15])

    panels = [
        (ax, 5070, [f"{i:02d}" for i in range(1, 57) if f"{i:02d}" not in ("02", "15")]),
        (ax_ak, 3338, ["02"]),
        (ax_hi, 26962, ["15"]),
    ]
    for axis, epsg, fips in panels:
        sub = counties[counties["STATEFP"].isin(fips)].to_crs(epsg=epsg)
        stl = states[states["STATEFP"].isin(fips)].to_crs(epsg=epsg)
        sub.plot(ax=axis, color=sub["color"], edgecolor="#ffffff", linewidth=0.12)
        stl.boundary.plot(ax=axis, color="#ffffff", linewidth=0.55)
        axis.set_axis_off()
        axis.set_facecolor(sr.PAPER)

    suffolk = counties[counties["GEOID"] == "25025"].to_crs(epsg=5070)
    suffolk.plot(ax=ax, color=sr.ACCENT, edgecolor=sr.ACCENT, linewidth=2.6, zorder=5)
    pt = suffolk.geometry.centroid.iloc[0]
    ax.annotate(
        "Suffolk County, MA\n32.2% of median income",
        xy=(pt.x, pt.y),
        xytext=(pt.x + 620000, pt.y + 330000),
        fontsize=10.4, fontweight=600, color=sr.ACCENT, ha="left", va="center",
        arrowprops=dict(arrowstyle="-", color=sr.ACCENT, lw=1.2),
        zorder=6,
    )
    ax.text(0.020, 0.265, "ALASKA", transform=ax.transAxes, fontsize=8.8,
            color=sr.MID, fontweight=600)
    ax.text(0.205, 0.190, "HAWAII", transform=ax.transAxes, fontsize=8.8,
            color=sr.MID, fontweight=600)

    lax = fig.add_axes([0.30, 0.045, 0.62, 0.05])
    lax.set_axis_off()
    for j, (label, color) in enumerate(zip(sr.BIN_LABELS, sr.RAMP)):
        lax.add_patch(Rectangle((j * 0.145, 0.45), 0.10, 0.36, facecolor=color,
                                edgecolor="none", transform=lax.transAxes))
        lax.text(j * 0.145, 0.16, label, fontsize=9.8, color=sr.INK, transform=lax.transAxes)
    lax.add_patch(Rectangle((0.875, 0.45), 0.10, 0.36, facecolor=sr.NODATA,
                            edgecolor=sr.RULE, lw=0.8, transform=lax.transAxes))
    lax.text(0.875, 0.16, "not reported", fontsize=9.8, color=sr.MID, transform=lax.transAxes)

    save(fig, "m02_choropleth.png")


def fig_scatter():
    """Income against price, with iso-burden diagonals. Cheap is not affordable."""
    d = D18.dropna(subset=["MHI", "annual_infant"])
    cmap = dict(zip(sr.BIN_LABELS, sr.RAMP))
    colors = sr.bin_burden(d["burden"]).astype(object).map(cmap).fillna(sr.NODATA)

    fig, ax = plt.subplots(figsize=(8.6, 5.4))
    ax.scatter(d["MHI"], d["annual_infant"], s=13, c=colors, alpha=0.72,
               linewidth=0, zorder=2)

    x = np.array([18000, 156000])
    anchors = {7: 152000, 15: 146000, 25: 112000}
    for share, style, color in ((7, "-", sr.ACCENT), (15, (0, (5, 3)), sr.RAMP[4]),
                                (25, (0, (2, 3)), sr.RAMP[3])):
        ax.plot(x, x * share / 100, ls=style, color=color, lw=1.8 if share == 7 else 1.3, zorder=3)
        ax_x = anchors[share]
        ax.text(ax_x, ax_x * share / 100 + 550, f"{share}% of income",
                color=color, fontsize=9.2, va="bottom", ha="right",
                fontweight=600 if share == 7 else 400, zorder=6,
                bbox=dict(facecolor=sr.PAPER, edgecolor="none", pad=1.4, alpha=0.85))

    suf = d[d["County_FIPS_Code"] == "25025"]
    if len(suf):
        ax.scatter(suf["MHI"], suf["annual_infant"], s=110, facecolor="none",
                   edgecolor=sr.ACCENT, linewidth=2.2, zorder=5)
        ax.annotate("Suffolk County, MA", xy=(suf["MHI"].iloc[0], suf["annual_infant"].iloc[0]),
                    xytext=(-14, 16), textcoords="offset points", fontsize=9.4,
                    fontweight=600, color=sr.ACCENT, ha="right",
                    arrowprops=dict(arrowstyle="-", color=sr.ACCENT, lw=1.0))

    for fips, label, dx, dy, ha in (("28151", "Washington Co., MS", 12, 14, "left"),
                                    ("06075", "San Francisco, CA", -12, 12, "right")):
        row = d[d["County_FIPS_Code"] == fips]
        if len(row):
            ax.scatter(row["MHI"], row["annual_infant"], s=44, facecolor="none",
                       edgecolor=sr.INK, linewidth=1.4, zorder=5)
            ax.annotate(label, xy=(row["MHI"].iloc[0], row["annual_infant"].iloc[0]),
                        xytext=(dx, dy), textcoords="offset points", fontsize=8.8,
                        color=sr.INK, ha=ha,
                        arrowprops=dict(arrowstyle="-", color=sr.MID, lw=0.8))

    ax.set_xlim(18000, 158000)
    ax.set_ylim(0, 30000)
    ax.set_xticks([25000, 50000, 75000, 100000, 125000, 150000])
    ax.set_xticklabels(["$25k", "$50k", "$75k", "$100k", "$125k", "$150k"], fontsize=9)
    ax.set_yticks([0, 5000, 10000, 15000, 20000, 25000, 30000])
    ax.set_yticklabels(["$0", "$5k", "$10k", "$15k", "$20k", "$25k", "$30k"], fontsize=9)
    ax.set_xlabel("Median household income, 2018", fontsize=9.8, labelpad=7)
    ax.set_ylabel("Annualized center-based infant care", fontsize=9.8, labelpad=7)
    ax.grid(axis="both", color=sr.RULE, lw=0.5, zorder=0)
    ax.set_axisbelow(True)
    save(fig, "m02_scatter.png")


def fig_trend():
    """One county read against its state and the nation, in constant dollars."""
    years = np.arange(2008, 2019)
    idx = np.interp(years, [2008, 2018], [sr.CPI[2008], sr.CPI[2018]])
    deflator = pd.Series(sr.CPI[2018] / idx, index=years)

    d = DF.dropna(subset=["MCInfant"])
    nat = d.groupby("StudyYear")["MCInfant"].median() * deflator
    ma = d[d.State_Abbreviation == "MA"].groupby("StudyYear")["MCInfant"].median() * deflator
    suf = (d[d.County_FIPS_Code == "25025"].set_index("StudyYear")["MCInfant"] * deflator)

    fig, ax = plt.subplots(figsize=(4.9, 3.1))
    series = [
        (suf, "Suffolk County, MA", sr.ACCENT, 2.6, 1.0),
        (ma, "Massachusetts median", sr.RAMP[4], 2.0, 0.95),
        (nat, "National county median", sr.RAMP[2], 2.0, 0.95),
    ]
    for s, label, color, lw, alpha in series:
        ax.plot(s.index, s.values, color=color, lw=lw, alpha=alpha, solid_capstyle="round")
        ax.scatter([s.index[-1]], [s.values[-1]], s=34, color=color, zorder=4)
        ax.text(2018.25, s.values[-1], f"  {label}\n  ${s.values[-1]:.0f}/wk",
                fontsize=9.2, va="center", color=color,
                fontweight=600 if color == sr.ACCENT else 400)
        ax.text(2007.75, s.values[0], f"${s.values[0]:.0f}  ", fontsize=8.8, ha="right",
                va="center", color=color)

    ax.set_xlim(2006.4, 2021.8)
    ax.set_ylim(100, 430)
    ax.set_xticks(range(2008, 2019, 2))
    ax.set_xticklabels(["2008", "'10", "'12", "'14", "'16", "2018"], fontsize=9)
    ax.set_yticks([100, 200, 300, 400])
    ax.set_yticklabels(["$100", "$200", "$300", "$400"], fontsize=9)
    ax.set_ylabel("Weekly price, constant 2018 dollars", fontsize=9.6, labelpad=7)
    ax.grid(axis="y", color=sr.RULE, lw=0.5)
    ax.set_axisbelow(True)
    ax.spines["bottom"].set_color(sr.RULE)
    save(fig, "m02_trend.png")


# ===================================================== MEDIUM 03 | BRIEF


def fig_slope():
    """Price rank against burden rank. Cheap states are not affordable states."""
    st = sr.state_2018(DF)
    risers = ["NC", "TN", "OR", "AZ", "WV", "MI"]     # cheap on paper, unaffordable in fact
    fallers = ["NJ", "MD", "UT", "DE", "NH"]           # expensive on paper, mid-pack in fact

    fig, ax = plt.subplots(figsize=(4.8, 6.3))
    for abbr, row in st.iterrows():
        pr, br = row["price_rank"], row["burden_rank"]
        if abbr in risers:
            color, lw, alpha, z = sr.ACCENT, 2.1, 1.0, 4
        elif abbr in fallers:
            color, lw, alpha, z = sr.INK, 2.1, 1.0, 4
        else:
            color, lw, alpha, z = sr.MUTED, 0.9, 0.55, 2
        ax.plot([0, 1], [pr, br], color=color, lw=lw, alpha=alpha, zorder=z)
        ax.scatter([0, 1], [pr, br], s=18 if z == 4 else 8, color=color, alpha=alpha, zorder=z + 1)

        if abbr in risers or abbr in fallers or pr <= 4 or br <= 4:
            bold = abbr in risers or abbr in fallers
            # 51 ranks in a six-inch column leaves ~8.5pt of pitch, so the labels
            # have to stay under that to avoid colliding on consecutive ranks.
            ax.text(-0.035, pr, f"{abbr} {pr}", ha="right", va="center", fontsize=7.5,
                    color=color if bold else sr.MID, fontweight=700 if bold else 400)
            ax.text(1.035, br, f"{br} {abbr}", ha="left", va="center", fontsize=7.5,
                    color=color if bold else sr.MID, fontweight=700 if bold else 400)

    ax.text(0, -1.9, "RANKED BY PRICE", ha="center", va="bottom", fontsize=9.4,
            fontweight=700, color=sr.INK)
    ax.text(0, -0.6, "median weekly cost", ha="center", va="bottom", fontsize=8.6, color=sr.MID)
    ax.text(1, -1.9, "RANKED BY BURDEN", ha="center", va="bottom", fontsize=9.4,
            fontweight=700, color=sr.INK)
    ax.text(1, -0.6, "share of local income", ha="center", va="bottom", fontsize=8.6, color=sr.MID)

    ax.legend(
        handles=[
            Line2D([0], [0], color=sr.ACCENT, lw=2.1, label="Looks cheap, lands harder"),
            Line2D([0], [0], color=sr.INK, lw=2.1, label="Looks costly, lands softer"),
        ],
        loc="lower center", bbox_to_anchor=(0.5, -0.075), ncol=2, frameon=False, fontsize=9.2,
    )

    ax.set_xlim(-0.30, 1.30)
    ax.set_ylim(52, -3.4)
    ax.axis("off")
    save(fig, "m03_slope.png")


def fig_ridgeline():
    """Eleven annual distributions, drifting right away from the benchmark."""
    d = sr.priced(DF)
    years = sorted(d.StudyYear.unique())
    grid = np.linspace(0, 40, 400)
    step = 0.62

    fig, ax = plt.subplots(figsize=(4.7, 4.3))
    for i, year in enumerate(years):
        s = d.loc[d.StudyYear == year, "burden"]
        s = s[s <= 40]
        kde = np.histogram(s, bins=grid.size, range=(0, 40), density=True)[0]
        kde = np.convolve(kde, np.ones(22) / 22, mode="same")
        kde = kde / kde.max()
        base = (len(years) - 1 - i) * step
        shade = sr.RAMP[1 + int(i / (len(years) - 1) * 4)]
        ax.fill_between(grid, base, base + kde, color=shade, alpha=0.95, zorder=i + 2)
        ax.plot(grid, base + kde, color=sr.PAPER, lw=1.0, zorder=i + 2)
        ax.text(-0.9, base + 0.12, str(year), ha="right", va="bottom", fontsize=9,
                color=sr.INK if year in (2008, 2018) else sr.MID,
                fontweight=700 if year in (2008, 2018) else 400)
        med = s.median()
        ax.plot([med, med], [base, base + 0.30], color=sr.PAPER, lw=1.4, zorder=30 + i)

    top = (len(years) - 1) * step + 1.25
    ax.plot([sr.BENCHMARK, sr.BENCHMARK], [0, top], color=sr.ACCENT, lw=2.0, zorder=50)
    ax.text(sr.BENCHMARK, top + 0.08, "7% federal standard", color=sr.ACCENT, fontsize=9.4,
            fontweight=600, ha="center", va="bottom")
    top_base = (len(years) - 1) * step
    ax.annotate(                                   # 2008 sits on the top row
        "median 15.4%",
        xy=(15.4, top_base + 0.30), xytext=(26.0, top_base + 0.66),
        fontsize=8.8, color=sr.INK,
        arrowprops=dict(arrowstyle="-", color=sr.MID, lw=0.8),
    )
    ax.annotate(                                   # 2018 sits on the bottom row
        "median 16.1%",
        xy=(16.1, 0.26), xytext=(26.0, 0.78), fontsize=8.8, color=sr.INK,
        arrowprops=dict(arrowstyle="-", color=sr.MID, lw=0.8),
    )

    ax.set_xlim(-3.2, 40)
    ax.set_ylim(-0.9, top + 1.0)
    ax.set_yticks([])
    ax.set_xticks(range(0, 41, 10))
    ax.set_xticklabels([f"{v}%" for v in range(0, 41, 10)], fontsize=9)
    for side in ("left", "bottom"):
        ax.spines[side].set_visible(False)
    ax.tick_params(length=0)
    ax.set_xlabel("Infant care as a share of median household income", fontsize=9.6, labelpad=6)
    save(fig, "m03_ridgeline.png")


def fig_thresholds():
    """How much of the country sits above each line, year by year."""
    t = sr.threshold_shares(DF)

    fig, ax = plt.subplots(figsize=(4.7, 3.0))
    tracks = [
        (10, sr.RAMP[2], "above 10% of income"),
        (15, sr.RAMP[4], "above 15% of income"),
        (20, sr.INK, "above 20% of income"),
    ]
    for thr, color, label in tracks:
        s = t[thr]
        ax.plot(s.index, s.values, color=color, lw=2.3, solid_capstyle="round")
        ax.scatter([2008, 2018], [s.loc[2008], s.loc[2018]], s=34, color=color, zorder=4)
        ax.text(2018.25, s.loc[2018], f"  {label}\n  {s.loc[2008]:.0f}% → {s.loc[2018]:.0f}%",
                fontsize=9.2, va="center", color=color, fontweight=600)

    ax.set_xlim(2007.6, 2022.6)
    ax.set_ylim(0, 105)
    ax.set_xticks(range(2008, 2019, 2))
    ax.set_xticklabels(["2008", "'10", "'12", "'14", "'16", "2018"], fontsize=9)
    ax.set_yticks([0, 25, 50, 75, 100])
    ax.set_yticklabels(["0%", "25%", "50%", "75%", "100%"], fontsize=9)
    ax.set_ylabel("Share of reporting counties", fontsize=9.6, labelpad=7)
    ax.grid(axis="y", color=sr.RULE, lw=0.5)
    ax.set_axisbelow(True)
    ax.spines["bottom"].set_color(sr.RULE)
    save(fig, "m03_thresholds.png")


if __name__ == "__main__":
    print("Medium 01 | printed infographic")
    fig_waffle()
    fig_bullet()
    fig_dumbbell()
    print("Medium 02 | interactive map")
    fig_choropleth()
    fig_scatter()
    fig_trend()
    print("Medium 03 | policy brief")
    fig_slope()
    fig_ridgeline()
    fig_thresholds()
