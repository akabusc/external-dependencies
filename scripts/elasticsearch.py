import os
from service.data_ingestion import DataIngestion


#  Function appends the index information for Elasticsearch to ingest successfully
def update_line(line):
    index_prefix = '{"index": {}}'
    return f'{index_prefix}\n{line}'


# Function determines the new file name for ingestion, which may differ from source to source
def get_new_file_name(file_name):
    filename_without_extension = os.path.splitext(file_name)[0]
    return f'{filename_without_extension}{DataIngestion.keyword}.json'


if __name__ == "__main__":
    # Processing the data updates needed for ingestion
    DataIngestion().process_update(
        update_line_func=update_line,
        get_new_file_name_func=get_new_file_name
    )
