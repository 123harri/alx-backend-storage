-- List bands with Glam rock as their main style, ranked by longevity in years until 2022

SELECT band_name,
       DATEDIFF('2022-01-01', SUBSTRING_INDEX(lifespan, '–', 1)) AS lifespan
FROM metal_bands
WHERE style LIKE '%Glam rock%'
ORDER BY lifespan DESC;
