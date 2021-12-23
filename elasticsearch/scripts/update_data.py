import os


def get_data_directory():
    return f'{os.getcwd()}/../data'


def get_filenames():
    for directory_path, _, filenames in os.walk(get_data_directory()):
        for file_name in filenames:
            yield (directory_path, file_name)


def get_filepath(directory_path: str, file_name: str):
    return f'{directory_path}/{file_name}'


def get_prepped_file_name(file_name: str):
    filename_without_extension = os.path.splitext(file_name)[0]
    return f'{filename_without_extension}_updated.json'


original_files = []
prepped_files = []

# Getting all of the data files (tuple: path & filename)
for path, filename in get_filenames():
    # Capturing the filepath of the original file
    filepath = get_filepath(path, filename)
    original_files.append(filepath)

    # Capturing the filepath of the new file
    new_filename = get_prepped_file_name(filename)
    new_filepath = get_filepath(path, new_filename)
    prepped_files.append(new_filepath)

    # Reading the original file (to leave it untouched)
    with open(filepath, 'r') as file:
        # Writing each line (from the original) to the new file with index information
        with open(new_filepath, 'w') as new_file:
            for line in file:
                index_prefix = '{"index": {}}'
                new_file.write(f'{index_prefix}\n{line}')

    # Iterating over each "prepped" file to replace the original file
    for prepped in prepped_files:
        original_file_name = prepped.replace('_updated', '')
        print(f'Before: {prepped}\nAfter: {original_file_name}\n')
        if os.path.exists(prepped):
            os.replace(prepped, original_file_name)
