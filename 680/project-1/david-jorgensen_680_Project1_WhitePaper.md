# Capital Allocation and Travel Demand Elasticity: Highway Expansion vs. Multimodal Transit on the Wasatch Front (2000–2024)

**David Jorgensen**  
Department of Data Science, Bellevue University  
DSC680-T302 Applied Data Science | Professor Xu Ashton | September 26, 2026  

---

### Author Note & Abstract
Correspondence: David Jorgensen. Code: [datasci-school/680/project-1](https://github.com/CmdrJorgs/datasci-school/tree/main/680/project-1).  
**Abstract:** Evaluating 2000–2024 Wasatch Front investments ($N=25$), this paper estimates travel elasticities and lifecycle costs per passenger-mile traveled (PMT) via an ARDL model in first differences ($\Delta \ln$). While 2-year lag lane-mile elasticity is positive ($\beta_2 = +0.4125, p < 0.001$), cumulative elasticity is $+0.3054$ ($p = 0.230$), failing to reject zero cumulative induced demand at $N=22$. Transit elasticity is positive ($\gamma = +0.6977, p = 0.0096$), reflecting growth co-movement rather than driving suppression. Highways achieve lower regional costs ($0.103 vs. $0.947/PMT), but transit is superior in peak bottlenecks ($0.45–$0.85 vs. $1.40–$2.20/PMT).  
*Keywords:* induced demand, travel elasticity, ARDL, Wasatch Front, transit.
---

# Business Problem & Research Questions

Between 2000 and 2024, Wasatch Front population grew 53.0% (1.71M to 2.62M) and employment rose 57.9% (878.6k to 1,387.6k), prompting $22.09B in highway and $5.50B in transit outlays. Capacity induces latent travel, while transit requires density to amortize capital. Without cross-modal accounting, capital risks misallocation:

1. **RQ1 (Highway Elasticity):** Per capita freeway VMT elasticity to lane-miles? $H_{1,0}: \sum \beta_k = 0$; $H_{1,a}: 0.6 \le \sum \beta_k \le 1.0$ (Duranton & Turner, 2011).
2. **RQ2 (Transit Effect):** Does transit service suppress freeway VMT? $H_{2,0}: \gamma = 0$; $H_{2,a}: \gamma < 0$.
3. **RQ3 (Cost Efficiency):** Capital cost per PMT? $H_{3,0}: \text{Cost}_{\text{HW}} = \text{Cost}_{\text{Transit}}$; $H_{3,a}:$ Highway lower regionally, but transit superior in peak choke points.
---

# Background & Historical Context

The Wasatch Front is a 120-mile corridor bounded by mountains and the Great Salt Lake, funneling travel through a single spine (I-15, Legacy Parkway, FrontRunner rail, TRAX light rail) with bottlenecks at Point of the Mountain. Inversions trap $\text{PM}_{2.5}$, triggering Clean Air Act non-attainment (vehicles yield 42%–48% of precursors). Milestones include: 2002 Olympics I-15 ($1.59B); 2008 FrontRunner North/Legacy Parkway ($685M); 2012 I-15 CORE ($1.725B)/FrontRunner South; 2018 UVX BRT ($190M); 2020 Tech Corridor ($415M); and 2024 West Davis Highway ($750M). Downs (1962) and Duranton and Turner (2011) established induced demand ($\approx 1.03$ elasticity); Litman (2020) showed grade-separated transit sets a speed floor.
---

# Data Explanation, Preparation & Data Dictionary

Annual series (2000–2024, $N=25$) for Weber, Davis, Salt Lake, and Utah counties compile FRED, FHWA (VM-2, HM-60, SF-4C, HM-71/72), UDOT, and UTA (ACFR/NTD 80001) records. Freeway VMT is per capita ($\text{VMT\_PC}_t$); highway PMT assumes Average Vehicle Occupancy of 1.20; continuous series are log-differenced ($\Delta \ln$) for stationarity ($p=2$). $D_{\text{COVID}} = 1$ (2020–2021) controls for remote work. Missing values are zero. Transit VRM carries a 27.7% paratransit residual. FHWA shifts in 2004 (+4.99pp) and 2013 (+17.8%) were verified against UDOT counts.

### Key Fields Data Dictionary

| Field | Source | Description |
| :--- | :--- | :--- |
| `pop_wasatch_front` | Census | 4-county population |
| `emp_wasatch_front` | BLS | 4-county employment |
| `highway_lane_miles_freeway` | FHWA | Freeway lane-miles |
| `vmt_urban_freeway_per_capita` | Derived | Freeway VMT / capita |
| `transit_vrm_total` | UTA | Vehicle revenue miles |
| `highway_capital_outlay_millions`| FHWA | Highway capital ($M) |
| `transit_capital_outlay_millions`| UTA | Transit capital ($M) |
| `d_ln_vmt_pc` | Derived | Differenced $\ln(\text{VMT\_PC})$ |
---

# Econometric Methods & Model Justification

To estimate demand elasticities without spurious co-trending, we specify an **Autoregressive Distributed Lag (ARDL)** model in first differences:

$$\Delta \ln(\text{VMT\_PC}_t) = \alpha + \sum_{k=0}^2 \beta_k \Delta \ln(\text{LM}_{t-k}) + \gamma \Delta \ln(\text{VRM}_t) + \theta_1 \Delta \ln(\text{Emp}_t) + \theta_2 \Delta \ln(\text{Gas}_t) + \delta D_{\text{COVID}} + \epsilon_t$$

Where $\beta_0$ is contemporaneous elasticity, $\beta_1$ and $\beta_2$ are lagged adjustments, $\beta_{\text{LR}} = \sum_{k=0}^2 \beta_k$ is cumulative elasticity, and $\gamma$ is transit elasticity. ADF tests confirm $I(0)$ stationarity. Lags capture disruption ($k=0$), diversion ($k=1$), and sprawl ($k=2$). Standard errors use Newey-West HAC ($m = 2$). Levels OLS was rejected due to spurious co-trending ($R^2 > 0.95$, DW $< 0.90$); VAR due to sample size ($N=22$); ML lacked causal interpretability. Stability is verified via Chow and QLR tests against Andrews' (1993) 4.09 bound.
---

# Analysis & Empirical Findings

The ARDL model was estimated over 22 observations (2003–2024): $R^2 = 0.593$, Adjusted $R^2 = 0.389$, $F(7, 14) = 10.11$ ($p = 0.000154$), $\text{AIC} = -71.00$, $\text{BIC} = -62.27$.

### Primary Econometric Estimation Results

| Variable | Coef. | SE | $p$ | 95% CI |
| :--- | :--- | :--- | :--- | :--- |
| Constant ($\alpha$) | -0.0337 | 0.0150 | 0.0241 | [-0.0630, -0.0044] |
| $\Delta \ln(\text{LM}_t) \ [\beta_0]$ | -0.2265 | 0.1303 | 0.0822 | [-0.4820, +0.0289] |
| $\Delta \ln(\text{LM}_{t-1}) \ [\beta_1]$ | +0.1194 | 0.1614 | 0.4591 | [-0.1969, +0.4357] |
| $\Delta \ln(\text{LM}_{t-2}) \ [\beta_2]$ | **+0.4125** | 0.0874 | **< 0.0001** | [+0.2413, +0.5838] |
| $\Delta \ln(\text{VRM}_t) \ [\gamma]$ | **+0.6977** | 0.2692 | **0.0096** | [+0.1700, +1.2254] |
| $\Delta \ln(\text{Emp}_t) \ [\theta_1]$ | **+1.0151** | 0.4014 | **0.0114** | [+0.2284, +1.8018] |
| $\Delta \ln(\text{Gas}_t) \ [\theta_2]$ | -0.0745 | 0.0461 | 0.1058 | [-0.1648, +0.0158] |
| $D_{\text{COVID}} \ [\delta]$ | +0.0556 | 0.0411 | 0.1764 | [-0.0250, +0.1362] |

### Hypothesis Evaluation & Model Diagnostics
1. **Induced Demand ($H_1$):** Short-run elasticity is negative ($\beta_0 = -0.2265, p = 0.082$); Lag 2 confirms delayed induction ($\beta_2 = +0.4125, p < 0.0001$). Cumulative elasticity $\sum \beta_k = +0.3054$ ($SE = 0.2544, p = 0.2299, 95\%\text{ CI } [-0.1932, +0.8041]$) fails to reject $H_{1,0}$ at $N=22$. A Wald test rejects unit elasticity ($H_0: \sum \beta = 1.0, \chi^2 = 7.45, p = 0.0063$).
2. **Transit Effect ($H_2$):** Transit elasticity $\gamma = +0.6977$ ($p = 0.0096$) is positive, rejecting suppression ($H_{2,a}$) due to growth co-movement. Modal models confirm this: Bus+Rail $\gamma = +0.7151$ ($p = 0.0238$); Rail-only $\gamma = +0.4567$ ($p = 0.0373$).
3. **Cost Efficiency ($H_3$):** Regionally ($22.09B highway, $5.50B transit), highways delivered 213.8B PMT at **$0.1033/PMT** ($0.1393 real), and transit delivered 5.81B PMT at **$0.9467/PMT** ($1.3195 real) (9.16x nominal, 9.48x real). In peak bottlenecks (Point of the Mountain, I-15 CORE), highway widening costs **$1.40–$2.20/PMT** (mean $1.80/PMT), whereas transit costs **$0.45–$0.85/PMT** (mean $0.65/PMT) (0.20x–0.61x advantage; $H_{3,a}$ supported).
4. **Validation & Diagnostics:** Expanding-window CV (2015–2024, $N=10$): $\text{RMSE} = 0.0685$, $\text{MAE} = 0.0403$, out-of-sample $R^2 = -0.1993$. Residual tests: DW = 2.5515; Ljung-Box $p > 0.15$; Breusch-Pagan $p = 0.9909$; Shapiro-Wilk $p = 0.0330$; VIFs $< 4.5$. Chow tests at 2008 ($p = 0.0741$) and 2012 ($p = 0.0824$) show stability. QLR peaks at 2019 ($\sup F = 3.6915 < 4.09$ Andrews bound). Jackknife sums span $-0.0694$ to $+0.5097$; omitting 2012 yields $-0.0694$ ($p = 0.8207$).
---

# Visualizations & Empirical Illustrations

![Figure 1: Trajectories](figures/figure_1_longitudinal_trajectories.png)
*Figure 1.* Trajectories (2000–2024): freeway lane-miles (+133.3%) and VMT (+117.0%) outpaced population (+53.0%) and employment (+57.9%).

![Figure 2: Growth Trends](figures/figure_2_decoupling_growth_indices.png)
*Figure 2.* Growth indices (2000 = 100): per capita VMT rose 41.8% to 3,598 miles (peaking at 3,722 in 2019).

![Figure 3: Elasticity Profile](figures/figure_3_elasticity_profile.png)
*Figure 3.* ARDL elasticities (95% HAC CI): disruption ($\beta_0 = -0.2265$), delayed induction ($\beta_2 = +0.4125, p < 0.001$), cumulative sum (+0.3054).

![Figure 4: Structural Breaks](figures/figure_4_structural_break_analysis.png)
*Figure 4.* Transit PMT share (peak 3.52% in 2012; 2.23% in 2024) and Chow $F$-sequence vs. Andrews' 4.09 bound.

![Figure 5: Capital Efficiency](figures/figure_5_capital_efficiency.png)
*Figure 5.* Outlays ($22.09B vs. $5.50B) and cost per PMT ($0.103 vs. $0.947 regional; $1.80 vs. $0.65 in choke points).
---

# Conclusion

1. **Highway Elasticity:** Lane additions induce delayed driving ($\beta_2 = +0.4125, p < 0.0001$), though cumulative elasticity (+0.3054, $p = 0.230$) spans zero at $N=22$; unit elasticity is rejected ($p = 0.0063$).
2. **Transit Effect:** Transit co-moves with driving ($\gamma = +0.6977, p = 0.0096$), reflecting shared growth rather than suppression.
3. **Cost Efficiency:** Highways deliver lower regional costs per PMT, while transit achieves superior capital efficiency in peak choke points.

**Takeaway:** Highway widening cannot resolve corridor congestion due to delayed rebound; agencies must manage corridors multimodally with transit as a peak relief valve.
---

# Assumptions & Limitations

### Assumptions
Average Vehicle Occupancy is 1.20 (sensitivity 1.10–1.67 yields $0.074–$0.113/PMT). The 4-county spine captures >80% of Utah population. Employment and fuel prices are weakly exogenous; differencing ensures stationarity. Paratransit scales with fixed routes.

### Limitations
Small sample size ($N=22$) limits lag depth. Lane-miles expanded via four mega-projects (2008, 2012, 2020, 2024). FHWA shifts in 2004 (+4.99pp) and 2013 (+17.8%) introduce minor measurement shifts. Table SF-4C captures statewide disbursements, giving a conservative highway baseline.
---

# Challenges Encountered & Solutions

FHWA shifts were resolved by cross-checking UDOT counts. Spurious macro trends were eliminated via stationary first differences ($\Delta \ln$). Small-sample constraints were managed with a parsimonious lag structure ($p=2$) and jackknife testing. Transit paratransit residuals were verified via modal sub-models.
---

# Future Uses & Additional Applications

Empirical lag elasticities can calibrate WFRC and MAG travel demand models, inform dynamic traffic assignment at Point of the Mountain, guide transit value-capture frameworks, and refine Clean Air Act SIP emissions forecasting.
---

# Recommendations & Implementation Plan

### Policy Recommendations
1. **Multimodal Accounting:** Evaluate investments by peak choke-point cost per PMT.
2. **Congestion Pricing:** Implement variable congestion pricing on freeways.
3. **TOD Zoning:** Mandate high-density zoning (25–45 units/acre) around stations.
4. **Off-Peak Transit:** Expand midday and weekend transit for all-day utility.

### Phased Implementation Roadmap

| Phase | Years | Lead | Deliverables |
| :--- | :--- | :--- | :--- |
| **1: Alignment** | 1–2 | UDOT/WFRC/MAG | Corridor metrics; monitoring; STIP update |
| **2: Rebalancing** | 3–5 | UDOT/UTA/State | Dynamic pricing; FrontRunner double-tracking; TOD incentives |
| **3: Maturation** | 6–10 | UTA/UDOT/Cities | FrontRunner electrification; regional BRT; electric fleet |
---

# Ethical Assessment

### Concerns, Likelihood & Impact Matrix

| Concern | Risk | Mitigation |
| :--- | :--- | :--- |
| **Transit Equity Disparities** | High | Screen capital plans against Title VI and EPA EJScreen |
| **Policy Misuse of Ratios** | High | Emphasize corridor complementarity and peak transit efficiency |
| **Pandemic Trend Distortion** | Med | Apply COVID controls to prevent highway over-building |
| **Data Provenance Vulnerability** | Med | Document transformations and publish replication code |

### Regulatory Compliance & Ethical Data Acquisition
Data were compiled from public federal and state repositories under Title 23/49 U.S.C., NEPA, and Clean Air Act conformity (40 CFR Part 93), without personal data.
---

# Code & Reproducibility

- **Repository:** [https://github.com/CmdrJorgs/datasci-school](https://github.com/CmdrJorgs/datasci-school)
- **Primary Notebook:** [680/project-1/david-jorgensen_680_Project1.ipynb](https://github.com/CmdrJorgs/datasci-school/blob/main/680/project-1/david-jorgensen_680_Project1.ipynb)
- **Environment:** Python 3.10+, `statsmodels 0.14+`, `pandas 2.0+`, `matplotlib 3.8+`, `seaborn 0.13+`. Data: `data/wasatch_front_transportation_2000_2024.csv`.
---

# Milestone 3 Audience Defense Questions

1. **Transit Sign:** Why is $\gamma = +0.6977$ positive, reflecting growth co-movement rather than suppression?
2. **Lagged vs. Cumulative:** Why is Lag 2 ($\beta_2 = +0.4125$) significant while cumulative elasticity (+0.3054) spans zero?
3. **Unit Elasticity:** Why does the model reject unit elasticity ($p = 0.0063$)?
4. **AVO Sensitivity:** How sensitive is cost per PMT to vehicle occupancy assumptions (1.10–1.67)?
5. **Cross-Validation:** Why does out-of-sample $R^2 = -0.1993$ not invalidate explanatory findings?
6. **FHWA Shifts:** How were 2004 (+4.99pp) and 2013 (+17.8%) FHWA shifts verified with UDOT counts?
7. **QLR Bound:** Why does the 2019 Chow test fail to break Andrews' 4.09 bound?
8. **Jackknife Influence:** Why does omitting 2012 flip cumulative elasticity from $+0.3054$ to $-0.0694$?
9. **Choke-Point Costs:** Why invest in transit when regional highway cost per PMT ($0.103) is below transit ($0.947)?
10. **Post-COVID Alignment:** How should capital allocation adapt to hybrid work and flattened peaks?
---

# Appendix: Supporting Documentation & Proofs

### Appendix A: Proof of Long-Run Elasticity in ARDL Models
In an $\text{ARDL}(p, q)$ model where $y_t = \ln(\text{VMT}_t)$ and $x_t = \ln(\text{LaneMiles}_t)$:

$$y_t = \alpha + \sum_{i=1}^p \rho_i y_{t-i} + \sum_{k=0}^q \beta_k x_{t-k} + \mathbf{Z}_t \boldsymbol{\theta} + \epsilon_t$$

In steady state ($y_t = y^*, x_t = x^*$):

$$y^* \left(1 - \sum_{i=1}^p \rho_i\right) = \alpha + x^* \sum_{k=0}^q \beta_k + \mathbf{Z}^* \boldsymbol{\theta} \implies \mathcal{E}_{\text{LR}} = \frac{\partial y^*}{\partial x^*} = \frac{\sum_{k=0}^q \beta_k}{1 - \sum_{i=1}^p \rho_i}$$

Without autoregressive terms ($\rho_i = 0$):

$$\mathcal{E}_{\text{LR}} = \sum_{k=0}^q \beta_k = \beta_0 + \beta_1 + \dots + \beta_q$$

Thus, the sum of distributed lag coefficients directly measures cumulative long-run travel demand elasticity.
---

# References (APA 7th Edition)

- Andrews, D. W. K. (1993). Tests for parameter instability and structural change with unknown change point. *Econometrica*, 61(4), 821–856.
- Downs, A. (1962). The law of peak-hour expressway congestion. *Traffic Quarterly*, 16(3), 393–409.
- Duranton, G., & Turner, M. A. (2011). The fundamental law of road congestion: Evidence from US cities. *American Economic Review*, 101(6), 2616–2652.
- Federal Highway Administration. (2000–2023). *Highway statistics: Tables VM-2, HM-60, SF-4C, HM-71, HM-72*. USDOT.
- Federal Transit Administration. (2000–2024). *National Transit Database: Agency 80001*. USDOT.
- Greene, W. H. (2018). *Econometric analysis* (8th ed.). Pearson.
- Hymel, K. M. (2014). Do traffic congestion relief policies work? *Journal of Urban Economics*, 80, 97–112.
- Litman, T. (2020). *Evaluating public transit benefits and costs: Best practices guidebook*. VTPI.
- Mogridge, M. J. (1997). The self-defeating nature of urban road capacity policy. *Transport Policy*, 4(1), 5–23.
- Newey, W. K., & West, K. D. (1987). A simple positive semi-definite, HAC covariance matrix. *Econometrica*, 55(3), 703–708.
- U.S. Bureau of Labor Statistics. (2024). *Local area unemployment statistics: Utah counties*. USDOL.
- U.S. Census Bureau. (2024). *Annual population estimates for Utah counties: 2000 to 2024*. USDOC.
- U.S. Energy Information Administration. (2024). *Rocky Mountain regular retail gasoline prices*. USDOE.
- Utah Department of Transportation. (2024). *Annual traffic conditions and count station summaries*. UDOT.
- Utah Transit Authority. (2000–2025). *Annual Comprehensive Financial Reports*. UTA.
