USE labdb;

-- Drop tables in correct order (because of foreign keys)

SET FOREIGN_KEY_CHECKS = 0; -- Disable foreign key checks so we can drop tables in any order without constraint errors

DROP TABLE IF EXISTS students;
DROP TABLE IF EXISTS courses;
DROP TABLE IF EXISTS enrollments;

SET FOREIGN_KEY_CHECKS = 1; -- Re-enable foreign key checks so constraints are enforced for all future operations


-- Create students table
CREATE TABLE students (
    student_id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100),
    major VARCHAR(100)
);

-- Create courses table
CREATE TABLE courses (
    course_id INT PRIMARY KEY AUTO_INCREMENT,
    course_name VARCHAR(100),
    instructor VARCHAR(100)
);

-- Create enrollments table (many-to-many relationship)
CREATE TABLE enrollments (
    enrollment_id INT PRIMARY KEY AUTO_INCREMENT,
    student_id INT,
    course_id INT,
    grade VARCHAR(2),
    FOREIGN KEY (student_id) REFERENCES students(student_id),
    FOREIGN KEY (course_id) REFERENCES courses(course_id)
);
