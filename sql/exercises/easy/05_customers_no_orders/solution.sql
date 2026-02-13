-- Solution: Customers Who Never Order
SELECT
    c.name AS customers
FROM customers c
LEFT JOIN orders o ON c.id = o.customerId
WHERE o.id IS NULL
ORDER BY c.name;
