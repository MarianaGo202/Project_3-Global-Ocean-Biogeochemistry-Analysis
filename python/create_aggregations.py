import xarray as xr
import pandas as pd
import numpy as np
from pathlib import Path

# NOTE: the depth_statistics.csv produced here duplicates the
# depth profile already produced by 07_preparar_profundidade.py
# (global_depth_profiles.csv), which is the one actually loaded
# into the database by 09_criar_banco.py. depth_statistics.csv
# is kept here for reference but is not used downstream.

print("PROJECT 3 — SCIENTIFIC AGGREGATIONS")

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

print("\nOpening datasets...")

ds = xr.open_dataset(MONTHLY_FILE)
mask_ds = xr.open_dataset(MASK_FILE)

ocean_mask = mask_ds["mask"].isel(depth=0)

print("Datasets opened.")

surface = ds[variables].isel(depth=0)
surface = surface.where(ocean_mask == 1)


# 1) Global statistics per variable
print("\nCalculating global statistics...")

records = []

for variable in variables:
    data = surface[variable]
    values = data.values.flatten()
    values = values[~np.isnan(values)]
    record = {
        "time": pd.Timestamp(ds.time.values[0]),
        "variable": variable,
        "count": len(values),
        "mean": float(np.mean(values)),
        "median": float(np.median(values)),
        "std": float(np.std(values)),
        "minimum": float(np.min(values)),
        "maximum": float(np.max(values)),
        "q25": float(np.percentile(values, 25)),
        "q75": float(np.percentile(values, 75))
    }
    records.append(record)

df_global = pd.DataFrame(records)

global_file = OUTPUT_DIR / "global_surface_statistics.csv"
df_global.to_csv(global_file, index=False)

print(f"Saved: {global_file}")


# 2) Average value per latitude band (averaged across longitude)
print("\nCalculating latitude statistics...")

records = []

for variable in variables:
    grouped = (
        surface[variable]
        .mean(dim="longitude", skipna=True)
        .squeeze()
    )
    for latitude, value in zip(
        grouped.latitude.values,
        grouped.values
    ):
        if not np.isnan(value):
            records.append({
                "time": pd.Timestamp(ds.time.values[0]),
                "latitude": float(latitude),
                "variable": variable,
                "mean_value": float(value)
            })

df_latitude = pd.DataFrame(records)

latitude_file = OUTPUT_DIR / "latitude_surface_statistics.csv"
df_latitude.to_csv(latitude_file, index=False)

print(f"Saved: {latitude_file}")


# 3) Average value per longitude band (averaged across latitude)
print("\nCalculating longitude statistics...")

records = []

for variable in variables:
    grouped = (
        surface[variable]
        .mean(dim="latitude", skipna=True)
        .squeeze()
    )
    for longitude, value in zip(
        grouped.longitude.values,
        grouped.values
    ):
        if not np.isnan(value):
            records.append({
                "time": pd.Timestamp(ds.time.values[0]),
                "longitude": float(longitude),
                "variable": variable,
                "mean_value": float(value)
            })

df_longitude = pd.DataFrame(records)

longitude_file = OUTPUT_DIR / "longitude_surface_statistics.csv"
df_longitude.to_csv(longitude_file, index=False)

print(f"Saved: {longitude_file}")


# 4) Average value per depth level (full water column, not just
#    surface) — kept for reference, see note at the top of the file.
print("\nCalculating depth statistics...")

records = []

for variable in variables:
    grouped = (
        ds[variable]
        .where(ocean_mask == 1)
        .mean(dim=["latitude", "longitude"], skipna=True)
        .squeeze()
    )
    for depth, value in zip(
        grouped.depth.values,
        grouped.values
    ):
        if not np.isnan(value):
            records.append({
                "time": pd.Timestamp(ds.time.values[0]),
                "depth": float(depth),
                "variable": variable,
                "mean_value": float(value)
            })

df_depth = pd.DataFrame(records)

depth_file = OUTPUT_DIR / "depth_statistics.csv"
df_depth.to_csv(depth_file, index=False)

print(f"Saved: {depth_file}")

print("STEP 06 COMPLETE")

print("\nFiles created:")
print(global_file.name)
print(latitude_file.name)
print(longitude_file.name)
print(depth_file.name)

ds.close()
mask_ds.close()
