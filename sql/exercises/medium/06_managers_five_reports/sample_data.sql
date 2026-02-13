-- Insert employees
INSERT INTO employee (id, name, department, managerId) VALUES
(101, 'John', 'A', NULL),
(102, 'Dan', 'A', 101),
(103, 'James', 'A', 101),
(104, 'Amy', 'A', 101),
(105, 'Anne', 'A', 101),
(106, 'Ron', 'B', 101),
(107, 'Lisa', 'B', 108),
(108, 'Maria', 'B', NULL),
(109, 'Tom', 'B', 108),
(110, 'Pat', 'B', 108),
(111, 'Sam', 'B', 108),
(112, 'Kate', 'B', 108);
