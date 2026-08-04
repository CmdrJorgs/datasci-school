# Data Transformation & Calculation Summary

Project: "Winning the lottery is a scam that is getting worse over time."
Sources: Powerball (2010+), Mega Millions (2002+), Pick 10 (1987+) historical winning numbers.
Stack: Power Query M (ETL) + DAX (measures) in Power BI.

---

## 1. Source & Load

| Step | What | Why |
|------|------|-----|
| `SharePoint.Files(SiteUrl)` | Pull 3 CSVs from OneDrive/personal-SharePoint site root | Service-resolvable moniker; static base URL maps to stored credentials (fixed the `DMTS_MonikerNotFoundError` 404) |
| Filter `[Folder Path]` contains `/Data/640/Lottery/` | Load only the 3 target files | Avoid same-named files elsewhere in OneDrive; faster enumeration |
| `Csv.Document` + `Table.PromoteHeaders` | Parse each CSV, promote header row | Raw text → typed table |

Site root used (root only, not the folder path):
`https://bellevueuniversity-my.sharepoint.com/personal/djorgensen_my365_bellevue_edu`

---

## 2. Query `_Base` — normalize 3 schemas into 1

Three lotteries ship three different layouts. Unified to a common shape so they can append and share one parse.

| Transform | Applied to | Reasoning |
|-----------|-----------|-----------|
| Add `Lottery` literal | all | Identity column survives the append; drives all faceting/legends |
| `Date.FromText(.., "MM/dd/yyyy")` → `DrawDate` | all | Text date → real date; enables Year axis and time trend (core of the "over time" story) |
| `Nums()` helper: split on space, drop blanks, `Number.FromText` | all | Winning numbers arrive as one packed string; convert to a list of ints |
| `List.FirstN(...,5)` main / `List.Last(...)` special | Powerball | 6 tokens = 5 white + trailing Powerball; last token is the red ball |
| main = `Winning Numbers`, special = `Mega Ball` column | Mega Millions | Special ball already in its own column |
| main = all 20, special = `null` | Pick 10 | No special ball in that game |
| `Table.TransformColumns` on existing `Multiplier` | Powerball, Mega Millions | Fixes the "Multiplier already exists" error — source already had the column, so transform in place instead of adding. `Text.From` guards values SharePoint pre-typed as numeric |
| `Multiplier = null` added | Pick 10 | No such column; keep schema aligned for the append |
| `Table.Combine` | all 3 | Single fact source; one parse feeds both downstream tables (DRY) |
| Add `Year = Date.Year([DrawDate])` | combined | Primary time grain for every trend visual |

Output columns: `Lottery, DrawDate, Year, MainList (list), SpecialNumber, Multiplier`.

---

## 3. Query `LotteryDraws` — one row per draw (odds engine)

| Calculation | Formula | Reasoning |
|-------------|---------|-----------|
| `MaxMainNumber` | `List.Max(MainList)` | Highest ball drawn = proxy for the number-matrix size |
| `MinMainNumber`, `MainCount` | list aggregates | Sanity checks; distinguishes 5-pick vs 20-pick games |
| `PoolMainMax` | annual max of `MaxMainNumber` per Lottery/Year (group + join) | Pool-size proxy. Lotteries expand the matrix (Powerball 59→69, Mega 56→75→70); annual observed max captures each jump. Bigger pool = worse odds — the mechanical heart of "getting worse" |
| `PoolSpecialMax` | annual max of `SpecialNumber` per Lottery/Year | Special-ball pool also grew; multiplies jackpot odds |
| `EstJackpotOdds` | `C(PoolMainMax,5) × PoolSpecialMax`, only when `MainCount = 5` | Combinatorial jackpot odds. `C(n,5) = n(n-1)(n-2)(n-3)(n-4)/120`. Pick 10 excluded (different win mechanic) → null |

Why annual pool, not the true matrix: the data carries no matrix metadata. Observed annual max understates the true cap by ~1–3 but reproduces every expansion **step** — sufficient for the trend argument.

---

## 4. Query `LotteryNumbers` — tidy long (one ball per row)

| Transform | Reasoning |
|-----------|-----------|
| `ExpandListColumn(MainList)` → `BallValue`, tag `BallCategory = "Main"` | Wide packed numbers → tidy rows; required for histogram / density / frequency plots |
| Special rows: filter non-null, `BallValue = SpecialNumber`, tag `"Special"` | Keep special balls analyzable separately |
| `Table.Combine` main + special, type `BallValue` as Int64 | Single distribution table, faceted by Lottery (small multiples) |

