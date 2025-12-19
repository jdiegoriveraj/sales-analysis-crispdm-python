# sales-analysis-crispdm-python
End-to-end sales analysis using CRISP-DM, including KPIs, RFM segmentation and business insights in Python (Jupyter Notebook)

# Sales Analysis using CRISP-DM

End-to-end sales analysis for a real liquid cleaning products business (Bclean), applying CRISP-DM to identify purchase patterns, segment customers (RFM) and support data-driven decision making in Python (Jupyter Notebook)

---

## Project Overview

This project analyzes a sales dataset to uncover **customer behavior**, **top-performing products**, and **sales trends over time**.  
The analysis follows the **CRISP-DM framework**, ensuring a structured and business-oriented approach.

The goal is not only to analyze data, but to **generate insights and recommendations** that could support real business decisions.

---

## CRISP-DM Phases

### 1.Business Understanding
- Identify key business questions:
  - Who are the most valuable customers?
  - Which products generate the highest revenue?
  - How do sales behave over time?
- Define KPIs to measure performance.

---

### 2️.Data Understanding
- Explore dataset structure and data types
- Identify missing values and duplicates
- Perform descriptive statistics

---

### 3️.Data Preparation
- Clean and standardize column names
- Convert date fields and extract:
  - Year
  - Month
  - Day of week
- Create additional features for analysis

---

### 4️.Modeling
- **RFM Analysis** (Recency, Frequency, Monetary)
- Customer segmentation:
  - Champions
  - Loyal
  - Potential
  - At Risk
- **ABC Analysis** for products (Pareto principle)

---

### 5️.Evaluation
- Identify:
  - Top 20% customers by revenue
  - Products driving 80% of sales
  - Best and worst sales months
- Validate insights with visualizations

---

### 6️.Conclusions & Business Recommendations
- Customer retention strategies
- Inventory optimization
- Sales and cross-selling opportunities

---

## Key Insights

- A small percentage of customers generates the majority of revenue.
- Product sales follow a Pareto distribution (80/20 rule).
- Clear seasonality patterns are present in monthly sales.
- High-value customers can be targeted with loyalty programs.

---

## Strategic Recommendations

- Focus retention strategies on **Champions** customers
- Prioritize inventory for **Category A** products
- Launch reactivation campaigns for **At Risk** customers
- Use data-driven decision making for pricing and promotions

---

## Tech Stack

- **Python**
- pandas
- numpy
- matplotlib
- seaborn
- Jupyter Notebook
