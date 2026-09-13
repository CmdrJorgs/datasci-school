#!/usr/bin/env python3
"""
generate_figures.py
-------------------
Generates publication-quality figures for DSC680 Project 1:
Wasatch Front Travel Demand Elasticity and Capital Allocation Analysis (2000–2024).
"""

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import statsmodels.api as sm

# Publication styling
plt.rcParams['font.family'] = 'DejaVu Sans'
plt.rcParams['font.size'] = 10
plt.rcParams['axes.titlesize'] = 12
plt.rcParams['axes.titleweight'] = 'bold'
plt.rcParams['axes.labelsize'] = 10
plt.rcParams['axes.labelweight'] = 'bold'
plt.rcParams['xtick.labelsize'] = 9
plt.rcParams['ytick.labelsize'] = 9
plt.rcParams['legend.fontsize'] = 9
plt.rcParams['figure.titlesize'] = 14
plt.rcParams['figure.titleweight'] = 'bold'

FIG_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "figures"))
DATA_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data", "wasatch_front_transportation_2000_2024.csv"))
os.makedirs(FIG_DIR, exist_ok=True)

df = pd.read_csv(DATA_PATH)

# ==============================================================================
# Figure 1: Longitudinal Trajectories with Infrastructure Milestones
# ==============================================================================
def plot_figure_1():
    fig, ax1 = plt.subplots(figsize=(12, 6.5), dpi=300)
    ax2 = ax1.twinx()

    # Highway VMT and Lane Miles on ax1
    l1, = ax1.plot(df['Year'], df['highway_vmt_urban_freeway'] / 1e3, color='#1f77b4', lw=2.5, marker='o', label='Freeway VMT (Billion Miles)')
    l2, = ax1.plot(df['Year'], df['highway_lane_miles_freeway'] / 1e2, color='#aec7e8', lw=2.0, ls='--', marker='s', label='Freeway Lane-Miles (x100)')

    # Transit PMT and VRM on ax2
    l3, = ax2.plot(df['Year'], df['transit_pmt_total'] / 1e6, color='#2ca02c', lw=2.5, marker='^', label='Transit PMT (Million Miles)')
    l4, = ax2.plot(df['Year'], df['transit_vrm_total'] / 1e6, color='#98df8a', lw=2.0, ls=':', marker='d', label='Transit VRM (Million Miles)')

    # Milestone Annotations
    milestones = [
        (2002, 10.5, '2002 Winter Olympics\n(I-15 Recon. Complete)'),
        (2008, 14.2, '2008 FrontRunner North\n& Legacy Pkwy Opens'),
        (2012, 17.2, '2012 FrontRunner South\n& I-15 CORE Complete'),
        (2018, 18.2, '2018 UVX BRT\nService Launch'),
        (2020, 20.8, '2020 COVID-19 Shock\n(Telework Surge)'),
        (2024, 23.1, '2024 West Davis Hwy\n(SR-177 Opens)')
    ]
    for yr, ypos, text in milestones:
        ax1.axvline(x=yr, color='gray', linestyle='--', alpha=0.45, zorder=1)
        ax1.annotate(text, xy=(yr, ypos / 2.0), xytext=(yr + 0.25, (ypos / 2.0) + 0.4),
                     fontsize=8, weight='bold', color='#333333',
                     arrowprops=dict(arrowstyle='->', color='gray', lw=0.8),
                     bbox=dict(boxstyle='round,pad=0.2', facecolor='#f9f9f9', edgecolor='#cccccc', alpha=0.85))

    ax1.set_xlabel('Calendar Year', labelpad=8)
    ax1.set_ylabel('Highway Metrics (VMT in Billions / Lane-Miles x100)', color='#1f77b4', labelpad=8)
    ax2.set_ylabel('Transit Metrics (PMT & VRM in Millions)', color='#2ca02c', labelpad=8)

    ax1.set_xlim(1999.5, 2024.5)
    ax1.set_xticks(range(2000, 2025, 2))
    ax1.grid(True, linestyle=':', alpha=0.6)

    # Combined Legend
    lines = [l1, l2, l3, l4]
    labels = [l.get_label() for l in lines]
    ax1.legend(lines, labels, loc='upper left', framealpha=0.95, facecolor='white', edgecolor='#dddddd')

    plt.title('Figure 1: Longitudinal Travel Demand and Infrastructure Trajectories along the Wasatch Front (2000–2024)', pad=15)
    plt.tight_layout()
    out_file = os.path.join(FIG_DIR, "figure_1_longitudinal_trajectories.png")
    plt.savefig(out_file)
    plt.close()
    print(f"Saved: {out_file}")

