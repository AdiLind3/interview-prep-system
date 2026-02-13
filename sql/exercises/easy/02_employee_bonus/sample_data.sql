-- Insert employees
INSERT INTO employee (empId, name, supervisor, salary) VALUES
(1, 'John', 3, 60000),
(2, 'Dan', 3, 55000),
(3, 'Brad', NULL, 80000),
(4, 'Thomas', 3, 45000),
(5, 'Karen', 3, 50000);

-- Insert bonus records (not every employee has one)
INSERT INTO bonus (empId, bonus) VALUES
(2, 500),
(4, 2000),
(5, 800);
