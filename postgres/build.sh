#! /bin/sh
set -e

SCRIPTS_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" >/dev/null 2>&1 && pwd)
DATA_DIR="$SCRIPTS_DIR/data"
PYTHON_SCRIPTS_DIR="$(dirname $SCRIPTS_DIR)/scripts"

function create_ingestible_data() {
  echo "Creating the data for Postgres ingestion"
  python3 "$PYTHON_SCRIPTS_DIR/postgres.py"
}

# Updating the sample data with the index (and other) information to support ingestion into Postgres
create_ingestible_data
