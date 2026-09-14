# Methodological & Accuracy Audit
### `david-jorgensen_680_Project1.ipynb` — Wasatch Front Capital Allocation & Travel Demand Elasticity

Audit scope: notebook (32 cells, all executed, no errors), `data/wasatch_front_transportation_2000_2024.csv`,
`scripts/fetch_and_build_dataset.py`, `scripts/generate_figures.py`, `scripts/build_notebook.py`, five figures,
and Milestone 1 proposal. All numeric claims below were re-derived from the shipped CSV.

---

## Verdict

The framing, literature grounding, model family, and ethical treatment are strong — better than typical for the
assignment. The problems are concentrated in three places: **(1) the provenance of the core data, (2) narrative
claims that contradict the notebook's own printed output, and (3) robustness of the headline elasticity.**

Two findings are blocking for submission as written: the data-provenance claim, and the Conclusion asserting a
statistically significant result the notebook itself reports as *p* = 0.23.

---

## A. Blocking findings

### A1. Core data is hardcoded, but documented as audited federal source data

Only three series are actually fetched: county population, county employment, and gasoline price (FRED, via
`curl`, cached in `data/raw/`). Everything the analysis actually turns on — freeway VMT, freeway lane-miles,
highway capital outlays, transit UPT/VRM/PMT, transit capital outlays — is a literal Python table inside
`fetch_and_build_dataset.py` (`get_audited_uta_transit_data`, `get_audited_highway_data`). No raw file, no URL,
no retrieval code, no per-value citation.

Section 3 attributes these to FHWA Tables VM-2, HM-60, SF-4C, HM-71/72 and NTD TS2.1. Section 10 goes further:

> "We developed an automated multi-pattern URL discovery pipeline that systematically queried historical web
> archives, parsed table structures using BeautifulSoup, and cross-validated extracted figures against UDOT
> Continuous Count Station reports."

No such code exists in the repo. `BeautifulSoup` is never imported. The same applies to the claim of having
"directly accessed and parsed UTA's audited ACFRs."

Two internal tells that the figures were fitted to the narrative rather than retrieved:
- 2012 highway capital outlay = **1725.0** ($M), which is exactly the I-15 CORE *total project cost* quoted in
  Section 1 ($1.725B) — not a plausible single-year statewide SF-4C capital outlay.
- Cumulative totals land on the round narrative anchors: $22.09B highway ("exceeded $22 billion"),
  $5.50B transit ("over $5.5 billion").

Fix: either retrieve the series for real and cache the raw files alongside the FRED CSVs, or relabel the tables
honestly as author-compiled estimates, delete the fabricated scraping paragraph, and add a limitation stating
the elasticity estimates are conditional on unverified inputs.

### A2. The Conclusion states the opposite of the notebook's own test result

Conclusion, RQ1:

> "...we firmly reject the null hypothesis of zero induced demand ($H_0: \sum \beta = 0$, $p < 0.05$)."

Code Cell 4 output:

```
Cumulative Long-Run Elasticity (Sum beta_k):  +0.3054 (SE = 0.2544, p = 0.2299)
95% Confidence Interval: [-0.1932, 0.8041]
```

*p* = 0.2299. The null of zero cumulative induced demand **cannot** be rejected at any conventional level. The
CI includes zero. Figure 3 draws this correctly — the red cumulative bar's error bar visibly crosses zero — so
the figure and the prose disagree with each other.

The defensible version of RQ1: the *lag-2* coefficient is positive and significant in this specification, but the
*cumulative* long-run elasticity is not distinguishable from zero at N = 22.

### A3. "+0.654" has no derivation anywhere

The interval "+0.305 to +0.654" appears three times (Abstract, Figure 3 interpretation, Conclusion RQ1). It is a
hardcoded string in `build_notebook.py`; nothing computes it. It is not the CI upper bound (0.804), not
β₁ + β₂ (0.532), not any reported quantity. Replace with the actual CI, [−0.193, +0.804].

### A4. Hypothesis 2 is rejected in the opposite direction, and this is never stated plainly

H₂ₐ predicted γ < 0 (transit suppresses driving). The estimate is **γ = +0.698, *p* = 0.010** — significantly
*positive*: transit service growth is associated with *higher* per-capita freeway VMT growth.

