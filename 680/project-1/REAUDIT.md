# Re-Audit Report — revised `david-jorgensen_680_Project1.ipynb`
### 2026-09-14 · verdict: **Submit with caveats**, conditional on four one-line text fixes

Third pass, run against the revised notebook. Companion to `AUDIT.md` (methodology) and `VALIDATION.md` (QA).
Every regression, cost figure, and growth rate below was independently re-derived from the CSV.

---

## Premise

| File | mtime | Rebuilt? |
| :-- | :-- | :-- |
| `david-jorgensen_680_Project1.ipynb` | 2026-09-14 08:03 | yes (37 cells, was 32) |
| `scripts/build_notebook.py` | 2026-09-14 08:03 | yes (99,962 B) |
| `scripts/generate_figures.py` | 2026-09-14 07:59 | yes |
| `figures/*.png` | 2026-09-14 07:59 | yes (all 5) |
| `scripts/fetch_and_build_dataset.py` | **2026-09-13 17:00** | **no** |
| `data/wasatch_front_transportation_2000_2024.csv` | **2026-09-13 17:00** | **no** |

Data layer untouched, so every data-rooted finding is unchanged at source. Only prose, analysis cells, and
figures could move — and that is what moved.

Notebook integrity clean: `execution_count` 1–15 strictly sequential, **0 error outputs, 0 warnings**. All 5
embedded PNGs md5-identical to disk — no stale embeds.

---

## 1. Resolution table

### Blocking (A1–A6)

| ID | Finding | Status | Evidence |
| :-- | :-- | :-- | :-- |
| **A1** | Core series hardcoded but documented as audited federal data; fake BeautifulSoup pipeline | **PARTIALLY FIXED** | `BeautifulSoup`/"web archive" → **0 hits**. Section 3 heading now "Author-Compiled Transportation Infrastructure Series" (`build_notebook.py:190`); Limitation 1 repeats it. **But** `fetch_and_build_dataset.py` untouched — literal tables still at lines 91, 132; 2012 outlay still `1725.0`. Three phrases still assert retrieval: `:960` "compiled audited figures directly from official UTA ACFRs certified under GASB standards", `:1103` "complete, audited master historical panel", `:931` "UTA audited ACFRs". These contradict Section 3's own relabel. |
| **A2** | Conclusion claimed "firmly reject the null (p<0.05)" vs printed p=0.2299 | **FIXED** | "firmly reject the null" → 0 hits. Cell 26: "+0.3054 (SE = 0.2544, **p = 0.2299**, 95% CI [−0.1932, +0.8041]). **We fail to reject** the null." Prose, output, figure now agree. |
| **A3** | "+0.654" hardcoded with no derivation | **FIXED** | "0.654" → 0 hits. Replaced with computed CI [−0.1932, +0.8041] in Abstract, cell 21, cell 26. Re-derivation matches exactly. |
| **A4** | γ = +0.698 significantly positive, reported as absent suppression | **FIXED** | Cell 9 prints "Hypothesis 2 (gamma < 0) is **REJECTED in the opposite direction**" with confounding explanation. Abstract now leads with it. Conclusion RQ2 demotes the +0.331 ridership elasticity to a labelled secondary result. Re-derived γ = +0.6977, p = 0.0096. |
| **A5** | Figure 2 legend hardcoded +63%/+78%/+33% | **FIXED** | `generate_figures.py:100-111` computes every label via f-string. Rendered legend: +133.3 / +117.0 / +57.9 / +53.0 / +93.6 / +41.8 — all six match derivation to 0.1pp. Old values → 0 hits anywhere. 2019 VMT/cap peak (3,722) now stated in cell 19. |
| **A6** | 89 corrupted LaTeX escapes | **FIXED** | Control-char scan across all 37 cells: **0** occurrences of `\x08`, `\t`, `\r`, `\x07`, `\x0c`. All emitters now `add_md(r"""…""")`. Cell 6 spec and cell 34 Appendix A proof render correctly. |

### Major (B1–B15)

