#!/usr/bin/env bash
# hive_stack_down.sh — Stop HiveServer2, Metastore, YARN, and HDFS (best-effort).
set -euo pipefail

: "${HADOOP_HOME:?HADOOP_HOME not set}"
: "${HIVE_HOME:?HIVE_HOME not set}"

echo "[INFO] Stopping HiveServer2 & Metastore (best effort)"
pkill -f 'org.apache.hive.service.server.HiveServer2' || true
pkill -f 'org.apache.hadoop.hive.metastore.HiveMetaStore' || true

echo "[INFO] Stopping YARN"
"$HADOOP_HOME/sbin/stop-yarn.sh" || true

echo "[INFO] Stopping HDFS"
"$HADOOP_HOME/sbin/stop-dfs.sh" || true

echo "[INFO] Done."