The Abstract renders this as transit's "ability to suppress overall highway VMT is constrained." The Conclusion
renders it as "does not produce a statistically significant overall suppression." Both are technically
non-false and materially misleading. A significant positive coefficient is a different result from a null.

Separately, RQ2 is then answered with a number from a *different model* — the +0.331 rail-VRM→ridership
elasticity. That quantity measures transit ridership response to transit service. It is not a cross-modal
suppression elasticity and cannot answer RQ2.

(The honest reading is that both series co-move with regional growth; the positive γ is almost certainly
confounding, not a causal claim that transit generates driving. Say that.)

### A5. Figure 2's legend contradicts Figure 2's own lines

`generate_figures.py:100-105` hardcodes the growth labels. Three are wrong:

| Series | Legend label | Actual (from CSV) | Where the line ends on the chart |
| :-- | :-- | :-- | :-- |
| Regional Population | +63% | **+53.0%** | ~153 |
| Total Employment | +78% | **+57.9%** | ~158 |
| VMT per Capita | +33% | **+41.8%** | ~142 |
| Freeway Lane-Miles | +133% | +133.3% | ✓ |
| Freeway VMT | +117% | +117.0% | ✓ |
| Transit PMT | +94% | +93.6% | ✓ |

The +63% population figure also propagates into the Abstract, Section 1, and the Figure 2 interpretation. It is
inherited from the Milestone 1 proposal (which assumed a 1.60M baseline); the assembled data has a 1.71M
baseline. Compute all six labels from the dataframe.

Also in the Executive Abstract: 2024 VMT per capita is 3,598.4, but the series peaks at 3,722.3 in **2019** — worth
noting since the text implies a monotone fill-up.

### A6. 89 corrupted LaTeX commands — every formula in the methods section and appendix is broken

`build_notebook.py` writes markdown with non-raw Python strings, so backslash escapes were consumed by Python:

| Escape | Intended | Rendered as | Count |
| :-- | :-- | :-- | --: |
| `\t` | `\text`, `\tau`, `\theta` | TAB + "ext" | 40 |
| `\b` | `\beta` | BACKSPACE + "eta" | 27 |
| `\r` | `\rho`, `\right` | CR + "ho" / "ight" | 10 |
| `\a` | `\approx` | BEL + "pprox" | 6 |
| `\f` | `\frac` | FF + "rac" | 6 |

Affected cells: 1 (7), 2 (3), **6 (31)**, 25 (3), 26 (1), **29 (44)**. The entire Appendix A long-run-elasticity
proof and the Section 4 model specification render as garbage. Fix by making every `add_markdown("""...""")`
call in `build_notebook.py` a raw string (`r"""..."""`) and rebuilding.

---

## B. Major methodological findings

### B1. The lane-mile series is inconsistent with the project inventory the paper itself lists — by ~4×

`d_ln_lanemiles` is effectively a four-spike series; the entire elasticity is identified off four events:

| Year | Δ lane-miles in data | Named project | Physically plausible lane-miles |
| :-- | --: | :-- | --: |
| 2008 | +274 | Legacy Parkway (14 mi, 4 lanes) | ~56 |
| 2012 | +255 | I-15 CORE (24 mi, +2 GP lanes each way) | ~96 |
| 2020 | +240 | I-15 Tech Corridor (~6 mi widening) | ~25 |
| 2024 | +180 | West Davis Hwy (16 mi, 4 lanes) | ~64 |
| | **949** | | **~240** |

The stated +133% growth in regional freeway lane-miles over 25 years is not credible on its face either.

This matters directly: elasticity is Δln VMT ÷ Δln lane-miles. If the denominator is inflated ~4×, β is
attenuated ~4× toward zero. The Wald test "rejecting" Duranton & Turner's unit elasticity (*p* = 0.0063) is then
a measurement artifact, not a finding. Drop or heavily qualify that claim.

### B2. The COVID dummy is mis-specified for a first-differenced dependent variable

`d_covid = 1` for both 2020 **and** 2021. In a levels model that is a two-year regime shift. In a *differenced*
model it forces one common effect onto Δln VMT/cap = **−15.8%** (2020) and **+9.9%** (2021) — a shock and its
rebound, same sign of dummy.

