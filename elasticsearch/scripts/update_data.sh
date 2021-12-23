#! /bin/sh
set -e

SCRIPTS_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" >/dev/null 2>&1 && pwd)
DATA_DIR="$(dirname $SCRIPTS_DIR)/data"

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

# TODO Update the following to call the python script to also update the data within needed index info and re-toggle
toggle_compression