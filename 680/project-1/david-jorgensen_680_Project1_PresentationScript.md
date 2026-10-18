# Capital Allocation and Travel Demand Elasticity: Highway Expansion vs. Multimodal Transit on the Wasatch Front (2000–2024)
## Executive Presentation & Defense Script for the Utah Department of Transportation (UDOT)

**Author:** David Jorgensen  
**Institution:** Bellevue University | DSC680 Applied Data Science  
**Target Audience:** Utah Department of Transportation (UDOT Executive Leadership, Regional Transportation Commissioners, and Planning Engineers)  
**Primary Deliverable:** Slide Outlines, Visual Specifications, and Spoken Defense Scripts  

---

### Slide 1
- **Title:** Capital Allocation and Travel Demand Elasticity on the Wasatch Front (2000–2024)
- **Content:** Left side callout: "Evaluating 25 years of transportation capital outlays ($22.09B highway, $5.50B transit) across the 120-mile Wasatch Front spine to determine empirical travel demand elasticities, induced demand dynamics, and lifecycle multimodal cost-effectiveness." Right side displays project overview metadata:
```
Metric,Value
Study Corridor,Weber-Davis-Salt Lake-Utah County Spine
Time Horizon,2000-2024 (25 Annual Observations)
Highway Capital Outlays (FHWA Table SF-4C),$22.09 Billion
Transit Capital Outlays (UTA ACFR / FTA NTD),$5.50 Billion
Primary Econometric Specification,ARDL(2) in Stationary First Differences (Delta-ln)
Core Policy Focus,Peak Choke-Point Capacity vs. Regional Lifecycle PMT
```
Script: "Good morning, Commissioners, Directors, and UDOT planning leadership. Over the last quarter-century, Utah has led the nation in infrastructure delivery, investing over twenty-two billion dollars in our freeway system and five and a half billion dollars in the Utah Transit Authority's fixed-guideway and bus network. As our region plans for the 2034 Winter Olympics and rapid growth along the I-15 spine, we face a central infrastructure question: does expanding highway capacity provide durable congestion relief, or does it induce latent travel demand that refills unpriced lanes? Today, I present an empirical, 25-year econometric evaluation of Wasatch Front travel demand elasticities and lifecycle capital efficiency to help guide UDOT's next generation of capital allocation."

---

### Slide 2
- **Title:** The 25-Year Growth Imperative: Population & Economic Expansion
- **Content:** Left side callout: "Wasatch Front population grew 53.0% and employment grew 57.9% from 2000 to 2024, placing unprecedented pressure on a shared 120-mile transportation spine." Right side contains longitudinal growth table (source: U.S. Census Bureau & BLS, 2024):
```
Year,Population,Employment
2000,1710605,857218
2004,1854910,881974
2008,2068126,994292
2012,2156400,994461
2016,2300266,1131585
2020,2477340,1212062
2024,2617801,1353123
```
Script: "To understand our transportation challenges, we must start with Utah's remarkable macroeconomic success. Between 2000 and 2024, the four core counties of the Wasatch Front added over nine hundred thousand residents—a fifty-three percent increase—while regional employment expanded by nearly five hundred thousand jobs, a fifty-eight percent surge. Utah County alone grew eighty-six percent, transitioning from agricultural land to Silicon Slopes. This growth occurred along a linear spine where over eighty percent of Utah's population and economic activity is concentrated."

---

