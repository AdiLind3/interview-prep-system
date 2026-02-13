-- Solution: Average Selling Price
SELECT
    p.product_id,
    ROUND(IFNULL(SUM(p.price * u.units) * 1.0 / SUM(u.units), 0), 2) AS average_price
FROM prices p
LEFT JOIN units_sold u
    ON p.product_id = u.product_id
    AND u.purchase_date BETWEEN p.start_date AND p.end_date
GROUP BY p.product_id
ORDER BY p.product_id;
