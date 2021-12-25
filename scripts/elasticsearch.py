from service.data_ingestion import DataIngestion


#  Function appends the index information for Elasticsearch to ingest successfully
def update_line(line):
    index_prefix = '{"index": {}}'
    return f'{index_prefix}\n{line}'


if __name__ == "__main__":
    # Processing the data updates needed for ingestion
    DataIngestion().process_update(update_line)
