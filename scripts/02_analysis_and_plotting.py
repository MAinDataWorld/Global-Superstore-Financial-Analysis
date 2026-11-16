# ============================================================
# GLOBAL SUPERSTORE — FINANCIAL DATA ANALYSIS
# ============================================================
# Analysis of financial performance, sales trends, products, geography,
# customers, discounts, and shipping operations.

# ============================================================
# 1. PROJECT SETUP
# ============================================================

from pathlib import Path

# Define the main project directory
project_dir = Path(__file__).resolve().parent.parent

# Define directories for raw and processed data
raw_data_dir = project_dir / "data" / "raw"
processed_data_dir = project_dir / "data" / "processed"

# Define directories for charts and analysis outputs
figures_dir = project_dir / "figures"
output_dir = project_dir / "output"

# Create output directories if they do not already exist
figures_dir.mkdir(parents=True, exist_ok=True)
output_dir.mkdir(parents=True, exist_ok=True)


# ============================================================
# 2. IMPORT REQUIRED LIBRARIES
# ============================================================

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.ticker as ticker
from matplotlib.patches import Patch


# ============================================================
# 3. DATA IMPORT AND PREPARATION
# ============================================================
# Load the cleaned Global Superstore dataset and prepare fields used
# throughout the financial and operational analyses.

# Configure pandas display options
pd.set_option("display.max_columns", None)
pd.set_option("display.max_colwidth", 40)
pd.set_option("display.width", 180)
pd.set_option("display.expand_frame_repr", True)

# Import the previously cleaned dataset
a = pd.read_csv(processed_data_dir / "cleaned.csv")


# ------------------------------------------------------------
# 3.1 DATA TYPE RESTORATION AND FEATURE ENGINEERING
# ------------------------------------------------------------
# Restore appropriate data types before deriving date-based and
# per-unit measures used in subsequent calculations.

## Recheck and convert data types as needed

a["postal_code"] = a["postal_code"].astype("string")
a["order_date"] = pd.to_datetime(a["order_date"], dayfirst=True)
a["ship_date"] = pd.to_datetime(a["ship_date"], dayfirst=True)


## Extract year, month, and day information from dates

a["order_year"] = a["order_date"].dt.year
a["order_month"] = a["order_date"].dt.month
a["order_month_name"] = a["order_date"].dt.month_name()
a["order_day"] = a["order_date"].dt.day
a["order_day_name"] = a["order_date"].dt.day_name()
a["order_quarter"] = a["order_date"].dt.quarter
a["days_till_shipping"] = (a["ship_date"] - a["order_date"]).dt.days


## Create new calculated columns

a["profit_margin"] = (a["profit"] / a["sales"]) * 100
a["profit_per_unit"] = a["profit"] / a["quantity"]
a["sales_price_per_unit"] = a["sales"] / a["quantity"]


# ============================================================
# 3. OVERALL FINANCIAL KPIs
# ============================================================
# Calculate headline measures that summarize the dataset as a whole.

## 3.1 Overall financial KPI calculations

total_sales = a["sales"].sum()
total_profit = a["profit"].sum()
profit_margin_percent = (total_profit / total_sales) * 100
total_orders = a["order_id"].nunique()
average_order_value = total_sales / total_orders
total_units_sold = a["quantity"].sum()
average_discount_percent = a["discount"].mean() * 100
total_shipping_cost = a["shipping_cost"].sum()
average_shipping_time = a["days_till_shipping"].mean()

kpis = {
    "Total Sales": total_sales,
    "Total Profit": total_profit,
    "Profit Margin (%)": profit_margin_percent,
    "Total Orders": total_orders,
    "Average Order Value": average_order_value,
    "Total Units Sold": total_units_sold,
    "Average Line-Item Discount (%)": average_discount_percent,
    "Total Shipping Cost": total_shipping_cost,
    "Average Order-to-Ship Time (Days)": average_shipping_time
}

kpi_summary = pd.DataFrame(
    list(kpis.items()),
    columns=["KPI", "Value"]
)

kpi_summary["Value"] = kpi_summary["Value"].round(2)

kpi_summary.to_csv(output_dir / "kpis.csv", index=False)


## 3.2 Overall financial performance chart

financial_overview = pd.Series({
    "Total Sales": total_sales,
    "Total Profit": total_profit
})

ax = financial_overview.plot(
    kind="bar",
    figsize=(8, 5),
    title="Overall Financial Performance"
)

plt.ylabel("Amount")
plt.xlabel("")
plt.xticks(rotation=0)

# Display full values on the y-axis
ax.ticklabel_format(axis="y", style="plain")

plt.tight_layout()
plt.savefig(figures_dir / "01_overall_financial_performance.png", dpi=300, bbox_inches="tight")