Consequence, from the influence diagnostics:

```
Year  leverage  Cook's D  studentized resid
2020     0.790     2.082      -2.102
2021     0.790     2.082      +2.102
```

Cook's D of 2.08 (threshold ~1) on two symmetric mirror-image residuals. This is the dominant source of the
residual non-normality the notebook detects and then waves off (Shapiro *p* = 0.033, skew 1.23, kurtosis 4.90).

Replacing `d_covid` with separate 2020 / 2021 indicators:

| Spec | β₀ | β₂ | Σβ | *p*(Σβ) |
| :-- | --: | --: | --: | --: |
| As published | −0.226 | +0.413 | **+0.305** | 0.230 |
| Separate 2020, 2021 | −0.135 | +0.312 | **+0.161** | 0.392 |
| Separate 2020, 2021, 2022 | −0.136 | +0.327 | **+0.181** | 0.336 |

The headline cumulative elasticity roughly halves.

### B3. One observation drives the sign

Leave-one-out over all 22 years, cumulative elasticity Σβ:

- Drop **2012** → **Σβ = −0.069** (sign flips)
- Drop 2011 → +0.183 · Drop 2020/21 → +0.161 · Drop 2013 → +0.510 · Drop 2004 → +0.412
- Σβ is significant at 5% in exactly **one** of the 22 leave-one-out fits (drop 2004, *p* = 0.044)

A result that inverts on removal of a single year should not be reported without the jackknife shown.

### B4. "*p* < 0.001" on β₂ is an artifact of the uncorrected HAC estimator at N = 22

Newey–West with `maxlags=2` and no small-sample correction is badly undersized in samples this small.
Same point estimate, different covariance:

| Covariance | *p*(β₀) | *p*(β₂) | *p*(Σβ) |
| :-- | --: | --: | --: |
| HAC(2), as published | 0.082 | **0.000** | 0.230 |
| HAC(2) + small-sample correction | 0.166 | 0.000 | 0.338 |
| HC3 | 0.464 | **0.043** | 0.580 |
| Plain OLS | 0.267 | **0.072** | 0.493 |

β₂ is "significant" at *p* < 0.001, at *p* = 0.043, or not at all, depending on the estimator. Report a
robustness table rather than the single most favourable number.

### B5. The transit ridership model is a spurious levels regression — the exact thing Section 4 forbids

Section 4 rejects static levels regressions "due to non-stationarity, extreme serial autocorrelation
(Durbin-Watson < 0.40), and omitted variable bias." Code Cell 8 then runs exactly that: ln(UPT) on ln(rail VRM),
ln(gas), ln(pop), COVID, in levels.

Evidence it is spurious:
- Durbin–Watson = **0.897** (printed in the notebook, never discussed)
- Engle–Granger ADF on residuals: *p* = **0.720** — cannot reject no-cointegration
- ADF on the levels: ln(UPT) 0.202, ln(rail VRM) 0.236, ln(pop) 0.912 — all non-stationary
- Condition number 6.44e+03 (statsmodels flags it in the printed output)
- **ln(pop) coefficient = −1.376, *p* = 0.003** — i.e. a 10% population increase cuts transit ridership 13.8%.
  Not interpretable; a classic co-trending artifact.

Re-estimated in first differences, the specification the paper argues for:

| Term | Levels (published) | First differences |
| :-- | --: | --: |
| rail VRM elasticity | **+0.331** (*p* < 0.001) | **+0.178** (*p* = 0.147) |
| gas price | +0.124 (*p* = 0.235) | +0.348 (*p* = 0.023) |
| population | −1.376 (*p* = 0.003) | −3.745 (*p* = 0.235) |

The +0.331 does not survive. Recommendation 3 (TOD zoning mandates, 30–50 DU/acre, parking-minimum repeal) is
justified entirely by that number in the text.

### B6. Stationarity is asserted as an Assumption but never tested

No ADF, KPSS, or Phillips-Perron appears anywhere. Running them:

| Series | ADF *p* | KPSS *p* |
| :-- | --: | --: |
| `d_ln_vmt_pc` | 0.000 | >0.10 |
| `d_ln_lanemiles` | **0.315** | >0.10 |
| `d_ln_transit_vrm` | 0.000 | >0.10 |
| `d_ln_emp` | 0.057 | >0.10 |
| `d_ln_gas_price` | 0.000 | >0.10 |

