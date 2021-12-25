SCRIPTS_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" >/dev/null 2>&1 && pwd)

# Elasticsearch Directory and Scripts
ELASTICSEARCH_DIR="$SCRIPTS_DIR/elasticsearch"
ELASTICSEARCH_SCRIPTS_DIR="$ELASTICSEARCH_DIR/scripts"

# Postgres Directory and Scripts
POSTGRES_DIR="$SCRIPTS_DIR/postgres"
POSTGRES_SCRIPTS_DIR="$POSTGRES_DIR/scripts"

function update_elasticsearch_data() {
  pushd $ELASTICSEARCH_SCRIPTS_DIR >/dev/null
  sh update_data.sh
  popd >/dev/null
}

function update_postgres_data() {
  pushd $ELASTICSEARCH_SCRIPTS_DIR >/dev/null
  sh update_data.sh
  popd >/dev/null
}

# Updating the elasticsearch data
update_elasticsearch_data

# Updating the postgres data
update_postgres_data