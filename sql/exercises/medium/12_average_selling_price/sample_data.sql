-- Insert price periods
INSERT INTO prices (product_id, start_date, end_date, price) VALUES
(1, '2024-02-17', '2024-02-28', 5),
(1, '2024-03-01', '2024-03-22', 20),
(2, '2024-02-01', '2024-02-20', 15),
(2, '2024-02-21', '2024-03-31', 30),
(3, '2024-02-21', '2024-03-31', 30);

-- Insert units sold
INSERT INTO units_sold (product_id, purchase_date, units) VALUES
(1, '2024-02-25', 100),
(1, '2024-03-01', 15),
(2, '2024-02-10', 200),
(2, '2024-03-22', 30);
-- Note: product 3 has no sales
