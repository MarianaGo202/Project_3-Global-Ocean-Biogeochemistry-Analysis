import xarray as xr
import numpy as np
from pathlib import Path

project_path = Path(__file__).resolve().parent.parent

coordinates_file = (
    project_path
    / "data"
    / "raw"
    / "Coordinates"
    / "GLOBAL_REANALYSIS_BIO_001_029_coordinates.nc"
)

mask_file = (
    project_path
    / "data"
    / "raw"
    / "Mask"
    / "GLOBAL_REANALYSIS_BIO_001_029_mask.nc"
)

print("PROJECT 3 — GRID AND OCEAN MASK ANALYSIS")

print("\nChecking input files...")

if not coordinates_file.exists():
    raise FileNotFoundError(
        f"Coordinates file not found:\n{coordinates_file}"
    )

if not mask_file.exists():
    raise FileNotFoundError(
        f"Mask file not found:\n{mask_file}"
    )

print("Coordinates file: OK")
print("Mask file: OK")

# Open both datasets
print("OPENING DATASETS")

coordinates = xr.open_dataset(coordinates_file)
mask_ds = xr.open_dataset(mask_file)

print("\nDatasets opened successfully!")


# Grid size (number of points along each axis)
print("GRID DIMENSIONS")

latitude = coordinates["latitude"]
longitude = coordinates["longitude"]
depth = coordinates["depth"]

n_latitude = latitude.size
n_longitude = longitude.size
n_depth = depth.size

total_horizontal_cells = n_latitude * n_longitude
total_vertical_cells = n_latitude * n_longitude * n_depth

print(f"\nLatitude points:       {n_latitude:,}")
print(f"Longitude points:      {n_longitude:,}")
print(f"Depth levels:          {n_depth:,}")

print(f"\nHorizontal grid cells: {total_horizontal_cells:,}")
print(f"Total 3D grid cells:   {total_vertical_cells:,}")


# Geographic extent
print("GEOGRAPHIC EXTENT")

print(
    f"\nLatitude range:  "
    f"{float(latitude.min()):.2f}° to {float(latitude.max()):.2f}°"
)

print(
    f"Longitude range: "
    f"{float(longitude.min()):.2f}° to {float(longitude.max()):.2f}°"
)


# Vertical grid (depth levels)
print("VERTICAL GRID")

depth_values = depth.values

print("\nAll model depth levels (m):")

for index, value in enumerate(depth_values, start=1):
    print(f"{index:02d}: {float(value):10.3f} m")

print("DEPTH STATISTICS")

print(f"\nMinimum model depth: {float(np.nanmin(depth_values)):.3f} m")
print(f"Maximum model depth: {float(np.nanmax(depth_values)):.3f} m")


# Ocean mask: ocean vs. land coverage at the surface level
print("OCEAN MASK ANALYSIS")

mask = mask_ds["mask"]

# The mask is 3D: depth × latitude × longitude
# For a global horizontal analysis we use the surface level (depth=0)
surface_mask = mask.isel(depth=0)

mask_values = surface_mask.values

ocean_cells = np.count_nonzero(mask_values == 1)
land_cells = np.count_nonzero(mask_values == 0)
valid_mask_cells = np.count_nonzero(~np.isnan(mask_values))
total_mask_cells = mask_values.size

ocean_percentage = (ocean_cells / total_mask_cells) * 100
land_percentage = (land_cells / total_mask_cells) * 100
nan_percentage = (
    (total_mask_cells - valid_mask_cells) / total_mask_cells
) * 100

print(f"\nTotal horizontal cells: {total_mask_cells:,}")
print(f"Ocean cells:            {ocean_cells:,}")
print(f"Land cells:             {land_cells:,}")
print(f"Missing mask cells:     {total_mask_cells - valid_mask_cells:,}")

print(f"\nOcean coverage: {ocean_percentage:.2f}%")
print(f"Land coverage:  {land_percentage:.2f}%")
print(f"Missing:        {nan_percentage:.2f}%")


