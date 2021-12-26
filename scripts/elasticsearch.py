import os
from service.data_ingestion import DataIngestion
from service.extension import Extension

if __name__ == "__main__":
    data_ingestion = DataIngestion(
        target_file_extension=Extension.JSON,
        target_directory=f'{os.getcwd()}/data'
    )

    # Processing the data updates needed for ingestion
    data_ingestion.process_update(update_line_func=lambda _, line: (
        '{"index": {}}'
        f'\n{line}'
    ))
