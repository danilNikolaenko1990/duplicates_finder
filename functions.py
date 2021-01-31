from os import walk
import os
import hashlib
import os.path
import pathlib
import yaml

FILENAMES = "filenames"
COUNT = "count"
SIZE = "size"


def get_config() -> dict:
    with open(r'config.yml') as file:
        return yaml.load(file, Loader=yaml.FullLoader)


config = get_config()
folders_list_to_skan = config.get('folders_list_to_skan')
file_extensions_to_ignore = config.get('file_extensions_to_ignore')
ignored_folders_rel = config.get('ignored_folders_rel')
ignored_folders_abs = config.get('ignored_folders_abs')
MAX_FILE_SIZE_TO_CHECK_IN_MB = config.get('MAX_FILE_SIZE_TO_CHECK_IN_MB')


def md5(fname: str):
    hash_md5 = hashlib.md5()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()


def make_file_name(dirpath: str, filename: str):
    return os.path.join(dirpath, filename)


def convert_human_readable(size_in_bytes):
    return size_in_bytes / (1024 * 1024)


def get_file_size(file_name):
    size = os.path.getsize(file_name)
    return convert_human_readable(size)


files = {}


def file_exists(fileName):
    return os.path.isfile(fileName)


def file_extension_ignored(file: str):
    return pathlib.Path(file).suffix in file_extensions_to_ignore


def path_ignored(path: str):
    for ignored_folder in ignored_folders_abs:
        if ignored_folder in path:
            return True

    return False


def folder_ignored(path: str) -> bool:
    return os.path.basename(path) in ignored_folders_rel


def folder_name_ignored(path: str) -> bool:
    print(os.path.dirname(path))
    return False


def scan(dirName: str, files: dict):
    for (dirpath, dirnames, filenames) in walk(dirName):
        if path_ignored(dirpath):
            continue
        if folder_ignored(dirpath):
            continue
        print("scanning folder {foldername}".format(foldername=dirpath))
        for file in filenames:
            if file_extension_ignored(file):
                continue

            full_file_name = make_file_name(dirpath, file)
            if not file_exists(full_file_name):
                print("can't handle file {filename} ".format(filename=full_file_name))
                continue

            file_size = get_file_size(full_file_name)
            if int(file_size) > MAX_FILE_SIZE_TO_CHECK_IN_MB:
                print("file {filename} is bigger than {maxsize}, skip...".format(filename=full_file_name,
                                                                                 maxsize=MAX_FILE_SIZE_TO_CHECK_IN_MB))
                continue
            key = md5(make_file_name(dirpath, file))
            existing_file = files.get(key)
            if existing_file is None:
                files[key] = {COUNT: 1, SIZE: file_size, FILENAMES: [full_file_name]}
            else:
                existing_file[COUNT] = existing_file[COUNT] + 1
                existing_file[FILENAMES].append(full_file_name)
                files[key] = existing_file
