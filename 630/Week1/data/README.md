# 🏅 Global Sports Fan Survey 2024

**2,200 respondents · 42 columns · 15 countries · 26 sports**

A richly featured synthetic survey dataset for EDA, fan segmentation, classification, and regression. All correlations (income ↔ spend, age ↔ viewing method, loyalty ↔ years) are intentionally calibrated to be internally consistent and realistic.

---

## Quick facts

| | |
|---|---|
| Rows | 2,200 |
| Columns | 42 |
| Countries | 15 |
| Sports | 26 across 4 categories |
| Survey period | January – December 2024 |
| Missing data | `secondary_sport` only (~44 % — fans who chose none) |
| License | CC0 1.0 — No rights reserved |

---

## Files

| File | Description |
|---|---|
| `sports_fan_survey_2024.csv` | Main dataset (2,200 × 42) |
| `data_dictionary.csv` | All 42 columns: type and description |
| `starter_notebook.ipynb` | EDA + K-Means segmentation + Random Forest classifier |

---

## Column groups

| Group | Columns |
|---|---|
| Survey metadata | respondent_id, survey_year, survey_month, survey_platform, response_time_minutes |
| Demographics | country, region, age, gender, education_level, employment_status, income_bracket |
| Sport preferences | primary_sport, sport_category, secondary_sport, years_following_sport, fan_loyalty_score |
| Viewing habits | primary_viewing_method, watch_frequency, weekly_hours_watching, streaming_subscriptions |
| Engagement | stadium_visits_per_year, social_media_follows_athletes, social_media_hours_weekly, creates_sports_content, news_source |
| Spending | merchandise_spend_usd, ppv_spend_usd, total_annual_spend_usd, extra_spend_willingness_usd |
| Participation | sports_betting_participation, fantasy_sports_participation |
| Attitudes | primary_motivation, willing_to_attend_major_event |
| Ratings (1–10) | broadcast_quality_rating, athlete_professionalism_rating, event_value_for_money_rating, media_coverage_rating, community_atmosphere_rating, overall_satisfaction_rating, sport_growth_perception_rating |
| 🎯 Target variable | fan_tier (Bronze / Silver / Gold / Platinum) |

---

## Highlights

### Top 5 sports
| Sport | Respondents |
|---|---|
| Soccer | 608 |
| Cricket | 321 |
| Basketball | 235 |
| Tennis | 155 |
| Rugby | 124 |

### Top 5 countries
| Country | Respondents |
|---|---|
| USA | 424 |
| India | 327 |
| Brazil | 166 |
| UK | 166 |
| Germany | 136 |

### Fan tier distribution
| Tier | Share | Description |
|---|---|---|
| 🥉 Bronze  | 30% | Casual fans — low engagement across all dimensions |
| 🥈 Silver  | 38% | Regular fans — moderate viewing and some spending |
| 🥇 Gold    | 22% | Committed fans — high loyalty, regular attendance |
| 🏆 Platinum | 10% | Super fans — top decile on every engagement metric |

### Key stats
| Metric | Value |
|---|---|
| Median weekly viewing | 6.4 hrs |
| Median stadium visits/year | 1 |
| Median total annual spend | $57 |
| Platinum vs Bronze spend ratio | 6.8× |
| Create online sports content | 11% |
| Participate in sports betting | 31% |
| Primary viewing: streaming (under 30) | 40% |
| Primary viewing: streaming (50+) | 21% |
| Avg social media hrs/week (under 30) | 3.4 hrs |
| Avg social media hrs/week (50+) | 1.0 hrs |

---

## Built-in correlations

| Pattern | Direction |
|---|---|
| Income ↔ spending | Higher income → more merch, PPV, and stadium visits |
| Age ↔ viewing method | Younger fans stream; older fans use cable TV |
| Loyalty ↔ years following | More years → higher loyalty score |
| Loyalty ↔ merchandise | Higher loyalty → significantly more merch spend |
| Rating inter-correlation | Shared latent positivity factor (as in real surveys) |
| Content creation | Young + loyal + social-active → more likely to post content |

---

## Suggested analyses

**🟢 Beginner**
- Distribution of primary sports by region (horizontal bar / choropleth)
- Merchandise spend by income bracket (grouped box plot)
- What % of each fan tier attends live events?

**🟡 Intermediate**
- Predict `fan_tier` with a Random Forest classifier (~75 % accuracy achievable)
- Cluster fans into personas using K-Means on engagement columns
- Regress `total_annual_spend_usd` on loyalty, income, and stadium visits

**🔴 Advanced**
- PCA / UMAP on the 7 rating columns — do rating archetypes emerge?
- Quantile regression: how does `extra_spend_willingness_usd` vary across income groups?
- Build a sport-category classifier from demographics alone (country, age, gender)

---

## Provenance

Synthetic dataset generated in Python (`numpy`, `pandas`). No real personal data. Distributions calibrated against public sports viewership research to ensure realistic internal correlations.

## License

**CC0 1.0 Universal.** No rights reserved. Use freely for any purpose.
