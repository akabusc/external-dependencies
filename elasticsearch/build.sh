#! /bin/sh
set -e

SCRIPTS_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" >/dev/null 2>&1 && pwd)
DATA_DIR="$SCRIPTS_DIR/data"
PYTHON_SCRIPTS_DIR="$(dirname $SCRIPTS_DIR)/scripts"

function toggle_compression() {
  pushd $DATA_DIR >/dev/null
  for FILE in *; do
    FILENAME="${FILE%%.*}"
    if [ -f "$FILENAME.json" ]; then
      echo "Compressing $FILENAME.json"
      gzip "$FILENAME.json"
    elif [ -f "$FILENAME.json.gz" ]; then
      echo "Decompressing $FILENAME.json.gz"
      gunzip "$FILENAME.json.gz"
    fi
  done
  popd >/dev/null
}

function create_ingestible_data() {
  echo "Creating the data for Elasticsearch ingestion"
  python3 "$PYTHON_SCRIPTS_DIR/elasticsearch.py"
}

# Updating the sample data with the index (and other) information to support ingestion into Elasticsearch
create_ingestible_data

# Converting the JSON file to a GZIP file
toggle_compression
