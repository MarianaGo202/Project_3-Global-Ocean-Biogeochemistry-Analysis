import xarray as xr
from pathlib import Path


project_path = Path(__file__).resolve().parent.parent

file_path = (
    project_path
    / "data"
    / "raw"
    / "Coordinates"
    / "GLOBAL_REANALYSIS_BIO_001_029_coordinates.nc"
)

print("PROJECT 3 — COORDINATES INSPECTION")

print("\nChecking file:")
print(file_path)

if not file_path.exists():
    raise FileNotFoundError(
        f"Coordinates file not found:\n{file_path}"
    )

print("\nCoordinates file found successfully!")


# Open dataset
print("OPENING COORDINATES DATASET")

ds = xr.open_dataset(file_path)

print("\nDataset successfully opened!")

print("DATASET INFORMATION")

print(ds)


# Grid dimensions (number of points along each axis)
print("DIMENSIONS")

for dimension, size in ds.sizes.items():
    print(f"{dimension}: {size}")


# Coordinate axes (latitude, longitude, depth values)
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


# Grid-cell size variables (e1t, e2t, e3t) used for spatial weight
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

print("DATASET ATTRIBUTES")

for attribute, value in ds.attrs.items():
    print(f"{attribute}: {value}")

print("COORDINATES INSPECTION COMPLETE")

ds.close()