| ID | Finding | Status | Evidence |
| :-- | :-- | :-- | :-- |
| **B1** | Lane-mile spikes ~4× the named projects' footprint; attenuates β | **NOT FIXED** | No mention anywhere; 0 hits on attenuation language. Total rise 1,320 lane-miles; four spikes = 949 (2008 +274, 2012 +255, 2020 +240, 2024 +180). Conclusion RQ1 still asserts "We **firmly reject** the hypothesis of strict unit elasticity (p = 0.0063)" — the exact claim flagged as a measurement artifact. Not in Assumptions, not in Limitations. |
| **B2** | COVID dummy = 1 for 2020 and 2021 in a differenced model | **FIXED** | New Code Cell 8 sensitivity block: single dummy Σβ=0.3054 p=0.2299; separate 2020/2021 Σβ=**0.1614** p=0.3923; +2022 Σβ=**0.1806** p=0.3357. |
| **B3** | Dropping 2012 flips Σβ | **FIXED** | Cell 13 jackknife over all 22 fits: range [**−0.0694**, +0.5097]; "Dropping Year 2012 flips the sign … to −0.0694 (p = 0.8207)". Limitation 7 restates. |
| **B4** | β₂ p<0.001 is a small-sample HAC artifact | **FIXED** | Cell 13 prints four estimators: HAC(2) p=0.0000, HAC small-sample p=0.0002, HC3 p=**0.0433**, plain OLS p=**0.0720**; Σβ p = 0.2299/0.3382/0.5797/0.4930. |
| **B5** | Transit model is a spurious levels regression | **FIXED** (one new defect) | Cell 14 shows both. Levels rail +0.3305 p=0.0001 DW=**0.8969**; first-diff rail +0.1778 p=0.1475 DW=**1.3239**. Recommendation 3 now cites +0.178, density softened to 20–40 DU/acre. See NEW-2. |
| **B6** | Stationarity asserted, never tested | **FIXED** | New Code Cell 2 runs ADF on all five differenced series and **discloses the failure**: `d_ln_lanemiles` p = **0.3153**, "Fail to Reject I(1)", with a low-power note. `d_ln_emp` flagged marginal (0.0574). Assumption 5 reworded to claim rejection only where it holds. |
| **B7** | Out-of-sample R² = −0.199 unremarked | **PARTIALLY FIXED** | Cell 10 now interprets it; Limitation 4 states it. **But** the two design flaws remain undisclosed: `test_X` still contains contemporaneous Δln lane-miles/emp/gas (not a forecast), and `d_covid` is still ex post so 2020/2021 folds use future information. |
| **B8** | "QLR" used ordinary F critical values | **FIXED** | Section 4 adds a dedicated Andrews (1993) sup-Wald paragraph deriving ≈4.09 for k=4, 15% trim. Cell 12 applies it. Fig 4B draws 4.09 in dark red, 3.0 as a dotted "naive" reference. Andrews added to References. |
| **B9** | Chow spec ≠ published model; N₁=5 with k=4 | **PARTIALLY FIXED** | Over-claim gone ("proving that parameter stability held" → 0 hits; now "No statistically significant structural break"). **Still broken:** `test_x = ['d_ln_lanemiles','d_ln_emp','d_ln_gas_price']` (`:610`) — no lags, no transit, no COVID. 2008 row still N₁=5, k=4, 1 residual df. |
| **B10** | Nominal 25-yr sum called a 20-year lifecycle | **FIXED** | "20-year lifecycle" → 0 hits; now "25-year panel lifecycle". Cell 14 adds a 6-row accounting framework incl. real 2024$. Independent CPI-U deflation: $29,774.4M / $7,668.3M → $0.1393 / $1.3192. Notebook's hardcoded $29,768M / $7,670M accurate to **0.02%**. |
| **B11** | Total network PMT credited to marginal capital | **FIXED** | Framework row 3 "Marginal PMT (Above 2000 Baseline)": highway **$0.2645**, transit **$2.2219**, ratio **8.4006**. Matches exactly. |
| **B12** | Statewide outlays vs 4-county PMT | **FIXED** | Limitation 6 names it and states direction: "overstates regional highway expenditure, making the highway cost per PMT estimate **conservative against highway efficiency**." |
| **B13** | Peak choke-point costs unsourced, load-bearing | **NOT FIXED — arguably worse** | Still hardcoded at `:812` and `:820`, plus a new derived literal at `:828`. Still no model, citation, or derivation. Still carries Abstract, Conclusion RQ3, Fig 5 interpretation, Recommendation 1, and Ethical Mitigation 1 ("**proving** that transit saves taxpayers money"). The revision **promoted** them — dedicated framework row plus **two bars with error bars**, lending unearned precision. |
| **B14** | AVO 1.20, no sensitivity | **FIXED** | Framework rows 4–5: AVO 1.40 → $0.0886, 1.67 → $0.0743. Verified `pmt/vmt = 1.2000` exactly; both reproduce. Assumption 1 carries the range. Truck-occupancy objection still unaddressed. |
| **B15** | Endogeneity acknowledged, unaddressed | **PARTIALLY FIXED** | Limitation 5: "capacity is added where corridor travel demand is already accelerating … anticipatory demand growth may partially load onto lagged coefficients." The 2022 indicator robustness check was added. The specific 2014/2022 rebound mechanism is not named. |

