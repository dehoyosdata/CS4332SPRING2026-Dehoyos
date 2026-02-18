USE labdb;

-- Show student enrollments with course names
SELECT s.name, c.course_name, e.grade
FROM enrollments e
JOIN students s ON e.student_id = s.student_id
JOIN courses c ON e.course_id = c.course_id;

-- Show courses with number of students enrolled
SELECT c.course_name, COUNT(e.student_id) AS total_enrolled
FROM courses c
LEFT JOIN enrollments e ON c.course_id = e.course_id
GROUP BY c.course_name;
