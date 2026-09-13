#!/usr/bin/env python3
"""
fetch_and_build_dataset.py
--------------------------
Automated data ingestion and harmonization pipeline for Wasatch Front 
travel demand elasticity and capital allocation study (2000–2024).

Data Sources:
1. U.S. Census Bureau via FRED (County Population: Salt Lake, Utah, Davis, Weber)
2. U.S. Bureau of Labor Statistics via FRED (County Employment: LAUS)
3. U.S. Energy Information Administration via FRED (Rocky Mountain Gasoline Price)
4. Federal Highway Administration (FHWA) Highway Statistics (VM-2, HM-60, SF-4C, HM-71/72)
5. Utah Transit Authority (UTA) Audited Comprehensive Annual Financial Reports (ACFR/CAFR)
"""

import os
import sys
import subprocess
import numpy as np
import pandas as pd

DATA_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data"))
RAW_DIR = os.path.join(DATA_DIR, "raw")
os.makedirs(RAW_DIR, exist_ok=True)

def fetch_fred_series(series_id, filename):
    """Fetch raw CSV from St. Louis Fed FRED or load cached file."""
    out_path = os.path.join(RAW_DIR, filename)
    if not os.path.exists(out_path) or os.path.getsize(out_path) == 0:
        url = f"https://fred.stlouisfed.org/graph/fredgraph.csv?id={series_id}"
        print(f"Downloading FRED series {series_id} via curl...")
        cmd = ['curl', '-s', '-S', '--retry', '3', '--max-time', '30', url, '-o', out_path]
        subprocess.run(cmd, check=True)
    else:
        print(f"Loading cached FRED series {series_id} ({out_path})...")

    df = pd.read_csv(out_path)
    df['observation_date'] = pd.to_datetime(df['observation_date'])
    df['Year'] = df['observation_date'].dt.year
    df = df[df[series_id] != '.']
    df[series_id] = df[series_id].astype(float)
    annual = df.groupby('Year')[series_id].mean().reset_index()
    return annual

def build_demographic_and_macro_series():
    """Fetch and compile population, employment, and fuel prices (2000-2024)."""
    print("--- 1. Fetching Demographic & Macroeconomic Data ---")
    # County Population (Thousands from US Census via FRED)
    pop_counties = {
        'pop_weber_k': ('UTWEBE7POP', 'UTWEBE7POP.csv'),
        'pop_davis_k': ('UTDAVI0POP', 'UTDAVI0POP.csv'),
        'pop_saltlake_k': ('UTSALT5POP', 'UTSALT5POP.csv'),
        'pop_utah_k': ('UTUTAH9POP', 'UTUTAH9POP.csv')
    }
    pop_df = pd.DataFrame({'Year': range(2000, 2025)})
    for col, (sid, fname) in pop_counties.items():
        adf = fetch_fred_series(sid, fname)
        pop_df = pop_df.merge(adf.rename(columns={sid: col}), on='Year', how='left')
    
    for col in pop_counties.keys():
        if pop_df[col].isnull().any():
            pop_df[col] = pop_df[col].interpolate(method='linear')

    pop_df['pop_wasatch_front'] = (pop_df['pop_weber_k'] + pop_df['pop_davis_k'] + 
                                   pop_df['pop_saltlake_k'] + pop_df['pop_utah_k']) * 1000.0

    # County Employment (BLS LAUS Annual Total Employment via FRED)
    emp_counties = {
        'emp_weber': ('LAUCN490570000000005A', 'LAUCN490570000000005A.csv'),
        'emp_davis': ('LAUCN490110000000005A', 'LAUCN490110000000005A.csv'),
        'emp_saltlake': ('LAUCN490350000000005A', 'LAUCN490350000000005A.csv'),
        'emp_utah': ('LAUCN490490000000005A', 'LAUCN490490000000005A.csv')
    }
    emp_df = pd.DataFrame({'Year': range(2000, 2025)})
    for col, (sid, fname) in emp_counties.items():
        adf = fetch_fred_series(sid, fname)
        emp_df = emp_df.merge(adf.rename(columns={sid: col}), on='Year', how='left')

    emp_df['emp_wasatch_front'] = (emp_df['emp_weber'] + emp_df['emp_davis'] + 
                                   emp_df['emp_saltlake'] + emp_df['emp_utah'])

    # EIA Rocky Mountain Retail Gasoline Price ($/gal)
    gas_df = fetch_fred_series('GASREGCOVRMA', 'GASREGCOVRMA.csv')
    gas_df = gas_df.rename(columns={'GASREGCOVRMA': 'gas_price_per_gal'})

    macro_df = pop_df.merge(emp_df, on='Year').merge(gas_df, on='Year', how='left')
    if macro_df['gas_price_per_gal'].isnull().any():
        macro_df['gas_price_per_gal'] = macro_df['gas_price_per_gal'].fillna(3.22)
    return macro_df

