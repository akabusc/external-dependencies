import os
import json
import re
from service.data_ingestion import DataIngestion

# Used to track each individual insert id from 1+
initial_index = 1

# Used to track the number of files needed for insertion from 99-
last_sql_file_num = 99


#  Function appends the index information for Elasticsearch to ingest successfully
def update_line(line):
    global initial_index
    data = json.loads(line)
    author = data['author']
    body = get_body(data, 'body') if 'body' in data else get_body(data, 'selftext')
    insert_id = initial_index
    initial_index += 1
    return f"insert into data.reddit (id, author, body) values ({insert_id}, '{author}', '{body}');\n"


# Function is used to remove undesirable characters from the body
def get_body(data, field_name):
    return re.sub('[^a-zA-Z0-9 ?!.,]*', '', data[field_name])


# Function determines the new file name for ingestion, which may differ from source to source
def get_new_file_name(file_name):
    global last_sql_file_num
    filename_without_extension = os.path.splitext(file_name)[0]
    file_number = last_sql_file_num
    last_sql_file_num -= 1
    return f'{file_number}-{filename_without_extension}{DataIngestion.keyword}.sql'


# Function is used to ensure the sql connection line for the insert file
def file_prefix_line():
    return f'\connect training\n'


if __name__ == "__main__":
    # Processing the data updates needed for ingestion
    DataIngestion().process_update(
        update_line_func=update_line,
        get_new_file_name_func=get_new_file_name,
        file_prefix_line_func=file_prefix_line
    )