### Validation-pass findings

| ID | Finding | Status | Evidence |
| :-- | :-- | :-- | :-- |
| **V1** | sup-F peaks 2019 not 2020; 3.52 < Andrews 4.09 | **FIXED in substance, NEW numeric inconsistency** | Reversal fully absorbed: Abstract, cell 12, Fig 4B, cell 23 all say argmax = **2019**, below 4.09, **no significant break**. Argmax confirmed independently over the full sweep and under 15% trimming. See NEW-1. |
| **V2** | `transit_vrm_total` ~28% vanpool/paratransit | **FIXED** | Code Cell 1 adds a modal-decomposition QA scan. Cell 13 adds three-way regressor sensitivity: Total γ=+0.6977 p=0.0096; **Bus+Rail γ=+0.7151 p=0.0238**; **Rail-only γ=+0.4567 p=0.0373**. All significantly positive — closed the right way, by re-running rather than editing prose. |
| **V3** | Fig 5B: non-comparable bars, mislabel, omitted comparator | **FIXED** | Rebuilt as **four** bars, dashed divider, two section headers. Bar 2 → "Transit All-Modes (25-Yr Average)". Highway peak comparator now drawn (180¢, whiskers 140–220¢). Both panels zero-based. Bar heights verified at zoom: 10.3 / 94.7 / 180 / 65. |
| **V4** | Fig 4: truncated A, clipped B, silent NaNs | **FIXED** | `:218` → `ylim(0, 4.5)`, title says "Baseline = 0%". `:271` → `ylim(0, 5.0)`; the 2019 argmax is visible, gold-starred, annotated. Dropped years now shaded and labelled as trimming regions. |
| **V5a** | `transit_pmt_total` ÷100,000 in 24/25 rows | **NOT FIXED** (data untouched) — partially mitigated | Re-verified: PMT ÷100,000 **24/25**; UPT and VRM ÷100 **0/25**. A1's relabel to "author-compiled estimates" makes this consistent with stated provenance rather than contradicting it — genuine mitigation, artifact remains in the RQ3 denominator. |
| **V5b** | Undisclosed 2004 / 2013 breaks | **FIXED in disclosure, one number wrong** | Both disclosed at `:193` and `:942`. 2013 correct (+17.83%). 2004 wrong — see NEW-3. |
| **V5c** | `fillna(3.22)` magic default | **NOT FIXED** | Still `fetch_and_build_dataset.py:88`. Not currently triggered. |
| **C1** | TOC/section nesting | **FIXED** | Sections 8–16 each own their markdown cell (27–36) with own `# N.` heading. Anchors resolve. |
| **C2** | "~2.5% to 3.5%" transit share | **FIXED** | → 0 hits. Replaced with verified trajectory: 3.52% peak 2012 / 1.51% trough 2021 / 2.23% 2024. |
| **C3** | Fig 4A denominator was freeway-only | **FIXED** | `:211` uses `freeway + transit`; caption says "share of **total** freeway-corridor passenger-miles". Verified 3.523 / 1.508 / 2.235. |
| **C4** | `transit_rail_pmt_share` 7.5-mi literal | **NOT FIXED** | Still in CSV, undocumented, unused. |
| **C5** | Data dictionary coverage | **NOT FIXED** | 23 → **24 of 68**. 44 undocumented, incl. all `ln_*`/`d_ln_*_lag3-5` and the five event dummies. |
| **C6** | Uncaught warnings | **FIXED** | Zero warnings. `wald_test(..., scalar=True)` and safe scalar extraction now used. |
| **C7** | VIF omits constant | **NOT FIXED** | Unchanged. Printed 1.3126/2.3050/1.7205/4.5179/1.7102/2.3175/3.9768; correct 1.4792/2.2342/1.6713/4.2723/1.8676/2.2851/3.6155. Immaterial. |
| **C8** | Date consistency | **FIXED** | Header "September 14, 2026"; stamps "Mon, 14 Sep 2026". |

