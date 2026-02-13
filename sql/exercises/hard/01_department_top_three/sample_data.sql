-- Insert departments
INSERT INTO department (id, name) VALUES
(1, 'IT'),
(2, 'Sales');

-- Insert employees
INSERT INTO employee (id, name, salary, departmentId) VALUES
(1, 'Joe', 85000, 1),
(2, 'Henry', 80000, 2),
(3, 'Sam', 60000, 2),
(4, 'Max', 90000, 1),
(5, 'Janet', 69000, 1),
(6, 'Randy', 85000, 1),
(7, 'Will', 70000, 1),
(8, 'Karen', 75000, 2),
(9, 'Tom', 80000, 2),
(10, 'Alice', 90000, 1),
(11, 'Bob', 65000, 2);