# ============================================================
# 4. ANNUAL FINANCIAL PERFORMANCE
# ============================================================
# Aggregate sales, profit, orders, and units by calendar year.

## 4.1 Annual performance calculations

yearly_performance = (
    a.groupby("order_year")
    .agg(
        total_sales=("sales", "sum"),
        total_profit=("profit", "sum"),
        total_orders=("order_id", "nunique"),
        total_units=("quantity", "sum")
    )
    .reset_index()
)

yearly_performance["profit_margin_percent"] = (
    yearly_performance["total_profit"] /
    yearly_performance["total_sales"]
) * 100


## 4.2 Plotting yearly sales

from matplotlib.ticker import StrMethodFormatter

plt.figure(figsize=(10, 5))

plt.plot(
    yearly_performance["order_year"],
    yearly_performance["total_sales"],
    marker="o"
)

plt.title("Total Sales per Year")
plt.xlabel("Year")
plt.ylabel("Sales")

plt.xticks(yearly_performance["order_year"])

# Format y-axis with commas and two decimal places
plt.gca().yaxis.set_major_formatter(
    StrMethodFormatter("{x:,.2f}")
)

plt.grid(axis="y", alpha=0.3)

plt.tight_layout()
plt.savefig(figures_dir / "02_annual_sales_trend.png", dpi=300, bbox_inches="tight")


# ============================================================
# 5. MONTHLY FINANCIAL PERFORMANCE
# ============================================================
# Examine monthly sales patterns across the full analysis period.

## 5.1 Monthly performance calculations

monthly_performance = (
    a.groupby(["order_year", "order_month", "order_month_name"])
    .agg(
        total_sales=("sales", "sum"),
        total_profit=("profit", "sum"),
        total_orders=("order_id", "nunique"),
        total_units=("quantity", "sum")
    )
    .reset_index()
)

monthly_performance["year_month_name"] = (
    monthly_performance["order_year"].astype(str) + " " +
    monthly_performance["order_month_name"]
)


## 5.2 Plotting monthly performance

plt.figure(figsize=(14, 6))

plt.plot(
    monthly_performance["year_month_name"],
    monthly_performance["total_sales"],
    marker="o",
    markersize=3
)

plt.title("Monthly Sales Trend")
plt.xlabel("Month")
plt.ylabel("Sales")

plt.xticks(rotation=45)

# Format y-axis with commas
plt.gca().yaxis.set_major_formatter(
    StrMethodFormatter("{x:,.0f}")
)

plt.grid(axis="y", alpha=0.3)

plt.tight_layout()
plt.savefig(figures_dir / "03_monthly_sales_trend.png", dpi=300, bbox_inches="tight")


# ============================================================
# 6. QUARTERLY FINANCIAL PERFORMANCE
# ============================================================
# Compare sales performance across quarters and years.

## 6.1 Quarterly performance calculations

quarterly_performance = (
    a.groupby(["order_year", "order_quarter"])
    .agg(
        total_sales=("sales", "sum"),
        total_profit=("profit", "sum"),
        total_orders=("order_id", "nunique"),
        total_units=("quantity", "sum")
    )
    .reset_index()
)

quarterly_performance["year_quarter"] = (
    quarterly_performance["order_year"].astype(str) +
    " Qtr " +
    quarterly_performance["order_quarter"].astype(str)
)

quarterly_pivot = quarterly_performance.pivot(
    index="order_quarter",
    columns="order_year",
    values="total_sales"
)


## 6.2 Plotting quarterly sales comparison

ax = quarterly_pivot.plot(
    kind="bar",
    figsize=(11, 6)
)

plt.title("Quarterly Sales Comparison Across Years")
plt.xlabel("Quarter")
plt.ylabel("Sales")

plt.xticks(rotation=0)

# Format y-axis with commas
ax.yaxis.set_major_formatter(
    StrMethodFormatter("{x:,.0f}")
)

plt.grid(axis="y", alpha=0.3)

plt.tight_layout()
plt.savefig(figures_dir / "04_quarterly_sales_comparison.png", dpi=300, bbox_inches="tight")


# ============================================================
# 7. SALES GROWTH ANALYSIS
# ============================================================
# Measure changes in sales over time using month-over-month and
# year-over-year comparisons.

## 7.1 Month-over-month (MoM) sales growth

monthly_sales = (
    a.groupby(["order_year", "order_month", "order_month_name"])["sales"]
    .sum()
    .reset_index(name="current_month_sales")
)

monthly_sales = monthly_sales.sort_values(["order_year", "order_month"])

# Align each month with the preceding month to calculate the percentage change.
monthly_sales["previous_month_sales"] = monthly_sales["current_month_sales"].shift(1)

monthly_sales["mom_change"] = (
    (monthly_sales["current_month_sales"] - monthly_sales["previous_month_sales"])
    / monthly_sales["previous_month_sales"]
) * 100

