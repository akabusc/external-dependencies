import os
from service.data_ingestion import DataIngestion
from service.extension import Extension


#  Function appends the index information for Elasticsearch to ingest successfully
def update_line(_, line):
    index_prefix = '{"index": {}}'
    return f'{index_prefix}\n{line}'


if __name__ == "__main__":
    data_ingestion = DataIngestion(
        target_file_extension=Extension.JSON,
        target_directory=f'{os.getcwd()}/data'
    )

    # Processing the data updates needed for ingestion
    data_ingestion.process_update(update_line_func=update_line)
