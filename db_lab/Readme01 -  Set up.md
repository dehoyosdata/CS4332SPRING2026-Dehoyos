# Docker Volumes Cheatsheet - DB Lab

---

## 1. Storage Types

| Storage Type | Compose Example               | Where Data Lives       | Best Use Case            |
| ------------ | ----------------------------- | ---------------------- | ------------------------ |
| No Volume    | (none defined)                | Inside container layer | Temporary testing only   |
| Named Volume | `mysql_data:/var/lib/mysql`   | Docker-managed storage | Regular labs, easy reset |
| Bind Mount   | `./mysql_data:/var/lib/mysql` | Host project folder    | Storage internals demo   |

---

## 2. Start / Stop Behavior

| Command                  | Containers      | Named Volumes       | Bind-Mounted Folders |
| ------------------------ | --------------- | ------------------- | -------------------- |
| `docker compose up -d`   | Created/Started | Created (if needed) | Used if exists       |
| `docker compose down`    | Removed         | Kept                | Kept                 |
| `docker compose down -v` | Removed         | Deleted             | Kept                 |

---

## 3. Viewing Volumes

| Action         | Command                                  |
| -------------- | ---------------------------------------- |
| List volumes   | `docker volume ls`                       |
| Inspect volume | `docker volume inspect <volume_name>`    |
| See mountpoint | Look at `"Mountpoint"` in inspect output |

---

## 4. Access Volume Contents

| Action                           | Command                                                  |
| -------------------------------- | -------------------------------------------------------- |
| Mount volume into temp container | `docker run --rm -it -v <volume_name>:/data ubuntu bash` |
| Read-only mount                  | `-v <volume_name>:/data:ro`                              |
| View files                       | `cd /data && ls -lh`                                     |

---

## 5. Connect to Databases

| Database   | Command                                                 |
| ---------- | ------------------------------------------------------- |
| MySQL      | `docker exec -it lab-mysql mysql -u labuser -p`         |
| PostgreSQL | `docker exec -it lab-postgres psql -U labuser -d labdb` |
| Oracle     | `docker exec -it lab-oracle sqlplus`                    |

Perfect - below are **clean, test-ready SQL snippets** for MySQL, PostgreSQL, and Oracle.

Each includes:

* Show databases
* Create/select database
* Create table
* Insert rows
* Query rows

You can copy-paste directly after connecting.

---

##### MySQL Test Snippet

After connecting:

```bash
docker exec -it lab-mysql mysql -u labuser -p
```

###### Show databases

```sql
SHOW DATABASES;
```

###### Select database

```sql
USE labdb;
```

###### Create table

```sql
CREATE TABLE students (
    id INT PRIMARY KEY,
    name VARCHAR(50),
    major VARCHAR(50)
);
```

###### Insert rows

```sql
INSERT INTO students VALUES
(1, 'Alice', 'CS'),
(2, 'Bob', 'Math'),
(3, 'Carol', 'Physics');
```

These queries are longer, so make sure you’ve completed **Readme00** and installed `vi`.

If `vi` is installed, you can open the editor directly inside MySQL using:

```sql
\e
```

Write or modify your SQL in Vim, then save and exit with:

```
:wq
```

After returning to MySQL, ensure your query ends with a semicolon `;` to execute it.

Alternatively, you can also write a sql query and save it as `.sql` and execute it.

```bash
 # Access the terminal session
 docker exec -it lab-mysql bash
 ```
Now you can create a sql script here, may be using `vi`, e.g., 
```sql
-- script.sql
SELECT * FROM students
```
Now login to sql 
```bash
mysql -u labuser -p # enter the password when prompted
```
Then you can do following
```sql
USE labdb; -- use labdb
SOURCE script.sql --run script or ./ script.sql
```



###### Query rows

```sql
SELECT * FROM students;
```

---

##### PostgreSQL Test Snippet

After connecting:

```bash
docker exec -it lab-postgres psql -U labuser -d labdb
```

###### List databases

```sql
\l
-- \c labdb     -- connect to labdb
-- \dt          -- show all tables

```

###### Create table

```sql
CREATE TABLE students (
    id INT PRIMARY KEY,
    name VARCHAR(50),
    major VARCHAR(50)
);
```

###### Insert rows

```sql
INSERT INTO students VALUES
(1, 'Alice', 'CS'),
(2, 'Bob', 'Math'),
(3, 'Carol', 'Physics');
```

###### Query rows

```sql
SELECT * FROM students;
```

---

##### Oracle Test Snippet (PL/SQL Environment)

After connecting:

```bash
docker exec -it lab-oracle sqlplus
```

Login using your credentials. (user: `system`)

###### Show current user

```sql
SELECT USER FROM dual;
```

###### Create table

```sql
CREATE TABLE students (
    id NUMBER PRIMARY KEY,
    name VARCHAR2(50),
    major VARCHAR2(50)
);
```

###### Insert rows

```sql
INSERT INTO students VALUES (1, 'Alice', 'CS');
INSERT INTO students VALUES (2, 'Bob', 'Math');
INSERT INTO students VALUES (3, 'Carol', 'Physics');

COMMIT;
```

###### Query rows

```sql
SELECT * FROM students;
```

---

###### Small Syntax Differences to Highlight in Class

| Feature        | MySQL             | PostgreSQL           | Oracle                |
| -------------- | ----------------- | -------------------- | --------------------- |
| Show DBs       | `SHOW DATABASES;` | `\l`                 | Not same concept      |
| Select DB      | `USE db;`         | Connect with `-d db` | Use schemas           |
| String type    | `VARCHAR`         | `VARCHAR`            | `VARCHAR2`            |
| Commit needed? | Auto-commit       | Auto-commit          | Often manual `COMMIT` |

---

# 6. Shell Inside Container

| Purpose                           | Command                             |
| --------------------------------- | ----------------------------------- |
| Open bash in MySQL container      | `docker exec -it lab-mysql bash`    |
| Open bash in PostgreSQL container | `docker exec -it lab-postgres bash` |
| Open bash in Oracle container     | `docker exec -it lab-oracle bash`   |

---

## 7. Remove Volumes

| Action                 | Command                          |
| ---------------------- | -------------------------------- |
| Remove specific volume | `docker volume rm <volume_name>` |
| Remove unused volumes  | `docker volume prune`            |
| Full lab reset         | `docker compose down -v`         |

---

## 8. Database Storage Locations

| Database   | Internal Path              | Example Files                |
| ---------- | -------------------------- | ---------------------------- |
| MySQL      | `/var/lib/mysql`           | `ibdata1`, `.ibd`, redo logs |
| PostgreSQL | `/var/lib/postgresql/data` | `base/`, `pg_wal/`           |
| Oracle     | `/opt/oracle/oradata`      | Datafiles, redo logs         |

---

## 9. Data Deletion Summary

| Action             | Named Volume | Bind Mount   |
| ------------------ | ------------ | ------------ |
| Stop container     | Data stays   | Data stays   |
| Remove container   | Data stays   | Data stays   |
| `down -v`          | Data deleted | Data stays   |
| Delete host folder | No effect    | Data deleted |

---

## 10. Core Commands (Most Used)

| Purpose        | Command                                           |
| -------------- | ------------------------------------------------- |
| Start lab      | `docker compose up -d`                            |
| Stop lab       | `docker compose down`                             |
| Full reset     | `docker compose down -v`                          |
| List volumes   | `docker volume ls`                                |
| Inspect volume | `docker volume inspect <name>`                    |
| Debug volume   | `docker run --rm -it -v <name>:/data ubuntu bash` |