monthly_sales["month_year"] = (
    monthly_sales["order_month_name"] + ", "
    + monthly_sales["order_year"].astype(str)
)

# Export monthly sales growth data
monthly_sales.to_csv(output_dir / "01_mom_sales_growth.csv", index=False)


## Plotting MoM analysis

plt.figure(figsize=(14, 6))

plt.bar(
    monthly_sales["month_year"],
    monthly_sales["mom_change"]
)

plt.axhline(0, linewidth=1)

plt.title("Month-over-Month Sales Growth")
plt.xlabel("Month")
plt.ylabel("Growth (%)")

plt.xticks(rotation=45)

plt.grid(axis="y", alpha=0.3)

plt.tight_layout()
plt.savefig(figures_dir / "05_mom_sales_growth.png", dpi=300, bbox_inches="tight")


## 7.2 Year-over-year (YoY) sales growth

yearly_sales = (
    a.groupby("order_year")["sales"]
    .sum()
    .reset_index(name="current_year_sales")
)

yearly_sales = yearly_sales.sort_values("order_year")

# Align each year with the preceding year to calculate annual sales growth.
yearly_sales["previous_year_sales"] = yearly_sales["current_year_sales"].shift(1)

yearly_sales["yoy_analysis"] = (
    (yearly_sales["current_year_sales"] - yearly_sales["previous_year_sales"])
    / yearly_sales["previous_year_sales"]
) * 100

# Export yearly sales growth data
yearly_sales.to_csv(output_dir / "02_yoy_sales_growth.csv", index=False)


## Plotting YoY

plt.figure(figsize=(10, 6))

plt.bar(
    yearly_sales["order_year"].astype(str),
    yearly_sales["yoy_analysis"]
)

plt.axhline(0, linewidth=1)

plt.title("Year-over-Year Sales Growth")
plt.xlabel("Year")
plt.ylabel("Growth (%)")

plt.grid(axis="y", alpha=0.3)

plt.tight_layout()
plt.savefig(figures_dir / "06_yoy_sales_growth.png", dpi=300, bbox_inches="tight")


# ============================================================
# 8. PRODUCT PERFORMANCE
# ============================================================
# Identify products generating the highest and lowest sales and profit.

## 8.1 Product-level performance calculations

product_performance = (
    a.groupby(["product_id", "product_name"])
    .agg(
        total_sales=("sales", "sum"),
        total_profit=("profit", "sum"),
        total_quantity=("quantity", "sum"),
        total_orders=("order_id", "nunique")
    )
    .reset_index()
)

product_performance["profit_margin"] = (
    product_performance["total_profit"] /
    product_performance["total_sales"]
) * 100

top_10_products_by_sales = product_performance.sort_values(
    "total_sales", ascending=False
).head(10)

least_10_products_by_sales = product_performance.sort_values(
    "total_sales", ascending=True
).head(10)

top_10_products_by_profit = product_performance.sort_values(
    "total_profit", ascending=False
).head(10)

least_10_products_by_profit = product_performance.sort_values(
    "total_profit", ascending=True
).head(10)


## 8.2 Plotting top 10 products by sales

top_products = top_10_products_by_sales.sort_values("total_sales")

plt.figure(figsize=(12, 7))

plt.barh(
    top_products["product_name"],
    top_products["total_sales"]
)

plt.title("Top 10 Products by Total Sales")
plt.xlabel("Sales")
plt.ylabel("Product")

# Format x-axis with commas
plt.gca().xaxis.set_major_formatter(
    StrMethodFormatter("{x:,.0f}")
)

plt.tight_layout()
plt.savefig(figures_dir / "07_top_10_products_by_sales.png", dpi=300, bbox_inches="tight")


## 8.3 Plotting least 10 products by sales

least_products = least_10_products_by_sales.sort_values("total_sales")

plt.figure(figsize=(12, 7))

plt.barh(
    least_products["product_name"],
    least_products["total_sales"]
)

plt.title("10 Products with the Lowest Total Sales")
plt.xlabel("Sales")
plt.ylabel("Product")

# Format x-axis with commas
plt.gca().xaxis.set_major_formatter(
    StrMethodFormatter("{x:,.2f}")
)

plt.tight_layout()
plt.savefig(figures_dir / "08_lowest_10_products_by_sales.png", dpi=300, bbox_inches="tight")


## 8.4 Plotting top 10 products by profit

top_profit_products = top_10_products_by_profit.sort_values("total_profit")

plt.figure(figsize=(12, 7))

plt.barh(
    top_profit_products["product_name"],
    top_profit_products["total_profit"]
)

plt.title("Top 10 Products by Total Profit")
plt.xlabel("Profit")
plt.ylabel("Product")

# Format x-axis with commas
plt.gca().xaxis.set_major_formatter(
    StrMethodFormatter("{x:,.0f}")
)

