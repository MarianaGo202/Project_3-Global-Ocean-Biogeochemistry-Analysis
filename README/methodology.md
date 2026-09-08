# Methodology — Global Ocean Biogeochemistry Hindcast

## Objective

Build an end-to-end analytics pipeline — from raw ocean model
NetCDF files to a queryable database and a Power BI dashboard —
to explore global patterns in ocean biogeochemistry (nutrients,
oxygen, pH, chlorophyll and primary production).

## Data source

Copernicus Marine Service / Mercator Ocean — Global Ocean
Biogeochemistry Hindcast (`GLOBAL_REANALYSIS_BIO_001_029`),
monthly mean for September 2025. Three raw files are used:

- **Monthly** — the biogeochemical fields themselves (10
  variables, 3D: depth × latitude × longitude)
- **Coordinates** — the model grid definition (latitude,
  longitude, depth, cell dimensions)
- **Mask** — ocean/land mask and bathymetry for the same grid

## Pipeline overview

The pipeline is organized as a sequence of numbered scripts in
`python/`, each with a single responsibility:

| Step | Script | Purpose |
|---|---|---|
| 01 | `01_inspecionar_netcdf.py` | Inspect the monthly NetCDF file (dimensions, variables, missing values) |
| 02 | `02_inspecionar_coordinates.py` | Inspect the grid coordinates file |
| 03 | `03_inspecionar_mask.py` | Inspect the ocean/land mask file |
| 04 | `04_analisar_grade.py` | Cross-check the coordinates and mask files, quantify ocean vs. land coverage |
| 05 | `05_preparar_dados.py` | Extract the surface level, apply the ocean mask, export `surface_biogeochemistry_2025_09.csv` |
| 06 | `06_criar_agregacoes.py` | Compute global, latitude and longitude summary statistics |
| 07 | `07_preparar_profundidade.py` | Compute the full-depth global vertical profile for each variable |
| 08 | `08_criar_dimensoes.py` | Build the dimension tables (`dim_variable`, `dim_depth`, `dim_date`) |
| 09 | `09_criar_banco.py` | Load every processed CSV into `ocean_biogeochemistry.db` (SQLite) and create indexes |
| 10 | `10_validar_banco.py` | Validate the finished database (tables, row counts, nulls, ranges, integrity check) |
| 12 | `12_gerar_figuras.py` | Generate PNG figures directly from the database for the repository |

## Key processing decisions

- **Ocean masking:** every value is masked using the model's own
  ocean/land mask (`mask == 1`) before export, so land cells and
  cells with no valid data are excluded rather than appearing as
  nulls in the final tables.
- **Surface vs. full depth:** the main fact table
  (`surface_biogeochemistry`) uses only the surface level (depth
  ≈ 0.5 m) to keep the row count manageable (682,424 rows) for
  Power BI and SQL exploration. The full water column is kept
  separately, aggregated to a single global profile per variable
  and depth level (`global_depth_profiles`), since a full 3D
  export (75 depth levels × full grid) would be too large to be
  practical for this project's scope.
- **Depth categories:** depth levels are grouped into six
  readable categories (Surface, Shallow, Upper Ocean,
  Intermediate, Deep Ocean, Abyssal) to make depth-based analysis
  and dashboard filtering easier than working with raw meters.
- **Star-schema-style database:** the database separates fact
  tables (observations and statistics) from dimension tables
  (`dim_variable`, `dim_depth`, `dim_date`), so Power BI can build
  a clean data model with relationships instead of relying on
  repeated text columns.

## Tools used

- **Python** (`xarray`, `pandas`, `numpy`, `matplotlib`) — NetCDF
  processing, aggregation and figure generation
- **SQLite** — lightweight relational database for the processed
  data
- **SQL** — exploratory and analytical queries
  (`sql/01_exploracao.sql` through `sql/06_powerbi_queries.sql`)
- **Power BI** — final interactive dashboard

## Limitations

- Single reference month (September 2025) — no time-series /
  seasonal analysis in this version of the project.
- The vertical (depth) analysis uses a globally averaged profile
  rather than a full 3D cube, so it cannot show how a profile
  changes by region.
- `spco2` and a few other variables show high maximum values
  relative to their mean; these were checked for validity
  (`02_quality_control.sql`) but were not individually
  cross-referenced against known extreme regions — see
  `data_quality.md` for details.
