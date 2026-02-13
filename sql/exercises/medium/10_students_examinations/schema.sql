-- Create students table
CREATE TABLE students (
    student_id INTEGER PRIMARY KEY,
    student_name TEXT NOT NULL
);

-- Create subjects table
CREATE TABLE subjects (
    subject_name TEXT PRIMARY KEY
);

-- Create examinations table
CREATE TABLE examinations (
    student_id INTEGER NOT NULL,
    subject_name TEXT NOT NULL
);