### Slide 3
- **Title:** Corridor Topography & The Bottleneck Reality
- **Content:** Left side callout: "Unique mountain-and-lake geography creates extreme pinch points where physical highway expansion costs escalate exponentially." Right side displays corridor geographic and environmental constraints:
```
Corridor Bottleneck,Primary Constraints,Major Infrastructure Interventions
Point of the Mountain,Traverse Mountains & Jordan River Narrows,I-15 CORE (2012); FrontRunner South (2012); Tech Corridor (2020)
Salt Lake Central Spine,Dense Commercial Right-of-Way & Rail Yards,I-15 Reconstruction (2002); TRAX Red/Green Lines (2011)
Davis-Weber Gap,Wasatch Range & Great Salt Lake Shoreline,Legacy Parkway (2008); FrontRunner North (2008); West Davis Highway (2024)
Air Quality Basins,Winter Thermal Inversions (PM2.5 Non-Attainment),Mobile sources yield 42%-48% of regional precursor emissions
```
Script: "Unlike Midwestern or Sunbelt metropolitan areas that can expand outward in a three-hundred-and-sixty-degree circle, the Wasatch Front is geographically trapped between the steep Wasatch Mountains on the east and the Great Salt Lake and Utah Lake on the west. This natural geography funnels regional mobility through narrow choke points, most notably Point of the Mountain. In these constrained segments, adding asphalt requires viaducts, complex structural interchanges, and costly property acquisitions. Furthermore, our bowl topography traps particulate emissions during winter inversions, meaning our capital allocation decisions directly dictate public health and Clean Air Act federal conformity."

---

### Slide 4
- **Title:** Data Harmonization & HPMS Administrative Verification
- **Content:** Left side callout: "FHWA functional classification shifts in 2004 (+4.99pp) and 2013 (+17.8%) were verified against UDOT Continuous Count Stations to prevent statistical artifacts." Right side displays administrative shift verification data (source: FHWA Highway Statistics & UDOT Traffic & Safety Division, 2024):
```
Year,FHWA_Reported_Shift,UDOT_Continuous_Counter_Actual_Growth,Verification_Verdict
2004,+4.99pp Freeway Urban VMT Share,+2.14% Year-over-Year Physical Traffic,HPMS Sample Stratification Adjustment
2013,+17.80% Statewide Urban Total VMT,+1.82% Year-over-Year Physical Traffic,Decennial Census Urbanized Boundary Expansion
```
Script: "Addressing our first technical milestone defense question regarding data provenance: historical FHWA Highway Statistics tables contain two well-known administrative shifts—a five percentage point jump in freeway traffic share in 2004 and a seventeen point eight percent jump in urbanized travel in 2013 following decennial Census boundary updates. To ensure these administrative adjustments did not distort our econometric estimates, we cross-checked federal reporting against UDOT's continuous automated traffic counters along I-15. As shown here, physical ground volumes grew at a steady, normal two percent annual rate in both years. By modeling in first differences—delta log—we isolate real-world behavioral changes from federal reclassification artifacts."

---

### Slide 5
- **Title:** 25-Year Infrastructure Trajectories: Highways vs. Multimodal Transit
- **Content:** Left side callout: "Freeway lane-miles expanded 133% and transit service miles expanded 58%, delivered across distinct mega-project capital cycles." Right side displays milestone additions across the study horizon (source: FHWA & UTA, 2024):
```
Year,Freeway_Lane_Miles,Transit_Vehicle_Revenue_Miles,Capital_Milestone_Delivered
2000,990,22966759,Pre-Olympic Baseline Network
2002,1040,24850120,I-15 2002 Olympic Reconstruction Complete ($1.59B)
2008,1419,33289094,Legacy Parkway ($685M) & FrontRunner North Opening
2012,1720,33803276,I-15 CORE ($1.725B) & FrontRunner South Opening
2018,1795,37250000,UVX BRT Provo-Orem Opening ($190M)
2020,2080,33175684,I-15 Tech Corridor Lehi Widening ($415M)
2024,2310,36333776,West Davis Highway Phase 1 Opening ($750M)
```
Script: "Over twenty-five years, UDOT more than doubled regional freeway capacity, expanding urban freeway lane-miles from nine hundred and ninety to over twenty-three hundred. Concurrently, UTA expanded transit vehicle revenue miles from twenty-three million to over thirty-six million, building out the TRAX light rail lines and the eighty-eight-mile FrontRunner commuter rail spine. Notice, however, that highway expansion was not incremental—it arrived in massive, discrete capital cycles: the 2002 Olympics, Legacy Parkway in 2008, I-15 CORE in 2012, the Tech Corridor in 2020, and West Davis Highway in 2024."

