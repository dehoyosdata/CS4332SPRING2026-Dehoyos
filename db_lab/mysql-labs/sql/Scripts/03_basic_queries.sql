USE labdb;

-- View all students
SELECT * FROM students;

-- View all courses
SELECT * FROM courses;

-- View all enrollments
SELECT * FROM enrollments;

-- Filter students by major using WHERE
SELECT * FROM students
WHERE major = 'Computer Science';

-- Find students whose name starts with 'A' using LIKE
SELECT * FROM students
WHERE name LIKE 'A%';

-- Sort students alphabetically by name
SELECT * FROM students
ORDER BY name ASC;

-- Count students per major
SELECT major, COUNT(*) AS total_students
FROM students
GROUP BY major;

-- Only show majors with more than 1 student using HAVING
SELECT major, COUNT(*) AS total_students
FROM students
GROUP BY major
HAVING COUNT(*) > 1;

-- Show enrollments with grades better than or equal to 'B' (alphabetically A < B)
SELECT * FROM enrollments
WHERE grade <= 'B'
ORDER BY grade;