plt.tight_layout()
plt.savefig(figures_dir / "09_top_10_products_by_profit.png", dpi=300, bbox_inches="tight")


## 8.5 Plotting least 10 products by profit

least_profit_products = least_10_products_by_profit.sort_values("total_profit")

plt.figure(figsize=(12, 7))

plt.barh(
    least_profit_products["product_name"],
    least_profit_products["total_profit"]
)

plt.title("10 Products with the Lowest Total Profit")
plt.xlabel("Profit")
plt.ylabel("Product")

# Format x-axis with commas
plt.gca().xaxis.set_major_formatter(
    StrMethodFormatter("{x:,.0f}")
)

plt.tight_layout()
plt.savefig(figures_dir / "10_lowest_10_products_by_profit.png", dpi=300, bbox_inches="tight")


# ============================================================
# 9. CATEGORY AND SUB-CATEGORY PERFORMANCE
# ============================================================
# Compare category and sub-category contributions to sales, profit,
# quantity sold, order volume, and profitability.

## 9.1 Product category performance

product_category_analysis = (
    a.groupby("category")
    .agg(
        total_sales=("sales", "sum"),
        total_profit=("profit", "sum"),
        total_quantity=("quantity", "sum"),
        total_orders=("order_id", "nunique")
    )
    .reset_index()
)

product_category_analysis["profit_margin"] = (
    product_category_analysis["total_profit"] /
    product_category_analysis["total_sales"]
) * 100


## 9.2 Plotting sales and profit by category

category_pivot = (
    product_category_analysis
    .sort_values("total_sales", ascending=False)
    .set_index("category")[["total_sales", "total_profit"]]
)

ax = category_pivot.plot(
    kind="bar",
    figsize=(9, 6)
)

plt.title("Sales and Profit by Product Category")
plt.xlabel("Category")
plt.ylabel("Amount")

plt.xticks(rotation=0)

# Format y-axis with commas
ax.yaxis.set_major_formatter(
    StrMethodFormatter("{x:,.0f}")
)

plt.grid(axis="y", alpha=0.3)

plt.tight_layout()
plt.savefig(figures_dir / "11_sales_and_profit_by_category.png", dpi=300, bbox_inches="tight")


## 9.3 Annual sales trends by product category

yearly_category_sales = (
    a.groupby(["category", "order_year"])["sales"]
    .sum()
    .reset_index(name="total_sales")
)


## Plotting yearly sales by category

category_yearly_pivot = yearly_category_sales.pivot(
    index="order_year",
    columns="category",
    values="total_sales"
)

ax = category_yearly_pivot.plot(
    kind="line",
    figsize=(12, 6),
    marker="o"
)

plt.title("Yearly Sales Trend by Product Category")
plt.xlabel("Year")
plt.ylabel("Total Sales")

plt.xticks(category_yearly_pivot.index)

# Format y-axis with commas
ax.yaxis.set_major_formatter(
    StrMethodFormatter("{x:,.0f}")
)

plt.grid(axis="y", alpha=0.3)
plt.legend(title="Category")

plt.tight_layout()
plt.savefig(figures_dir / "12_yearly_sales_trend_by_category.png", dpi=300, bbox_inches="tight")


## 9.4 Sub-category performance calculations

subcategory_performance = (
    a.groupby(["category", "sub_category"])
    .agg(
        total_sales=("sales", "sum"),
        total_profit=("profit", "sum"),
        total_quantity=("quantity", "sum"),
        total_orders=("order_id", "nunique")
    )
    .reset_index()
)

subcategory_performance["profit_margin"] = (
    subcategory_performance["total_profit"] /
    subcategory_performance["total_sales"]
) * 100


## 9.5 Category colors for sub-category plots

category_colors = {
    "Furniture": "steelblue",
    "Office Supplies": "darkorange",
    "Technology": "seagreen"
}


## 9.6 Plotting total sales by sub-category

subcategory_sales = subcategory_performance.sort_values("total_sales")

plt.figure(figsize=(12, 9))

plt.barh(
    subcategory_sales["category"] + " - " + subcategory_sales["sub_category"],
    subcategory_sales["total_sales"],
    color=subcategory_sales["category"].map(category_colors)
)

legend_handles = [
    Patch(color=color, label=category)
    for category, color in category_colors.items()
]

plt.legend(handles=legend_handles, title="Category")

plt.title("Total Sales by Category and Sub-Category")
plt.xlabel("Sales")
plt.ylabel("Category - Sub-Category")

plt.gca().xaxis.set_major_formatter(StrMethodFormatter("{x:,.0f}"))

plt.tight_layout()
plt.savefig(figures_dir / "13_sales_by_category_and_sub_category.png", dpi=300, bbox_inches="tight")


## 9.7 Plotting total profit by sub-category

