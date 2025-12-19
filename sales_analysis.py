"""
Sales Analysis using CRISP-DM
Real business case based on Bclean (liquid cleaning products company)
"""

# =========================
# Imports & Configuration
# =========================
import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

plt.style.use("seaborn-v0_8-darkgrid")
sns.set_palette("husl")
plt.rcParams["figure.figsize"] = (12, 6)
plt.rcParams["font.size"] = 10

# =========================
# Paths
# =========================
DATA_PATH = "data/bclean_sales.xlsx"
RESULTS_PATH = "results"

os.makedirs(RESULTS_PATH, exist_ok=True)

# =========================
# Load Data
# =========================
df = pd.read_excel(DATA_PATH)

print("=" * 60)
print("CRISP-DM PHASE: DATA UNDERSTANDING")
print("=" * 60)

print("\nFirst 5 rows:")
print(df.head())

print("\nDataset structure:")
print(df.info())

# =========================
# Data Preparation
# =========================
print("\n" + "=" * 60)
print("CRISP-DM PHASE: DATA PREPARATION")
print("=" * 60)

df.columns = [
    "Sale_Date", "Sale", "Sale_ID", "Customer", "Product",
    "Amount", "Price", "Total_Sale", "Pay", "Image",
    "Month", "Year", "Sale_Type"
]

df["Sale_Date"] = pd.to_datetime(df["Sale_Date"])
df["Month_Name"] = df["Sale_Date"].dt.month_name()
df["Weekday"] = df["Sale_Date"].dt.day_name()

print("\nMissing values:")
print(df.isnull().sum())

print(f"\nDuplicates: {df.duplicated().sum()}")

# =========================
# Business KPIs
# =========================
print("\n" + "=" * 60)
print("CRISP-DM PHASE: MODELING – DESCRIPTIVE ANALYSIS")
print("=" * 60)

total_sales = df["Total_Sale"].sum()
transactions = len(df)
avg_ticket = df["Total_Sale"].mean()
unique_customers = df["Customer"].nunique()

print(f"Total Sales: ${total_sales:,.0f}")
print(f"Transactions: {transactions}")
print(f"Average Ticket: ${avg_ticket:,.0f}")
print(f"Unique Customers: {unique_customers}")

# =========================
# Monthly Sales
# =========================
monthly_sales = (
    df.groupby(df["Sale_Date"].dt.to_period("M"))["Total_Sale"]
    .sum()
)

# =========================
# Product Analysis (ABC)
# =========================
products = (
    df.groupby("Product")
    .agg(
        Num_Sales=("Sale_ID", "count"),
        Units_Sold=("Amount", "sum"),
        Revenue=("Total_Sale", "sum")
    )
    .sort_values("Revenue", ascending=False)
    .reset_index()
)

products["Revenue_Pct"] = products["Revenue"] / products["Revenue"].sum() * 100
products["Cum_Pct"] = products["Revenue_Pct"].cumsum()

products["ABC_Category"] = products["Cum_Pct"].apply(
    lambda x: "A" if x <= 80 else "B" if x <= 95 else "C"
)

# =========================
# RFM Analysis
# =========================
reference_date = df["Sale_Date"].max() + pd.Timedelta(days=1)

rfm = (
    df.groupby("Customer")
    .agg(
        Recency=("Sale_Date", lambda x: (reference_date - x.max()).days),
        Frequency=("Sale_ID", "count"),
        Monetary=("Total_Sale", "sum")
    )
    .reset_index()
)

def rfm_score(series, ascending=True):
    try:
        return pd.qcut(
            series, 5,
            labels=[5,4,3,2,1] if ascending else [1,2,3,4,5],
            duplicates="drop"
        )
    except ValueError:
        return pd.cut(
            series, 5,
            labels=[5,4,3,2,1] if ascending else [1,2,3,4,5]
        )

rfm["R"] = rfm_score(rfm["Recency"], ascending=True)
rfm["F"] = rfm_score(rfm["Frequency"].rank(method="first"), ascending=False)
rfm["M"] = rfm_score(rfm["Monetary"].rank(method="first"), ascending=False)

rfm = rfm.fillna(3)

def segment_customer(row):
    r, f, m = int(row["R"]), int(row["F"]), int(row["M"])
    if r >= 4 and f >= 4 and m >= 4:
        return "Champions"
    elif f >= 4 and m >= 4:
        return "Loyal"
    elif r >= 4 and f <= 2:
        return "Potential"
    elif r <= 2 and f >= 3:
        return "At Risk"
    elif r <= 2 and f <= 2:
        return "Lost"
    else:
        return "Occasional"

rfm["Segment"] = rfm.apply(segment_customer, axis=1)
rfm.sort_values("Monetary", ascending=False, inplace=True)

rfm.to_csv(f"{RESULTS_PATH}/rfm_analysis.csv", index=False)

# =========================
# Visualizations
# =========================

# 1. Monthly Sales Trend
monthly_sales.plot(marker="o")
plt.title("Monthly Sales Trend")
plt.ylabel("Sales ($)")
plt.tight_layout()
plt.savefig(f"{RESULTS_PATH}/1_monthly_sales_trend.png", dpi=300)
plt.close()

# 2. Top 10 Customers
top_customers = rfm.head(10)
plt.barh(top_customers["Customer"], top_customers["Monetary"])
plt.title("Top 10 Customers by Revenue")
plt.xlabel("Revenue ($)")
plt.tight_layout()
plt.savefig(f"{RESULTS_PATH}/2_top_customers.png", dpi=300)
plt.close()

# 3. RFM Segments Distribution
rfm["Segment"].value_counts().plot.pie(autopct="%1.1f%%")
plt.title("Customer Segmentation (RFM)")
plt.ylabel("")
plt.tight_layout()
plt.savefig(f"{RESULTS_PATH}/3_rfm_segments_distribution.png", dpi=300)
plt.close()

# 4. Top Products
top_products = products.head(10)
plt.barh(top_products["Product"], top_products["Revenue"])
plt.title("Top 10 Products by Revenue")
plt.xlabel("Revenue ($)")
plt.tight_layout()
plt.savefig(f"{RESULTS_PATH}/4_top_products.png", dpi=300)
plt.close()

# 5. Pareto Chart
fig, ax1 = plt.subplots()
ax1.bar(products.index, products["Revenue"])
ax2 = ax1.twinx()
ax2.plot(products.index, products["Cum_Pct"], color="red")
ax2.axhline(80, linestyle="--")
plt.title("Pareto Analysis – Products")
plt.tight_layout()
plt.savefig(f"{RESULTS_PATH}/5_pareto_products.png", dpi=300)
plt.close()

print("\nAnalysis completed successfully.")
print(f"Results saved in '{RESULTS_PATH}/'")
