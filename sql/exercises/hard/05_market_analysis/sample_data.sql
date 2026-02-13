-- Insert users
INSERT INTO users (user_id, join_date, favorite_category) VALUES
(1, '2023-01-01', 'Electronics'),
(2, '2023-02-09', 'Books'),
(3, '2023-01-19', 'Electronics'),
(4, '2023-05-21', 'Books');

-- Insert items
INSERT INTO items (item_id, item_category) VALUES
(1, 'Electronics'),
(2, 'Books'),
(3, 'Electronics'),
(4, 'Books'),
(5, 'Clothing');

-- Insert orders
INSERT INTO orders (order_id, order_date, item_id, buyer_id, seller_id) VALUES
(1, '2024-01-12', 1, 2, 1),
(2, '2024-02-18', 2, 3, 1),
(3, '2024-03-01', 3, 1, 2),
(4, '2024-04-05', 4, 2, 3),
(5, '2024-05-10', 5, 1, 3),
(6, '2024-06-15', 1, 3, 1),
(7, '2023-11-20', 2, 1, 4);
