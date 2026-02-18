# Lab: MySQL with Docker + DBeaver

---

# Part 0 - Install DBeaver (Community Edition)

### 1. Download DBeaver

Go to:

```
https://dbeaver.io/download/
```

Select:

> **DBeaver Community Edition (Free)**

Choose your operating system:

* Windows
* macOS
* Linux

Download and install using default settings.

---

# Part 1 - Make Sure Docker Is Running

### 1. Start Docker Desktop

Make sure Docker Desktop is running.

---

### 2. Verify MySQL Container

```bash
docker ps
```

You should see:

```
lab-mysql   mysql:8   Up ...
```

If not running:

```bash
docker compose up -d
```

Verify again:

```bash
docker ps
```

---

# Part 2 - Login to MySQL (CLI)

Connect:

```bash
docker exec -it lab-mysql mysql -u labuser -p
```

Enter password.

Select database:

```sql
USE labdb;
```

---

# Part 3 - Create Tables with Relationships

## Students Table

```sql
DROP TABLE IF EXISTS students;
CREATE TABLE students (
    student_id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100),
    major VARCHAR(100)
);
```

---

## Courses Table

```sql
DROP TABLE IF EXISTS courses;
CREATE TABLE courses (
    course_id INT PRIMARY KEY AUTO_INCREMENT,
    course_name VARCHAR(100),
    instructor VARCHAR(100)
);
```

---

## Enrollments Table (Foreign Keys)

```sql
DROP TABLE IF EXISTS enrollments;
CREATE TABLE enrollments (
    enrollment_id INT PRIMARY KEY AUTO_INCREMENT,
    student_id INT,
    course_id INT,
    grade VARCHAR(2),
    FOREIGN KEY (student_id) REFERENCES students(student_id),
    FOREIGN KEY (course_id) REFERENCES courses(course_id)
);
```

---

# Part 4 - Insert Sample Data

```sql
INSERT INTO students (name, major) VALUES
('Alice', 'Computer Science'),
('Bob', 'Mathematics'),
('Charlie', 'Physics');

INSERT INTO courses (course_name, instructor) VALUES
('Database Systems', 'Dr. Smith'),
('Algorithms', 'Dr. White');

INSERT INTO enrollments (student_id, course_id, grade) VALUES
(1, 1, 'A'),
(1, 2, 'B'),
(2, 1, 'A'),
(3, 2, 'C');
```

Verify:

```sql
SELECT * FROM students;
SELECT * FROM courses;
SELECT * FROM enrollments;
```

---

# Part 5 - Connect to MySQL in DBeaver

### 1. Open DBeaver

Click:

> New Database Connection

Choose:

> MySQL

---

### 2. Enter Connection Details

| Field    | Value           |
| -------- | --------------- |
| Host     | localhost       |
| Port     | 3306            |
| Database | labdb           |
| Username | labuser         |
| Password | (your password) |

Click:

> Test Connection

If successful, click:

> Finish

---

# Part 6 - Explore in DBeaver

### View Tables

Expand:

```
labdb → Tables
```

You should see:

* students
* courses
* enrollments

---

### View Data

Right-click table →
Click **View Data → All Rows**

---

### View ER Diagram

Right-click `labdb` →
Select **ER Diagram**

Or:

Select multiple tables →
Right-click → **ER Diagram**

You should see foreign key relationships visually.

---

# Final Student Tasks

1. Insert a new student.
2. Insert a new course.
3. Enroll that student in a course.
4. Refresh DBeaver.
5. Observe the relationship in the ER diagram.

---

# Learning Objectives

* Understand foreign keys
* Create relational schema
* Insert and query data
* Use CLI and GUI tools
* Visualize relationships

---