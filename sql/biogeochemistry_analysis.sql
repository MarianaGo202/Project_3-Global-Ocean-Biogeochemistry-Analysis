-- Query 1: rank variables by their global mean value
WITH ranked_variables AS (
    SELECT
        variable,
        mean,
        std,
        RANK() OVER (
            ORDER BY mean DESC
        ) AS mean_rank
    FROM global_surface_statistics
)
SELECT
    variable,
    ROUND(mean, 4) AS mean_value,
    ROUND(std, 4) AS standard_deviation,
    mean_rank
FROM ranked_variables
ORDER BY mean_rank;

-- Query 2: classify each variable by its coefficient of variation
WITH variability AS (
    SELECT
        variable,
        mean,
        std,
        std / NULLIF(mean, 0)
            AS coefficient_variation
    FROM global_surface_statistics
)
SELECT
    variable,
    ROUND(mean, 4) AS mean_value,
    ROUND(std, 4) AS std_dev,
    ROUND(coefficient_variation, 4)
        AS coefficient_variation,
    CASE
        WHEN coefficient_variation >= 1
            THEN 'Very High Variability'
    
        WHEN coefficient_variation >= 0.5
            THEN 'High Variability'

        WHEN coefficient_variation >= 0.2
            THEN 'Moderate Variability'

        ELSE 'Low Variability'
    END AS variability_class
FROM variability
ORDER BY coefficient_variation DESC;

-- Query 3: global average of every biogeochemical variable
SELECT
    ROUND(AVG(spco2), 2)
        AS mean_surface_co2,
    
    ROUND(AVG(chl), 4)
        AS mean_chlorophyll,

    ROUND(AVG(no3), 4)
        AS mean_nitrate,

    ROUND(AVG(po4), 4)
        AS mean_phosphate,

    ROUND(AVG(si), 4)
        AS mean_silicate,

    ROUND(AVG(o2), 4)
        AS mean_oxygen,

    ROUND(AVG(ph), 4)
        AS mean_ph,

    ROUND(AVG(nppv), 4)
        AS mean_primary_production
FROM surface_biogeochemistry;

-- Query 4: nutrient ratios (Redfield-type relationships)
SELECT
    AVG(no3) /
        NULLIF(AVG(po4), 0)
        AS nitrate_phosphate_ratio,

    AVG(si) /
        NULLIF(AVG(no3), 0)
        AS silicate_nitrate_ratio
FROM surface_biogeochemistry;

-- Query 5: classify observations by productivity level
-- (based on chlorophyll and net primary production vs. global average)
SELECT
    CASE
        WHEN chl >= (
            SELECT AVG(chl)
            FROM surface_biogeochemistry
        )
        AND nppv >= (
            SELECT AVG(nppv)
            FROM surface_biogeochemistry
        )
        THEN 'High Productivity'
        WHEN chl < (
            SELECT AVG(chl)
            FROM surface_biogeochemistry
        )
        AND nppv < (
            SELECT AVG(nppv)
            FROM surface_biogeochemistry
        )
        THEN 'Low Productivity'
        ELSE 'Intermediate Productivity'
    END AS productivity_class,
    COUNT(*) AS observations
FROM surface_biogeochemistry
GROUP BY productivity_class
ORDER BY observations DESC;
