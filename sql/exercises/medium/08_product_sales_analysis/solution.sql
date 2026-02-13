-- Solution: Product Sales Analysis III
WITH ranked_sales AS (
    SELECT
        product_id,
        year AS first_year,
        quantity,
        price,
        RANK() OVER (PARTITION BY product_id ORDER BY year) AS rk
    FROM sales
)
SELECT
    product_id,
    first_year,
    quantity,
    price
FROM ranked_sales
WHERE rk = 1
ORDER BY product_id;
