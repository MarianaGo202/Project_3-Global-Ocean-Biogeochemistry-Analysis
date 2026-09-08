import pandas as pd
import xarray as xr
from pathlib import Path

print("PROJECT 3 — CREATING DIMENSION TABLES")

PROJECT_ROOT = Path(__file__).resolve().parents[1]

MONTHLY_FILE = (
    PROJECT_ROOT
    / "data"
    / "raw"
    / "Monthly"
    / "mercatorfreebiorys2v4_global_mean_202509.nc"
)

OUTPUT_DIR = PROJECT_ROOT / "data" / "processed"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


# dim_variable: code, descriptive name and unit for each variable
print("\nBuilding dim_variable...")

variables = [
    ("spco2", "Surface CO2", "Pa"),
    ("chl", "Total Chlorophyll", "mg m-3"),
    ("fe", "Dissolved Iron", "mmol m-3"),
    ("no3", "Nitrate", "mmol m-3"),
    ("nppv", "Primary Production", "mg m-3 day-1"),
    ("o2", "Dissolved Oxygen", "mmol m-3"),
    ("ph", "pH", "1"),
    ("phyc", "Total Phytoplankton", "mmol m-3"),
    ("po4", "Phosphate", "mmol m-3"),
    ("si", "Dissolved Silicate", "mmol m-3")
]

df_variables = pd.DataFrame(
    variables,
    columns=["variable_code", "variable_name", "unit"]
)

df_variables.to_csv(
    OUTPUT_DIR / "dim_variable.csv",
    index=False
)

print(f"Rows: {len(df_variables)}")


# dim_depth: each model depth level with its readable category
print("\nBuilding dim_depth...")

ds = xr.open_dataset(MONTHLY_FILE)

depths = ds.depth.values

df_depth = pd.DataFrame({
    "depth_id": range(1, len(depths) + 1),
    "depth_m": depths
})


def classify_depth(depth):
    if depth <= 10:
        return "Surface"
    elif depth <= 50:
        return "Shallow"
    elif depth <= 200:
        return "Upper Ocean"
    elif depth <= 1000:
        return "Intermediate"
    elif depth <= 4000:
        return "Deep Ocean"
    return "Abyssal"


df_depth["depth_category"] = df_depth["depth_m"].apply(classify_depth)

df_depth.to_csv(
    OUTPUT_DIR / "dim_depth.csv",
    index=False
)

print(f"Rows: {len(df_depth)}")


# dim_date: a single row describing the reference date/month
print("\nBuilding dim_date...")

date = pd.Timestamp(ds.time.values[0])

df_date = pd.DataFrame([{
    "date_id": int(date.strftime("%Y%m%d")),
    "date": date.date(),
    "year": date.year,
    "month": date.month,
    "month_name": date.strftime("%B"),
    "quarter": f"Q{date.quarter}"
}])

df_date.to_csv(
    OUTPUT_DIR / "dim_date.csv",
    index=False
)

print(f"Rows: {len(df_date)}")

ds.close()

print("STEP 08 COMPLETE")

print("\nCreated:")
print(" - dim_variable.csv")
print(" - dim_depth.csv")
print(" - dim_date.csv")
