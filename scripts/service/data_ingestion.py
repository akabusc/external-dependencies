import os


class DataIngestion:

    @staticmethod
    def __get_data_directory():
        return f'{os.getcwd()}/../data'

    def __get_filenames(self):
        for directory_path, _, filenames in os.walk(self.__get_data_directory()):
            for file_name in filenames:
                yield directory_path, file_name

    @staticmethod
    def __get_filepath(directory_path: str, file_name: str):
        return f'{directory_path}/{file_name}'

    @staticmethod
    def __get_prepped_file_name(file_name: str):
        filename_without_extension = os.path.splitext(file_name)[0]
        return f'{filename_without_extension}_updated.json'

    def process_update(self, update_line_func):
        original_files = []
        prepped_files = []

        # Getting all of the data files (tuple: path & filename)
        for path, filename in self.__get_filenames():
            # Capturing the filepath of the original file
            filepath = self.__get_filepath(path, filename)
            original_files.append(filepath)

            # Capturing the filepath of the new file
            new_filename = self.__get_prepped_file_name(filename)
            new_filepath = self.__get_filepath(path, new_filename)
            prepped_files.append(new_filepath)

            # Reading the original file (to leave it untouched)
            with open(filepath, 'r') as file:
                # Writing each line (from the original) to the new file with adjustments/updates
                with open(new_filepath, 'w') as new_file:
                    for line in file:
                        new_file.write(update_line_func(line))

        # Iterating over each "prepped" file to replace the original file
        for prepped in prepped_files:
            original_file_name = prepped.replace('_updated', '')
            print(f'Before: {prepped}\nAfter: {original_file_name}\n')
            if os.path.exists(prepped):
                os.replace(prepped, original_file_name)
