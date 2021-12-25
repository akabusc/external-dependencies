#!/bin/sh

INDEX_PATH=/usr/local/bin/elasticsearch-init/indexes

# Adding Index and Data for reddit comments
REDDIT_COMMENTS_FILE=${INDEX_PATH}/reddit-comments-index.json
curl -v -X PUT "http://localhost:9200/reddit_comments_index" -H "Content-Type: application/json" -d @${REDDIT_COMMENTS_FILE}
gunzip -c /usr/local/bin/elasticsearch-init/data/comments_sample.json.gz | curl -v -X PUT "http://localhost:9200/reddit_comments_index/_bulk?pretty" -H 'Content-Type: application/x-ndjson' --data-binary @-

# Adding Index and Data for reddit submissions
REDDIT_SUBMISSIONS_FILE=${INDEX_PATH}/reddit-submissions-index.json
curl -v -X PUT "http://localhost:9200/reddit_submissions_index" -H "Content-Type: application/json" -d @${REDDIT_SUBMISSIONS_FILE}
gunzip -c /usr/local/bin/elasticsearch-init/data/submissions_sample.json.gz | curl -v -X PUT "http://localhost:9200/reddit_submissions_index/_bulk?pretty" -H 'Content-Type: application/x-ndjson' --data-binary @-