subcategory_profit = subcategory_performance.sort_values("total_profit")

plt.figure(figsize=(12, 9))

plt.barh(
    subcategory_profit["category"] + " - " + subcategory_profit["sub_category"],
    subcategory_profit["total_profit"],
    color=subcategory_profit["category"].map(category_colors)
)

legend_handles = [
    Patch(color=color, label=category)
    for category, color in category_colors.items()
]

plt.legend(handles=legend_handles, title="Category")

plt.title("Total Profit by Category and Sub-Category")
plt.xlabel("Profit")
plt.ylabel("Category - Sub-Category")

plt.gca().xaxis.set_major_formatter(StrMethodFormatter("{x:,.0f}"))

plt.tight_layout()
plt.savefig(figures_dir / "14_profit_by_category_and_sub_category.png", dpi=300, bbox_inches="tight")


## 9.8 Plotting profitability by sub-category

profitability_sorted = subcategory_performance.sort_values("profit_margin")

plt.figure(figsize=(12, 9))

plt.barh(
    profitability_sorted["category"] + " - " + profitability_sorted["sub_category"],
    profitability_sorted["profit_margin"]
)

plt.axvline(0, linewidth=1)

plt.title("Profit Margin by Category and Sub-Category")
plt.xlabel("Profit Margin (%)")
plt.ylabel("Category - Sub-Category")

plt.tight_layout()
plt.savefig(figures_dir / "15_profit_margin_by_category_and_sub_category.png", dpi=300, bbox_inches="tight")


# ============================================================
# 10. GEOGRAPHIC PERFORMANCE
# ============================================================
# Compare financial performance across regions, markets, countries,
# and (for the United States) individual states.

## 10.1 Regional performance

region_performance = (
    a.groupby("region")
    .agg(
        total_sales=("sales", "sum"),
        total_profit=("profit", "sum"),
        total_quantity=("quantity", "sum"),
        total_orders=("order_id", "nunique")
    )
    .reset_index()
)

region_performance["profit_margin"] = (
    region_performance["total_profit"] /
    region_performance["total_sales"]
) * 100


## Plotting regional performance

region_sales = region_performance.sort_values("total_sales")

plt.figure(figsize=(11, 7))

plt.barh(
    region_sales["region"],
    region_sales["total_sales"]
)

plt.title("Total Sales by Region")
plt.xlabel("Sales")
plt.ylabel("Region")

plt.gca().xaxis.set_major_formatter(StrMethodFormatter("{x:,.0f}"))

plt.tight_layout()
plt.savefig(figures_dir / "16_sales_by_region.png", dpi=300, bbox_inches="tight")


## 10.2 Market-level performance

market_performance = (
    a.groupby("market")
    .agg(
        total_sales=("sales", "sum"),
        total_profit=("profit", "sum"),
        total_quantity=("quantity", "sum"),
        total_orders=("order_id", "nunique")
    )
    .reset_index()
)

market_performance["profit_margin"] = (
    market_performance["total_profit"] /
    market_performance["total_sales"]
) * 100


## Plotting total sales by market

market_sales = market_performance.sort_values(
    "total_sales",
    ascending=False
)

plt.figure(figsize=(10, 6))

plt.bar(
    market_sales["market"],
    market_sales["total_sales"]
)

plt.title("Total Sales by Market")
plt.xlabel("Market")
plt.ylabel("Sales")

plt.gca().yaxis.set_major_formatter(StrMethodFormatter("{x:,.0f}"))

plt.xticks(rotation=30)

plt.tight_layout()
plt.savefig(figures_dir / "17_sales_by_market.png", dpi=300, bbox_inches="tight")


## Plotting total profit by market

market_profit = market_performance.sort_values(
    "total_profit",
    ascending=False
)

plt.figure(figsize=(10, 6))

plt.bar(
    market_profit["market"],
    market_profit["total_profit"]
)

plt.title("Total Profit by Market")
plt.xlabel("Market")
plt.ylabel("Profit")

plt.gca().yaxis.set_major_formatter(StrMethodFormatter("{x:,.0f}"))

plt.xticks(rotation=30)

plt.tight_layout()
plt.savefig(figures_dir / "18_profit_by_market.png", dpi=300, bbox_inches="tight")


## 10.3 Country-level performance

country_performance = (
    a.groupby("country")
    .agg(
        total_sales=("sales", "sum"),
        total_profit=("profit", "sum"),
        total_quantity=("quantity", "sum"),
        total_orders=("order_id", "nunique")
    )
    .reset_index()
)

country_performance["profit_margin"] = (
    country_performance["total_profit"] /
    country_performance["total_sales"]
) * 100

top_10_countries_by_sales = country_performance.sort_values(
    "total_sales", ascending=False
).head(10)

least_10_countries_by_sales = country_performance.sort_values(
    "total_sales", ascending=True
).head(10)


