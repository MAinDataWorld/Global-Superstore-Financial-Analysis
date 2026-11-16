
# ============================================================
# 1. PROJECT SETUP
# ============================================================

from pathlib import Path

# Define the main project directory
project_dir = Path(__file__).resolve().parent.parent

# Define data directories
raw_data_dir = project_dir / "data" / "raw"
processed_data_dir = project_dir / "data" / "processed"

# Define output directories
figures_dir = project_dir / "figures"
output_dir = project_dir / "output"


# ============================================================
# 2. IMPORT LIBRARIES
# ============================================================

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import janitor

# ============================================================
# 3. DISPLAY SETTINGS
# ============================================================
# Configure pandas display settings

pd.set_option("display.max_columns", None)
pd.set_option("display.max_colwidth", 40)
pd.set_option("display.width", 180)
pd.set_option("display.expand_frame_repr", True)

# ============================================================
# 4. IMPORT RAW DATA
# ============================================================
 
a = pd.read_csv(raw_data_dir / "Global_Superstore.csv")



# ============================================================
# 5. COLUMN NAME STANDARDIZATION
# ============================================================

# Convert all column names to snake_case
a = a.clean_names(case_type = "snake")


# ============================================================
# 6. DATA EXPLORATION AND QUALITY CHECKS
# ============================================================

# Check the number of rows and columns
print(a.shape)

#CHeck the names of columns and thier data dtypes
print(a.dtypes)

a["postal_code"] = a["postal_code"].astype("string")
a["order_date"] = pd.to_datetime(a["order_date"], dayfirst = True)
a["ship_date"] = pd.to_datetime(a["ship_date"], dayfirst = True)
print(a.dtypes)



##Check for duplicated rows....zero duplicated rows

print(a.duplicated().sum())

## check for missing values in every column..found 41296 missing in postal_code

print(a.isna().sum())

##The dataset shows 51290 rows for 25035 unique order ids, in 147 unique countries
print(a.shape)
print("Number of entries: ", a.shape[0])
print("Unique order IDs: ", a["order_id"].nunique())
print("Unique countries: ", a["country"].nunique())
print("Period covered: from: ", a["order_date"].min(), "to: ", a["order_date"].max())


# Save the cleaned DataFrame as a CSV file
a.to_csv(processed_data_dir / "cleaned.csv", index = False)