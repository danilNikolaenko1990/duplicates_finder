#!/usr/bin/env python
from os import walk
import os
import hashlib
import os.path
import pathlib

foldersListToSkan = [
    "/home/danil/Dropbox",
    "/home/danil/Dropbox (Old)",
    "/home/danil/dropbox_old2",
    "/home/danil/dell_latitude",
]

fileExtensionsToIgnore = [
    'yml',
    'php',
    'go',
    'java',
    'html'
]

# вычисление md5 на больших файлах будет делаться медленно, поэтому скипаем их
MAX_FILE_SIZE_TO_CHECK_IN_MB = 1000

FILENAMES = "filenames"
COUNT = "count"
SIZE = "size"


def md5(fname: str):
    hash_md5 = hashlib.md5()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()


def makeFileName(dirpath: str, filename: str):
    return dirpath + "/" + filename


def convertHumanReadable(size_in_bytes):
    return size_in_bytes / (1024 * 1024)


def getFileSize(file_name):
    size = os.path.getsize(file_name)
    return convertHumanReadable(size)


files = {}


def fileExists(fileName):
    return os.path.isfile(fileName)


def fileExtensionIgnored(file: str):
    return pathlib.Path(file).suffix in fileExtensionsToIgnore


def scan(dirName: str, files: dict):
    for (dirpath, dirnames, filenames) in walk(dirName):
        for file in filenames:
            if fileExtensionIgnored(file):
                continue
            fullFileName = makeFileName(dirpath, file)
            if not fileExists(fullFileName):
                print("can't handle file {filename} ".format(filename=fullFileName))
                continue

            fileSize = getFileSize(fullFileName)
            if int(fileSize) > MAX_FILE_SIZE_TO_CHECK_IN_MB:
                print("file {filename} is bigger than {maxsize}, skip...".format(filename=fullFileName,
                                                                                 maxsize=MAX_FILE_SIZE_TO_CHECK_IN_MB))
                continue
            key = md5(makeFileName(dirpath, file))
            existingFile = files.get(key)
            if existingFile is None:
                files[key] = {COUNT: 1, SIZE: fileSize, FILENAMES: [fullFileName]}
            else:
                existingFile[COUNT] = existingFile[COUNT] + 1
                existingFile[FILENAMES].append(fullFileName)
                files[key] = existingFile


for folderToScan in foldersListToSkan:
    scan(folderToScan, files)

for fileKey in files:
    filedata = files.get(fileKey)
    if filedata[COUNT] > 1:
        print("count: {count}, filesize in MB:{filesize}, filepaths:".format(count=filedata[COUNT],
                                                                             filesize="{:.2f}".format(filedata[SIZE])))
        for duplicatePath in filedata[FILENAMES]:
            print(" " * 2 + duplicatePath)
