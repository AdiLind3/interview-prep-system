-- Create department table
CREATE TABLE department (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL
);

-- Create employee table
CREATE TABLE employee (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    salary INTEGER NOT NULL,
    departmentId INTEGER NOT NULL,
    FOREIGN KEY (departmentId) REFERENCES department(id)
);
