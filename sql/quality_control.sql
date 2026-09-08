-- Query 1: missing values per biogeochemical variable
SELECT
    COUNT(*) AS total_rows,
    SUM(
        CASE WHEN spco2 IS NULL THEN 1 ELSE 0 END
    ) AS missing_spco2,
    SUM(
        CASE WHEN chl IS NULL THEN 1 ELSE 0 END
    ) AS missing_chl,
    SUM(
        CASE WHEN fe IS NULL THEN 1 ELSE 0 END
    ) AS missing_fe,
    SUM(
        CASE WHEN no3 IS NULL THEN 1 ELSE 0 END
    ) AS missing_no3,
    SUM(
        CASE WHEN nppv IS NULL THEN 1 ELSE 0 END
    ) AS missing_nppv,
    SUM(
        CASE WHEN o2 IS NULL THEN 1 ELSE 0 END
    ) AS missing_o2,
    SUM(
        CASE WHEN ph IS NULL THEN 1 ELSE 0 END
    ) AS missing_ph,
    SUM(
        CASE WHEN phyc IS NULL THEN 1 ELSE 0 END
    ) AS missing_phyc,
    SUM(
        CASE WHEN po4 IS NULL THEN 1 ELSE 0 END
    ) AS missing_po4,
    SUM(
        CASE WHEN si IS NULL THEN 1 ELSE 0 END
    ) AS missing_si

FROM surface_biogeochemistry;

-- Query 2: pH values outside the valid chemical range (0-14)
SELECT
    COUNT(*) AS invalid_ph
FROM surface_biogeochemistry
WHERE ph IS NOT NULL
AND (
    ph < 0
    OR ph > 14
);

-- Query 3: negative dissolved oxygen values (should not occur)
SELECT
    COUNT(*) AS negative_oxygen_values
FROM surface_biogeochemistry
WHERE o2 < 0;

-- Query 4: negative nitrate values (should not occur)
SELECT
    COUNT(*) AS negative_nitrate_values
FROM surface_biogeochemistry
WHERE no3 < 0;

-- Query 5: negative phosphate values (should not occur)
SELECT
    COUNT(*) AS negative_phosphate_values
FROM surface_biogeochemistry
WHERE po4 < 0;

-- Query 6: negative silicate values (should not occur)
SELECT
    COUNT(*) AS negative_silicate_values
FROM surface_biogeochemistry
WHERE si < 0;

-- Query 7: coordinates outside valid latitude/longitude ranges
SELECT
    COUNT(*) AS invalid_coordinates
FROM surface_biogeochemistry
WHERE latitude < -90
   OR latitude > 90
   OR longitude < -180
   OR longitude > 180;