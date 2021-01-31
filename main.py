#!/usr/bin/env python
import functions as f

for folder_to_scan in f.folders_list_to_skan:
    f.scan(folder_to_scan, f.files)

print("-------report---------")
for file_key in f.files:
    file_data = f.files.get(file_key)
    if file_data[f.COUNT] > 1:
        print("count: {count}, filesize in MB:{filesize}, filepaths:".format(count=file_data[f.COUNT],
                                                                             filesize="{:.2f}".format(
                                                                                 file_data[f.SIZE])))
        for duplicate_path in file_data[f.FILENAMES]:
            print(" " * 2 + duplicate_path)

print("----clear duplicates----")
for file_key in f.files:
    file_data = f.files.get(file_key)
    if file_data[f.COUNT] > 1:
        print("new duplicate")
        for duplicate_path in file_data[f.FILENAMES]:
            print(duplicate_path)