# Bathymetry (sea-floor depth)
print("BATHYMETRY ANALYSIS")

deptho = mask_ds["deptho"]
deptho_values = deptho.values
valid_deptho = deptho_values[~np.isnan(deptho_values)]

print(f"\nValid bathymetry cells: {valid_deptho.size:,}")
print(f"Minimum bathymetry: {float(np.nanmin(deptho_values)):.3f} m")
print(f"Maximum bathymetry: {float(np.nanmax(deptho_values)):.3f} m")
print(f"Mean bathymetry: {float(np.nanmean(deptho_values)):.3f} m")
print(f"Median bathymetry: {float(np.nanmedian(deptho_values)):.3f} m")


# Sea-floor model level (which depth index is the ocean floor)
print("SEA-FLOOR MODEL LEVEL")

deptho_lev = mask_ds["deptho_lev"]
deptho_lev_values = deptho_lev.values
valid_levels = deptho_lev_values[~np.isnan(deptho_lev_values)]

print(f"\nValid sea-floor cells: {valid_levels.size:,}")
print(f"Minimum model level: {float(np.nanmin(valid_levels)):.0f}")
print(f"Maximum model level: {float(np.nanmax(valid_levels)):.0f}")
print(f"Mean model level: {float(np.nanmean(valid_levels)):.2f}")


# Grid cell physical dimensions (e1t, e2t, e3t)
print("GRID CELL DIMENSIONS")

e1t = coordinates["e1t"]
e2t = coordinates["e2t"]
e3t = coordinates["e3t"]

print(
    f"\ne1t — X dimension:"
    f"\n  Minimum: {float(e1t.min()):.3f} m"
    f"\n  Maximum: {float(e1t.max()):.3f} m"
    f"\n  Mean:    {float(e1t.mean()):.3f} m"
)

print(
    f"\ne2t — Y dimension:"
    f"\n  Minimum: {float(e2t.min()):.3f} m"
    f"\n  Maximum: {float(e2t.max()):.3f} m"
    f"\n  Mean:    {float(e2t.mean()):.3f} m"
)

print(
    f"\ne3t — Z dimension:"
    f"\n  Minimum: {float(e3t.min()):.3f} m"
    f"\n  Maximum: {float(e3t.max()):.3f} m"
    f"\n  Mean:    {float(e3t.mean()):.3f} m"
)


# Grid consistency checks between coordinates and mask files
print("GRID CONSISTENCY CHECKS")

checks_passed = True

if coordinates["latitude"].equals(mask_ds["latitude"]):
    print("\nLatitude grids:  PASS")
else:
    print("\nLatitude grids:  FAIL")
    checks_passed = False

if coordinates["longitude"].equals(mask_ds["longitude"]):
    print("Longitude grids: PASS")
else:
    print("Longitude grids: FAIL")
    checks_passed = False

if coordinates["depth"].equals(mask_ds["depth"]):
    print("Depth grids:     PASS")
else:
    print("Depth grids:     FAIL")
    checks_passed = False

if e1t.shape == (n_latitude, n_longitude):
    print("e1t dimensions:  PASS")
else:
    print("e1t dimensions:  FAIL")
    checks_passed = False

if e2t.shape == (n_latitude, n_longitude):
    print("e2t dimensions:  PASS")
else:
    print("e2t dimensions:  FAIL")
    checks_passed = False

if e3t.shape == (n_depth,):
    print("e3t dimensions:  PASS")
else:
    print("e3t dimensions:  FAIL")
    checks_passed = False

print("QUALITY CONTROL RESULT")

if checks_passed:
    print("\nALL GRID CONSISTENCY CHECKS PASSED!")
else:
    print("\nWARNING: ONE OR MORE CHECKS FAILED.")

coordinates.close()
mask_ds.close()

print("GRID ANALYSIS COMPLETE")