The key regressor fails ADF. (With N = 24 and a four-spike series ADF has almost no power, so this isn't damning
on its own — but the assumption is stated as satisfied without any test, and one test contradicts it.)

### B7. The out-of-sample result is printed and then silently abandoned

```
Out-of-Sample R-squared (R2):  -0.1993
```

A negative out-of-sample R² means the model predicts one-step-ahead growth **worse than the training mean**.
This number appears nowhere in Section 7, the Limitations, or the Abstract. It is the single most honest
validation in the notebook and it is unremarked.

Two further problems with the CV design:
- It is not a forecast. `test_X` contains *contemporaneous* Δln lane-miles, Δln employment, and Δln gas price —
  none knowable at t−1. It is a conditional-fit test, not out-of-sample prediction.
- `d_covid` is defined ex post, so 2020 and 2021 test folds use information from the future.
- Training folds start at 12 observations for 8 parameters (4 residual df).

Either reframe honestly as "conditional predictive stability" or rebuild with lagged-only regressors.

### B8. The "QLR test" is not a QLR test

Figure 4 Panel B sweeps Chow F-statistics over break years 2005–2021 and draws a critical line at F = 3.0
"(p ≈ 0.05)". Taking the *supremum* of an F-sequence over a searched range does not have an F distribution —
that is the whole point of Andrews (1993) / Quandt, which requires non-standard sup-Wald critical values
(≈ 4.09 at 5% for k = 4 with 15% trimming, not 3.0). Reporting the max's ordinary-F *p*-value materially
overstates significance. Either apply Andrews critical values or stop calling it QLR.

### B9. The Chow tests are underpowered, mis-specified, and over-claimed

- They use a **different model** than the published one: `['d_ln_lanemiles', 'd_ln_emp', 'd_ln_gas_price']` —
  no distributed lags, no transit VRM, no COVID dummy. So they do not test the stability of the estimated model.
- The 2008 split has **N₁ = 5 observations for k = 4 parameters** (1 residual df). The `N1 <= k` guard lets it
  through. The test is degenerate.
- Chow assumes homoskedasticity *across regimes*. At a COVID break that assumption fails badly; a robust Wald
  test is required.
- The 2020 break model **omits** `d_covid`, so the "structural break" is mechanically the COVID outlier itself.
  Circular.
- Section 10 claims the tests were "proving that parameter stability held across the non-pandemic periods."
  The table shows *p* = 0.074 (2008), 0.082 (2012), 0.085 (2013) — weak *evidence against* stability, and in any
  case failing to reject is not proof.
- Figure 4's narrative reports F = 3.430, *p* = 0.033 for 2020; Code Cell 7's table reports F = 3.6394,
  *p* = 0.0311. Same event, two numbers, two undisclosed specifications.

### B10. The "20-year lifecycle" cost is a 25-year nominal sum with no discounting

RQ3 asks for "annualized public capital expenditure per net PMT... over a 20-year lifecycle." What is computed is
`sum(outlays) / sum(PMT)` over 25 years, in **nominal dollars**, with no discount rate, no amortization schedule,
and no asset-life assumption. A 2000 dollar and a 2024 dollar are added together.

In constant 2024 dollars (CPI-U):

| | Published (nominal) | Real, 2024$ |
| :-- | --: | --: |
| Highway capital | $22.09B | $29.77B |
| Transit capital | $5.50B | $7.67B |
| Highway $/PMT | $0.1033 | **$0.1393** |
| Transit $/PMT | $0.9467 | **$1.3192** |
| Ratio | 9.16× | 9.47× |

The *ratio* survives — the headline RQ3 conclusion is directionally robust — but every per-PMT level quoted in
the Abstract, Conclusion, Figure 5, and the Ethical Assessment is understated by ~35%.

### B11. Total network throughput is credited to marginal capital spending

The highway denominator is **all** freeway PMT, 2000–2024 (213.8B). But the 2000 network already carried
4,342M VMT with none of the $22.09B spent. Attributing 25 years of total throughput to 25 years of marginal
capacity investment is not a defensible cost-effectiveness calculation — and it is asymmetric, because most
transit PMT genuinely is attributable to the new capital (FrontRunner, TRAX, UVX all post-date 2000).

