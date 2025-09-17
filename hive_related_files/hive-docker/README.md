# Running Hive using Docker

This is a **ready-to-run Docker Compose** that spins up a single-node Hadoop (HDFS + YARN), a **PostgreSQL** metastore, the **Hive Metastore** service, and **HiveServer2**. It mounts a minimal `hive-site.xml` so you don’t have to guess env vars.

### 1) Files

Create this structure:

```
hive-docker/
├─ docker-compose.yml
└─ conf/
   └─ hive-site.xml
```

**docker-compose.yml**

```yaml
version: "3.8"

networks:
  bigdata:
    driver: bridge

services:
  # Postgres for Hive Metastore
  postgres:
    image: postgres:14
    container_name: postgres
    environment:
      POSTGRES_DB: hive
      POSTGRES_USER: hive
      POSTGRES_PASSWORD: hive
    ports:
      - "5432:5432"
    networks: [bigdata]
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U hive -d hive"]
      interval: 5s
      timeout: 5s
      retries: 20

  # Hadoop (single node)
  namenode:
    image: bde2020/hadoop-namenode:2.0.0-hadoop3.2.1-java8
    container_name: namenode
    environment:
      - CLUSTER_NAME=hadoop
    ports:
      - "9870:9870"  # NN UI
      - "8020:8020"  # RPC
    volumes:
      - namenode:/hadoop/dfs/name
    networks: [bigdata]
    healthcheck:
      test: ["CMD-SHELL", "curl -fsS http://localhost:9870 || exit 1"]
      interval: 5s
      timeout: 5s
      retries: 50

  datanode:
    image: bde2020/hadoop-datanode:2.0.0-hadoop3.2.1-java8
    container_name: datanode
    environment:
      - CORE_CONF_fs_defaultFS=hdfs://namenode:8020
      - SERVICE_PRECONDITION=namenode:9870
    ports:
      - "9864:9864" # DN UI
    volumes:
      - datanode:/hadoop/dfs/data
    networks: [bigdata]
    depends_on: [namenode]

  resourcemanager:
    image: bde2020/hadoop-resourcemanager:2.0.0-hadoop3.2.1-java8
    container_name: resourcemanager
    environment:
      - CORE_CONF_fs_defaultFS=hdfs://namenode:8020
      - YARN_CONF_yarn_resourcemanager_hostname=resourcemanager
      - SERVICE_PRECONDITION=namenode:9870 datanode:9864
    ports:
      - "8088:8088"  # YARN UI
    networks: [bigdata]
    depends_on: [namenode, datanode]

  nodemanager:
    image: bde2020/hadoop-nodemanager:2.0.0-hadoop3.2.1-java8
    container_name: nodemanager
    environment:
      - CORE_CONF_fs_defaultFS=hdfs://namenode:8020
      - YARN_CONF_yarn_resourcemanager_hostname=resourcemanager
      - SERVICE_PRECONDITION=namenode:9870 datanode:9864 resourcemanager:8088
    networks: [bigdata]
    depends_on: [resourcemanager]

  # Hive Metastore service (thrift on 9083)
  hive-metastore:
    image: bde2020/hive:3.1.3
    container_name: hive-metastore
    command: ["bash", "-lc", "schematool -dbType postgres -initSchema --userName hive --passWord hive --url jdbc:postgresql://postgres:5432/hive || true && hive --service metastore"]
    environment:
      - HIVE_HOME=/opt/hive
      - HADOOP_HOME=/opt/hadoop
      - HADOOP_CONF_DIR=/opt/hadoop/etc/hadoop
      - JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64
      - SERVICE_PRECONDITION=namenode:9870 datanode:9864 resourcemanager:8088 postgres:5432
      - HIVE_CONF_DIR=/opt/hive/conf
    volumes:
      - ./conf/hive-site.xml:/opt/hive/conf/hive-site.xml:ro
    ports:
      - "9083:9083"
    networks: [bigdata]
    depends_on:
      postgres:
        condition: service_healthy
      resourcemanager:
        condition: service_started

  # HiveServer2 (JDBC on 10000)
  hive-server:
    image: bde2020/hive:3.1.3
    container_name: hive-server
    command: ["bash", "-lc", "hive --service hiveserver2"]
    environment:
      - HIVE_HOME=/opt/hive
      - HADOOP_HOME=/opt/hadoop
      - HADOOP_CONF_DIR=/opt/hadoop/etc/hadoop
      - JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64
      - HIVE_CONF_DIR=/opt/hive/conf
      - SERVICE_PRECONDITION=hive-metastore:9083
    volumes:
      - ./conf/hive-site.xml:/opt/hive/conf/hive-site.xml:ro
    ports:
      - "10000:10000"
    networks: [bigdata]
    depends_on: [hive-metastore]

volumes:
  namenode:
  datanode:
```

**conf/hive-site.xml**

```xml
<?xml version="1.0"?>
<configuration>
  <!-- Tell Hive/HS2 where the metastore thrift service is -->
  <property>
    <name>hive.metastore.uris</name>
    <value>thrift://hive-metastore:9083</value>
  </property>

  <!-- HDFS defaults so Hive can find HDFS -->
  <property>
    <name>fs.defaultFS</name>
    <value>hdfs://namenode:8020</value>
  </property>

  <property>
    <name>hive.metastore.warehouse.dir</name>
    <value>/user/hive/warehouse</value>
  </property>

  <!-- HS2 server binding -->
  <property>
    <name>hive.server2.thrift.bind.host</name>
    <value>0.0.0.0</value>
  </property>
  <property>
    <name>hive.server2.thrift.port</name>
    <value>10000</value>
  </property>

  <!-- Relax schema checks on first boot -->
  <property>
    <name>hive.metastore.schema.verification</name>
    <value>false</value>
  </property>
</configuration>
```

### 2) Start it

From the `hive-docker/` folder:

```bash
docker compose up -d
# Wait ~30–60s, then:
docker compose ps
```

Create warehouse dir (first run):

```bash
docker compose exec namenode hdfs dfs -mkdir -p /user/hive/warehouse
docker compose exec namenode hdfs dfs -chmod 1777 /user/hive/warehouse
```

Verify ports:

```bash
# On host
curl -s http://localhost:8088 >/dev/null && echo "YARN OK"
nc -z localhost 9083 && echo "Metastore OK"
nc -z localhost 10000 && echo "HS2 OK"
```

### 3) Connect with Beeline (from your host)

```bash
beeline -u jdbc:hive2://localhost:10000 -n $(whoami)
# or from inside the HS2 container:
docker compose exec hive-server beeline -u jdbc:hive2://localhost:10000 -n hive
```

Quick test:

```sql
SHOW DATABASES;
CREATE DATABASE demo;
USE demo;
CREATE TABLE t(id INT, name STRING);
SHOW TABLES;
```

### 4) Stop / clean

```bash
docker compose down
# or to remove volumes too:
docker compose down -v
```

---

### Notes & tips

* If port **10000** isn’t listening, check HS2 logs:

  ```
  docker compose logs --tail=200 hive-server
  ```

  and metastore:

  ```
  docker compose logs --tail=200 hive-metastore
  ```
* If you see **Guava/Slf4j** warnings, they’re usually harmless.
* Want MySQL instead of Postgres? Swap the `postgres` service for `mysql:8`, change the JDBC URL in the `schematool` command, and ensure the MySQL driver jar is available (most Hive images include it; if not, mount it under `/opt/hive/lib`).

If you prefer, I can also give you a **single-node “all-in-one”** container (Hadoop + Hive + Derby) for very quick demos, but the Compose above is closer to a real deployment and avoids Derby lock issues.