## Plotting top 10 countries by sales

top_countries = top_10_countries_by_sales.sort_values("total_sales")

plt.figure(figsize=(11, 7))

plt.barh(
    top_countries["country"],
    top_countries["total_sales"]
)

plt.title("Top 10 Countries by Total Sales")
plt.xlabel("Sales")
plt.ylabel("Country")

plt.gca().xaxis.set_major_formatter(StrMethodFormatter("{x:,.0f}"))

plt.tight_layout()
plt.savefig(figures_dir / "19_top_10_countries_by_sales.png", dpi=300, bbox_inches="tight")


## Plotting least 10 countries by sales

least_countries = least_10_countries_by_sales.sort_values("total_sales")

plt.figure(figsize=(11, 7))

plt.barh(
    least_countries["country"],
    least_countries["total_sales"]
)

plt.title("10 Countries with the Lowest Total Sales")
plt.xlabel("Sales")
plt.ylabel("Country")

plt.gca().xaxis.set_major_formatter(StrMethodFormatter("{x:,.0f}"))

plt.tight_layout()
plt.savefig(figures_dir / "20_lowest_10_countries_by_sales.png", dpi=300, bbox_inches="tight")


## 10.4 State-level performance within the United States

# Further examine sales and profit across US states.

state_performance_in_usa = (
    a[a["country"] == "United States"].groupby("state")
    .agg(
        total_sales=("sales", "sum"),
        total_profit=("profit", "sum"),
        total_quantity=("quantity", "sum"),
        total_orders=("order_id", "nunique")
    )
    .reset_index()
)

state_performance_in_usa["profit_margin"] = (
    state_performance_in_usa["total_profit"] /
    state_performance_in_usa["total_sales"]
) * 100


## Plotting top 10 US states by sales

top_10_states = state_performance_in_usa.nlargest(
    10,
    "total_sales"
).sort_values("total_sales")

plt.figure(figsize=(12, 7))

plt.barh(
    top_10_states["state"],
    top_10_states["total_sales"]
)

plt.title("Top 10 US States by Total Sales")
plt.xlabel("Sales")
plt.ylabel("State")

plt.gca().xaxis.set_major_formatter(StrMethodFormatter("{x:,.0f}"))

plt.tight_layout()
plt.savefig(figures_dir / "21_top_10_us_states_by_sales.png", dpi=300, bbox_inches="tight")


## Plotting 10 US states with the lowest sales

least_10_states = state_performance_in_usa.nsmallest(
    10,
    "total_sales"
).sort_values("total_sales")

plt.figure(figsize=(12, 7))

plt.barh(
    least_10_states["state"],
    least_10_states["total_sales"]
)

plt.title("10 US States with the Lowest Total Sales")
plt.xlabel("Sales")
plt.ylabel("State")

plt.gca().xaxis.set_major_formatter(StrMethodFormatter("{x:,.0f}"))

plt.tight_layout()
plt.savefig(figures_dir / "22_lowest_10_us_states_by_sales.png", dpi=300, bbox_inches="tight")


## 10.5 Total sales: USA versus the rest of the world

total_sales_by_usa = (
    a[a["country"] == "United States"]["sales"].sum()
)

total_sales_by_rest_of_world = (
    a[a["country"] != "United States"]["sales"].sum()
)

total_sales_all_countries = a["sales"].sum()

usa_sales_percentage = (
    total_sales_by_usa / total_sales_all_countries
) * 100

rest_of_world_sales_percentage = (
    total_sales_by_rest_of_world / total_sales_all_countries
) * 100

sales_values = [
    total_sales_by_usa,
    total_sales_by_rest_of_world
]

sales_labels = [
    "United States",
    "Rest of the World"
]


def sales_autopct(values):
    def format_label(percentage):
        total = sum(values)
        amount = percentage * total / 100
        return f"{percentage:.2f}%\n(${amount:,.2f})"
    return format_label


## Plotting USA versus rest-of-world sales distribution

plt.figure(figsize=(9, 7))

plt.pie(
    sales_values,
    labels=sales_labels,
    autopct=sales_autopct(sales_values),
    startangle=90,
    pctdistance=0.65
)

plt.title(
    f"Share of Total Sales: USA vs. Rest of the World "
    f"({a['order_year'].min()}–{a['order_year'].max()})"
)

plt.tight_layout()
plt.savefig(figures_dir / "23_usa_vs_rest_of_world_sales_share.png", dpi=300, bbox_inches="tight")


# ============================================================
# 11. CUSTOMER PERFORMANCE
# ============================================================
# Examine financial contribution by customer segment and purchasing
# frequency (one-time versus repeat customers).

## 11.1 Customer segment performance

