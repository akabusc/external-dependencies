#!/bin/sh

INDEX_PATH=/usr/local/bin/elasticsearch-init/indexes

REDDIT_COMMENTS_FILE=${INDEX_PATH}/reddit-comments-index.json
REDDIT_SUBMISSIONS_FILE=${INDEX_PATH}/reddit-submissions-index.json

# Add analyzer template
printf "\nAnalyzer Template update started\n"
curl -v -X PUT "http://localhost:9200/_template/analyzer_template" -H "Content-Type: application/json" -d @${ANALYZER_FILE}
printf "\nAnalyzer Template update completed\n"

# Index / mappings
printf "\nIndex Mappings update started\n"
curl -v -X PUT "http://localhost:9200/reddit_comments_index" -H "Content-Type: application/json" -d @${REDDIT_COMMENTS_FILE}
curl -v -X PUT "http://localhost:9200/reddit_submissions_index" -H "Content-Type: application/json" -d @${REDDIT_SUBMISSIONS_FILE}
printf "\nIndex Mappings update completed\n"

# Data
printf "\nData upload update started\n"
gunzip -c /usr/local/bin/elasticsearch-init/data/submissions_sample.json.gz | curl -v -X PUT "http://localhost:9200/reddit_submissions_index/_bulk?pretty" -H 'Content-Type: application/x-ndjson' --data-binary @-
gunzip -c /usr/local/bin/elasticsearch-init/data/comments_sample.json.gz | curl -v -X PUT "http://localhost:9200/reddit_comments_index/_bulk?pretty" -H 'Content-Type: application/x-ndjson' --data-binary @-
printf "\nData upload update completed\n"

printf "\nPre-Hook script completed\n"