Output columns: `Lottery, DrawDate, Year, BallCategory, BallValue`.

DAX calculated column for binning (histogram + heatmap; must be a **column**, not a measure — needs row context):
```dax
BallBin = ROUNDDOWN( LotteryNumbers[BallValue] / 3, 0 ) * 3 + 1
```
Bin width 3, labeled by left edge (1,4,7,…). Continuous X axis required or bins collapse.

Optional normalized-frequency measure (comparison across games with different draw volumes; used if density-style % ever needed):
```dax
Ball Density % =
DIVIDE(
    COUNTROWS( LotteryNumbers ),
    CALCULATE( COUNTROWS( LotteryNumbers ),
        ALLEXCEPT( LotteryNumbers, LotteryNumbers[Lottery] ) )
)
```

---

## 5. DAX Measures

### Core odds
- `Jackpot Odds = MAX(EstJackpotOdds)` — one value per filter context (constant within Lottery/Year).
- `Win Probability Pct = 1 / [Jackpot Odds] * 100` — tiny by design; visualizes hopelessness.
- `Pool Size = MAX(PoolMainMax)` — bubble size.

### Cost to win
- `Ticket Price` — `SWITCH` by lottery (Powerball/Mega $2, Pick 10 $1); no price in the data.
- `Expected Spend to Win = [Jackpot Odds] × [Ticket Price]` — dollars burned to statistically buy one jackpot.

### Getting-worse engine
- `Baseline Odds` — odds in each lottery's launch year (`MIN(Year)` per lottery, via `ALLEXCEPT`).
- `Odds vs Launch = [Jackpot Odds] / [Baseline Odds]` — "X× harder to win than at launch." Headline metric.
- `Prev Year Odds` / `Odds YoY %` — year-over-year worsening.

### Support
- `Draws Count`, `Avg Multiplier` (multiplier-upsell angle).

---

## 6. What-if `Jackpot $` + real expected value

> **Status:** what-if scaler dropped from the dashboard — the disconnected `GENERATESERIES` param table timed out on every build. EV measures below retained for reference. Act-3 "verdict" now carried by the static **Breakeven Jackpot** line (Year × Breakeven Jackpot), which needs no parameter.

| Item | Reasoning |
|------|-----------|
| Disconnected `Jackpot $` parameter (`GENERATESERIES`) + `SELECTEDVALUE` | Slider input, no relationship — jackpot dollars are not in the data. **Abandoned: PBI timeout on build** |
| `Prob Jackpot = 1 / [Jackpot Odds]` | Win probability |
| `EV Per Ticket = [Prob Jackpot] × [Jackpot $ Value] − [Ticket Price]` | Raw expected value; nearly always negative |
| `EV Return % = [Prob Jackpot] × [Jackpot $ Value] / [Ticket Price]` | Cents back per $1; < 1 = losing bet |
| `Breakeven Jackpot = [Jackpot Odds] × [Ticket Price]` | Jackpot needed for EV = 0; rises with every expansion = moving goalpost |
| `EV Per Ticket (Real)` — × 0.63 tax × 0.52 lump-sum × 0.70 split | Corrects naive EV for reality; stays negative across the whole range = the kill shot |

---

## 7. Visualization mapping

| Visual | Table | Encoding |
|--------|-------|----------|
| Scatterplot | LotteryDraws | Year × MaxMainNumber (pool expansion) |
| Bubble chart | LotteryDraws | Year × Win Probability Pct (log Y), size = Pool Size, color = Lottery |
| Histogram | LotteryNumbers | count of BallValue, binned via `BallBin` |
| Heatmap (Matrix) | LotteryNumbers | Year (rows) × BallBin (cols), background color = count. Ceiling marches right over time = pool growth. Replaced density plot (no native KDE; binned-area workaround looked poor) |
| Small multiples | LotteryNumbers | BallValue distribution faceted by Lottery |
| Line chart (6th) | LotteryDraws | Year × Breakeven Jackpot (log Y), color = Lottery — the moving goalpost. Replaced what-if EV scaler (disconnected param table timed out on build) |

---

## 8. Assumptions & limitations (disclose to graders)

- Pool size = observed **annual max**, a slight understatement of the true matrix cap.
- Ticket prices hardcoded; no price data in source.
- EV realism factors (tax 0.63 / lump-sum 0.52 / split 0.70) are round-number estimates.
- Pick 10 has no jackpot-odds / EV (different game mechanic); it serves as a stable long-history contrast baseline.
