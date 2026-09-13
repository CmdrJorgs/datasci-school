&nbsp;

&nbsp;

&nbsp;

&nbsp;

**1.1 Project 1: Proposal and Data Selection/Milestone 1**

**Capital Allocation and Long-Term Travel Demand Elasticity: Evaluating Highway Expansion Versus Multimodal Transit along the Wasatch Front (2000–2024)**

&nbsp;

David Jorgensen

Bellevue University

DSC680-T302 Applied Data Science (2271-1)

Xu Ashton

September 13, 2026

&nbsp;

# **Topic**

This study investigates the long-term effectiveness of capital investments by comparing the travel demand and congestion relief outcomes of highway lane additions versus multimodal transit expansions along Utah’s primary regional travel spine.

# **Business Problem**

State transportation agencies like UDOT face multi-billion-dollar capital allocation trade-offs under constraints of finite land, air quality mandates, and rapid population growth. While road expansions are often justified by short-term congestion mitigation, they risk long-term induced travel demand; conversely, capital-intensive transit projects require documented ridership capture to justify high initial outlays. Without empirical, cross-modal comparison at the regional spine level, planning agencies risk misallocating infrastructure funds to projects with depreciating congestion-relief returns.

## **Research Questions**

What is the long-run elasticity of vehicle miles traveled (VMT) per capita with respect to highway lane-mile expansion along the Wasatch Front spine over a 3- to 10-year lag?

Does an increase in regional transit capacity (measured in transit vehicle revenue miles or passenger-miles delivered) produce a statistically significant suppression in the growth rate of regional highway VMT per capita?

What is the annualized public capital expenditure per net passenger-mile traveled (PMT) delivered across roadway expansions versus fixed-guideway transit over a 20-year lifecycle?

# **Datasets**

All data will be aggregated to annual intervals (2000–2024) across the 4-county regional spine (Weber, Davis, Salt Lake, and Utah counties):

**UDOT Traffic Monitoring System & Highway Performance Monitoring System (HPMS).** Historical annual Average Daily Traffic (AADT), centerline miles, and lane-mile inventories along the I-15/Legacy/Bangerter corridors.

**Federal Transit Administration (FTA) National Transit Database (NTD).** Historical annual agency profiles for the Utah Transit Authority (UTA), including Unlinked Passenger Trips (UPT), Passenger Miles Traveled (PMT), and Vehicle Revenue Miles (VRM) segmented by mode (Commuter Rail, Light Rail, Bus Rapid Transit, and Motorbus).

**Demographic & Macroeconomic Baselines.** County-level annual population, total employment, and labor force data from the Kem C. Gardner Policy Institute; historical annual retail gasoline price series from the U.S. Energy Information Administration (EIA).

**Capital Expenditure Records.** Historical capital outlays, facility investment schedules, and federal grant allocations compiled from UDOT Statewide Transportation Improvement Programs (STIP) and UTA Comprehensive Annual Financial Reports (CAFR/ACFR).

# **Methods**

**Metric Standardization & Harmonization.** Convert disparate modal units into common person-throughput metrics. Compute regional VMT per Capita and Transit PMT per Capita, converting highway vehicle counts using average regional vehicle occupancy rates (\~1.2 persons/vehicle).

**Dynamic Distributed Lag Modeling (Autoregressive Distributed Lag / ARDL).** Fit econometric time-series models with lagged capacity variables (1 to 5+ years) to estimate both short-run and long-run elasticities of travel demand while controlling for exogenous population, employment, and fuel price shocks:  
$\Delta \ ln(VM{T}_{t})\ =\ \alpha \ +\sum\limits_{k=0}^{p}\ {\beta }_{k}\Delta \ ln({LaneMiles}_{t-k})\ +\sum\limits_{j=0}^{q}\ {\gamma }_{j}\Delta \ ln({TransitCap}_{t-j})\ +{x}_{t}\theta \ +\ {\epsilon }_{t}$

**Structural Break & Intervention Analysis.** Identify whether major infrastructure milestones (e.g., 2008 FrontRunner North opening, 2012 FrontRunner South opening, 2018 UVX launch, major I-15 CORE expansions) caused structural shifts in corridor travel share using Chow tests or Bai-Perron break tests.

**Comparative Capital Efficiency Ratio.** Calculate net capital cost per annualized person-mile delivered across both modes over 10- and 20-year amortization windows.

# **Ethical Considerations**

Spine-level aggregation may mask disparities in transit access for low-income or car-less populations who do not live near regional rail hubs (Likelihood: High, Impact: Medium). To mitigate this, the study will explicitly acknowledge the regional macro scope and cross-reference findings against federal Title VI transit equity frameworks in the final report.

Results could be politicized to advocate for completely defunding one mode over another, ignoring the necessary complementary nature of feeder networks (Likelihood: Medium, Impact: High). The proposed mitigation is to frame conclusions around multimodal network synergy and optimal portfolio balance rather than zero-sum modal replacement.

Conflating temporary shocks (such as the 2020 remote-work shift) with structural citizen behavior changes presents an ethical risk (Likelihood: High, Impact: Medium). To address this, indicator dummy variables for the 2020–2022 pandemic period will be included to prevent macroeconomic anomalies from skewing elasticity coefficients.

# **Challenges / Issues**

**Limited Degrees of Freedom.** Analyzing 20–25 annual observations restricts the number of simultaneous lagged parameters that can be estimated without overfitting or degrees-of-freedom exhaustion.

**Capital Cost Normalization.** Disentangling pure capacity expansion costs from routine maintenance, safety improvements, and pavement resurfacing within historical agency financial statements.

**Exogenous Confounders.** Rapid, non-linear growth in telecommuting post-2020 and large-scale shifts in corporate tech employment along the Silicon Slopes corridor complicating traditional VMT-to-employment relationships.

# **References**

Duranton, G., & Turner, M. A. (2011). The fundamental law of road congestion: Evidence from US cities. *American Economic Review*, *101*(6), 2616–2652.

Federal Transit Administration. (n.d.). *National Transit Database (NTD) annual data products*. U.S. Department of Transportation.

Kem C. Gardner Policy Institute. (n.d.). *Utah demographic and economic data profiles*. David Eccles School of Business, University of Utah.

Litman, T. (2020). *Evaluating public transit benefits and costs*. Victoria Transport Policy Institute.

Utah Department of Transportation. (n.d.). *Annual traffic conditions and continuous count station summaries*. UDOT Program Development.