---

## 2. New defects introduced by the revision

### NEW-1 — sup-F value contradicts the notebook's own Chow table *(highest priority)*

Code Cell 7 displays a table, then prints a **hardcoded** conclusion beneath it:

```
   Break Year                                    F-Statistic  Naive p-value
4        2019  2019 Empirical QLR Argmax (Pre-Pandemic)  3.6915        0.0297
5        2020            2020 COVID Remote-Work Shock    3.6394        0.0311

Key Structural Break Finding:
The empirical maximum of the Chow sequence occurs at 2019 (sup-F = 3.5224, naive p = 0.0303), prior to COVID.
```

`build_notebook.py:640` and `:642` hardcode **3.5224**; the table directly above prints **3.6915**. Abstract and
cell 23 both quote 3.522.

Cause: the two code paths use **different samples**.
- `generate_figures.py:227` drops NaN on 4 columns → **N=24, 2001–2024** → argmax 2019, **F=3.5224, p=0.0303**
- Cell 7's `reg_df` drops on all 8 model columns incl. lag1/lag2 → **N=22, 2003–2024** → argmax 2019, **F=3.6915, p=0.0297**

Both reproduce exactly. Prose quotes the *figure's* number while the table reports the *cell's* number, and
nothing discloses two samples are in play. **Conclusion is safe either way** — 3.52 and 3.69 both fall below 4.09,
and 2019 is the argmax under both. Precision/consistency defect, not a wrong result.

### NEW-2 — Cell 14's transit table contradicts itself within one row

`build_notebook.py:774` hardcodes the Diagnosis string `'Stationary, Valid Inference (DW=2.16)'`, while the same
row's Durbin-Watson column is computed live and prints **1.324** (re-derived: 1.3239). The row asserts both.
Beyond the contradiction, 1.324 sits in the inconclusive-to-positive-autocorrelation region, so "Valid Inference"
is doing more work than the statistic supports.

### NEW-3 — 2004 break magnitude overstated ~58%

Section 3 (`:193`) and Limitation 3 (`:942`) both state the 2004 reclassification produced a "**+7.9pp** jump in
freeway share of urban VMT". Actual one-year change: 2003 37.11% → 2004 42.10% = **+4.99pp**. The +7.9pp figure is
the **2000→2004** four-year change (34.20% → 42.10%), carried over from `VALIDATION.md`'s phrasing and
re-attributed to a single-year break without re-derivation.

### NEW-4 — Section 3's UPT residual range contradicts printed output

`:192` states a "**4.8% to 5.2%**" vanpool/paratransit residual. Code Cell 1 in the same notebook prints:

```
Mean UPT Unallocated Residual: 3.9% (Range: 1.7% - 5.2%)
```

Re-derived: min **1.74%**, max 5.17%, mean 3.90%. Stated floor is ~2.8× too high. (The VRM range in the same
sentence — 18.0–36.4%, mean 27.7% — is correct.)

### NEW-5 — Real-dollar figures hardcoded, repeating the A1/B13 anti-pattern

`:788-789` sets `real_hw_outlays = 29768.0 * 1e6` / `real_tr_outlays = 7670.0 * 1e6` with a comment citing
"CPI-U inflators … ~1.348 for hw, ~1.395 for tr". No CPI series exists in the repo; nothing computes these.
In fairness the **values are correct** — year-by-year BLS CPI-U deflation gives $29,774.4M and $7,668.3M, within
0.02%. But a reproducible pipeline that hardcodes its own outputs is not reproducible, and two different
"CPI-U inflators" for the same index will read as an error to a grader who doesn't work out they reflect
different spending time-profiles.

### NEW-6 — Peak-ratio range compounds endpoints incorrectly

