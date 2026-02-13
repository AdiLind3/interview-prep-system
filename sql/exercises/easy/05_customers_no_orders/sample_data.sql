-- Insert customers
INSERT INTO customers (id, name) VALUES
(1, 'Joe'),
(2, 'Henry'),
(3, 'Sam'),
(4, 'Max'),
(5, 'Linda');

-- Insert orders (not every customer has orders)
INSERT INTO orders (id, customerId) VALUES
(1, 3),
(2, 1),
(3, 3),
(4, 1);
