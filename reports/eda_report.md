# Comprehensive EDA & Business Insights Report — StockSense Hackathon

**Author**: Member 1 (EDA, Business KPIs & Statistical Analysis)  
**Dataset Analyzed**: `data/processed/master_dataset.csv`  
**Dataset Scope**: 736 daily observations across 46 days (`2026-08-01` to `2026-09-15`), 4 retail stores, and 4 product categories.  
**Generated Date**: 2026-09-29  

---

## 1. Executive Summary & Key Findings

| Dimension | Primary Finding | Quantitative Evidence | Strategic Business Action |
| :--- | :--- | :--- | :--- |
| **Top Revenue Category** | **Dairy** and **Beverages** generate 74.4% of total retail turnover. | Dairy: ₹1,135,980 (35.3%)<br>Beverages: ₹1,257,796 (39.1%) | Protect supply chains for high-volume staples with dedicated supplier SLAs. |
| **Store Footprint & Growth** | **Hypermarket (Chennai - S02)** generates the highest unit demand; all stores exhibit steady, healthy demand trajectories. | Hypermarket: 113.4 units/day<br>Supermarket: 79.8 units/day<br>Express: 59.6 units/day | Differentiate stock replenishment frequencies by store format rather than a one-size-fits-all policy. |
| **Promotional Lift** | Promotions trigger a massive, statistically significant surge in demand. | **+28.08% overall demand lift**<br>(100.5 vs 78.4 units/day, $p < 0.0001$) | Align store stock pre-orders with promotional event dates to avoid buffer exhaustion. |
| **Weekend Demand Dynamics** | Consumer shopping accelerates meaningfully over weekends (Sat–Sun). | **+10.24% weekend uplift**<br>(88.9 vs 80.6 units/day, $p = 0.0377$) | Shift store replenishment and restocking deliveries to Friday afternoons. |
| **Demand Volatility** | Dairy displays the highest demand variation due to perishable consumption patterns. | Dairy CV = **28.81%**<br>Snacks CV = **27.89%** | Implement dynamic safety stock buffers tailored to product shelf life. |
| **Inventory & Reorder Health** | No zero-stock stockouts were observed, but stores operate on **ultra-lean buffers**. | DOI: **1.16 days**<br>Reorder breach rate: **85.5%** of operating days | Replenishment works just-in-time, but higher safety stock is required during promo & weekend spikes. |

---

## 2. Business Question Analyses & Detailed Visual Insights

### Question 1: Which Product Categories Generate the Most Revenue?
- **Total Revenue**: ₹3,219,276.25 across 61,196 total units sold.
- **Category Breakdown**:
  1. **Beverages (`P330`)**: ₹1,257,796.00 (23,732 units sold | 39.1% revenue share)
  2. **Dairy (`P101`)**: ₹1,135,980.00 (18,933 units sold | 35.3% revenue share)
  3. **Snacks (`P442`)**: ₹450,150.00 (15,005 units sold | 14.0% revenue share)
  4. **Personal Care (`P205`)**: ₹375,350.25 (3,526 units sold | 11.7% revenue share)
- **Business Implication**: Beverages and Dairy are high-velocity revenue drivers. While Personal Care has lower volume, its unit margin is high (₹41/unit, 34.2% gross margin), making it a key profit contributor.

---

### Question 2: Which Stores are Growing or Declining?
- **Store Tiering**:
  - **S02 (Chennai - Hypermarket)**: Top performing store format with 20,864 units sold (113.4 units/day average).
  - **S01 (Coimbatore - Supermarket)**: Consistent, stable demand with 15,351 units sold (83.4 units/day average).
  - **S04 (Salem - Supermarket)**: 14,015 units sold (76.2 units/day average).
  - **S03 (Madurai - Express)**: Smallest footprint with 10,966 units sold (59.6 units/day average).
- **Trajectory**: 7-day rolling demand trends show no store is in active decline. All stores exhibit periodic volume surges corresponding to weekend clusters and promotional campaigns.

---

### Question 3: Do Promotions Increase Units Sold?
- **Non-Promotional Days (N=579)**: Mean demand = 78.45 units/day (Median = 79.0).
- **Active Promotional Days (N=157)**: Mean demand = 100.48 units/day (Median = 101.0).
- **Promotion Lift**: **+28.08%** ($t = 5.1605, p = 5.12 \times 10^{-7}$).
- **Lift by Category**:
  - **Dairy (`P101`)**: +29.7% lift under promotion
  - **Beverages (`P330`)**: +28.3% lift under promotion
  - **Snacks (`P442`)**: +26.9% lift under promotion
  - **Personal Care (`P205`)**: +25.4% lift under promotion

