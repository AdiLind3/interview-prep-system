-- Insert employees
INSERT INTO employees (id, name, department) VALUES
(1, 'John Doe', 'Sales'),
(2, 'Jane Smith', 'Sales'),
(3, 'Mike Johnson', 'Sales'),
(4, 'Sarah Williams', 'Marketing'),
(5, 'Tom Brown', 'Marketing'),
(6, 'Emily Davis', 'Engineering'),
(7, 'David Wilson', 'Engineering');

-- Insert sales data (multiple months)
INSERT INTO sales (id, employee_id, month, amount) VALUES
-- Sales department
(1, 1, '2024-01', 50000),
(2, 1, '2024-02', 55000),
(3, 1, '2024-03', 60000),
(4, 2, '2024-01', 45000),
(5, 2, '2024-02', 48000),
(6, 2, '2024-03', 52000),
(7, 3, '2024-01', 40000),
(8, 3, '2024-02', 42000),
(9, 3, '2024-03', 45000),
-- Marketing department
(10, 4, '2024-01', 35000),
(11, 4, '2024-02', 38000),
(12, 4, '2024-03', 41000),
(13, 5, '2024-01', 30000),
(14, 5, '2024-02', 32000),
(15, 5, '2024-03', 35000),
-- Engineering department
(16, 6, '2024-01', 25000),
(17, 6, '2024-02', 27000),
(18, 6, '2024-03', 30000),
(19, 7, '2024-01', 28000),
(20, 7, '2024-02', 29000),
(21, 7, '2024-03', 31000);