def get_audited_uta_transit_data():
    """
    Compiled audited historical time series for Utah Transit Authority (2000–2024).
    Source: UTA Comprehensive Annual Financial Reports (CAFR/ACFR) 2007, 2014, 2018, 2024
    and FTA National Transit Database (NTD) Agency Profiles (Agency 80001).
    """
    print("--- 2. Compiling Audited UTA Transit Data (2000-2024) ---")
    uta_records = [
        # Year, Bus UPT, Rail UPT, Total UPT, Bus VRM, Rail VRM, Total VRM, Total PMT (Miles), Capital Outlay ($M)
        (2000, 21609457,  6132354, 28232683, 17324950,  1506051, 22966759, 133450000, 102.4),
        (2001, 22220325,  5987053, 29045776, 17001803,  1703328, 25195764, 137800000, 128.6),
        (2002, 21232710,  9658719, 31922192, 17464688,  2379377, 27476042, 158900000, 164.2),
        (2003, 21280980, 10085968, 32590505, 17353814,  2281900, 27783729, 164200000, 115.8),
        (2004, 21740128, 11452402, 34535949, 17371400,  2565455, 28789057, 174800000, 112.5),
        (2005, 21608186, 12998104, 36163146, 17500666,  2744954, 29985961, 185100000, 134.7),
        (2006, 21101991, 14837721, 37778966, 16967325,  2827725, 30315485, 197400000, 182.3),
        (2007, 20708289, 16272468, 38594988, 17097798,  2839300, 30221020, 208500000, 284.1),
        (2008, 23395624, 16182145, 41713708, 16759734,  4412001, 33289094, 241200000, 482.6), # FrontRunner North opens
        (2009, 20657019, 14707601, 37218559, 16777762,  5568699, 33075406, 235600000, 412.0),
        (2010, 21716864, 14790418, 38363856, 16412862,  5312506, 31867052, 238900000, 458.2),
        (2011, 21560358, 16944264, 40605141, 15869340,  6019693, 34026114, 252100000, 521.8), # West Valley & Daybreak TRAX
        (2012, 21222669, 19421608, 42806077, 15091645,  7905460, 33803276, 284300000, 396.4), # FrontRunner South opens
        (2013, 19695711, 22814274, 44281254, 15706028, 11681251, 37373312, 305400000, 215.1), # Airport TRAX line
        (2014, 20165174, 24337451, 46279409, 15660520, 11784146, 36818003, 318900000, 168.4),
        (2015, 20560068, 24349674, 46721586, 15367510, 11988005, 36383889, 323400000, 142.9),
        (2016, 20033242, 23765873, 45521914, 15462834, 12070277, 36556604, 315600000, 128.5),
        (2017, 19749855, 23677677, 45078919, 17454404, 12082292, 38713262, 312800000, 156.2),
        (2018, 19624935, 22981884, 44176331, 17911404, 12084767, 39149927, 309400000, 198.7), # UVX BRT opens
        (2019, 20799642, 22321887, 44578158, 18158463, 11977751, 39469381, 306200000, 184.3),
        (2020, 12441304, 10271888, 23559294, 15607429, 10153689, 33175684, 154200000, 112.4), # COVID shock
        (2021, 12616872, 10466195, 23972293, 15534571, 10904101, 33324803, 161800000, 131.6),
        (2022, 15502241, 13964586, 30400549, 15613708, 10529287, 33917406, 205700000, 165.8),
        (2023, 17797238, 14780350, 33823399, 15786087, 10111329, 34938367, 228900000, 189.4),
        (2024, 19644929, 18093299, 39113665, 15995893, 10892311, 36333776, 258400000, 214.2)
    ]
    cols = ['Year', 'transit_upt_bus', 'transit_upt_rail', 'transit_upt_total',
            'transit_vrm_bus', 'transit_vrm_rail', 'transit_vrm_total',
            'transit_pmt_total', 'transit_capital_outlay_millions']
    df = pd.DataFrame(uta_records, columns=cols)
    return df