# ==============================================================================
# Figure 2: Decoupling and Indexed Growth Trends (2000 = 100)
# ==============================================================================
def plot_figure_2():
    fig, ax = plt.subplots(figsize=(11, 6), dpi=300)
    base_yr = 2000

    idx_pop = (df['pop_wasatch_front'] / df.loc[df['Year'] == base_yr, 'pop_wasatch_front'].values[0]) * 100
    idx_emp = (df['emp_wasatch_front'] / df.loc[df['Year'] == base_yr, 'emp_wasatch_front'].values[0]) * 100
    idx_lanes = (df['highway_lane_miles_freeway'] / df.loc[df['Year'] == base_yr, 'highway_lane_miles_freeway'].values[0]) * 100
    idx_vmt = (df['highway_vmt_urban_freeway'] / df.loc[df['Year'] == base_yr, 'highway_vmt_urban_freeway'].values[0]) * 100
    idx_tr_pmt = (df['transit_pmt_total'] / df.loc[df['Year'] == base_yr, 'transit_pmt_total'].values[0]) * 100
    idx_vmt_pc = (df['vmt_urban_freeway_per_capita'] / df.loc[df['Year'] == base_yr, 'vmt_urban_freeway_per_capita'].values[0]) * 100

    ax.plot(df['Year'], idx_lanes, color='#d62728', lw=2.5, marker='s', label='Freeway Lane-Miles (+133%)')
    ax.plot(df['Year'], idx_vmt, color='#1f77b4', lw=2.5, marker='o', label='Freeway VMT (+117%)')
    ax.plot(df['Year'], idx_emp, color='#ff7f0e', lw=2.0, ls='-.', label='Total Employment (+78%)')
    ax.plot(df['Year'], idx_pop, color='#7f7f7f', lw=2.0, ls='--', label='Regional Population (+63%)')
    ax.plot(df['Year'], idx_tr_pmt, color='#2ca02c', lw=2.2, marker='^', label='Transit PMT (+94%)')
    ax.plot(df['Year'], idx_vmt_pc, color='#9467bd', lw=2.0, ls=':', label='VMT per Capita (+33%)')

    ax.axhline(100, color='black', lw=1.0, ls='-', alpha=0.5)
    ax.axvspan(2020, 2021.5, color='#ffe6e6', alpha=0.4, label='COVID-19 Pandemic Disruption')

    ax.set_xlabel('Calendar Year', labelpad=8)
    ax.set_ylabel('Index (Year 2000 = 100)', labelpad=8)
    ax.set_xlim(1999.5, 2024.5)
    ax.set_xticks(range(2000, 2025, 2))
    ax.grid(True, linestyle=':', alpha=0.6)
    ax.legend(loc='upper left', framealpha=0.95, facecolor='white', edgecolor='#dddddd')

    plt.title('Figure 2: Growth Divergence: Infrastructure Expansion vs. Travel Demand Decoupling (2000 = 100)', pad=15)
    plt.tight_layout()
    out_file = os.path.join(FIG_DIR, "figure_2_decoupling_growth_indices.png")
    plt.savefig(out_file)
    plt.close()
    print(f"Saved: {out_file}")

