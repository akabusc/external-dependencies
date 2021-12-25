SCRIPTS_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" >/dev/null 2>&1 && pwd)

PUSH_SHIFT_DATA_DIR="$SCRIPTS_DIR/data"
PYTHON_SCRIPTS_DIR="$SCRIPTS_DIR/scripts"

ELASTICSEARCH_DIR="$SCRIPTS_DIR/elasticsearch"
ELASTICSEARCH_DATA_DIR="$ELASTICSEARCH_DIR/data"

POSTGRES_DIR="$SCRIPTS_DIR/postgres"
POSTGRES_DATA_DIR="$POSTGRES_DIR/data"

function remove_outdated_files() {
  echo "Removing outdated data from: $1"
  rm -vrf $1
  echo
}

function copying_push_shift_data() {
  echo "Copying files from: $PUSH_SHIFT_DATA_DIR"
  cp -vR "$PUSH_SHIFT_DATA_DIR/." "$1/"
  echo
}

function update_elasticsearch_data() {
  pushd $ELASTICSEARCH_DIR >/dev/null
  # Removing any outdated files
  # Note: ensuring that when we start with a clean slate when updating data
  remove_outdated_files $ELASTICSEARCH_DATA_DIR

  # Copying any new files from the parent data directory
  # Note: the data is shared and processed different between sources
  copying_push_shift_data $ELASTICSEARCH_DATA_DIR

  # Creating the new sample data in the format needed for ingestion (including post-processing)
  ./build.sh
  popd >/dev/null
}

function update_postgres_data() {
  pushd $POSTGRES_DIR >/dev/null
  # Removing any outdated files
  # Note: ensuring that when we start with a clean slate when updating data
  remove_outdated_files $POSTGRES_DATA_DIR

  # Copying any new files from the parent data directory
  # TODO: Implement the ingestion logic before uncommenting this line
  # copying_push_shift_data $POSTGRES_DATA_DIR

  # Creating the new sample data in the format needed for ingestion
  ./build.sh
  popd >/dev/null
}

# Updating the elasticsearch data
update_elasticsearch_data

# Updating the postgres data
update_postgres_data