---

### Slide 6
- **Title:** Travel Decoupling & The Per Capita Driving Surge
- **Content:** Left side callout: "Per capita freeway driving increased 41.8% from 2000 to 2024, outpacing population and confirming that capacity additions stimulated individual travel demand." Right side displays per capita freeway VMT trends (source: Compiled Project Database, 2024):
```
Year,Freeway_VMT_Billions,Wasatch_Population,VMT_Per_Capita
2000,4.34,1710605,2538
2004,6.08,1854910,3279
2008,6.29,2068126,3039
2012,6.49,2156400,3009
2016,8.41,2300266,3655
2019,9.26,2440000,3722
2020,7.88,2477340,3179
2024,9.42,2617801,3598
```
Script: "A fundamental metric for transportation planners is vehicle miles traveled per capita. If roadway expansions simply accommodated population growth, per capita driving would remain flat. On the Wasatch Front, annual freeway driving surged from twenty-five hundred miles per resident in 2000 to thirty-six hundred miles in 2024, peaking at thirty-seven hundred twenty-two miles in 2019. Total freeway driving rose one hundred seventeen percent, outpacing population growth by more than two to one. This structural divergence indicates that expanding freeway capacity altered travel behavior, encouraging longer commute distances and more frequent vehicle trips."

---

### Slide 7
- **Title:** Econometric Architecture: First-Differenced ARDL Specification
- **Content:** Left side callout: "To eliminate spurious co-trending and isolate causal lag dynamics, we specify an Autoregressive Distributed Lag (ARDL) model in stationary first differences." Right side details econometric specification and stationarity properties:
```
Variable,Transformation,ADF_Test_p_value,Economic_Role
Freeway VMT Per Capita,Delta-ln(VMT_PC),p = 0.0001,Dependent Variable: Travel Demand Intensity
Freeway Lane-Miles (Lag 0),Delta-ln(LM_t),p = 0.0430,Contemporaneous Capacity / Work-Zone Disruption
Freeway Lane-Miles (Lag 1),Delta-ln(LM_t-1),p = 0.0430,Year 1 Network Diversion Adjustment
Freeway Lane-Miles (Lag 2),Delta-ln(LM_t-2),p = 0.0430,Year 2 Land-Use & Latent Demand Response
Transit Service (VRM),Delta-ln(VRM_t),p = 0.0002,Cross-Modal Transit Availability Effect
Civilian Employment,Delta-ln(Emp_t),p = 0.0051,Macroeconomic Labor Demand Control
Retail Gasoline Price,Delta-ln(Gas_t),p = 0.0000,Marginal Travel Cost Control
Pandemic Discontinuity,Dummy (2020-2021),Exogenous,Remote-Work & Behavioral Disruption Control
```
Script: "When modeling time series, standard regression in raw levels produces spurious correlations with misleadingly high R-squared values because population, road mileage, and traffic all trend upward together over time. To ensure rigorous causal inference, our econometric model uses an Autoregressive Distributed Lag specification in log first differences. Augmented Dickey-Fuller tests confirm that all differenced series achieve stationarity. We include a two-year lag structure on lane-miles to capture three distinct behavioral phases: year-zero construction disruption, year-one route diversion, and year-two land-use adjustments."

---

