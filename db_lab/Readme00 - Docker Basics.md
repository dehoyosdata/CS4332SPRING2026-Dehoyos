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

When you are in bash, lets see few things.
```bash
# identify the operating system and distribution details
cat /etc/os-release
```
On my end I see something like this:
```text
NAME="Oracle Linux Server"
VERSION="9.7"
ID="ol"
ID_LIKE="fedora"
VARIANT="Server"
VARIANT_ID="server"
VERSION_ID="9.7"
PLATFORM_ID="platform:el9"
PRETTY_NAME="Oracle Linux Server 9.7"
ANSI_COLOR="0;31"
CPE_NAME="cpe:/o:oracle:linux:9:7:server"
HOME_URL="https://linux.oracle.com/"
BUG_REPORT_URL="https://github.com/oracle/oracle-linux"

ORACLE_BUGZILLA_PRODUCT="Oracle Linux 9"
ORACLE_BUGZILLA_PRODUCT_VERSION=9.7
ORACLE_SUPPORT_PRODUCT="Oracle Linux"
ORACLE_SUPPORT_PRODUCT_VERSION=9.7
```

Check what package manager is available
```bash
command -v microdnf || echo "no microdnf"
command -v yum      || echo "no yum"
command -v rpm      || echo "no rpm"
command -v apt-get  || echo "no apt-get"
command -v apk      || echo "no apk"
```

In my case:
```text
/usr/bin/microdnf
no yum
/usr/bin/rpm
no apt-get
no apk
```

Looks like I can use microdnf, I can use it to install packages, lets install VIM (assuming you are in root, otherwise requires `sudo`)
```bash
microdnf install -y vim-minimal
```

Also its a good idea to export this as our default editor
```bash
export EDITOR=vim
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