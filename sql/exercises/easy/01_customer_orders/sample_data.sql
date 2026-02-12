-- Insert sample customers
INSERT INTO customers (id, name, email) VALUES
(1, 'Alice Johnson', 'alice@email.com'),
(2, 'Bob Smith', 'bob@email.com'),
(3, 'Charlie Brown', 'charlie@email.com'),
(4, 'Diana Prince', 'diana@email.com'),
(5, 'Eve Martinez', 'eve@email.com');

-- Insert sample orders
INSERT INTO orders (id, customer_id, order_date, total_amount) VALUES
(1, 1, '2024-01-15', 150.00),
(2, 1, '2024-01-20', 200.50),
(3, 1, '2024-02-01', 75.25),
(4, 2, '2024-01-18', 500.00),
(5, 2, '2024-02-05', 300.00),
(6, 3, '2024-01-25', 125.75),
(7, 4, '2024-02-10', 450.00),
(8, 4, '2024-02-15', 275.50),
(9, 4, '2024-02-20', 180.25);
-- Note: Customer 5 (Eve Martinez) has no orders
