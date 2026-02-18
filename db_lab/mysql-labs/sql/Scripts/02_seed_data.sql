USE labdb;

-- Insert students
INSERT INTO students (name, major) VALUES
('Alice', 'Computer Science'),
('Bob', 'Mathematics'),
('Charlie', 'Physics'),
('David', 'Engineering');

-- Insert courses
INSERT INTO courses (course_name, instructor) VALUES
('Database Systems', 'Dr. Smith'),
('Algorithms', 'Dr. White'),
('Operating Systems', 'Dr. Brown');

-- Insert enrollments
INSERT INTO enrollments (student_id, course_id, grade) VALUES
(1, 1, 'A'),
(1, 2, 'B'),
(2, 1, 'A'),
(3, 3, 'B'),
(4, 2, 'C');
