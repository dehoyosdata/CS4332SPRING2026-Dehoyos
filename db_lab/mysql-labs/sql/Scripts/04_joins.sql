USE labdb;

-- Show student enrollments with course names
SELECT s.name, c.course_name, e.grade
FROM enrollments e
JOIN students s ON e.student_id = s.student_id
JOIN courses c ON e.course_id = c.course_id;

-- Show courses with number of students enrolled (LEFT JOIN includes courses with 0 enrollments)
SELECT c.course_name, COUNT(e.student_id) AS total_enrolled
FROM courses c
LEFT JOIN enrollments e ON c.course_id = e.course_id
GROUP BY c.course_name;

-- RIGHT JOIN: show all students, even those not enrolled in any course
SELECT s.name, c.course_name, e.grade
FROM enrollments e
JOIN courses c ON e.course_id = c.course_id
RIGHT JOIN students s ON e.student_id = s.student_id;

-- Find students who are NOT enrolled in any course using LEFT JOIN + NULL check
SELECT s.name, s.major
FROM students s
LEFT JOIN enrollments e ON s.student_id = e.student_id
WHERE e.enrollment_id IS NULL;
