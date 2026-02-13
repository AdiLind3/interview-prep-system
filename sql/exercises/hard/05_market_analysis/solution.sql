-- Solution: Market Analysis
WITH sales_2024 AS (
    SELECT
        seller_id,
        COUNT(*) AS items_sold_2024
    FROM orders
    WHERE order_date BETWEEN '2024-01-01' AND '2024-12-31'
    GROUP BY seller_id
),
ranked_orders AS (
    SELECT
        o.seller_id,
        i.item_category,
        ROW_NUMBER() OVER (PARTITION BY o.seller_id ORDER BY o.order_date, o.order_id) AS rn
    FROM orders o
    INNER JOIN items i ON o.item_id = i.item_id
),
second_items AS (
    SELECT seller_id, item_category AS second_item_category
    FROM ranked_orders
    WHERE rn = 2
)
SELECT
    u.user_id AS seller_id,
    u.join_date,
    IFNULL(s.items_sold_2024, 0) AS items_sold_2024,
    si.second_item_category,
    CASE
        WHEN si.second_item_category = u.favorite_category THEN 'yes'
        ELSE 'no'
    END AS category_match
FROM users u
LEFT JOIN sales_2024 s ON u.user_id = s.seller_id
LEFT JOIN second_items si ON u.user_id = si.seller_id
ORDER BY u.user_id;