customer_segment_performance = (
    a.groupby("segment")
    .agg(
        total_sales=("sales", "sum"),
        total_profit=("profit", "sum"),
        total_quantity=("quantity", "sum"),
        total_orders=("order_id", "nunique")
    )
    .reset_index()
)

customer_segment_performance["profit_margin"] = (
    customer_segment_performance["total_profit"] /
    customer_segment_performance["total_sales"]
) * 100


## 11.2 Plotting total sales by customer segment

segment_sales = customer_segment_performance.sort_values(
    "total_sales",
    ascending=False
)

plt.figure(figsize=(9, 6))

plt.bar(
    segment_sales["segment"],
    segment_sales["total_sales"]
)

plt.title("Total Sales by Customer Segment")
plt.xlabel("Customer Segment")
plt.ylabel("Sales")

plt.gca().yaxis.set_major_formatter(StrMethodFormatter("{x:,.0f}"))

plt.tight_layout()
plt.savefig(figures_dir / "24_sales_by_customer_segment.png", dpi=300, bbox_inches="tight")


## 11.3 Plotting total profit by customer segment

segment_profit = customer_segment_performance.sort_values(
    "total_profit",
    ascending=False
)

plt.figure(figsize=(9, 6))

plt.bar(
    segment_profit["segment"],
    segment_profit["total_profit"]
)

plt.title("Total Profit by Customer Segment")
plt.xlabel("Customer Segment")
plt.ylabel("Profit")

plt.gca().yaxis.set_major_formatter(StrMethodFormatter("{x:,.0f}"))

plt.tight_layout()
plt.savefig(figures_dir / "25_profit_by_customer_segment.png", dpi=300, bbox_inches="tight")


## 11.4 Repeat versus one-time customer analysis

# Classify customers according to the number of distinct orders placed.

orders_per_customer = (
    a.groupby("customer_id")["order_id"]
    .nunique()
    .reset_index(name="number_of_orders")
)

orders_per_customer["customer_type"] = np.where(
    orders_per_customer["number_of_orders"] > 1,
    "Repeat Customer",
    "One-Time Customer"
)

customer_type_summary = (
    orders_per_customer["customer_type"]
    .value_counts()
    .reset_index(name="number_of_customers")
)


## Plotting customer distribution by purchase frequency

plt.figure(figsize=(8, 6))

plt.pie(
    customer_type_summary["number_of_customers"],
    labels=customer_type_summary["customer_type"],
    autopct="%1.1f%%",
    startangle=90
)

plt.title("Customer Distribution by Purchase Frequency")

plt.tight_layout()
plt.savefig(figures_dir / "26_customer_distribution_by_purchase_frequency.png", dpi=300, bbox_inches="tight")


# ============================================================
# 12. PROFITABILITY AND DISCOUNT ANALYSIS
# ============================================================
# Explore the relationship between discount levels, sales, profit,
# and profit margin.

## 12.1 Discount-level performance calculations

discount_performance = (
    a.groupby("discount")
    .agg(
        total_sales=("sales", "sum"),
        total_profit=("profit", "sum"),
        total_quantity=("quantity", "sum"),
        transaction_count=("order_id", "count")
    )
    .reset_index()
)

discount_performance["profit_margin"] = (
    discount_performance["total_profit"] /
    discount_performance["total_sales"]
) * 100


## 12.2 Plotting discount level versus profit margin

discount_sorted = discount_performance.sort_values("discount")

plt.figure(figsize=(10, 6))

plt.plot(
    discount_sorted["discount"] * 100,
    discount_sorted["profit_margin"],
    marker="o"
)

plt.title("Discount Level versus Profit Margin")
plt.xlabel("Discount (%)")
plt.ylabel("Profit Margin (%)")

plt.axhline(0, linewidth=1)

plt.grid(alpha=0.3)

plt.tight_layout()
plt.savefig(figures_dir / "27_discount_level_vs_profit_margin.png", dpi=300, bbox_inches="tight")


## 12.3 Plotting sales and profit by discount level

discount_pivot = (
    discount_performance
    .sort_values("discount")
    .set_index("discount")[["total_sales", "total_profit"]]
)

ax = discount_pivot.plot(
    kind="bar",
    figsize=(10, 6)
)

plt.title("Sales and Profit by Discount Level")
plt.xlabel("Discount")
plt.ylabel("Amount")

plt.xticks(
    ticks=range(len(discount_pivot)),
    labels=[f"{discount * 100:.0f}%" for discount in discount_pivot.index],
    rotation=0
)

ax.yaxis.set_major_formatter(StrMethodFormatter("{x:,.0f}"))

plt.legend(["Total Sales", "Total Profit"])

plt.tight_layout()
plt.savefig(figures_dir / "28_sales_and_profit_by_discount_level.png", dpi=300, bbox_inches="tight")


