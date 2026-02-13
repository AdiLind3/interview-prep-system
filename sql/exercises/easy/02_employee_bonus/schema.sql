-- Create employee table
CREATE TABLE employee (
    empId INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    supervisor INTEGER,
    salary INTEGER NOT NULL
);

-- Create bonus table
CREATE TABLE bonus (
    empId INTEGER PRIMARY KEY,
    bonus INTEGER NOT NULL,
    FOREIGN KEY (empId) REFERENCES employee(empId)
);