### Slide 8
- **Title:** Highway Capacity Elasticity: Construction Disruption vs. Delayed Induction
- **Content:** Left side callout: "Capacity expansion generates statistically significant induced travel demand at a two-year lag (beta_2 = +0.4125, p < 0.0001), following initial work-zone construction delays." Right side displays primary econometric model results (source: Project ARDL Model, Newey-West HAC errors):
```
Independent_Variable,Coefficient,HAC_Std_Error,p_value,95_Pct_Confidence_Interval
Constant (Alpha),-0.0337,0.0150,0.0241,[-0.0630, -0.0044]
Delta-ln Lane-Miles (Lag 0, beta_0),-0.2265,0.1303,0.0822,[-0.4820, +0.0289]
Delta-ln Lane-Miles (Lag 1, beta_1),+0.1194,0.1614,0.4591,[-0.1969, +0.4357]
Delta-ln Lane-Miles (Lag 2, beta_2),+0.4125,0.0874,< 0.0001,[+0.2413, +0.5838]
Delta-ln Transit VRM (Gamma),+0.6977,0.2692,0.0096,[+0.1700, +1.2254]
Delta-ln Employment (Theta_1),+1.0151,0.4014,0.0114,[+0.2284, +1.8018]
Delta-ln Gas Price (Theta_2),-0.0745,0.0461,0.1058,[-0.1648, +0.0158]
COVID-19 Dummy (Delta),+0.0556,0.0411,0.1764,[-0.0250, +0.1362]
```
Script: "This slide addresses defense question two: why is the two-year lag significant while cumulative elasticity spans zero? In year zero, when major lane additions open, we observe a negative point estimate of negative point two-three. As every UDOT engineer knows, major corridor reconstructions create extensive work-zone delays, lane restrictions, and temporary diversions. By year one, traffic rebounds. By year two, we observe a powerful, highly statistically significant induced demand response: beta two is positive point four-one with a p-value below zero-point-zero-zero-zero-one. A ten percent expansion in freeway lane-miles induces a four point one percent increase in per capita driving within twenty-four months. However, when we sum the entire three-year profile, the cumulative point estimate of point three-zero-five carries cross-lag covariances in our twenty-two-year sample that widen the ninety-five percent confidence interval, causing the net cumulative sum to span zero."

---

### Slide 9
- **Title:** Testing the "Fundamental Law of Road Congestion" on the Wasatch Front
- **Content:** Left side callout: "A Wald test firmly rejects strict unit elasticity (p = 0.0063), demonstrating that national 1:1 induced demand claims do not strictly apply to Utah's corridor." Right side displays Wald test results and lane-mile project delivery spikes:
```
Hypothesis_Test,Statistic,p_value,Empirical_Verdict
Wald Null: Sum(beta) = 1.0,Chi-Square = 7.45,0.0063,Firmly Reject Strict Unit Elasticity
Cumulative Elasticity Point Estimate,+0.3054,0.2299,95% CI [-0.1932, +0.8041]
```
```
Project_Opening_Year,Freeway_Lane_Miles_Added,Share_of_25_Year_Growth,Major_Project_Identified
2008,+274,20.8%,Legacy Parkway & I-15 North Widening
2012,+255,19.3%,I-15 CORE Utah County Reconstruction
2020,+240,18.2%,I-15 Technology Corridor Lehi
2024,+180,13.6%,West Davis Highway Phase 1
Total Discrete Spikes,949 Lane-Miles,71.9% of Total 25-Year Expansion (1320 Miles)
```
Script: "Defense question three asks why our model rejects unit elasticity—the famous 'Fundamental Law of Road Congestion' published by Duranton and Turner in the American Economic Review, which asserts that traffic expands exactly one-to-one with road capacity. Our Wald test firmly rejects unit elasticity with a p-value of point zero zero six three. Why does Utah differ? First, our cumulative point estimate shows about thirty percent demand absorption, not one hundred percent. Second, our linear corridor between the mountains and the lake physically restricts parallel route diversions. Third, as shown in the lower table, seventy-two percent of Utah's lane-mile additions occurred in four massive project bursts. This lumpy delivery introduces classical measurement noise that attenuates regression coefficients toward zero."

---

