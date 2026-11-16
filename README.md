# Global Superstore – Financial Data Analysis

## Project Overview

This project explores the financial and commercial performance of a global retail business using Python and Power BI. The objective was to transform raw transactional data into meaningful financial insights by examining sales, profitability, products, geographical performance, customer segments, discounts, and shipping operations.

The project follows a complete data analysis workflow, from data cleaning and preparation to exploratory analysis, visualization, and interactive dashboard development.

## Tools & Technologies

- **Python:** Data cleaning, manipulation, analysis, and visualization
- **Pandas & NumPy:** Data preparation, aggregation, and financial calculations
- **Matplotlib:** Data visualization (33 figures)
- **Power BI:** Interactive dashboard development
- **CSV:** Storage and transfer of processed data and analytical outputs

## Project Workflow

The project was completed in three main stages:

**1. Data Exploration and Cleaning – Python**

The raw Global Superstore dataset was imported and examined using `01_data_exploration_and_cleaning.py`.

Key steps included:
- Standardizing column names using snake_case.
- Converting date columns into appropriate datetime formats.
- Checking data types, missing values, and duplicate records.
- Investigating missing postal-code values.
- Exporting the prepared dataset as `cleaned.csv`.

**2. Financial Analysis and Visualization – Python**

The cleaned dataset was imported into `02_analysis_and_plotting.py` for further analysis.

The script calculates financial KPIs, performs multiple analytical investigations, and generates 33 figures covering:

- Overall financial performance and annual, monthly, and quarterly trends.
- Month-over-month (MoM) and year-over-year (YoY) sales growth.
- Product, category, and sub-category performance.
- Regional, market, country, and US state-level performance.
- Customer segment and purchasing-frequency analysis.
- Discount levels and profitability.
- Shipping costs, delivery duration, and product-category shipping analysis.
- Average order value trends.

Three CSV files were exported for further use:
- `kpis.csv` – Overall financial KPIs.
- `01_mom_sales_growth.csv` – Monthly sales and MoM growth.
- `02_yoy_sales_growth.csv` – Annual sales and YoY growth.

**3. Interactive Dashboard – Power BI**

The cleaned dataset and analytical outputs were used to develop an interactive Power BI dashboard consisting of three pages:

- **Executive Overview:** Headline financial KPIs and overall business performance.
- **Product and Customer Performance:** Product, category, sub-category, and customer analysis.
- **Sales Trends and Operations:** Sales trends, growth, and operational performance.

## Dataset Overview

| Metric | Value |
|---|---:|
| Total records | 51,290 |
| Unique orders | 25,035 |
| Unique customers | 1,590 |
| Countries represented | 147 |
| Analysis period | 2011–2014 |

## Key Financial KPIs

| KPI | Result |
|---|---:|
| Total Sales | $12,642,501.91 |
| Total Profit | $1,467,457.29 |
| Overall Profit Margin | 11.61% |
| Total Orders | 25,035 |
| Average Order Value | $504.99 |
| Total Units Sold | 178,312 |
| Average Line-Item Discount | 14.29% |
| Total Shipping Cost | $1,352,820.69 |
| Average Order-to-Ship Time | 3.97 days |

## Key Insights

**1. Sales and Financial Performance**
- Annual sales increased from approximately $2.26 million in 2011 to $4.30 million in 2014, representing an increase of approximately 90.3%.
- Sales and profit increased across the four-year period.
- The fourth quarter consistently generated the highest sales, while the first quarter recorded the lowest overall sales.

**2. Product and Category Performance**
- Technology generated the largest share of sales (37.53%) and the highest total profit (approximately $663,779).
- Office Supplies generated the highest sales volume, with 108,182 units sold.
- Furniture had the lowest category-level profit margin (6.94%).
- The Tables sub-category generated a negative total profit of approximately $64,083, with a profit margin of -8.46%, despite generating more than $757,000 in sales.

**3. Geographical Performance**
- The United States was the largest individual country by sales, contributing approximately $2.30 million, or 18.17% of total sales.
- The remaining 81.83% of sales came from markets outside the United States.
- APAC was the largest market, contributing approximately 28.36% of total sales.

**4. Customer Performance**
- Consumer customers generated the largest share of sales (51.48%), followed by Corporate (30.25%) and Home Office (18.27%).

**5. Discount and Profitability Analysis**
- Higher discount levels were associated with substantially weaker profitability in the aggregated results.
- Discount levels above 20% generated an overall negative profit, highlighting the importance of monitoring discount policies and their impact on margins.

**6. Shipping and Operations**
- Standard Class accounted for the largest total shipping cost, approximately $614,631, and the highest order volume.
- Average order-to-ship time varied considerably across shipping modes, reflecting differences in delivery speed.

## Business Recommendations

Based on the findings, several opportunities for improvement can be identified:

- **Improve product profitability:** Investigate the negative profitability of Tables and review pricing, discounting, and product costs before increasing sales volume.
- **Review discount policies:** Introduce more careful discount controls, particularly for discounts exceeding 20%, and evaluate their effect on profit margins rather than sales alone.
- **Prepare for seasonal demand:** Plan inventory, staffing, and marketing activities ahead of the fourth-quarter sales peak, while exploring targeted strategies to improve first-quarter performance.
- **Expand geographical opportunities:** Explore growth opportunities outside the United States, particularly in markets with strong sales and profitability potential.
- **Strengthen category performance:** Maintain the strong contribution of Technology while identifying opportunities to improve Furniture's relatively low profit margin.
- **Monitor shipping efficiency:** Evaluate shipping costs alongside delivery times and order volumes to identify opportunities for operational optimization.

## Limitations

- The dataset contains 41,296 missing postal-code values (approximately 80.5%). These were not imputed because reliable geographical matching could not be established for all records. Postal codes were not used in the subsequent analysis.
- No duplicate records were identified during the initial data-quality checks.
- The analysis is based on historical data covering 2011–2014 and should not be interpreted as a representation of current business performance.
- The dataset provides aggregated transaction-level sales, profit, and shipping-cost information, but does not provide sufficient detail to investigate all underlying cost components or explain the causes of individual losses.
- Discount and profitability relationships are observational and do not independently establish causation.
- YoY growth comparisons are available for three years (2012–2014), as 2011 serves as the initial comparison baseline.

## Repository Structure

```text
Global-Superstore-Financial-Analysis/
│
├── data/
│   ├── raw/
│   │   └── Global_Superstore.csv
│   └── processed/
│       └── cleaned.csv
│
├── scripts/
│   ├── 01_data_exploration_and_cleaning.py
│   └── 02_analysis_and_plotting.py
│
├── figures/
│   └── 33 generated visualizations
│
├── output/
│   ├── kpis.csv
│   ├── 01_mom_sales_growth.csv
│   └── 02_yoy_sales_growth.csv
│
└── PowerBI/
    └── Global_Superstore_Dashboard.pbix
```

*Folder and file names may vary slightly depending on the final repository organization.*

## Conclusion

This project demonstrates an end-to-end financial data analysis workflow, combining Python-based data preparation and analytical visualization with Power BI dashboard development. It highlights how transactional data can be transformed into actionable insights about financial performance, product profitability, geographical sales distribution, customer behavior, discount strategies, and operational efficiency.
