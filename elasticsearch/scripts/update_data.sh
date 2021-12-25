#! /bin/sh
set -e

SCRIPTS_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" >/dev/null 2>&1 && pwd)
DATA_DIR="$(dirname $SCRIPTS_DIR)/data"
PUSH_SHIFT_DATA_DIR="$(dirname $SCRIPTS_DIR)/../data"
PYTHON_SCRIPTS_DIR="$(dirname $SCRIPTS_DIR)/../scripts"

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

function update_data() {
  echo "Updating the data for Elasticsearch ingestion"
  python3 "$PYTHON_SCRIPTS_DIR/elasticsearch.py"
}

function remove_outdated_files() {
  echo "Removing outdated data from: $DATA_DIR"
  rm -vrf $DATA_DIR
  echo
}

function copying_push_shift_data() {
  echo "Copying files from: $PUSH_SHIFT_DATA_DIR"
  cp -vR "$PUSH_SHIFT_DATA_DIR/." "$DATA_DIR/"
  echo
}

# Removing any outdated files (Note: ensuring that when we start with a clean slate when updating data)
remove_outdated_files

# copying any new files from the parent data directory (Note: the data is shared and processed different between sources)
copying_push_shift_data

# Updating the sample data with the index (and other) information to support ingestion into Elasticsearch
update_data

# Converting the JSON file to a GZIP file
toggle_compression
