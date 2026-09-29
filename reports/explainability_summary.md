# StockSense Model Explainability Report

## 1. Top Global Feature Drivers (Stock-out Risk)

| Rank | Feature | Importance Score | Business Impact Description |
| :---: | :--- | :---: | :--- |
| 1 | `inventory_to_demand_ratio` | 0.8172 | Driver of stockout risk classification decision |
| 2 | `days_of_inventory` | 0.0683 | Driver of stockout risk classification decision |
| 3 | `opening` | 0.0467 | Driver of stockout risk classification decision |
| 4 | `reorder_lvl` | 0.0305 | Driver of stockout risk classification decision |
| 5 | `rolling_std_7` | 0.0253 | Driver of stockout risk classification decision |
| 6 | `rolling_mean_14` | 0.0119 | Driver of stockout risk classification decision |
| 7 | `store_id_S03` | 0.0000 | Driver of stockout risk classification decision |
| 8 | `store_id_S04` | 0.0000 | Driver of stockout risk classification decision |

---

## 2. Sample Explanation Reasons (Store × Product Level)

- **Store `S04` | Product `P442` (Snacks)** [2026-08-30]
  - Stock: `111` units | Reorder Level: `110` units | 7-Day Forecast: `535` units
  - **Key Reasons**: Critically low days of inventory (1.5 days remaining based on 7-day trend) | 7-day forecasted demand (535 units) exceeds available stock (111 units) | Supplier replenishment lead time is relatively high (4 days)

- **Store `S04` | Product `P442` (Snacks)** [2026-08-31]
  - Stock: `114` units | Reorder Level: `108` units | 7-Day Forecast: `556` units
  - **Key Reasons**: Critically low days of inventory (1.5 days remaining based on 7-day trend) | 7-day forecasted demand (556 units) exceeds available stock (114 units)

- **Store `S04` | Product `P442` (Snacks)** [2026-09-01]
  - Stock: `73` units | Reorder Level: `106` units | 7-Day Forecast: `547` units
  - **Key Reasons**: Current closing stock (73 units) is at or below reorder threshold (106 units) | Critically low days of inventory (1.0 days remaining based on 7-day trend) | 7-day forecasted demand (547 units) exceeds available stock (73 units)

- **Store `S04` | Product `P442` (Snacks)** [2026-09-02]
  - Stock: `74` units | Reorder Level: `123` units | 7-Day Forecast: `542` units
  - **Key Reasons**: Current closing stock (74 units) is at or below reorder threshold (123 units) | Critically low days of inventory (1.0 days remaining based on 7-day trend) | 7-day forecasted demand (542 units) exceeds available stock (74 units) | Supplier replenishment lead time is relatively high (4 days)

- **Store `S04` | Product `P442` (Snacks)** [2026-09-03]
  - Stock: `65` units | Reorder Level: `120` units | 7-Day Forecast: `517` units
  - **Key Reasons**: Current closing stock (65 units) is at or below reorder threshold (120 units) | Critically low days of inventory (0.9 days remaining based on 7-day trend) | 7-day forecasted demand (517 units) exceeds available stock (65 units) | Supplier replenishment lead time is relatively high (3 days)

- **Store `S04` | Product `P442` (Snacks)** [2026-09-04]
  - Stock: `98` units | Reorder Level: `123` units | 7-Day Forecast: `504` units
  - **Key Reasons**: Current closing stock (98 units) is at or below reorder threshold (123 units) | Critically low days of inventory (1.3 days remaining based on 7-day trend) | 7-day forecasted demand (504 units) exceeds available stock (98 units)

- **Store `S04` | Product `P442` (Snacks)** [2026-09-05]
  - Stock: `87` units | Reorder Level: `140` units | 7-Day Forecast: `504` units
  - **Key Reasons**: Current closing stock (87 units) is at or below reorder threshold (140 units) | Critically low days of inventory (1.2 days remaining based on 7-day trend) | 7-day forecasted demand (504 units) exceeds available stock (87 units) | Supplier replenishment lead time is relatively high (3 days)

- **Store `S04` | Product `P442` (Snacks)** [2026-09-06]
  - Stock: `61` units | Reorder Level: `127` units | 7-Day Forecast: `521` units
  - **Key Reasons**: Current closing stock (61 units) is at or below reorder threshold (127 units) | Critically low days of inventory (0.8 days remaining based on 7-day trend) | 7-day forecasted demand (521 units) exceeds available stock (61 units) | Supplier replenishment lead time is relatively high (3 days)

- **Store `S04` | Product `P442` (Snacks)** [2026-09-07]
  - Stock: `107` units | Reorder Level: `104` units | 7-Day Forecast: `500` units
  - **Key Reasons**: Critically low days of inventory (1.4 days remaining based on 7-day trend) | 7-day forecasted demand (500 units) exceeds available stock (107 units)

- **Store `S04` | Product `P442` (Snacks)** [2026-09-08]
  - Stock: `158` units | Reorder Level: `146` units | 7-Day Forecast: `499` units
  - **Key Reasons**: Critically low days of inventory (2.0 days remaining based on 7-day trend) | 7-day forecasted demand (499 units) exceeds available stock (158 units) | Supplier replenishment lead time is relatively high (4 days)

