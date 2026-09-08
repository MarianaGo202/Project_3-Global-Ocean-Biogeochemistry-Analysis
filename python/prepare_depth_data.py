import xarray as xr
import pandas as pd
import numpy as np
from pathlib import Path

print("PROJECT 3 — DEPTH PROFILE PREPARATION")

PROJECT_ROOT = Path(__file__).resolve().parents[1]

MONTHLY_FILE = (
    PROJECT_ROOT
    / "data"
    / "raw"
    / "Monthly"
    / "mercatorfreebiorys2v4_global_mean_202509.nc"
)

MASK_FILE = (
    PROJECT_ROOT
    / "data"
    / "raw"
    / "Mask"
    / "GLOBAL_REANALYSIS_BIO_001_029_mask.nc"
)

OUTPUT_DIR = PROJECT_ROOT / "data" / "processed"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

variables = [
    "chl",
    "fe",
    "no3",
    "nppv",
    "o2",
    "ph",
    "phyc",
    "po4",
    "si"
]

ds = xr.open_dataset(MONTHLY_FILE)
mask_ds = xr.open_dataset(MASK_FILE)

ocean_mask = mask_ds["mask"]


# Global vertical profile per variable
print("\nCalculating global vertical profiles...")

records = []

for variable in variables:
    data = ds[variable].where(ocean_mask == 1)
    profile = data.mean(
        dim=["latitude", "longitude"],
        skipna=True
    ).squeeze()
    for depth, value in zip(
        profile.depth.values,
        profile.values
    ):
        if not np.isnan(value):
            records.append({
                "time": pd.Timestamp(ds.time.values[0]),
                "depth": float(depth),
                "variable": variable,
                "mean_value": float(value)
            })

df = pd.DataFrame(records)


# Classify each depth into a readable ocean-layer category
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
    else:
        return "Abyssal"

df["depth_category"] = df["depth"].apply(classify_depth)

output_file = OUTPUT_DIR / "global_depth_profiles.csv"
df.to_csv(output_file, index=False)

print(f"\nSaved: {output_file}")
print(f"Rows: {len(df):,}")

print("STEP 07 COMPLETE")

ds.close()
mask_ds.close()
