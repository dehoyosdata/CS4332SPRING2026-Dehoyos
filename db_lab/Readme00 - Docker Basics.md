# Docker Cheatsheet (DB Lab)

## Start / Stop

Start all services:

```bash
docker compose up -d
```

Stop services (keep data):

```bash
docker compose down
```

Stop and delete data:

```bash
docker compose down -v
```

---

## View Containers

Running containers:

```bash
docker ps
```

All containers:

```bash
docker ps -a
```

---

## Logs

All logs:

```bash
docker compose logs
```

Specific service:

```bash
docker compose logs mysql
docker compose logs postgres
docker compose logs oracle
```

---

## Connect to Databases

MySQL:

```bash
docker exec -it lab-mysql mysql -u labuser -p
```

PostgreSQL:

```bash
docker exec -it lab-postgres psql -U labuser -d labdb
```

Oracle:

```bash
docker exec -it lab-oracle sqlplus
```

---

## Shell Inside Container

```bash
docker exec -it lab-mysql bash
```

---

## Volumes

List volumes:

```bash
docker volume ls
```

Remove volume:

```bash
docker volume rm <volume_name>
```

---

# 🔹 Core Commands You’ll Use Most

```bash
docker compose up -d
docker compose down
docker compose down -v
docker ps
docker compose logs mysql
docker exec -it lab-mysql mysql -u labuser -p
```