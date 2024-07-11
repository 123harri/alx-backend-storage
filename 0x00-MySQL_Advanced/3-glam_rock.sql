-- List bands with Glam rock as their main style, ranked by longevity in years until 2022

SELECT band_name, (IFNULL(split, 2022) - formed) AS lifespan
FROM (
    SELECT band_name, formed,
           CAST(SPLIT_PART(lifespan, '-', 1) AS UNSIGNED) AS split
    FROM metal_bands
    WHERE FIND_IN_SET('Glam rock', IFNULL(style, "")) > 0
) AS glam_bands
ORDER BY lifespan DESC;
