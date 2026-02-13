-- Insert departments
INSERT INTO department (id, name) VALUES
(1, 'IT'),
(2, 'Sales'),
(3, 'Marketing');

-- Insert employees
INSERT INTO employee (id, name, salary, departmentId) VALUES
(1, 'Joe', 85000, 1),
(2, 'Jim', 90000, 1),
(3, 'Henry', 80000, 2),
(4, 'Sam', 60000, 2),
(5, 'Max', 90000, 1),
(6, 'Janet', 69000, 1),
(7, 'Randy', 85000, 1),
(8, 'Will', 70000, 3),
(9, 'Dana', 70000, 3);
