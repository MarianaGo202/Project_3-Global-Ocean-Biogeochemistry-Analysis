import xarray as xr
from pathlib import Path


# Project root folder (one level above /python)
project_path = Path(__file__).resolve().parent.parent


# Monthly NetCDF file with all biogeochemical variables
file_path = (
    project_path
    / "data"
    / "raw"
    / "Monthly"
    / "mercatorfreebiorys2v4_global_mean_202509.nc"
)

print("PROJECT 3 — GLOBAL OCEAN BIOGEOCHEMISTRY HINDCAST")

print("\nChecking file:")
print(file_path)

if not file_path.exists():
    print("\nERROR: NetCDF file was not found.")
    print("\nExpected location:")
    print(file_path)
    raise FileNotFoundError(
        "The monthly NetCDF file could not be found."
    )

print("\nNetCDF file found successfully!")


# Open dataset
print("OPENING NETCDF DATASET")

ds = xr.open_dataset(file_path)

print("\nDataset successfully opened!")


# General dataset overview (dims, coords, variables, attrs)
print("DATASET INFORMATION")

print(ds)


# Dimensions: how many points along each axis (time, depth, lat, lon)
print("DIMENSIONS")

for dimension, size in ds.sizes.items():
    print(f"{dimension}: {size}")


# Coordinates: the axis values themselves (time, depth, lat, lon)
print("COORDINATES")

for coordinate in ds.coords:
    data = ds[coordinate]
    print(f"\n- {coordinate}")
    print(f"  Dimensions: {data.dims}")
    print(f"  Shape: {data.shape}")
    print(f"  Data type: {data.dtype}")
    if data.size > 0:
        print(f"  First value: {data.values.flat[0]}")
        print(f"  Last value:  {data.values.flat[-1]}")


# Data variables: the biogeochemical fields (chl, o2, ph, etc.)
print("DATA VARIABLES")

for variable in ds.data_vars:

    data = ds[variable]

    print(f"\nVariable: {variable}")
    print(f"  Dimensions: {data.dims}")
    print(f"  Shape: {data.shape}")
    print(f"  Data type: {data.dtype}")

    units = data.attrs.get("units", "Not specified")
    long_name = data.attrs.get("long_name", "Not specified")

    print(f"  Units: {units}")
    print(f"  Long name: {long_name}")


# Global metadata attached to the file (source, institution, etc.)
print("DATASET ATTRIBUTES")

for attribute, value in ds.attrs.items():
    print(f"{attribute}: {value}")


# Missing-value check per variable — helps anticipate how much
# data will be dropped later (e.g. land cells, ice-covered cells)
print("MISSING VALUES")

for variable in ds.data_vars:
    data = ds[variable]
    try:

        missing = data.isnull().sum().item()
        total = data.size
        percentage = (missing / total) * 100

        print(
            f"{variable}: "
            f"{missing:,} missing values "
            f"({percentage:.2f}%)"
        )
    except Exception as error:

        print(
            f"{variable}: "
            f"Could not calculate missing values "
            f"({error})"
        )

print("INSPECTION COMPLETE")

ds.close()