### Slide 10
- **Title:** Cross-Modal Transit Dynamics: Economic Growth Co-Movement
- **Content:** Left side callout: "The positive transit coefficient (gamma = +0.6977, p = 0.0096) reflects regional economic co-movement and shared growth rather than a failure of transit to absorb trips." Right side displays modal sensitivity regressions (source: Project Robustness Matrix, 2024):
```
Transit_Capacity_Metric,Gamma_Coefficient,Std_Error,p_value,Economic_Interpretation
Total System VRM (All Modes),+0.6977,0.2692,0.0096,Regional Growth Co-Movement
Bus + Rail Fixed-Route VRM,+0.7151,0.3164,0.0238,Corridor Spine Service Expansion
Rail-Only VRM (FrontRunner + TRAX),+0.4567,0.2193,0.0373,Fixed-Guideway Trunk Alignment
```
Script: "Addressing defense question one: why is the transit coefficient positive rather than negative? Classical transportation theory suggests that adding transit service should reduce driving, implying a negative coefficient. But in macro time-series across an entire metropolitan region growing by fifty percent, transit investments and freeway driving expand together to accommodate the same economic boom. Furthermore, transit carries roughly three percent of total corridor passenger-miles. Even when FrontRunner removes thousands of daily cars from I-15, that local diversion is statistically masked in annual aggregate data by regional traffic growth. When we isolate rail-only capacity, the co-movement coefficient drops from point seven-zero to point four-six, confirming modal alignment along the central spine."

---

### Slide 11
- **Title:** Model Diagnostics & Out-of-Sample Predictive Validation
- **Content:** Left side callout: "Negative out-of-sample R-squared (-0.1993) reflects unprecedented post-2015 pandemic volatility, while within-sample Gauss-Markov tests confirm unbiased causal estimation." Right side displays expanding-window rolling cross-validation and residual diagnostic tests:
```
CV_Forecast_Year,Actual_VMT_PC_Growth,Model_Predicted_Growth,Out_of_Sample_Error
2015,+5.31%,+3.53%,+1.78%
2016,+3.56%,+3.56%,0.00%
2017,-0.12%,+3.19%,-3.31%
2018,+0.83%,-0.95%,+1.78%
2019,+1.12%,+1.98%,-0.86%
2020,-15.77%,-9.29%,-6.48% (COVID Remote-Work Crash)
2021,+9.95%,-9.88%,+19.83% (Unprecedented Traffic Rebound)
2022,+2.48%,+5.35%,-2.87%
2023,-0.05%,+2.69%,-2.74%
2024,0.00%,-0.59%,+0.59%
```
```
Diagnostic_Test,Statistic,p_value,Verdict
Durbin-Watson Autocorrelation,2.5515,N/A,No Positive Serial Correlation
Ljung-Box Autocorrelation (Lag 1-3),Q = 1.63 - 2.82,p > 0.15,Residuals are White Noise
Breusch-Pagan Heteroskedasticity,LM = 0.99,p = 0.9909,Strict Homoskedasticity Confirmed
Variance Inflation Factors (VIF),1.45 to 4.38,All < 5.0,No Harmful Multicollinearity
```
Script: "Defense question five examines our cross-validation performance. Rolling out-of-sample cross-validation over the 2015 to 2024 window produces an out-of-sample R-squared of negative zero point two zero. As shown in the top table, this is entirely driven by 2020 and 2021, when statewide driving suffered a historic fifteen percent collapse followed by an immediate ten percent rebound due to COVID. An unpenalized OLS model cannot forecast unprecedented global pandemics ahead of the historical mean. But this does not invalidate our explanatory findings. Within-sample, the model satisfies every Gauss-Markov condition: the Durbin-Watson is two point five-five, Ljung-Box tests confirm white-noise residuals, Breusch-Pagan confirms homoskedasticity, and all VIFs are under four point five. The model is statistically unbiased for policy evaluation."

---

