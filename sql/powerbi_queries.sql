-- Query 1: global summary statistics (one row per variable)
SELECT
    variable,
    ROUND(mean, 4) AS mean_value,
    ROUND(median, 4) AS median_value,
    ROUND(std, 4) AS standard_deviation,
    ROUND(minimum, 4) AS minimum_value,
    ROUND(maximum, 4) AS maximum_value
FROM global_surface_statistics
ORDER BY variable;

-- Query 2: full surface observations (main fact table for the map/scatter visuals)
SELECT
    time,
    latitude,
    longitude,
    spco2,
    chl,
    fe,
    no3,
    nppv,
    o2,
    ph,
    phyc,
    po4,
    si
FROM surface_biogeochemistry;

-- Query 3: latitude profile for every variable (line charts by latitude)
SELECT
    latitude,
    variable,
    mean_value
FROM latitude_surface_statistics
ORDER BY
    variable,
    latitude;

-- Query 4: depth profile for every variable (line charts by depth)
SELECT
    depth,
    depth_category,
    variable,
    mean_value
FROM global_depth_profiles
ORDER BY
    variable,
    depth;

-- Query 5: KPI card — biological/productivity variables
SELECT
    AVG(chl) AS average_chlorophyll,
    AVG(nppv) AS average_primary_production,
    AVG(phyc) AS average_phytoplankton,
    AVG(o2) AS average_oxygen,
    AVG(ph) AS average_ph
FROM surface_biogeochemistry;

-- Query 6: KPI card — nutrient variables
SELECT
    AVG(no3) AS average_nitrate,
    AVG(po4) AS average_phosphate,
    AVG(si) AS average_silicate,
    AVG(fe) AS average_iron
FROM surface_biogeochemistry;
