import os
from typing import Callable
from .extension import Extension


class DataIngestion:
    keyword = '_updated'

    def __init__(self, target_directory: str, target_file_extension: Extension):
        self.target_directory: str = target_directory
        self.target_file_extension: Extension = target_file_extension
        pass

    def __get_new_file_name(self, file_name: str):
        filename_without_extension: str = os.path.splitext(file_name)[0]
        return f'{filename_without_extension}{DataIngestion.keyword}.{self.target_file_extension.value}'

    def __get_filenames(self):
        for directory_path, _, filenames in os.walk(self.target_directory):
            for file_name in filenames:
                yield directory_path, file_name

    def __get_filepath(self, file_name: str):
        return f'{self.target_directory}/{file_name}'

    def process_update(self,
                       update_line_func: Callable[[int, str], str],
                       file_prefix_func: Callable[[], str] = None):
        new_file_locations: list = []

        ingestion_line_number: int = 0
        # Getting all of the data files (tuple: path & filename)
        for path, filename in self.__get_filenames():

            # Capturing the filepath of the original file
            filepath: str = self.__get_filepath(filename)

            # Capturing the filepath of the new file
            new_filename: str = self.__get_new_file_name(filename)
            new_filepath: str = self.__get_filepath(new_filename)
            new_file_locations.append(new_filepath)

            # Reading the original file (to leave it untouched)
            with open(filepath, 'r') as file:
                # Writing each line (from the original) to the new file with adjustments/updates
                with open(new_filepath, 'w') as new_file:
                    if file_prefix_func is not None:
                        new_file.write(file_prefix_func())

                    for line in file:
                        new_file.write(update_line_func(ingestion_line_number, line))
                        ingestion_line_number += 1

        # Iterating over each new file to replace the original file
        for new_file_location in new_file_locations:
            original_file_name: str = new_file_location.replace(DataIngestion.keyword, '')
            print(f'Before: {new_file_location}\nAfter: {original_file_name}\n')
            if os.path.exists(new_file_location):
                os.replace(new_file_location, original_file_name)