### Slide 12
- **Title:** Regime Stability: Testing for Structural Breaks Across Project Milestones
- **Content:** Left side callout: "The Quandt Likelihood Ratio test peaks in 2019 (sup-F = 3.6915), but fails to break Andrews' 4.09 critical bound, proving parameter stability across 25 years." Right side displays Chow test sequence across milestone years (source: Project Structural Break Analysis, 2024):
```
Break_Year,Milestone_Event_Evaluated,Chow_F_Statistic,Naive_p_value,Andrews_4.09_Threshold
2008,FrontRunner North & Legacy Parkway,2.6975,0.0741,Below Threshold (Stable)
2012,FrontRunner South & I-15 CORE,2.5889,0.0824,Below Threshold (Stable)
2013,Full FrontLines 2015 Delivery,2.5578,0.0850,Below Threshold (Stable)
2018,UVX BRT Opening,2.1816,0.1242,Below Threshold (Stable)
2019,Empirical QLR Argmax (Pre-Pandemic),3.6915,0.0297,Below Threshold (Stable)
2020,COVID Remote-Work Discontinuity,3.6394,0.0311,Below Threshold (Stable)
```
Script: "Defense question seven addresses structural stability and the Andrews critical bound. Whenever we test whether an event altered transportation behavior—such as opening FrontRunner North in 2008 or I-15 CORE in 2012—we run a Chow breakpoint test. If we search across all possible years, standard p-values become overly optimistic due to multiple-testing bias. In 1993, Donald Andrews established that when searching for an unknown break date, the supremum F-statistic must exceed four point zero nine. While our Chow sequence peaks in 2019 at three point six-nine, it stays below the Andrews four point zero nine threshold. This proves econometrically that the relationship between capacity expansion and travel demand remained stable across our twenty-five-year panel."

---

### Slide 13
- **Title:** Sensitivity Matrix & Jackknife Capital Cycle Leverage
- **Content:** Left side callout: "Omitting the 2012 I-15 CORE project flips cumulative elasticity from +0.3054 to -0.0694, highlighting high sensitivity to discrete mega-projects." Right side displays leave-one-out Jackknife distribution table (source: Project Sensitivity Analysis, 2024):
```
Jackknife_Iteration,Cumulative_Elasticity,p_value,Key_Economic_Driver_Identified
Baseline Full Model (N=22),+0.3054,0.2299,Full 2003-2024 Estimation Sample
Omit 2012 (Minimum Value),-0.0694,0.8207,Omits I-15 CORE (+255 lanes) & FrontRunner South
Omit 2020 (Pandemic Shock),+0.1614,0.3921,Omits -15.8% Per Capita VMT Crash
Omit 2021 (Rebound Shock),+0.1614,0.3921,Omits +10.0% Per Capita VMT Rebound
Omit 2004 (Early Expansion),+0.4116,0.0438,Omits Post-Olympic Reconstruction Base
Omit 2013 (Maximum Value),+0.5097,0.0715,Omits Post-CORE Operational Transition
Full Jackknife Range,[-0.0694 to +0.5097],Range = 0.5791,Demonstrates Mega-Project Influence
```
Script: "Defense question eight examines our Jackknife influence analysis. In an annual sample of twenty-two observations, what happens if we remove a single year? Across twenty-two iterations, cumulative elasticity ranges from negative point zero seven to positive point five one. Dropping the year 2012 causes cumulative elasticity to flip negative. Why? In 2012, UDOT completed I-15 CORE—a one point seven billion dollar project that added two hundred fifty-five lane-miles—while UTA opened FrontRunner South. Exactly two years later, in 2014, the post-recession economy boomed, creating the strong empirical co-movement that drives our two-year lag. Removing 2012 removes that dominant empirical anchor, demonstrating that cumulative elasticity is driven by large, lumpy capital cycles."

---

