import matplotlib.pyplot as plt
import openpyxl
import pandas as pd
import seaborn as sns

# Set visual style for charts
sns.set_theme(style="whitegrid")

# ==========================================
# STEP 1: LOAD AND INSPECT DATA
# ==========================================
file_name = "retail_sales_dataset.xlsx"
print(f"Loading dataset from '{file_name}'...")

try:
  df = pd.read_excel(file_name)
except FileNotFoundError:
  print(
      f"Error: '{file_name}' not found. Please ensure it's in the same directory."
  )
  exit()

print(f"\n--- Dataset Overview ---")
print(f"Total Rows: {df.shape[0]}, Total Columns: {df.shape[1]}")
print(df.info())

# Ensure Date column is datetime type
df["Date"] = pd.to_datetime(df["Date"])
df["Month"] = df["Date"].dt.to_period("M")

# ==========================================
# STEP 2: CALCULATE KEY ANALYTICS & KPIS
# ==========================================
print("\nCalculating Business KPIs...")

total_revenue = df["Total_Sales"].sum()
total_units_sold = df["Quantity"].sum()
total_transactions = df["Transaction_ID"].nunique()
avg_order_value = total_revenue / total_transactions

# 1. Sales by Product Category
category_sales = (
    df.groupby("Category")
    .agg(
        Total_Revenue=("Total_Sales", "sum"),
        Units_Sold=("Quantity", "sum"),
        Order_Count=("Transaction_ID", "count"),
    )
    .reset_index()
)
category_sales["Avg_Transaction_Value"] = (
    category_sales["Total_Revenue"] / category_sales["Order_Count"]
).round(2)
category_sales = category_sales.sort_values(
    by="Total_Revenue", ascending=False
)

# 2. Sales by Region
region_sales = (
    df.groupby("Region")
    .agg(
        Total_Revenue=("Total_Sales", "sum"),
        Units_Sold=("Quantity", "sum"),
        Transactions=("Transaction_ID", "count"),
    )
    .reset_index()
    .sort_values(by="Total_Revenue", ascending=False)
)

# 3. Monthly Sales Trends
monthly_sales = (
    df.groupby("Month")
    .agg(
        Total_Revenue=("Total_Sales", "sum"),
        Transactions=("Transaction_ID", "count"),
    )
    .reset_index()
)
monthly_sales["Month"] = monthly_sales["Month"].astype(str)

# 4. Top Payment Methods
payment_analysis = (
    df.groupby("Payment_Method")
    .agg(
        Total_Revenue=("Total_Sales", "sum"),
        Usage_Count=("Transaction_ID", "count"),
    )
    .reset_index()
    .sort_values(by="Total_Revenue", ascending=False)
)

# ==========================================
# STEP 3: EXPORT RESULTS TO A MULTI-SHEET EXCEL REPORT
# ==========================================
output_report = "retail_sales_analysis_report.xlsx"
print(f"\nExporting analytical report to '{output_report}'...")

with pd.ExcelWriter(output_report, engine="openpyxl") as writer:
  # Sheet 1: Raw Data (preserved)
  df.drop(columns=["Month"]).to_excel(
      writer, sheet_name="Original_Data", index=False
  )

  # Sheet 2: Category Summary
  category_sales.to_excel(writer, sheet_name="Category_Performance", index=False)

  # Sheet 3: Regional Breakdown
  region_sales.to_excel(writer, sheet_name="Regional_Analysis", index=False)

  # Sheet 4: Monthly Trends
  monthly_sales.to_excel(writer, sheet_name="Monthly_Trends", index=False)

  # Sheet 5: Payment Methods
  payment_analysis.to_excel(writer, sheet_name="Payment_Methods", index=False)

print("Excel analytics workbook generated successfully!")

# ==========================================
# STEP 4: GENERATE VISUALIZATIONS
# ==========================================
print("\nGenerating charts...")

fig, axes = plt.subplots(1, 2, figsize=(16, 6))

# Chart 1: Revenue by Category
sns.barplot(
    data=category_sales,
    x="Category",
    y="Total_Revenue",
    ax=axes[0],
    palette="viridis",
)
axes[0].set_title("Total Revenue by Product Category", fontsize=14, fontweight="bold")
axes[0].set_xlabel("Category", fontsize=12)
axes[0].set_ylabel("Revenue ($)", fontsize=12)
axes[0].tick_params(axis="x", rotation=30)

# Chart 2: Revenue by Region
sns.barplot(
    data=region_sales,
    x="Region",
    y="Total_Revenue",
    ax=axes[1],
    palette="magma",
)
axes[1].set_title("Total Revenue by Region", fontsize=14, fontweight="bold")
axes[1].set_xlabel("Region", fontsize=12)
axes[1].set_ylabel("Revenue ($)", fontsize=12)

plt.tight_layout()
chart_filename = "sales_performance_charts.png"
plt.savefig(chart_filename, dpi=300)
plt.close()

print(f"Charts successfully saved as '{chart_filename}'.")
print("\n--- Project Execution Complete! ---")