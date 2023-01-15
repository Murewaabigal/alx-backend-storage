-- Lists all bands with Glam rock as their main style, ranked by their longevity.

SELECT
    band_name AS band_name,
    IFNULL(split, CURRENT_DATE()) - IFNULL(formed, 0) AS lifespan
FROM metal_bands
WHERE style LIKE '%Glam rock%'
ORDER BY lifespan DESC;
