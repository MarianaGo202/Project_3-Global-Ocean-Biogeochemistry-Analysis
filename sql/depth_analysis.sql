-- Query 1: full vertical profile for every variable
SELECT

    depth,
    variable,
    ROUND(mean_value, 5)
        AS mean_value,
    depth_category

FROM global_depth_profiles

ORDER BY
    variable,
    depth;

-- Query 2: dissolved oxygen profile by depth
SELECT

    depth,
    mean_value AS oxygen

FROM global_depth_profiles

WHERE variable = 'o2'

ORDER BY depth;

-- Query 3: chlorophyll profile by depth
SELECT

    depth,
    mean_value AS chlorophyll

FROM global_depth_profiles

WHERE variable = 'chl'

ORDER BY depth;

-- Query 4: nitrate profile by depth
SELECT

    depth,
    mean_value AS nitrate

FROM global_depth_profiles

WHERE variable = 'no3'

ORDER BY depth;

-- Query 5: pH profile by depth
SELECT

    depth,
    mean_value AS ph

FROM global_depth_profiles

WHERE variable = 'ph'

ORDER BY depth;

-- Query 6: summary statistics by depth category (Surface, Shallow, etc.)
SELECT

    depth_category,

    variable,

    ROUND(AVG(mean_value), 4)
        AS average_value,

    ROUND(MIN(mean_value), 4)
        AS minimum_value,

    ROUND(MAX(mean_value), 4)
        AS maximum_value

FROM global_depth_profiles

GROUP BY
    depth_category,
    variable

ORDER BY
    depth_category,
    variable;