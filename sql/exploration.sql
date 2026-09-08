-- Query 1: list all tables in the database
SELECT
    name AS table_name
FROM sqlite_master
WHERE type = 'table'
ORDER BY name;

-- Query 2: row count for the main fact tables
SELECT
    'surface_biogeochemistry' AS table_name,
    COUNT(*) AS row_count
FROM surface_biogeochemistry

UNION ALL

SELECT
    'global_surface_statistics',
    COUNT(*)
FROM global_surface_statistics

UNION ALL

SELECT
    'global_depth_profiles',
    COUNT(*)
FROM global_depth_profiles;

-- Query 3: variable dictionary (code, name, unit)
SELECT
    variable_code,
    variable_name,
    unit
FROM dim_variable
ORDER BY variable_code;

-- Query 4: global summary statistics per variable
SELECT
    variable,
    count,
    ROUND(mean, 4) AS mean_value,
    ROUND(median, 4) AS median_value,
    ROUND(std, 4) AS standard_deviation,
    ROUND(minimum, 4) AS minimum_value,
    ROUND(maximum, 4) AS maximum_value
FROM global_surface_statistics
ORDER BY variable;

-- Query 5: coefficient of variation per variable (relative variability)
SELECT
    variable,
    ROUND(mean, 4) AS mean_value,
    ROUND(std, 4) AS standard_deviation,
    ROUND(
        std / NULLIF(mean, 0),
        4
    ) AS coefficient_of_variation
FROM global_surface_statistics
ORDER BY coefficient_of_variation DESC;

-- Query 6: geographic coverage of the surface dataset
SELECT
    COUNT(*) AS total_observations,
    MIN(latitude) AS minimum_latitude,
    MAX(latitude) AS maximum_latitude,
    MIN(longitude) AS minimum_longitude,
    MAX(longitude) AS maximum_longitude
FROM surface_biogeochemistry;