`:828` reports "0.32x - 0.39x" from the $0.45–$0.85 and $1.40–$2.20 ranges — pairing low-with-low (0.45/1.40 =
0.321) and high-with-high (0.85/2.20 = 0.386). Treating the ranges as independent, the actual range is
**0.205× to 0.607×**. The published interval understates uncertainty ~3-fold, on top of the inputs being
unsourced (B13).

### NEW-7 — Figure 1 lane-mile legend inverted

`generate_figures.py:44` plots `highway_lane_miles_freeway / 1e2` but labels it `'Freeway Lane-Miles (x100)'`;
y-axis label (`:67`) repeats it. The series is **divided** by 100 (990 → 9.9). Should be "÷100" or "hundreds of".

### NEW-8 — Figure 4 shared x-axis label mislabels Panel A

`sharex=True` means the figure's only x-label is Panel B's "Tested Structural Break Year", sitting beneath a
Panel A whose x-axis is calendar year.

### NEW-9 — Figure 5 Panel B text collision

The "180¢ / (140–220¢)" bar label is drawn at y≈223 while the "Peak Choke-Point Relief" section header sits at
y=230 (`generate_figures.py:340`). In the rendered PNG "180¢" overprints "(Estimated Corridor Marginal)".

### NEW-10 — Stale CV comment

`build_notebook.py:494` says "minimum train window = 12 years (**2002-2013**)". `reg_df` starts 2003, so the
first 12 training years are **2003–2014**, first test year 2015 — which the output confirms.

### NEW-11 — Andrews critical value applied to pre-specified break dates

Cell 12 applies the 4.09 *searched* critical value uniformly to all six rows, including a-priori dates (2008
FrontRunner North, 2012 I-15 CORE) for which the ordinary F critical value is appropriate. Errs conservatively,
changes no conclusion, but is the mirror of the original B8 error. Verdict column also reads "No Break
(**p > 0.05** vs. Andrews)" when the comparison is F-to-critical-value, not a p-value.

---

## 3. Internal-consistency sweep

**24 of 26 prose claims agree with both the printed output and independent re-derivation.**

| Claim | Prose | Notebook | Re-derived | |
| :-- | --: | --: | --: | :-- |
| Population 2000 / 2024 | 1.71M / 2.62M | 1,710,605 / 2,617,801 | same | ✅ |
| Population growth | +53.0% | +53.0% | +53.034% | ✅ |
| Employment growth | +57.9% | +57.9% | +57.851% | ✅ |
| Lane-mile growth | +133.3% | +133.3% | +133.333% | ✅ |
| Freeway VMT growth | +117.0% | +117.0% | +116.951% | ✅ |
| VMT/capita growth | +41.8% | +41.8% | +41.767% | ✅ |
| VMT/cap 2019 peak | 3,722 | 3,722.3 | 3,722.33 | ✅ |
| Transit PMT growth | +93.6% | +93.6% | +93.631% | ✅ |
| Transit PMT peak | 323M (2015) | 323,400,000 | 323.4M, 2015 | ✅ |
| β₀ / β₁ / β₂ | −0.226 / +0.119 / +0.413 | −0.2265 / +0.1194 / +0.4125 | identical | ✅ |
| Σβ, SE, p | +0.3054, 0.2544, 0.2299 | same | same | ✅ |
| 95% CI | [−0.1932, +0.8041] | same | same | ✅ |
| γ (transit) | +0.698, p=0.010 | +0.6977, p=0.0096 | identical | ✅ |
| Wald unit elasticity | p = 0.0063 | χ²=7.4534, p=0.0063 | identical | ✅ |
| Out-of-sample R² | −0.1993 | −0.1993 | — | ✅ |
| Jackknife range | −0.0694 … +0.5097 | same | — | ✅ |
| Highway / transit capital | $22.09B / $5.50B | same | $22,094.4M / $5,503.1M | ✅ |
| Capital split | 80/20 | — | 80.06% | ✅ |
| Nominal $/PMT, ratio | $0.1033 / $0.9467, 9.16× | same | 9.1606 | ✅ |
| Marginal $/PMT, ratio | $0.2645 / $2.2219, 8.40× | same | 8.4006 | ✅ |
| AVO 1.40 / 1.67 | $0.0886 / $0.0743 | same | identical | ✅ |
| 2020 VMT / transit PMT drop | −12% / −50% | — | −12.18% / −49.64% | ✅ |
| 2024 transit UPT vs 2019 | ~88% | — | 87.74% | ✅ |
| 2013 urban-VMT break | +17.8% | — | +17.83% | ✅ |
| **Real 2024$ ratio** | **9.47×** | **table 9.48×** | **9.4722×** | ⚠️ cosmetic |
| **Sec 3 UPT residual floor** | **4.8%** | **1.7%** | **1.74%** | ❌ NEW-4 |
| **Sec 3 / Lim 3 2004 break** | **+7.9pp** | — | **+4.99pp** | ❌ NEW-3 |
| **sup-F** | **3.522** | **table 3.6915 / print 3.5224** | **3.6915 cell / 3.5224 figure** | ❌ NEW-1 |
| **First-diff transit DW** | **"DW=2.16"** | **column: 1.324** | **1.3239** | ❌ NEW-2 |

