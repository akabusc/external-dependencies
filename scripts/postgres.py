import os
import json
from service.data_ingestion import DataIngestion
from service.extension import Extension


#  Function appends the index information for Elasticsearch to ingest successfully
def update_line(ingestion_line_number, line):
    data = json.loads(line)
    author = data['author']

    body = get_string_value(data, 'body')
    self_text = get_string_value(data, 'selftext')

    insert_id = ingestion_line_number + 1
    return (
        "insert into data.reddit (id, author, body, selftext)\n"
        f"values ({insert_id}, '{author}', {body}, {self_text});\n"
    )


# Function is used to remove undesirable characters from the body
def get_string_value(data, field_name, default_value="null"):
    if field_name not in data:
        return default_value

    # Escaping the single-quote character within SQL
    sub = data[field_name].replace("'", "''")
    if not sub:
        return default_value

    # Wrapping the value in single-quotes for SQL to insert as string
    return f"'{sub}'"


if __name__ == "__main__":
    data_ingestion = DataIngestion(
        target_file_extension=Extension.SQL,
        target_directory=f'{os.getcwd()}/data'
    )

    # Processing the data updates needed for ingestion
    data_ingestion.process_update(
        update_line_func=update_line,
        file_prefix_func=lambda: '\connect training\n'
    )