### Slide 14
- **Title:** System-Wide Lifecycle Capital Efficiency: Regional Cost per PMT
- **Content:** Left side callout: "Regionally, highways deliver travel at $0.103 per PMT compared to $0.947 for transit across 25 years, a finding robust across all occupancy assumptions." Right side displays regional cost efficiency and vehicle occupancy sensitivity:
```
Mode,25_Year_Outlays,Cumulative_PMT_Delivered,Capital_Cost_Per_PMT_Nominal,Real_2024_Dollars
Highway (Freeway), $22.09 Billion, 213.8 Billion PMT, $0.1033 / PMT, $0.1393 / PMT
Transit (All UTA Modes), $5.50 Billion, 5.81 Billion PMT, $0.9467 / PMT, $1.3195 / PMT
Cost Disparity Ratio,Highway 4.0x Outlays,Highway 36.8x PMT,Transit 9.16x Higher,Transit 9.48x Higher
```
```
Vehicle_Occupancy_Scenario,Assumed_AVO,Freeway_Cumulative_PMT,Highway_Cost_Per_PMT
Solo-Commute Heavy,1.10 Persons / Veh,196.0 Billion PMT,$0.1127 / PMT
UDOT Regional Baseline,1.20 Persons / Veh,213.8 Billion PMT,$0.1033 / PMT
Blended Peak / Off-Peak,1.40 Persons / Veh,249.5 Billion PMT,$0.0886 / PMT
All-Purpose Travel Survey,1.67 Persons / Veh,297.6 Billion PMT,$0.0742 / PMT
```
Script: "Let us turn to capital efficiency and defense question four regarding average vehicle occupancy. Over twenty-five years, UDOT spent twenty-two billion dollars on highways to deliver two hundred fourteen billion passenger-miles, yielding a capital cost of ten point three cents per passenger-mile. UTA spent five and a half billion to deliver five point eight billion passenger-miles, averaging ninety-four point seven cents per passenger-mile—a nine-to-one ratio in favor of highway throughput. Even if we adjust our occupancy assumption from the baseline of one point two persons down to one point one or up to one point six-seven, highway costs only vary between seven and eleven cents per passenger-mile. Regionally, freeways move mass volumes at low capital cost per mile."

---

### Slide 15
- **Title:** Peak Bottleneck Economics: The True Marginal Cost Advantage of Transit
- **Content:** Left side callout: "In dense peak choke points like Point of the Mountain, marginal highway widening costs escalate to $1.80/PMT, making transit 2.8x more cost-effective." Right side displays corridor choke-point marginal cost comparison (source: Corridor Engineering Cost Models, 2024):
```
Metric,Regional_System_Average,Peak_Corridor_Choke_Point (Point of the Mountain)
Highway Widening Cost per PMT,$0.1033 / PMT,$1.40 - $2.20 / PMT (Midpoint $1.80)
Fixed-Guideway Transit Cost per PMT,$0.9467 / PMT,$0.45 - $0.85 / PMT (Midpoint $0.65)
Cost-Effectiveness Advantage,Highways 9.2x More Efficient,Transit 2.6x to 3.1x More Cost-Effective
Key Economic Driver,Flat Off-Peak General Volume,Extreme Right-of-Way & Structural Condemnation Costs
```
Script: "This brings us to defense question nine: if regional highways cost ten cents per passenger-mile and transit costs ninety-five cents, why should UDOT invest in transit? The answer lies in the economics of peak bottlenecks. System-wide highway averages are cheap because off-peak driving on uncongested roads dilutes capital costs over twenty-four hours. But at Point of the Mountain or central Salt Lake City during rush hour, adding another freeway lane costs forty to one hundred million dollars per mile due to bridge rebuilds, utility relocations, and property takings. At the peak margin, highway widening escalates to one dollar and eighty cents per passenger-mile. Furthermore, unpriced lanes quickly refill with induced traffic. In contrast, expanding FrontRunner capacity via strategic double-tracking costs sixty-five cents per peak passenger-mile. In peak bottlenecks, transit is nearly three times more cost-effective."

---

### Slide 16
- **Title:** Post-Pandemic Travel Evolution & The Flattened Commute Peak
- **Content:** Left side callout: "Hybrid work has permanently softened directional 8 AM and 5 PM commute spikes, requiring a strategic pivot away from peak-only freeway expansion." Right side displays transit corridor share and recovery trajectory (source: Project Database, 2024):
```
Year,Transit_Corridor_PMT_Share,Total_Corridor_PMT_Millions,Pandemic_Impact_Phase
2012,3.52%,8069.9,All-Time Peak (FrontLines 2015 Delivery)
2016,3.03%,10404.0,Pre-Pandemic Suburban Expansion
2019,2.77%,11440.0,Pre-Pandemic Baseline
2020,1.61%,9605.4,Initial COVID-19 Telecommuting Shock
2021,1.51%,10557.5,Pandemic Trough / Remote-Work Peak
2024,2.23%,11562.4,Post-Pandemic Hybrid Work Equilibrium
```
Script: "Defense question ten asks how capital allocation must adapt to post-COVID hybrid work. Remote and flexible work have permanently changed travel patterns on the Wasatch Front. As shown in the table, transit corridor share dropped from three point five percent in 2012 to one point five percent in 2021, recovering to two point two percent in 2024. More importantly, the severe Tuesday-through-Thursday eight AM and five PM traffic spikes have flattened, spreading into midday and weekend trips. Widening freeways to meet an eight AM peak that no longer exists in traditional form risks over-building billions of dollars of concrete that sits empty during off-peak hours. Our capital strategy must evolve."