---

### Question 4: How Does Weekend Demand Differ from Weekday Demand?
- **Weekday Demand (Mon–Fri, N=512)**: Mean = 80.63 units/day.
- **Weekend Demand (Sat–Sun, N=224)**: Mean = 88.89 units/day.
- **Difference**: Weekend shopping drives a statistically verified **+10.24% increase** in daily units sold ($t = 2.0851, p = 0.0377$).
- **Peak Day**: Saturday represents the highest volume day across all four store locations.

---

### Question 5: Which Products Have the Most Volatile Demand?
- Demand volatility is measured via the **Coefficient of Variation** ($CV = \frac{\sigma}{\mu}$):
  1. **Dairy (`P101`)**: $CV = 28.81\%$ ($\mu = 102.90, \sigma = 29.64$) — *Highest volatility due to short 3-day shelf life and variable daily domestic consumption.*
  2. **Snacks (`P442`)**: $CV = 27.89\%$ ($\mu = 81.55, \sigma = 22.75$) — *Impulse purchasing patterns.*
  3. **Personal Care (`P205`)**: $CV = 26.79\%$ ($\mu = 19.16, \sigma = 5.13$) — *Steady, planned purchases.*
  4. **Beverages (`P330`)**: $CV = 25.34\%$ ($\mu = 128.98, \sigma = 32.68$) — *High volume, most stable coefficient of variation.*

---

### Question 6: Which Stores & Categories Experience Stock Depletion / Reorder Risks?
- **Stock-out Rate**: **0.00%** (No historical days reached closing stock of 0).
- **Reorder Level Breach Rate**: **85.46%** (629 of 736 store-product days had closing stock $\le$ reorder level).
- **Days of Inventory (DOI)**: **1.16 days** across the network.
  - S01 (Coimbatore): 1.25 days of inventory
  - S04 (Salem): 1.15 days of inventory
  - S02 (Chennai): 1.12 days of inventory
  - S03 (Madurai): 1.10 days of inventory
- **Supply Chain Finding**: Stores operate on an aggressive daily replenishment cadence (lead times between 1 to 4 days). Because average closing stock is nearly equal to one day's sales, any delivery delay during a promotion or weekend peak carries extreme stock-out risk.

---

## 3. Business KPI Dashboard Summary

| KPI | Value | Status / Benchmark | Business Meaning |
| :--- | :--- | :--- | :--- |
| **Total Revenue** | **₹3,219,276.25** | High | Gross point-of-sale customer revenue over 46 days. |
| **Total Units Sold** | **61,196 units** | High | Combined volume across 4 SKUs and 4 store branches. |
| **Stock-out Rate** | **0.00%** | Excellent | Zero unfulfilled customer demand recorded historically. |
| **Reorder Level Breach Rate** | **85.46%** | Warning / Lean | Buffer levels drop below safety reorder threshold regularly. |
| **Inventory Turnover Ratio** | **635.52x** (annualized: 5,048x) | Ultra-High Velocity | Rapid daily stock turnover; items sell as soon as received. |
| **Days of Inventory (DOI)** | **1.16 days** | Very Tight | Less than 28 hours of stock buffer on hand at any time. |
| **Promotion Demand Lift** | **+28.08%** | Strong Positive | Massive customer responsiveness to promotional campaigns. |
| **Estimated Lost Sales** | **₹0.00 (0 units)** | Clean Baseline | No unserved lost sales under historical replenishment. |

---

## 4. Recommendations for Member 2 (Machine Learning & Forecasting)

1. **Feature Engineering Recommendations**:
   - **Promotional Flags**: Create `promo_active`, `promo_lead_1d`, and `promo_lag_1d` features (vital given the +28.1% lift).
   - **Calendar & Day-of-Week**: `is_weekend`, `day_of_week`, `day_of_month` (captures the +10.2% weekend uplift).
   - **Store Type Encoding**: Include `store_type` categorical encodings or target encodings (Hypermarket vs Express volume disparity).
   - **Lag Features**: Construct `lag_1`, `lag_7`, `rolling_mean_7`, `rolling_std_7` to capture the serial autocorrelation in daily store demand.
2. **Stock-out Classification Modeling**:
   - Because historical absolute stockouts are 0, define realistic operational risk target labels such as `reorder_required` ($\text{closing} \le \text{reorder\_lvl}$) or `stockout_risk` ($\text{closing} < \text{lead\_days} \times \text{daily\_demand}$) to build predictive early-warning classifiers.
3. **Loss Function / Evaluation Metric**:
   - Use **RMSE / MAE** for volume forecasting and **WAPE / SMAPE** for cross-store comparability.
