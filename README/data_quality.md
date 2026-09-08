# Data Quality Report — Global Ocean Biogeochemistry Hindcast

This report summarizes the quality checks run against
`surface_biogeochemistry` (682,424 rows) using
`sql/02_quality_control.sql`.

## Completeness

No missing values in any of the 10 biogeochemical variables:

| Variable | Missing | % |
|---|---|---|
| spco2 | 0 | 0.00% |
| chl | 0 | 0.00% |
| fe | 0 | 0.00% |
| no3 | 0 | 0.00% |
| nppv | 0 | 0.00% |
| o2 | 0 | 0.00% |
| ph | 0 | 0.00% |
| phyc | 0 | 0.00% |
| po4 | 0 | 0.00% |
| si | 0 | 0.00% |

This is expected: the ocean mask (`GLOBAL_REANALYSIS_BIO_001_029_mask.nc`)
was applied before export, so land cells and cells with no data
were already dropped in step 05 (`05_preparar_dados.py`).

## Validity checks

| Check | Result |
|---|---|
| pH outside [0, 14] | 0 rows |
| Negative dissolved oxygen | 0 rows |
| Negative nitrate | 0 rows |
| Negative phosphate | 0 rows |
| Negative silicate | 0 rows |
| Coordinates outside valid range | 0 rows |

All checks passed — no invalid values found.

## Value ranges (sanity check)

| Variable | Min | Mean | Max |
|---|---|---|---|
| spco2 (Pa) | 6.21 | 40.69 | 440.47 |
| chl (mg m-3) | 0.013 | 0.284 | 19.66 |
| fe (mmol m-3) | 0.0000 | 0.0005 | 0.031 |
| no3 (mmol m-3) | 0.0004 | 7.226 | 129.04 |
| nppv (mg m-3 day-1) | 0.0001 | 5.407 | 1417.77 |
| o2 (mmol m-3) | 148.02 | 270.50 | 423.74 |
| ph | 5.89 | 8.02 | 8.53 |
| phyc (mmol m-3) | 0.040 | 1.547 | 56.10 |
| po4 (mmol m-3) | 0.0000 | 0.648 | 4.27 |
| si (mmol m-3) | 0.242 | 14.653 | 503.87 |

**Note on outliers:** `nppv` and `si` show very high maximum
values relative to their mean (consistent with their very high
coefficient of variation, see below) — this is expected for
these variables, since primary production and silicate are
concentrated in specific regions (coastal upwelling, polar
waters) rather than evenly distributed. `spco2` values above
~440 Pa should be spot-checked against known extreme regions
(e.g. upwelling zones) before being reported as typical values.

## Variability ranking

Coefficient of variation (std / mean) per variable, from
`03_biogeochemistry_analysis.sql`:

| Variable | Coefficient of Variation | Class |
|---|---|---|
| nppv | 2.43 | Very High |
| fe | 2.15 | Very High |
| si | 1.74 | Very High |
| no3 | 1.42 | Very High |
| chl | 1.14 | Very High |
| po4 | 1.05 | Very High |
| phyc | 0.75 | High |
| o2 | 0.23 | Moderate |
| spco2 | 0.10 | Low |
| ph | 0.005 | Low |

pH and spco2 are the most spatially uniform variables at the
surface; nutrient and productivity variables (nppv, fe, si, no3)
vary the most, reflecting strong regional differences (upwelling,
polar productivity, river input).

## Geographic and temporal coverage

- Latitude: -76.75° to 89.75°
- Longitude: -180.0° to 179.75°
- Reference month: September 2025 (single monthly mean)

## Database integrity

`PRAGMA integrity_check` was run against `ocean_biogeochemistry.db`
as part of `10_validar_banco.py` — result: `ok`.