# ============================================================
# 13. SHIPPING AND OPERATIONAL ANALYSIS
# ============================================================
# Evaluate shipping costs and order-to-ship duration by shipping mode
# and product category.

## 13.1 Shipping-mode performance

shipping_mode_performance = (
    a.groupby("ship_mode")
    .agg(
        total_shipping_cost=("shipping_cost", "sum"),
        total_sales=("sales", "sum"),
        total_orders=("order_id", "nunique"),
        average_shipping_days=("days_till_shipping", "mean")
    )
    .reset_index()
)

shipping_mode_performance["shipping_cost_percentage"] = (
    shipping_mode_performance["total_shipping_cost"]
    / shipping_mode_performance["total_sales"] * 100
)


## 13.2 Plotting total shipping cost by shipping mode

# This shows total cost contribution, which can be influenced by order volume.

shipping_cost = shipping_mode_performance.sort_values(
    "total_shipping_cost",
    ascending=False
)

plt.figure(figsize=(9, 6))

plt.bar(
    shipping_cost["ship_mode"],
    shipping_cost["total_shipping_cost"]
)

plt.title("Total Shipping Cost by Shipping Mode")
plt.xlabel("Shipping Mode")
plt.ylabel("Shipping Cost ($)")

plt.gca().yaxis.set_major_formatter(StrMethodFormatter("${x:,.0f}"))

plt.tight_layout()
plt.savefig(figures_dir / "29_shipping_cost_by_shipping_mode.png", dpi=300, bbox_inches="tight")


## 13.3 Plotting average order-to-ship time by shipping mode

shipping_duration = shipping_mode_performance.sort_values(
    "average_shipping_days",
    ascending=True
)

plt.figure(figsize=(9, 6))

plt.bar(
    shipping_duration["ship_mode"],
    shipping_duration["average_shipping_days"]
)

plt.title("Average Order-to-Ship Time by Shipping Mode")
plt.xlabel("Shipping Mode")
plt.ylabel("Average Shipping Days")

plt.tight_layout()
plt.savefig(figures_dir / "30_average_order_to_ship_time_by_shipping_mode.png", dpi=300, bbox_inches="tight")


## 13.4 Shipping cost by product category

category_shipping = (
    a.groupby("category")
    .agg(
        total_shipping_cost=("shipping_cost", "sum"),
        total_sales=("sales", "sum"),
        total_quantity=("quantity", "sum")
    )
    .reset_index()
)

category_shipping["shipping_cost_percentage"] = (
    category_shipping["total_shipping_cost"]
    / category_shipping["total_sales"] * 100
)


## 13.5 Plotting total shipping cost by product category

category_shipping_sorted = category_shipping.sort_values(
    "total_shipping_cost",
    ascending=False
)

plt.figure(figsize=(9, 6))

plt.bar(
    category_shipping_sorted["category"],
    category_shipping_sorted["total_shipping_cost"]
)

plt.title("Total Shipping Cost by Product Category")
plt.xlabel("Product Category")
plt.ylabel("Shipping Cost ($)")

plt.gca().yaxis.set_major_formatter(StrMethodFormatter("${x:,.0f}"))

plt.tight_layout()
plt.savefig(figures_dir / "31_shipping_cost_by_product_category.png", dpi=300, bbox_inches="tight")


## 13.6 Plotting total quantity sold by product category

quantity_per_category = product_category_analysis.sort_values(
    "total_quantity",
    ascending=False
)

plt.figure(figsize=(9, 6))

plt.bar(
    quantity_per_category["category"],
    quantity_per_category["total_quantity"]
)

plt.title("Total Units Sold by Product Category")
plt.xlabel("Product Category")
plt.ylabel("Units Sold")

plt.gca().yaxis.set_major_formatter(StrMethodFormatter("{x:,.0f}"))

plt.tight_layout()
plt.savefig(figures_dir / "32_units_sold_by_product_category.png", dpi=300, bbox_inches="tight")


# ============================================================
# 14. ADDITIONAL COMMERCIAL ANALYSIS
# ============================================================
# Examine changes in average order value across calendar years.

## 14.1 Average order value by year

yearly_performance["average_order_value"] = (
    yearly_performance["total_sales"] / yearly_performance["total_orders"]
)

yearly_performance = yearly_performance.sort_values("order_year")


## Plotting average order value by year

plt.figure(figsize=(9, 5))

plt.plot(
    yearly_performance["order_year"],
    yearly_performance["average_order_value"],
    marker="o",
    linewidth=2,
    color="steelblue"
)

plt.title("Average Order Value by Year")
plt.xlabel("Year")
plt.ylabel("Average Order Value")

plt.xticks(yearly_performance["order_year"])

plt.grid(axis="y", linestyle="--", alpha=0.3)

plt.tight_layout()
plt.savefig(figures_dir / "33_average_order_value_by_year.png", dpi=300, bbox_inches="tight")