import os


class DataIngestion:
    keyword = '_updated'

    @staticmethod
    def __get_data_directory():
        return f'{os.getcwd()}/data'

    def __get_filenames(self):
        directory = self.__get_data_directory()
        for directory_path, _, filenames in os.walk(directory):
            for file_name in filenames:
                yield directory_path, file_name

    @staticmethod
    def __get_filepath(directory_path: str, file_name: str):
        return f'{directory_path}/{file_name}'

    def process_update(self, update_line_func, get_new_file_name_func):
        new_file_locations = []

        # Getting all of the data files (tuple: path & filename)
        for path, filename in self.__get_filenames():
            # Capturing the filepath of the original file
            filepath = self.__get_filepath(path, filename)

            # Capturing the filepath of the new file
            new_filename = get_new_file_name_func(filename)
            new_filepath = self.__get_filepath(path, new_filename)
            new_file_locations.append(new_filepath)

            # Reading the original file (to leave it untouched)
            with open(filepath, 'r') as file:
                # Writing each line (from the original) to the new file with adjustments/updates
                with open(new_filepath, 'w') as new_file:
                    for line in file:
                        new_file.write(update_line_func(line))

        # Iterating over each new file to replace the original file
        for new_file_location in new_file_locations:
            original_file_name = new_file_location.replace(DataIngestion.keyword, '')
            print(f'Before: {new_file_location}\nAfter: {original_file_name}\n')
            if os.path.exists(new_file_location):
                os.replace(new_file_location, original_file_name)
