import os
import json
import re
from service.data_ingestion import DataIngestion
from service.extension import Extension


#  Function appends the index information for Elasticsearch to ingest successfully
def update_line(ingestion_line_number, line):
    data = json.loads(line)
    author = data['author']
    body = get_body(data, 'body') if 'body' in data else get_body(data, 'selftext')
    insert_id = ingestion_line_number + 1
    return f"insert into data.reddit (id, author, body) values ({insert_id}, '{author}', '{body}');\n"


# Function is used to remove undesirable characters from the body
def get_body(data, field_name):
    return re.sub('[^a-zA-Z0-9 ?!.,]*', '', data[field_name])


# Function is used to ensure the sql connection line for the insert file
def file_prefix_line():
    return f'\connect training\n'


if __name__ == "__main__":
    data_ingestion = DataIngestion(
        target_file_extension=Extension.SQL,
        target_directory=f'{os.getcwd()}/data'
    )

    # Processing the data updates needed for ingestion
    data_ingestion.process_update(
        update_line_func=update_line,
        file_prefix_func=file_prefix_line
    )
