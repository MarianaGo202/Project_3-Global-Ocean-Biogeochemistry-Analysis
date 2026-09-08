import xarray as xr
import pandas as pd
import numpy as np
from pathlib import Path

print("PROJECT 3 — PREPARING BIOGEOCHEMISTRY DATA")

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

print("\nChecking input files...")

if not MONTHLY_FILE.exists():
    raise FileNotFoundError(f"Monthly file not found:\n{MONTHLY_FILE}")

if not MASK_FILE.exists():
    raise FileNotFoundError(f"Mask file not found:\n{MASK_FILE}")

print("Monthly file: OK")
print("Mask file:    OK")

print("\nOpening datasets...")

ds = xr.open_dataset(MONTHLY_FILE)
mask_ds = xr.open_dataset(MASK_FILE)

print("Datasets opened successfully!")


# Apply the ocean mask (surface level only)
print("\nApplying ocean mask...")

ocean_mask = mask_ds["mask"].isel(depth=0)

print("Ocean mask loaded.")

variables = [
    "spco2",
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

print("\nVariables selected:")

for variable in variables:
    print(f" - {variable}")


# Build the surface dataset (depth=0, ocean cells only)
print("\nCreating surface dataset...")

surface_variables = variables

surface = ds[surface_variables].isel(depth=0)
surface = surface.where(ocean_mask == 1)

print("\nConverting surface data to DataFrame...")

df_surface = surface.to_dataframe().reset_index()

print(f"Rows generated: {len(df_surface):,}")


# Drop grid cells where every variable is NaN (land / no data)
print("\nRemoving rows without ocean observations...")

df_surface = df_surface.dropna(
    subset=variables,
    how="all"
)

print(f"Valid rows: {len(df_surface):,}")


# Add time attributes for easier filtering/aggregation later
print("\nCreating time attributes...")

df_surface["year"] = df_surface["time"].dt.year
df_surface["month"] = df_surface["time"].dt.month

df_surface["year_month"] = (
    df_surface["year"].astype(str)
    + "-"
    + df_surface["month"].astype(str).str.zfill(2)
)

df_surface["depth_category"] = "Surface"


# Reorder columns and save
columns = [
    "time",
    "year",
    "month",
    "year_month",
    "latitude",
    "longitude",
    "depth",
    "depth_category",
    "spco2",
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

df_surface = df_surface[columns]

output_file = OUTPUT_DIR / "surface_biogeochemistry_2025_09.csv"

print("\nSaving processed dataset...")

df_surface.to_csv(output_file, index=False)

print(f"Saved successfully:\n{output_file}")


# Summary
print("PROCESSING SUMMARY")

print(f"Rows:       {len(df_surface):,}")
print(f"Columns:    {len(df_surface.columns)}")
print(f"Latitude:   {df_surface['latitude'].min():.2f} to {df_surface['latitude'].max():.2f}")
print(f"Longitude:  {df_surface['longitude'].min():.2f} to {df_surface['longitude'].max():.2f}")
print(f"Date:       {df_surface['time'].min()}")

print("\nVariables:")
for variable in variables:
    print(f" - {variable}")

print("STEP 05 COMPLETE")

ds.close()
mask_ds.close()
