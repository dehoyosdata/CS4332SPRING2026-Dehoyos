
# MySQL `.ibd` Growth Demo - Full Commands

Assumptions:

* Container name: `lab-mysql`
* Database: `labdb`
* `innodb_file_per_table = ON`

---

# Option A - SQL Side (Insert Data)

## Connect to MySQL

| Goal                        | Command                                         |
| --------------------------- | ----------------------------------------------- |
| Connect as lab user         | `docker exec -it lab-mysql mysql -u labuser -p` |
| Connect as root (if needed) | `docker exec -it lab-mysql mysql -u root -p`    |

---

## Inside MySQL

| Step                 | Command                                                                                                         |
| -------------------- | --------------------------------------------------------------------------------------------------------------- |
| Check file-per-table | `SHOW VARIABLES LIKE 'innodb_file_per_table';`                                                                  |
| Select database      | `USE labdb;`                                                                                                    |
| Start fresh          | `DROP TABLE IF EXISTS big_table;`                                                                               |
| Create table         | `CREATE TABLE big_table (id INT PRIMARY KEY AUTO_INCREMENT, data TEXT);`                        |
| Insert large data    | `INSERT INTO big_table (data) SELECT REPEAT('A', 20000) FROM information_schema.columns LIMIT 20000;` |
| Verify rows          | `SELECT COUNT(*) FROM big_table;`                                                                               |

---

# Option B - Filesystem Side (Watch `.ibd` File)

You can either open an interactive shell or run one-liners.

---

## Method 1 - Interactive Shell (Recommended)

### Open container shell

```bash
docker exec -it lab-mysql bash
```

### Navigate to database folder

```bash
cd /var/lib/mysql/labdb
```

### Check file size

```bash
ls -lh big_table.ibd
```

### Check exact size in bytes

```bash
stat -c%s big_table.ibd
```

---

## Method 2 - One-Liner Commands (No Shell)

| Goal             | Command                                                                            |
| ---------------- | ---------------------------------------------------------------------------------- |
| List DB folder   | `docker exec -it lab-mysql bash -c "ls -lh /var/lib/mysql/labdb"`                  |
| Show `.ibd` size | `docker exec -it lab-mysql bash -c "ls -lh /var/lib/mysql/labdb/big_table.ibd"`    |
| Show exact bytes | `docker exec -it lab-mysql bash -c "stat -c%s /var/lib/mysql/labdb/big_table.ibd"` |

---

# Optional - Access MySQL From Inside Container (Alternative Way)

Instead of `docker exec mysql ...`, you can:

```bash
docker exec -it lab-mysql bash
```

Then inside container:

```bash
mysql -u labuser -p
```

This works the same way.

---

# What You Should Observe

| Action         | File Behavior       |
| -------------- | ------------------- |
| Create table   | `.ibd` file created |
| Insert data    | `.ibd` file grows   |
| Delete rows    | File size unchanged |
| Optimize table | File may shrink     |

---

**InnoDB** is MySQL’s default storage engine - it handles transactions, row-level locking, and crash recovery. It stores data in fixed-size pages.

An **`.ibd` file** (InnoDB Data file) is the physical file that stores a table’s data and indexes when `innodb_file_per_table = ON`.

What we saw:

* Creating a table created a `.ibd` file.
* Inserting data made the file grow.
* Deleting rows did not shrink it.
* `OPTIMIZE TABLE big_table` can reclaim space

Logical changes → physical page allocation on disk.