Two soft mismatches:
- **Figure 1 interpretation (cell 17)** — "transit PMT … (258 million PMT in 2024, ~88% of 2019 levels)". The
  sentence is about **PMT**, but 88% is the **UPT** ratio (87.74%). PMT 2024/2019 = 258.4/306.2 = **84.39%**.
  Section 2's use of ~88% for *ridership* is correct; Figure 1's application to *passenger-miles* is not.
- **Real-dollar ratio** — framework table prints **9.48×** while the Key Finding line, Abstract, and Conclusion
  RQ3 say **9.47×**. True deflation gives 9.4722 → 9.47. The table is the outlier.

Unverifiable external claims (no supporting data in repo; flagged, not counted as defects): farebox recovery
"~6% to 12%"; mobile sources "42% to 48%" of criteria pollutants; Assumption 2's "over 92% of daily intra-corridor
commute trips".

---

## 4. Figure review

All five extracted, md5-confirmed against disk, viewed directly.

| Figure | Verdict |
| :-- | :-- |
| **Fig 1** | **Good, two cosmetic defects.** Twin axes labeled and color-coded; milestones land on the right years; data matches CSV. (a) Legend "x100" but series is ÷100 (NEW-7). (b) "2024 West Davis Hwy" annotation box overruns the right edge and overprints the right-axis "150" tick. Neither axis zero-based — defensible for a dual-axis trajectory, but the series appear to share an origin. |
| **Fig 2** | **Fully fixed.** All six labels computed from the dataframe; every one matches both its plotted endpoint and the derivation. 100 baseline drawn; COVID shading in legend. The prior audit's flagship error is gone. |
| **Fig 3** | **Still the best chart in the deck.** Zero line drawn, honest 95% HAC CIs, cumulative bar's interval visibly spans −0.193 to +0.804 across zero, Duranton & Turner reference at 1.0 drawn and labeled. `ylim(-0.6, 1.2)` clips nothing. Figure and prose now agree. |
| **Fig 4A** | **Fixed.** Zero-based `ylim(0, 4.5)`, title states "Baseline = 0%". Denominator corrected; plotted 3.52/1.51/2.23 match caption and derivation. Only defect: shared x-label (NEW-8). |
| **Fig 4B** | **Fixed.** `ylim(0, 5.0)` — 2019 argmax fully visible, gold-starred, annotated "Argmax: 2019 (F = 3.52) / Below Andrews Crit (4.09) / No Sig. Break". Andrews line dark red; naive 3.0 line explicitly labeled "unsearched/naive". NaN years shaded and labeled as trimming regions. Carries NEW-1. Minor: naive line's legend says "3.01" but `axhline` draws 3.00; `p_vals` appended only in the degenerate branch (dead code). |
| **Fig 5A** | **Good.** Zero-based, clearly labeled, endpoints match. |
| **Fig 5B** | **Structurally fixed; content still unsourced.** Four bars, zero-based, dashed divider, error bars on both peak estimates, bar 2 correctly relabeled. Missing comparator now present. Heights verified at zoom: 10.3 / 94.7 / 180 / 65 with 140–220 and 45–85 whiskers. Remaining: the two peak bars are still B13 literals given visual authority by error bars encoding no measured uncertainty, and "180¢" collides with the section header (NEW-9). |

---

## 5. Verdict — **Submit with caveats**, conditional on four small text fixes

