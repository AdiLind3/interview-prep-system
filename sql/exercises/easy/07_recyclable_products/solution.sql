-- Solution: Recyclable and Low Fat Products
SELECT
    product_id
FROM products
WHERE low_fats = 'Y' AND is_recyclable = 'Y'
ORDER BY product_id;
