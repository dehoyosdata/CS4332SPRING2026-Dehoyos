SELECT s.id, s.name, s.email, COUNT(*) AS late_return_count
FROM students s
JOIN loans l ON s.id = l.student_id
WHERE l.returned_at IS NOT NULL
  AND l.returned_at > l.due_date
GROUP BY s.id, s.name, s.email
ORDER BY late_return_count DESC;