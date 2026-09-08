import xarray as xr
from pathlib import Path

project_path = Path(__file__).resolve().parent.parent

file_path = (
    project_path
    / "data"
    / "raw"
    / "Mask"
    / "GLOBAL_REANALYSIS_BIO_001_029_mask.nc"
)

print("PROJECT 3 — MASK INSPECTION")

print("\nChecking file:")
print(file_path)

if not file_path.exists():
    raise FileNotFoundError(
        f"Mask file not found:\n{file_path}"
    )

print("\nMask file found successfully!")


# Open dataset
print("OPENING MASK DATASET")

ds = xr.open_dataset(file_path)

print("\nDataset successfully opened!")

print("DATASET INFORMATION")

print(ds)

print("DIMENSIONS")

for dimension, size in ds.sizes.items():
    print(f"{dimension}: {size}")

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


# Mask-related variables: mask (ocean=1/land=0), deptho, deptho_lev
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

print("\n" + "=" * 70)
print("DATASET ATTRIBUTES")
print("=" * 70)

for attribute, value in ds.attrs.items():
    print(f"{attribute}: {value}")


# Check which discrete values the mask variables actually take
# (e.g. mask should only contain 0 and 1)
print("MASK VALUE DISTRIBUTION")

for variable in ds.data_vars:
    data = ds[variable]
    print(f"\nVariable: {variable}")
    try:

        values = data.values
        unique_values = set(values.flatten())

        print(f"  Number of unique values: {len(unique_values)}")
        print(f"  Unique values: {sorted(unique_values)[:20]}")
    except Exception as error:

        print(f"  Could not inspect values: {error}")

print("MASK INSPECTION COMPLETE")

ds.close()
