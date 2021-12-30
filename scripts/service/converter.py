import os
import json
from abc import ABC, abstractmethod


class Converter(ABC):
    keyword = '_updated'

    def __init__(self, target_file_extension):
        self.target_file_extension = target_file_extension

    def convert_lines(self, filepath: str, new_filepath: str, ingestion_line_number: int):
        line_number = ingestion_line_number

        # Reading the original file (to leave it untouched)
        with open(filepath, 'r') as file:
            # Writing each line (from the original) to the new file with adjustments/updates
            with open(new_filepath, 'w') as new_file:
                prefix_lines = self.write_prefix_lines()
                if prefix_lines is not None:
                    new_file.write(prefix_lines)

                for line in file:
                    new_file.write(self.get_formatted_line(line_number, line))
                    line_number += 1

        return line_number

    def get_new_file_name(self, file_name: str):
        filename_without_extension: str = os.path.splitext(file_name)[0]
        return f'{filename_without_extension}{Converter.keyword}.{self.target_file_extension}'

    @abstractmethod
    def write_prefix_lines(self) -> str:
        pass

    @abstractmethod
    def get_formatted_line(self, ingestion_line_number: int, line: str) -> str:
        pass


class ElasticsearchConverter(Converter):

    def __init__(self):
        super().__init__('json')

    def write_prefix_lines(self) -> str:
        pass

    def get_formatted_line(self, ingestion_line_number: int, line: str) -> str:
        return (
            '{"index": {}}'
            f'\n{line}'
        )


class PostgresConverter(Converter):

    def __init__(self):
        super().__init__('sql')

    def write_prefix_lines(self) -> str:
        return '\connect training\n'

    def get_formatted_line(self, ingestion_line_number: int, line: str) -> str:
        data = json.loads(line)
        insert_id = ingestion_line_number + 1
        return f'{PostgresData(data=data, insert_id=insert_id):}'


class PostgresData:
    __slots__ = ['_data', '_insert_id']

    def __init__(self, data: dict, insert_id: int):
        self._data = data
        self._insert_id = insert_id

    def __format__(self, _):
        body = self.get_string_value('body')
        self_text = self.get_string_value('self_text')
        author = self.get_string_value('author')
        return (
            "insert into data.reddit (id, author, body, selftext)\n"
            f"values ({self._insert_id}, {author}, {body}, {self_text});\n"
        )

    # Function is used to remove undesirable characters from the body
    def get_string_value(self, field_name: str, default_value: str = "null"):
        if field_name not in self._data:
            return default_value

        # Escaping the single-quote character within SQL
        sub: str = self._data[field_name].replace("'", "''")
        if not sub:
            return default_value

        # Wrapping the value in single-quotes for SQL to insert as string
        return f"'{sub}'"


class DataConversion:
    DEFAULT_TARGET_DIRECTORY = f'{os.getcwd()}/data'

    def __init__(self, target_directory: str = DEFAULT_TARGET_DIRECTORY):
        self.target_directory: str = target_directory
        pass

    def __get_filenames(self):
        for directory_path, _, filenames in os.walk(self.target_directory):
            for file_name in filenames:
                yield directory_path, file_name

    def __get_filepath(self, file_name: str):
        return f'{self.target_directory}/{file_name}'

    def process_update(self, converter):
        new_file_locations: list = []

        ingestion_line_number: int = 0
        # Getting all of the data files (tuple: path & filename)
        for path, filename in self.__get_filenames():
            # Capturing the filepath of the original file
            filepath: str = self.__get_filepath(filename)

            # Capturing the filepath of the new file
            new_filename: str = converter.get_new_file_name(filename)
            new_filepath: str = self.__get_filepath(new_filename)
            new_file_locations.append(new_filepath)

            ingestion_line_number += converter.convert_lines(
                filepath=filepath,
                new_filepath=new_filepath,
                ingestion_line_number=ingestion_line_number
            )

        # Iterating over each new file to replace the original file
        for new_file_location in new_file_locations:
            original_file_name: str = new_file_location.replace(Converter.keyword, '')
            print(f'Before: {new_file_location}\nAfter: {original_file_name}\n')
            if os.path.exists(new_file_location):
                os.replace(new_file_location, original_file_name)
