-- Solution: Customer Orders
SELECT
    c.id as customer_id,
    c.name,
    c.email,
    COUNT(o.id) as order_count
FROM customers c
INNER JOIN orders o ON c.id = o.customer_id
GROUP BY c.id, c.name, c.email
ORDER BY order_count DESC;
