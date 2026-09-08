-- Query 1: average chlorophyll by rounded latitude
SELECT
    ROUND(latitude, 2) AS latitude,
    ROUND(AVG(mean_value), 4)
        AS mean_biogeochemical_value
FROM latitude_surface_statistics
WHERE variable = 'chl'
GROUP BY latitude
ORDER BY latitude;

-- Query 2: chlorophyll profile across all latitudes
SELECT
    latitude,
    mean_value AS chlorophyll
FROM latitude_surface_statistics
WHERE variable = 'chl'
ORDER BY latitude;

-- Query 3: dissolved oxygen profile across all latitudes
SELECT
    latitude,
    mean_value AS oxygen
FROM latitude_surface_statistics
WHERE variable = 'o2'
ORDER BY latitude;

-- Query 4: net primary production profile across all latitudes
SELECT
    latitude,
    mean_value AS primary_production
FROM latitude_surface_statistics
WHERE variable = 'nppv'
ORDER BY latitude;

-- Query 5: classify latitudes into climate zones and average by zone
WITH zones AS (
    SELECT
        latitude,
        variable,
        mean_value,
        CASE
            WHEN latitude < -60
                THEN 'Southern Polar'
            WHEN latitude < -30
                THEN 'Southern Temperate'
            WHEN latitude < 0
                THEN 'Southern Subtropical'
            WHEN latitude < 30
                THEN 'Northern Subtropical'
            WHEN latitude < 60
                THEN 'Northern Temperate'
            ELSE 'Northern Polar'
        END AS latitude_zone
    FROM latitude_surface_statistics
)
SELECT
    latitude_zone,
    variable,
    ROUND(AVG(mean_value), 4)
        AS average_value
FROM zones
GROUP BY
    latitude_zone,
    variable
ORDER BY
    latitude_zone,
    variable;