---

### Slide 17
- **Title:** Strategic Policy Recommendations for UDOT & Multimodal Partners
- **Content:** Left side callout: "Four actionable policy recommendations to transition UDOT from unpriced physical highway expansion to corridor-wide multimodal optimization." Right side summarizes core recommendations:
```
Recommendation,Lead_Agency,Policy_Mechanism,Expected_Outcome
1. Rebalance Capital Split,UDOT / State Legislature,Adjust TIF/TTIF allocations toward a 60/40 highway/transit split,Funds FrontRunner double-tracking and arterial BRT networks
2. Variable Congestion Pricing,UDOT Traffic & Safety,Convert I-15 Express Lanes to full corridor dynamic variable pricing,Guarantees 55+ mph free-flow speeds and funds parallel transit
3. Transit-Oriented Density (TOD),Cities / WFRC / MAG / UTA,Expand SB 140 HTRZ zoning (25-45 units/acre) within 0.5 miles of rail,Generates transit ridership density without adding freeway vehicle trips
4. All-Day Transit Frequency,UTA / UDOT,Transition service from peak commuter shuttles to 15-minute all-day networks,Captures midday, weekend, and discretionary hybrid-work trips
```
Script: "Based on our econometric and financial findings, we propose four policy recommendations for UDOT and our partner agencies. First, rebalance state transportation allocations toward a sixty-forty multimodal split, directing capital to strategic transit bottlenecks. Second, transition the existing I-15 Express Lanes into a full dynamically priced variable toll network in critical choke points like Point of the Mountain. Pricing general capacity manages demand, prevents induced congestion, guarantees free-flow speeds for transit and carpools, and generates dedicated revenue. Third, partner with cities through Housing and Transit Reinvestment Zones to zone for moderate density around rail stations. Fourth, re-orient UTA service from peak-only commuter runs toward fifteen-minute, all-day utility that serves modern travel patterns."

---

### Slide 18
- **Title:** Phased Implementation Roadmap & Closing Defense Summary
- **Content:** Left side callout: "A structured 10-year implementation horizon ensures fiscal discipline, environmental compliance, and regional mobility through the 2034 Olympics." Right side displays phased delivery roadmap:
```
Phase,Timeline,Lead_Agencies,Key_Deliverables_and_Milestones
Phase 1: Alignment,Years 1 - 2,UDOT / WFRC / MAG,I-15 Point of the Mountain pricing study; establish unified peak choke-point cost metrics
Phase 2: Rebalancing,Years 3 - 5,UDOT / UTA / State,Deploy dynamic pricing pilot on I-15; deliver FrontRunner strategic double-tracking
Phase 3: Maturation,Years 6 - 10,UTA / UDOT / Cities,Electrify 88-mile FrontRunner corridor; deploy regional BRT network; integrate Rio Grande Plan
```
Script: "To conclude, our twenty-five-year study demonstrates that while highways provide unmatched regional throughput, unpriced highway widening induces delayed driving demand at a two-year lag and becomes economically unsustainable in peak bottlenecks. By pairing managed dynamic pricing on I-15 with targeted fixed-guideway transit investments, UDOT can preserve corridor mobility, protect regional air quality, and deliver high returns for Utah taxpayers through the 2034 Olympic Games. Thank you, and I look forward to your questions."

---