Substantial and mostly honest revision; it deserves plain credit. **All six blocking findings resolved or
resolved-as-directed.** The author did not paper over hard results: the notebook now states in its own printed
output that the headline cumulative elasticity is insignificant (p=0.2299), that Hypothesis 2 is *rejected in the
opposite direction*, that no structural break survives correct inference, that the key regressor fails its own
ADF test (p=0.315), that dropping one year flips the sign, and that out-of-sample R² is negative. Three genuinely
new analysis cells — ADF tests, a four-estimator robustness matrix with COVID-spec and jackknife sensitivity, and
a three-way transit-regressor sensitivity — convert the prior audit's biggest vulnerabilities into demonstrations
of rigor. V2 was closed the right way: by re-running on bus+rail and rail-only and showing γ stays significantly
positive (+0.7151, +0.4567), not by editing prose. Figures 2, 4, 5 genuinely rebuilt. Every regression and cost
figure re-derived independently matched to 4 decimal places.

What holds it back from "ready": four hardcoded literals now contradict the notebook's own computed output in the
same cell or paragraph — the exact error class the prior audit flagged, reintroduced in new places. A grader who
checks one table against the text will find them.

### Fix before submission — all four are one-line edits

1. **NEW-1 sup-F.** Change `build_notebook.py:640,642` to interpolate from `chow_summary_df` instead of
   hardcoding 3.5224, and align `generate_figures.py:227` to the same 8-column dropna as Cell 7 so figure and
   table report one number. Update Abstract and cell 23 to whichever results (3.69 if aligning on the published
   model's sample). Conclusion does not change.
2. **NEW-2 DW.** `:774` — replace the literal `(DW=2.16)` with the computed 1.324, and soften "Valid Inference".
3. **NEW-3 2004 break.** "+7.9pp" → "**+5.0pp**" at `:193` and `:942`, or re-attribute +7.9pp to 2000→2004.
4. **NEW-4 UPT residual.** "4.8% to 5.2%" → "**1.7% to 5.2% (mean 3.9%)**" at `:192`.

### Strongly recommended — closes the two remaining substantive gaps

5. **B13** — the peak choke-point figures remain the least-supported numbers in the document and still carry the
   Abstract, Conclusion RQ3, Recommendation 1, and the Ethics section's "*proving* that transit saves taxpayers
   money". Either cite a source or add one sentence labeling them an illustrative planning-level estimate and
   downgrade "proving" to "suggesting". Also widen NEW-6's ratio to 0.21×–0.61× or drop the interval.
6. **B1** — add one Limitation noting the lane-mile series' four project spikes (949 of the 1,320 total rise) are
   large relative to the named projects' physical footprint, that this attenuates β toward zero, and that the
   Wald rejection of unit elasticity (p=0.0063) should be read with that caveat. Currently the notebook rejects
   Duranton & Turner with no measurement caveat at all.
7. **A1 residual** — three phrases still claim direct retrieval and contradict Section 3's own "author-compiled
   estimates": `:960`, `:1103`, `:931`. Harmonize.

### Polish — no bearing on conclusions

Fig 1 legend "x100" → "÷100" (NEW-7); Fig 4 shared x-label (NEW-8); Fig 5 label collision (NEW-9); CV comment
"2002-2013" → "2003-2014" (NEW-10); compute real-dollar deflation from a CPI series instead of hardcoding
(NEW-5); align 9.47×/9.48× rounding; Fig 1's "~88% of 2019" applies the UPT ratio to PMT (84.4%); B9's Chow spec
still differs from the published model and the 2008 split still runs 5 observations on 4 parameters; VIF still
omits the constant (C7); data dictionary 24 of 68 (C5); `transit_rail_pmt_share` undocumented (C4);
`fillna(3.22)` at `fetch_and_build_dataset.py:88` (V5c).

### Do not touch — these are correct

Figure 3; the entire robustness matrix in Code Cell 8; the ADF table including its disclosure of the lane-mile
failure; the transit levels-vs-differences comparison (apart from the DW string); the marginal-PMT and AVO
sensitivity rows; the Andrews treatment in Section 4; and the RQ3 ~9× conclusion, confirmed robust across nominal
(9.16×), real 2024$ (9.47×), and marginal-PMT (8.40×) framings.
