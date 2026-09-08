# Data Dictionary — Global Ocean Biogeochemistry Hindcast

This document describes every table and column produced by the
Project 3 pipeline, from the raw NetCDF files to the final
SQLite database (`ocean_biogeochemistry.db`).

## Source data

- **Product:** Global Ocean Biogeochemistry Hindcast
  (Copernicus Marine Service / Mercator Ocean, product
  `GLOBAL_REANALYSIS_BIO_001_029`)
- **Reference month:** September 2025 (monthly mean)
- **Native grid:** 0.25° horizontal resolution, 75 depth levels
  (surface to abyssal)

## Biogeochemical variables

| Code | Name | Unit |
|---|---|---|
| spco2 | Surface CO2 | Pa |
| chl | Total Chlorophyll | mg m-3 |
| fe | Dissolved Iron | mmol m-3 |
| no3 | Nitrate | mmol m-3 |
| nppv | Primary Production | mg m-3 day-1 |
| o2 | Dissolved Oxygen | mmol m-3 |
| ph | pH | dimensionless |
| phyc | Total Phytoplankton | mmol m-3 |
| po4 | Phosphate | mmol m-3 |
| si | Dissolved Silicate | mmol m-3 |

## Tables

### `surface_biogeochemistry` (fact table, 682,424 rows)

Surface-level (depth ≈ 0.5 m) observation for every ocean grid
cell, for the reference month.

| Column | Type | Description |
|---|---|---|
| time | TEXT | Reference date of the monthly mean |
| year | INTEGER | Year extracted from `time` |
| month | INTEGER | Month extracted from `time` |
| year_month | TEXT | `YYYY-MM` label |
| latitude | REAL | Latitude in decimal degrees (-90 to 90) |
| longitude | REAL | Longitude in decimal degrees (-180 to 180) |
| depth | REAL | Depth of the surface level (m) |
| depth_category | TEXT | Always `Surface` in this table |
| spco2, chl, fe, no3, nppv, o2, ph, phyc, po4, si | REAL | Biogeochemical variables (see table above) |

### `global_surface_statistics` (10 rows)

One row per variable with global surface summary statistics:
`count`, `mean`, `median`, `std`, `minimum`, `maximum`, `q25`, `q75`.

### `latitude_surface_statistics` (6,670 rows)

Average value of each variable per latitude band (longitude
averaged out). Columns: `time`, `latitude`, `variable`, `mean_value`.

### `longitude_surface_statistics` (14,400 rows)

Average value of each variable per longitude band (latitude
averaged out). Columns: `time`, `longitude`, `variable`, `mean_value`.

### `global_depth_profiles` (666 rows)

Global average of each variable at every model depth level
(full water column, not just surface). Columns: `time`, `depth`,
`variable`, `mean_value`, `depth_category`.

### `dim_variable` (10 rows)

Lookup table with `variable_code`, `variable_name`, `unit` — used
to join human-readable names/units onto the fact tables in
Power BI.

### `dim_depth` (75 rows)

One row per model depth level, with `depth_id`, `depth_m` and
`depth_category` (Surface, Shallow, Upper Ocean, Intermediate,
Deep Ocean, Abyssal).

### `dim_date` (1 row)

Single reference row for the analyzed month: `date_id`, `date`,
`year`, `month`, `month_name`, `quarter`.

## Depth categories

| Category | Depth range |
|---|---|
| Surface | ≤ 10 m |
| Shallow | 10–50 m |
| Upper Ocean | 50–200 m |
| Intermediate | 200–1,000 m |
| Deep Ocean | 1,000–4,000 m |
| Abyssal | > 4,000 m |
