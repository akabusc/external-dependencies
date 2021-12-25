SCRIPTS_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" >/dev/null 2>&1 && pwd)

ELASTICSEARCH_DIR="$SCRIPTS_DIR/elasticsearch"
POSTGRES_DIR="$SCRIPTS_DIR/postgres"

# Postgres Directory and Scripts
POSTGRES_DIR="$SCRIPTS_DIR/postgres"
POSTGRES_SCRIPTS_DIR="$POSTGRES_DIR/scripts"

function update_elasticsearch_data() {
  pushd $ELASTICSEARCH_DIR >/dev/null
  ./build.sh
  popd >/dev/null
}

function update_postgres_data() {
  pushd $POSTGRES_DIR >/dev/null
  ./build.sh
  popd >/dev/null
}

# Updating the elasticsearch data
update_elasticsearch_data

# Updating the postgres data
#update_postgres_data