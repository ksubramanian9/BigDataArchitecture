# Hive using Docker Compose

### Bring it up cleanly

```bash
docker compose down -v
docker compose up -d

# first run only: create Hive warehouse in HDFS
docker compose exec namenode hdfs dfs -mkdir -p /user/hive/warehouse
docker compose exec namenode hdfs dfs -chmod 1777 /user/hive/warehouse
```

### Use Beeline **inside** the container

```bash
docker compose exec hive-server bash
beeline -u jdbc:hive2://localhost:10000 -n hive
-- then run HQL:
SHOW DATABASES;
CREATE DATABASE demo;
USE demo;
CREATE TABLE t(id INT, name STRING);
SHOW TABLES;
```

---

## Why this works

* The Derby DB lives on a **named volume** mounted at `/opt/hive/data`.
* Your error came from the container **not having write permission** to that path.
* Running the Hive containers as **root** (or pre-chowning the path) ensures the Derby files can be created.

If you prefer to avoid running as root, we can keep non-root and add an init step to `chown` the volume to the container’s `hive` user (need that UID/GID). Happy to give that variant too.