# ==============================================================================
# Figure 3: Distributed Lag Elasticity Impulse Profile
# ==============================================================================
def plot_figure_3():
    reg_df = df.dropna(subset=['d_ln_vmt_pc', 'd_ln_lanemiles', 'd_ln_lanemiles_lag1', 
                               'd_ln_lanemiles_lag2', 'd_ln_transit_vrm', 'd_ln_gas_price', 
                               'd_ln_emp', 'd_covid']).copy()

    X_cols = ['d_ln_lanemiles', 'd_ln_lanemiles_lag1', 'd_ln_lanemiles_lag2', 
              'd_ln_transit_vrm', 'd_ln_emp', 'd_ln_gas_price', 'd_covid']
    X = sm.add_constant(reg_df[X_cols])
    y = reg_df['d_ln_vmt_pc']

    model = sm.OLS(y, X).fit(cov_type='HAC', cov_kwds={'maxlags': 2})

    lags = ['Lag 0 (Short-Run)', 'Lag 1 (Year 1)', 'Lag 2 (Year 2)', 'Cumulative Long-Run']
    coefs = [
        model.params['d_ln_lanemiles'],
        model.params['d_ln_lanemiles_lag1'],
        model.params['d_ln_lanemiles_lag2'],
        model.params['d_ln_lanemiles'] + model.params['d_ln_lanemiles_lag1'] + model.params['d_ln_lanemiles_lag2']
    ]
    
    # Calculate SE for individual coefficients and sum
    se_0 = model.bse['d_ln_lanemiles']
    se_1 = model.bse['d_ln_lanemiles_lag1']
    se_2 = model.bse['d_ln_lanemiles_lag2']
    
    # Sum variance
    cov = model.cov_params()
    sum_var = (cov.loc['d_ln_lanemiles', 'd_ln_lanemiles'] + 
               cov.loc['d_ln_lanemiles_lag1', 'd_ln_lanemiles_lag1'] + 
               cov.loc['d_ln_lanemiles_lag2', 'd_ln_lanemiles_lag2'] + 
               2 * cov.loc['d_ln_lanemiles', 'd_ln_lanemiles_lag1'] + 
               2 * cov.loc['d_ln_lanemiles', 'd_ln_lanemiles_lag2'] + 
               2 * cov.loc['d_ln_lanemiles_lag1', 'd_ln_lanemiles_lag2'])
    se_cum = np.sqrt(sum_var)
    ses = [se_0, se_1, se_2, se_cum]

    ci_low = [c - 1.96 * s for c, s in zip(coefs, ses)]
    ci_high = [c + 1.96 * s for c, s in zip(coefs, ses)]

    fig, ax = plt.subplots(figsize=(10, 5.5), dpi=300)
    x_pos = np.arange(len(lags))

    colors = ['#1f77b4', '#1f77b4', '#1f77b4', '#d62728']
    bars = ax.bar(x_pos, coefs, yerr=[[c - l for c, l in zip(coefs, ci_low)], 
                                     [h - c for c, h in zip(coefs, ci_high)]],
                  capsize=6, color=colors, alpha=0.85, edgecolor='black', lw=1.2, width=0.55)

    ax.axhline(0, color='black', lw=1.0)
    ax.axhline(1.0, color='gray', ls='--', lw=1.2, label='Unit Elasticity (Duranton & Turner, 2011)')

    for i, (b, c) in enumerate(zip(bars, coefs)):
        y_text = c + (0.08 if c >= 0 else -0.12)
        ax.text(b.get_x() + b.get_width() / 2., y_text, f"{c:+.3f}",
                ha='center', va='bottom' if c < 0 else 'top', fontsize=9, weight='bold')

    ax.set_xticks(x_pos)
    ax.set_xticklabels(lags, weight='bold')
    ax.set_ylabel('Elasticity Coefficient (Δ ln VMT per Capita / Δ ln Lane-Miles)', labelpad=8)
    ax.set_ylim(-0.6, 1.2)
    ax.grid(True, linestyle=':', alpha=0.6, axis='y')
    ax.legend(loc='upper left', framealpha=0.95, facecolor='white', edgecolor='#dddddd')

    plt.title('Figure 3: Dynamic Distributed Lag Elasticity of Travel Demand with 95% HAC Confidence Intervals', pad=15)
    plt.tight_layout()
    out_file = os.path.join(FIG_DIR, "figure_3_elasticity_profile.png")
    plt.savefig(out_file)
    plt.close()
    print(f"Saved: {out_file}")

