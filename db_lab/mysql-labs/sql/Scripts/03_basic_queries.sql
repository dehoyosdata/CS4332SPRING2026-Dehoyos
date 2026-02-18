USE labdb;

-- View all students
SELECT * FROM students;

-- View all courses
SELECT * FROM courses;

-- View all enrollments
SELECT * FROM enrollments;

-- Count students per major
SELECT major, COUNT(*) AS total_students
FROM students
GROUP BY major;
