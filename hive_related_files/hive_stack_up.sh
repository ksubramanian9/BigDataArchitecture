#!/usr/bin/env bash
# hive_stack_up.sh — Start Hadoop (HDFS+YARN), Hive Metastore, and HiveServer2 in order.
# Usage:
#   ./hive_stack_up.sh                # start services
#   ./hive_stack_up.sh --connect      # start services and open Beeline
#   HIVE_DBTYPE=mysql ./hive_stack_up.sh   # if you use MySQL/Postgres metastore (set DB type)
#
# Requirements: JAVA_HOME, HADOOP_HOME, HIVE_HOME set; Hadoop configured & working.

set -euo pipefail

# ---------- Config (override via env) ----------
: "${JAVA_HOME:?JAVA_HOME not set}"
: "${HADOOP_HOME:?HADOOP_HOME not set}"
: "${HIVE_HOME:?HIVE_HOME not set}"

HDFS_WAREHOUSE_DIR="${HDFS_WAREHOUSE_DIR:-/user/hive/warehouse}"
HS2_HOST="${HS2_HOST:-localhost}"
HS2_PORT="${HS2_PORT:-10000}"
METASTORE_PORT="${METASTORE_PORT:-9083}"

# Derby for single-user quickstart; use 'mysql' or 'postgres' when you’ve configured hive-site.xml accordingly
HIVE_DBTYPE="${HIVE_DBTYPE:-derby}"

# How long to wait (seconds) for each service to become healthy
WAIT_SECS="${WAIT_SECS:-30}"

# ---------- Helpers ----------
log() { echo -e "[\e[1;34mINFO\e[0m] $*"; }
warn() { echo -e "[\e[1;33mWARN\e[0m] $*" >&2; }
err() { echo -e "[\e[1;31mERROR\e[0m] $*" >&2; }

is_listening() {
  local port="$1"
  if command -v ss >/dev/null 2>&1; then
    ss -ltn | awk '{print $4}' | grep -q ":${port}$"
  else
    netstat -tulnp 2>/dev/null | grep -q ":${port} "
  fi
}

wait_for_port() {
  local name="$1" port="$2" secs="$3"
  for i in $(seq 1 "$secs"); do
    if is_listening "$port"; then
      log "$name is listening on port $port"
      return 0
    fi
    sleep 1
  done
  return 1
}

ensure_hive_site() {
  if [ ! -f "$HIVE_HOME/conf/hive-site.xml" ]; then
    log "Creating $HIVE_HOME/conf/hive-site.xml from template"
    cp "$HIVE_HOME/conf/hive-default.xml.template" "$HIVE_HOME/conf/hive-site.xml"
  fi
}

init_metastore_if_needed() {
  log "Validating Hive metastore schema ($HIVE_DBTYPE)"
  if ! "$HIVE_HOME/bin/schematool" -dbType "$HIVE_DBTYPE" -validate >/dev/null 2>&1; then
    log "Initializing Hive metastore schema ($HIVE_DBTYPE)"
    "$HIVE_HOME/bin/schematool" -dbType "$HIVE_DBTYPE" -initSchema
  else
    log "Metastore schema already initialized"
  fi
}

ensure_warehouse_dir() {
  log "Ensuring HDFS warehouse dir: $HDFS_WAREHOUSE_DIR"
  "$HADOOP_HOME/bin/hdfs" dfs -mkdir -p "$HDFS_WAREHOUSE_DIR" || true
  "$HADOOP_HOME/bin/hdfs" dfs -chmod 1777 "$HDFS_WAREHOUSE_DIR" || true
}

start_hadoop() {
  log "Starting HDFS"
  "$HADOOP_HOME/sbin/start-dfs.sh"
  log "Starting YARN"
  "$HADOOP_HOME/sbin/start-yarn.sh"
  log "Hadoop services started"
}

start_metastore() {
  # If using embedded Derby, make sure only the metastore/HS2 access it (don’t run legacy 'hive' CLI concurrently).
  log "Starting Hive Metastore on port $METASTORE_PORT"
  nohup "$HIVE_HOME/bin/hive" --service metastore > "$HIVE_HOME/logs/metastore.out" 2>&1 &
  if ! wait_for_port "Metastore" "$METASTORE_PORT" "$WAIT_SECS"; then
    err "Metastore did not become ready on :$METASTORE_PORT. Check $HIVE_HOME/logs/metastore.out"
    exit 1
  fi
}

start_hiveserver2() {
  log "Starting HiveServer2 on $HS2_HOST:$HS2_PORT"
  nohup "$HIVE_HOME/bin/hive" --service hiveserver2 --hiveconf hive.server2.thrift.bind.host="$HS2_HOST" --hiveconf hive.server2.thrift.port="$HS2_PORT" > "$HIVE_HOME/logs/hiveserver2.out" 2>&1 &
  if ! wait_for_port "HiveServer2" "$HS2_PORT" "$WAIT_SECS"; then
    err "HiveServer2 did not become ready on :$HS2_PORT. Check $HIVE_HOME/logs/hiveserver2.out"
    exit 1
  fi
}

open_beeline() {
  log "Opening Beeline (press Ctrl+C to exit Beeline only)"
  "$HIVE_HOME/bin/beeline" -u "jdbc:hive2://${HS2_HOST}:${HS2_PORT}" -n "$(whoami)"
}

# ---------- Main ----------
log "JAVA_HOME=$JAVA_HOME"
log "HADOOP_HOME=$HADOOP_HOME"
log "HIVE_HOME=$HIVE_HOME"
mkdir -p "$HIVE_HOME/logs"

ensure_hive_site
start_hadoop
ensure_warehouse_dir
init_metastore_if_needed
start_metastore
start_hiveserver2

log "All services up ✅"
log "Try:  $HIVE_HOME/bin/beeline -u jdbc:hive2://${HS2_HOST}:${HS2_PORT} -n $(whoami)"

if [[ "${1:-}" == "--connect" ]]; then
  open_beeline
fi