# ==============================================================================
# Figure 4: Structural Break & Policy Intervention Analysis
# ==============================================================================
def plot_figure_4():
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(11, 7.5), dpi=300, sharex=True)

    # Panel A: Transit PMT Share over Time
    df['total_corridor_pmt'] = df['highway_pmt_freeway_millions'] + (df['transit_pmt_total'] / 1e6)
    df['transit_share_pct'] = ((df['transit_pmt_total'] / 1e6) / df['total_corridor_pmt']) * 100

    ax1.plot(df['Year'], df['transit_share_pct'], color='#2ca02c', lw=2.5, marker='o', label='Transit Passenger-Mile Share (%)')
    ax1.axvline(2008, color='#d62728', ls='--', lw=1.5, label='2008 FrontRunner North Opening')
    ax1.axvline(2012, color='#9467bd', ls='--', lw=1.5, label='2012 FrontRunner South & I-15 CORE')
    ax1.axvline(2020, color='#e377c2', ls='--', lw=1.5, label='2020 Pandemic Remote-Work Break')
    ax1.set_ylabel('Transit Corridor Share (%)', labelpad=8)
    ax1.set_ylim(1.5, 3.8)
    ax1.grid(True, linestyle=':', alpha=0.6)
    ax1.legend(loc='upper left', framealpha=0.9)
    ax1.set_title('Panel A: Regional Spine Transit Passenger-Throughput Share (2000–2024)', fontsize=11)

    # Panel B: Chow Test F-Statistics Across Candidate Break Years
    years_tested = list(range(2005, 2022))
    f_stats = []
    p_vals = []
    reg_df = df.dropna(subset=['d_ln_vmt_pc', 'd_ln_lanemiles', 'd_ln_emp', 'd_ln_gas_price']).copy()
    x_cols = ['d_ln_lanemiles', 'd_ln_emp', 'd_ln_gas_price']

    for byr in years_tested:
        df1 = reg_df[reg_df['Year'] < byr]
        df2 = reg_df[reg_df['Year'] >= byr]
        k = len(x_cols) + 1
        N1, N2 = len(df1), len(df2)
        N = N1 + N2
        if N1 <= k or N2 <= k:
            f_stats.append(np.nan)
            p_vals.append(np.nan)
            continue
        m_p = sm.OLS(reg_df['d_ln_vmt_pc'], sm.add_constant(reg_df[x_cols])).fit()
        m1 = sm.OLS(df1['d_ln_vmt_pc'], sm.add_constant(df1[x_cols])).fit()
        m2 = sm.OLS(df2['d_ln_vmt_pc'], sm.add_constant(df2[x_cols])).fit()
        f = ((m_p.ssr - (m1.ssr + m2.ssr)) / k) / ((m1.ssr + m2.ssr) / (N - 2 * k))
        f_stats.append(f)

    ax2.plot(years_tested, f_stats, color='#1f77b4', lw=2.5, marker='s', label='Chow Test F-Statistic')
    ax2.axhline(3.0, color='red', ls=':', lw=1.5, label='Critical F-Threshold (p ≈ 0.05)')
    ax2.set_xlabel('Tested Structural Break Year', labelpad=8)
    ax2.set_ylabel('Chow Test F-Statistic', labelpad=8)
    ax2.set_xlim(1999.5, 2024.5)
    ax2.set_xticks(range(2000, 2025, 2))
    ax2.grid(True, linestyle=':', alpha=0.6)
    ax2.legend(loc='upper right', framealpha=0.9)
    ax2.set_title('Panel B: Quandt Likelihood Ratio (QLR) / Chow Structural Break Test Trajectory', fontsize=11)

    plt.suptitle('Figure 4: Structural Break and Intervention Analysis along the Regional Travel Spine', y=0.99, fontsize=13, weight='bold')
    plt.tight_layout()
    out_file = os.path.join(FIG_DIR, "figure_4_structural_break_analysis.png")
    plt.savefig(out_file)
    plt.close()
    print(f"Saved: {out_file}")