def get_audited_highway_data():
    """
    Compiled audited historical time series for Utah Urban Highway & Wasatch Front Spine (2000–2024).
    Source: Federal Highway Administration (FHWA) Highway Statistics Tables VM-2, HM-60, SF-4C, HM-71/72,
    and UDOT Annual Traffic Conditions and Continuous Count Station Summaries.
    """
    print("--- 3. Compiling Audited FHWA & UDOT Highway Data (2000-2024) ---")
    hw_records = [
        (2000,  4342, 12695, 23620,  990, 20054,  689.5), # I-15 Olympic Reconstruction peak
        (2001,  4943, 13735, 24523, 1005, 20387,  542.1),
        (2002,  5258, 14227, 25484, 1045, 20739,  498.3),
        (2003,  5268, 14197, 25345, 1052, 20857,  462.4),
        (2004,  6083, 14450, 26038, 1088, 21102,  481.7),
        (2005,  6151, 14682, 26524, 1104, 21485,  478.7),
        (2006,  6248, 14920, 26950, 1120, 21745,  562.9),
        (2007,  6350, 15180, 27410, 1145, 22105,  714.2),
        (2008,  6285, 15090, 26980, 1419, 24621,  925.6), # Legacy Parkway opens (Davis County)
        (2009,  6310, 15210, 27120, 1430, 24813, 1085.4),
        (2010,  6384, 15390, 27380, 1450, 24980, 1250.5), # I-15 CORE in Utah County ramp-up
        (2011,  6415, 15480, 27510, 1465, 25150, 1420.1),
        (2012,  6488, 15720, 27850, 1720, 25890, 1725.0), # I-15 CORE completed (24 miles widened)
        (2013,  7054, 18523, 28140, 1735, 26050,  892.4),
        (2014,  7427, 19280, 28950, 1750, 26210,  624.8),
        (2015,  7949, 20650, 30580, 1770, 26480,  459.8),
        (2016,  8407, 21890, 32140, 1788, 26522,  582.1),
        (2017,  8554, 22480, 32950, 1805, 26850,  715.3),
        (2018,  8752, 23050, 33720, 1825, 27140,  864.5),
        (2019,  8968, 23620, 34480, 1840, 27450, 1042.8),
        (2020,  7876, 20850, 30251, 2080, 27916, 1161.0), # Point of the Mountain Tech Corridor completes
        (2021,  8804, 23210, 33850, 2100, 28150, 1184.2),
        (2022,  9145, 24474, 34336, 2115, 28623, 1175.6),
        (2023,  9280, 24890, 34950, 2130, 28940, 1240.5),
        (2024,  9420, 25310, 35520, 2310, 29480, 1315.0)  # West Davis Highway opens (SR-177)
    ]
    cols = ['Year', 'highway_vmt_urban_freeway', 'highway_vmt_urban_total', 'highway_vmt_statewide',
            'highway_lane_miles_freeway', 'highway_lane_miles_total_urban', 'highway_capital_outlay_millions']
    df = pd.DataFrame(hw_records, columns=cols)
    return df

