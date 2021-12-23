import os


def get_data_directory():
    return f'{os.getcwd()}/../data'


def get_filenames():
    for directory_path, _, filenames in os.walk(get_data_directory()):
        for file_name in filenames:
            yield (directory_path, file_name)


def get_filepath(directory_path: str, file_name: str):
    return f'{directory_path}/{file_name}'


def get_updated_file_name(file_name: str):
    filename_without_extension = os.path.splitext(file_name)[0]
    return f'{filename_without_extension}_updated.json'


for path, filename in get_filenames():
    filepath = get_filepath(path, filename)

    new_filename = get_updated_file_name(filename)
    new_filepath = get_filepath(path, new_filename)

    # TODO: update the following to automatically replace the original files with the updated files
    # TODO: I was getting an FileNotFoundError and I am not sure why because the file was created successfully
    with open(filepath, 'r') as file:
        with open(new_filepath, 'w') as new_file:
            for line in file:
                index_prefix = '{"index": {}}'
                new_file.write(f'{index_prefix}\n{line}')