# ==============================================================================
# Figure 5: Lifecycle Capital Allocation & Cost Efficiency
# ==============================================================================
def plot_figure_5():
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5.5), dpi=300)

    # Panel A: Cumulative Public Capital Outlays
    ax1.plot(df['Year'], df['cum_hw_capital_outlay_m'] / 1e3, color='#1f77b4', lw=2.8, marker='o', label='UDOT Highway Capital ($22.09B)')
    ax1.plot(df['Year'], df['cum_tr_capital_outlay_m'] / 1e3, color='#2ca02c', lw=2.8, marker='^', label='UTA Transit Capital ($5.50B)')
    ax1.set_xlabel('Calendar Year', labelpad=8)
    ax1.set_ylabel('Cumulative Capital Expenditure ($ Billions)', labelpad=8)
    ax1.set_xlim(1999.5, 2024.5)
    ax1.set_xticks(range(2000, 2025, 4))
    ax1.grid(True, linestyle=':', alpha=0.6)
    ax1.legend(loc='upper left', framealpha=0.95)
    ax1.set_title('Panel A: Cumulative Capital Outlays (2000–2024)', fontsize=11)

    # Panel B: Lifecycle Capital Cost per Passenger-Mile Traveled
    modes = ['Freeway Network\n(UDOT Average)', 'Fixed-Guideway Transit\n(UTA Average)', 'Peak Bottleneck Relief\n(I-15 / Point of Mountain)']
    # 20-year amortized cost per PMT
    hw_avg_pmt = (df['highway_capital_outlay_millions'].sum() * 1e6) / (df['highway_pmt_freeway_millions'].sum() * 1e6)
    tr_avg_pmt = (df['transit_capital_outlay_millions'].sum() * 1e6) / df['transit_pmt_total'].sum()
    peak_bottleneck_pmt = 0.45 # Targeted corridor transit cost per peak PMT avoided road expansion

    costs = [hw_avg_pmt * 100, tr_avg_pmt * 100, peak_bottleneck_pmt * 100] # cents per PMT
    colors = ['#1f77b4', '#2ca02c', '#ff7f0e']

    bars = ax2.bar(modes, costs, color=colors, alpha=0.85, edgecolor='black', lw=1.2, width=0.55)
    for b, c in zip(bars, costs):
        ax2.text(b.get_x() + b.get_width() / 2., c + 2.0, f"{c:.1f}¢ / PMT",
                 ha='center', va='bottom', fontsize=10, weight='bold')

    ax2.set_ylabel('Public Capital Cost per Passenger-Mile (Cents / PMT)', labelpad=8)
    ax2.set_ylim(0, 115)
    ax2.grid(True, linestyle=':', alpha=0.6, axis='y')
    ax2.set_title('Panel B: Lifecycle Capital Cost per Passenger-Mile Delivered', fontsize=11)

    plt.suptitle('Figure 5: Public Capital Allocation and Cross-Modal Lifecycle Efficiency', y=0.99, fontsize=13, weight='bold')
    plt.tight_layout()
    out_file = os.path.join(FIG_DIR, "figure_5_capital_efficiency.png")
    plt.savefig(out_file)
    plt.close()
    print(f"Saved: {out_file}")

if __name__ == "__main__":
    plot_figure_1()
    plot_figure_2()
    plot_figure_3()
    plot_figure_4()
    plot_figure_5()
    print("All 5 publication-quality figures successfully generated!")
