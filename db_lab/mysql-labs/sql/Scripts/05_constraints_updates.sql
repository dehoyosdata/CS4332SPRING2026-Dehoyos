USE labdb;

-- Update a student's major
UPDATE students
SET major = 'Data Science'
WHERE name = 'Alice';

-- Change a grade
UPDATE enrollments
SET grade = 'A'
WHERE student_id = 4 AND course_id = 2;

-- Delete a student (must remove enrollments first)
DELETE FROM enrollments WHERE student_id = 3;
DELETE FROM students WHERE student_id = 3;

-- Verify changes
SELECT * FROM students;
SELECT * FROM enrollments;
