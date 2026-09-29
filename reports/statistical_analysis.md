# Statistical Hypothesis Testing Report — StockSense Hackathon

**Member 1: EDA, Business KPIs & Statistical Analysis**  
**Dataset Analyzed**: `data/processed/master_dataset.csv` (736 records across 46 dates, 4 stores, 4 products)  
**Significance Threshold (α)**: 0.05  

---

## Executive Summary of Hypothesis Tests

| Test ID | Business Question | Test Method | Test Statistic | p-value | Decision (α=0.05) | Key Takeaway |
| :--- | :--- | :--- | :---: | :---: | :---: | :--- |
| **TEST 1** | Do promotions increase sales? | Welch's t-test / Mann-Whitney U | t = 5.1605 | **5.12e-07** | **Reject H0** | Highly significant +28.1% demand lift under active promotions. |
| **TEST 2** | Does demand differ by store format? | One-Way ANOVA / Kruskal-Wallis | F = 72.1985 | **2.39e-29** | **Reject H0** | Hypermarkets generate nearly double the volume of Express stores. |
| **TEST 3** | Is reorder breach linked to promo? | Chi-Square Test ($\chi^2$) | $\chi^2$ = 1.2188 | **0.2696** | **Fail to Reject H0** | High depletion pressure is universal across promo and non-promo days. |
| **TEST 4** | Does weekend demand exceed weekday? | Welch's t-test | t = 2.0851 | **0.0377** | **Reject H0** | Statistically significant weekend uplift of +10.2% in units sold. |

---

## Detailed Test Breakdowns

### TEST 1: Impact of Promotions on Daily Units Sold

- **Business Question**: Do promotional campaigns significantly increase customer demand?
- **Null Hypothesis ($H_0$)**: $\mu_{\text{promo}} = \mu_{\text{non-promo}}$ (Mean daily demand during promotions is equal to non-promotional demand).
- **Alternative Hypothesis ($H_1$)**: $\mu_{\text{promo}} \neq \mu_{\text{non-promo}}$ (Mean daily demand differs during promotions).
- **Statistical Results**:
  - Promotional Demand: Mean = **100.48 units** (N = 157)
  - Non-Promotional Demand: Mean = **78.45 units** (N = 579)
  - **Welch's t-test**: $t = 5.1605$, $p = 5.1232e-07$
  - **Mann-Whitney U Test**: $U = 58195.0$, $p = 6.9100e-08$
- **Decision**: **Reject $H_0$** ($p < 0.001$).
- **Business Implication**: Promotions produce an immediate **+28.08% lift** in unit velocity. Demand forecasting models must explicitly feature promotional calendar flags.

---

### TEST 2: Demand Disparity Across Store Formats

- **Business Question**: Does customer demand differ systematically across retail store types?
- **Null Hypothesis ($H_0$)**: $\mu_{\text{Hypermarket}} = \mu_{\text{Supermarket}} = \mu_{\text{Express}}$
- **Alternative Hypothesis ($H_1$)**: At least one store format has a different mean daily demand.
- **Statistical Results**:
  - **Hypermarket (S02 - Chennai)**: Mean = **113.39 units/day**
  - **Supermarket (S01 - Coimbatore, S04 - Salem)**: Mean = **79.80 units/day**
  - **Express (S03 - Madurai)**: Mean = **59.60 units/day**
  - **One-Way ANOVA**: $F = 72.1985$, $p = 2.3946e-29$
  - **Kruskal-Wallis Test**: $H = 147.1388$, $p = 1.1200e-32$
- **Decision**: **Reject $H_0$** ($p < 1e-28$).
- **Business Implication**: Store capacity and footfall drive dramatic volume divergence. Inventory replenishment parameters (reorder points, order batching) must be segmented by store format rather than globally unified.

---

### TEST 3: Inventory Reorder Risk vs Promotion Status

- **Business Question**: Are promotional days significantly more prone to breaching reorder buffer thresholds?
- **Null Hypothesis ($H_0$)**: Reorder threshold breaches are independent of promotional execution.
- **Alternative Hypothesis ($H_1$)**: Reorder threshold breaches are dependent on promotional execution.
- **Contingency Matrix**:
```
                      Reorder Safe (0)    Reorder Breach (1)    Total
No Promotion (0)             89                  490             579  (84.6% breach)
Active Promotion (1)         18                  139             157  (88.5% breach)
```
- **Statistical Results**:
  - **Pearson's $\chi^2$ Statistic**: $\chi^2 = 1.2188$ ($df = 1$)
  - **p-value**: $p = 0.2696$
- **Decision**: **Fail to Reject $H_0$** ($p = 0.2696 > 0.05$).
- **Business Implication**: While promotions increase unit velocity, inventory stock levels are kept lean across both promotional and non-promotional days (overall reorder breach rate is **85.5%** across the entire supply chain). Reorder buffers need structural upward calibration across all operating days.

---

### TEST 4: Weekend vs. Weekday Demand Distribution

- **Business Question**: Does consumer purchasing surge significantly on weekends?
- **Null Hypothesis ($H_0$)**: $\mu_{\text{Weekend}} = \mu_{\text{Weekday}}$
- **Alternative Hypothesis ($H_1$)**: $\mu_{\text{Weekend}} > \mu_{\text{Weekday}}$
- **Statistical Results**:
  - Weekend Mean: **88.89 units** (N = 224)
  - Weekday Mean: **80.63 units** (N = 512)
  - **Welch's t-test**: $t = 2.0851$, $p = 0.0377$
- **Decision**: **Reject $H_0$** ($p = 0.0377 < 0.05$).
- **Business Implication**: Weekend sales experience a statistically confirmed **+10.24% increase**. In-store restocking must occur by Friday evening to accommodate Saturday/Sunday traffic.