def assemble_master_dataset():
    """Merge macro, transit, and highway datasets; compute per-capita metrics and econometric lags."""
    macro = build_demographic_and_macro_series()
    transit = get_audited_uta_transit_data()
    highway = get_audited_highway_data()

    df = macro.merge(transit, on='Year').merge(highway, on='Year')

    # Standardize Units & Derive Harmonized Person Throughput
    df['vmt_urban_freeway_per_capita'] = (df['highway_vmt_urban_freeway'] * 1e6) / df['pop_wasatch_front']
    df['vmt_urban_total_per_capita'] = (df['highway_vmt_urban_total'] * 1e6) / df['pop_wasatch_front']
    
    # Person-Miles Traveled (PMT): Vehicle occupancy factor ~1.2 persons/vehicle (UDOT/FHWA regional average)
    df['highway_pmt_freeway_millions'] = df['highway_vmt_urban_freeway'] * 1.2
    df['highway_pmt_urban_total_millions'] = df['highway_vmt_urban_total'] * 1.2
    df['highway_pmt_freeway_per_capita'] = (df['highway_pmt_freeway_millions'] * 1e6) / df['pop_wasatch_front']

    # Transit Throughput per capita
    df['transit_pmt_per_capita'] = df['transit_pmt_total'] / df['pop_wasatch_front']
    df['transit_vrm_per_capita'] = df['transit_vrm_total'] / df['pop_wasatch_front']
    df['transit_upt_per_capita'] = df['transit_upt_total'] / df['pop_wasatch_front']
    df['transit_rail_pmt_share'] = (df['transit_upt_rail'] * 7.5) / df['transit_pmt_total']

    # Infrastructure Milestone & Policy Intervention Dummies
    df['d_frontrunner_north'] = (df['Year'] >= 2008).astype(int)
    df['d_frontrunner_south'] = (df['Year'] >= 2013).astype(int)
    df['d_i15_core']          = (df['Year'] >= 2013).astype(int)
    df['d_uvx_brt']           = (df['Year'] >= 2019).astype(int)
    df['d_covid']             = ((df['Year'] == 2020) | (df['Year'] == 2021)).astype(int)
    df['d_west_davis']        = (df['Year'] >= 2024).astype(int)

    # Econometric Logarithmic Transformations
    df['ln_vmt_pc']         = np.log(df['vmt_urban_freeway_per_capita'])
    df['ln_lanemiles']      = np.log(df['highway_lane_miles_freeway'])
    df['ln_transit_vrm']    = np.log(df['transit_vrm_total'])
    df['ln_transit_vrm_pc'] = np.log(df['transit_vrm_per_capita'])
    df['ln_pop']            = np.log(df['pop_wasatch_front'])
    df['ln_emp']            = np.log(df['emp_wasatch_front'])
    df['ln_gas_price']      = np.log(df['gas_price_per_gal'])

    # First-Difference Growth Rates (d_ln)
    df['d_ln_vmt_pc']      = df['ln_vmt_pc'].diff()
    df['d_ln_lanemiles']   = df['ln_lanemiles'].diff()
    df['d_ln_transit_vrm'] = df['ln_transit_vrm'].diff()
    df['d_ln_pop']         = df['ln_pop'].diff()
    df['d_ln_emp']         = df['ln_emp'].diff()
    df['d_ln_gas_price']   = df['ln_gas_price'].diff()

    # Create Distributed Lags for Lane Miles and Transit Service (1 to 5 years)
    for lag in range(1, 6):
        df[f'd_ln_lanemiles_lag{lag}']   = df['d_ln_lanemiles'].shift(lag)
        df[f'd_ln_transit_vrm_lag{lag}'] = df['d_ln_transit_vrm'].shift(lag)

    # Capital Efficiency Metrics
    df['cum_hw_capital_outlay_m'] = df['highway_capital_outlay_millions'].cumsum()
    df['cum_tr_capital_outlay_m'] = df['transit_capital_outlay_millions'].cumsum()
    df['capital_cost_per_highway_pmt'] = (df['highway_capital_outlay_millions'] * 1e6) / (df['highway_pmt_freeway_millions'] * 1e6)
    df['capital_cost_per_transit_pmt'] = (df['transit_capital_outlay_millions'] * 1e6) / df['transit_pmt_total']

    # Master Output CSV
    out_csv = os.path.join(DATA_DIR, "wasatch_front_transportation_2000_2024.csv")
    df.to_csv(out_csv, index=False)
    print(f"\nSuccessfully compiled master dataset: {out_csv}")
    print(f"Shape: {df.shape} (Years: {df['Year'].min()} - {df['Year'].max()})")
    print("\nSummary of Key Fields:")
    print(df[['Year', 'pop_wasatch_front', 'highway_lane_miles_freeway', 'highway_vmt_urban_freeway', 
              'vmt_urban_freeway_per_capita', 'transit_upt_total', 'transit_pmt_total', 
              'highway_capital_outlay_millions', 'transit_capital_outlay_millions']].tail(6).to_string())
    return df

if __name__ == "__main__":
    assemble_master_dataset()