Recomputed on PMT *above the 2000 baseline*:

| | Gross (published) | Marginal vs 2000 |
| :-- | --: | --: |
| Highway | $0.1033/PMT | **$0.2645/PMT** |
| Transit | $0.9467/PMT | **$2.2219/PMT** |
| Ratio | 9.16× | 8.40× |

Credit where due: the ~9× ratio is robust to both the inflation and the marginal reframing. RQ3's substantive
answer holds; only the quoted levels are wrong.

### B12. Numerator and denominator cover different geographies

FHWA Table SF-4C reports **statewide** State Highway Agency capital outlays. The PMT denominator is
four-county urban freeway only. Section 1 nonetheless says "state highway capital outlays **along the Wasatch
Front** exceeded $22 billion." Either apportion the outlays to the region or state the mismatch and its direction
(it inflates highway $/PMT, i.e. it is conservative against the paper's own highway-favourable finding).

### B13. The peak choke-point costs — the paper's entire pro-transit counter-argument — are unsourced literals

`$1.40–$2.20 / peak commuter PMT` (highway) and `$0.45–$0.85 / peak commuter PMT` (transit) are typed directly
into the `cap_eff_df` construction in Code Cell 8. No model, no citation, no derivation, no data.

These numbers then carry:
- the Abstract's rescue of transit,
- Conclusion RQ3's "rendering fixed-guideway investments highly cost-competitive,"
- Figure 5's interpretation,
- Recommendation 1's 60/40 reallocation,
- Ethical Assessment Part 3 Mitigation 1 ("proving that transit saves taxpayers money").

This is the load-bearing claim of the policy recommendation and it is the least supported number in the document.
Either derive it (marginal ROW + structure cost per added peak-hour person-throughput at a named interchange) with
a source, or delete it and soften every conclusion that depends on it.

### B14. Vehicle occupancy of 1.20 is applied to all freeway VMT, including trucks, with no sensitivity

1.20 is roughly a *commute-period* AVO; FHWA all-purpose regional AVO runs ~1.6–1.7. Freeway VMT also includes
heavy trucks, for which "occupancy" is not the right conversion at all. Sensitivity:

| AVO | Highway $/PMT |
| --: | --: |
| 1.20 (used) | $0.1033 |
| 1.40 | $0.0886 |
| 1.67 | $0.0743 |

This choice moves the headline number by 28% and is listed as Assumption 1 without a range.

### B15. Endogeneity is acknowledged and then left unaddressed

Section 4 correctly explains why Duranton & Turner's cross-sectional instruments cannot work in a single-region
time series. But it then treats "lag identification and first-differencing" as sufficient identification. It is
not: lanes get added where VMT is already growing, so β₂ absorbs anticipatory demand growth. Note too that the
lag-2 years driving the positive β₂ are **2014** and **2022** — a recovery from the Great Recession and a
recovery from COVID respectively, and the COVID dummy covers only 2020–2021, leaving the 2022 rebound to land
squarely on lag 2. Add a limitation naming this; consider a 2022 indicator as a robustness check (B2 shows it
moves the result).

---

## C. Minor findings

1. **Section numbering.** TOC lists 16 sections; sections 9, 10, 11 are nested under a cell titled "# 8.
   Assumptions" and 13 under "# 12. Recommendations". Anchors in the TOC will not resolve.
2. **Conclusion RQ2** says transit captures "~2.5% to 3.5%" of regional PMT; the 2024 value is 2.23% and the
   2021 trough is 1.51%. The 3.5% peak (2012) is correct.
3. **Transit share denominator.** Figure 4 Panel A computes transit share against *freeway* PMT only. Against
   all urban highway PMT the share is roughly half. The narrower denominator flatters transit.
4. **`transit_rail_pmt_share`** (in the shipped CSV) embeds a hardcoded 7.5-mile average rail trip length that
   appears in neither the data dictionary nor the Assumptions. It is unused in the analysis — drop it or document it.
5. **Data dictionary covers 23 of 68 columns** in the shipped CSV.
6. **Uncaught warnings in output.** Code Cell 4 ships two NumPy `DeprecationWarning`s and a statsmodels
   `FutureWarning` in the rendered output. Extract scalars with `.item()` / `float(np.asarray(x).ravel()[0])`
   and pass `scalar=True` to `wald_test`.
7. **VIFs computed without the constant** (`variance_inflation_factor(X[X_cols].values, i)`). Immaterial here —
   the corrected values are 1.48 / 2.23 / 1.67 / 4.27 / 1.87 / 2.29 / 3.62 — but the idiom is wrong.
8. **Date.** Notebook header says September 13, 2026; execution timestamps are `Sun, 13 Sep 2026`. Consistent —
   just confirm that is the intended term.

---

## D. What is genuinely good

- **Problem framing and domain grounding.** Duranton & Turner, Downs-Thomson, Mogridge, Litman are used
  correctly and the geographic/air-quality motivation is specific and real, not decorative.
- **Model family is the right choice.** Log first-differences + distributed lags + HAC is the appropriate
  approach for N = 25 annual data, and the explicit rejection of VAR (parameter count) and 2SLS (time-invariant
  instruments) shows real judgment rather than method shopping.
- **Figure 3 is honest.** It plots the cumulative CI crossing zero. The chart is right where the prose is wrong —
  fixing A2 means making the text agree with a figure you already drew correctly.
- **Diagnostics breadth.** DW, Ljung-Box at three lags, Breusch-Pagan, Shapiro-Wilk, VIF, plus an out-of-sample
  CV — more than the assignment requires. The gap is interpretation, not coverage.
- **Reproducible pipeline.** `build_notebook.py` / `generate_figures.py` / `fetch_and_build_dataset.py` as a
  regenerable chain is a real strength and makes every fix below cheap to apply.
- **Ethical Assessment.** Three-part structure with likelihood×impact and named mitigations; the Title VI and
  environmental-justice content is specific (Rose Park, Glendale, Poplar Grove) rather than boilerplate. The
  self-aware "political weaponization" concern is well judged.
- **RQ3's substantive answer is robust.** ~9× gross cost ratio survives inflation adjustment and marginal-PMT
  reframing. That conclusion stands; only its quoted levels need repair.

---

## E. Priority fix order

**Before submission**

1. A2 — Rewrite Conclusion RQ1 to match *p* = 0.2299. Say the lag-2 coefficient is significant but the
   cumulative long-run elasticity is not distinguishable from zero.
2. A1 — Delete the fabricated scraping paragraph in Section 10. Relabel the hardcoded tables as author-compiled
   estimates and add a limitation, or source them for real.
3. A5 — Compute Figure 2's legend labels from the dataframe; fix +63%/+78%/+33% everywhere they appear.
4. A6 — Make `build_notebook.py`'s markdown strings raw; rebuild. Verify Appendix A and Section 4 render.
5. A3 — Replace "+0.305 to +0.654" with the computed CI [−0.193, +0.804].
6. A4 — State plainly that γ = +0.698 (*p* = 0.010) is significantly positive, that H₂ is rejected in the
   opposite direction, and that the most likely explanation is shared regional-growth confounding.

**Substantially improves the grade**

7. B2 + B3 + B4 — Add one robustness table: separate COVID dummies, alternative covariance estimators, and the
   leave-one-out range for Σβ. This converts the paper's biggest weakness into a demonstration of rigor.
8. B5 — Re-run the transit model in first differences; report both and explain the difference. Soften
   Recommendation 3 accordingly.
9. B13 — Source or delete the $1.40–$2.20 / $0.45–$0.85 peak figures, and adjust every conclusion resting on them.
10. B10 + B11 — Report capital efficiency in constant 2024 dollars and add the marginal-PMT variant. Note that
    the ~9× ratio is robust — this strengthens RQ3 rather than weakening it.
11. B7 — Interpret the −0.199 out-of-sample R² in the Limitations instead of leaving it unmentioned.

**Polish**

12. B6 (add ADF/KPSS table), B8 (Andrews critical values or drop the QLR label), B9 (align the Chow spec with the
    published model; drop the 2008 split), B14 (AVO sensitivity), B1 (note the lane-mile/project inventory gap and
    its attenuation implication), C1, C6.
