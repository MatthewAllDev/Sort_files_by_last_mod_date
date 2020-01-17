# Script to sort files by last modified date.
# author Ilya Matthew Kuvarzin <luceo2011@yandex.ru>
# version 1.0 dated January 17, 2020

import os.path
from datetime import datetime

# SETTINGS
recursively = True  # Sort files from subfolders?
input_directories = ['D:/FILES']  # List input directories. Example: ['/home/Images', '/home/Photos']
output_directories = 'D:/FILES SORTED'  # Output folder
files_extensions = ['.jpg', '.png']  # List file extensions. Example: ['.png', '.jpg', '.avi', '.txt']


def check_extension(file):
    for extension in files_extensions:
        if file.endswith(extension):
            return True


def move_files(directory):
    files = os.listdir(path=directory)
    for file in files:
        if os.path.isdir('%s/%s' % (directory, file)) and recursively:
            move_files('%s/%s' % (directory, file))
            continue
        if check_extension(file):
            date = datetime.fromtimestamp(os.path.getmtime('%s/%s' % (directory, file)))
            folder = '%s/%i/%i/%i' % (output_directories, date.year, date.month, date.day)
            if os.path.exists(folder):
                os.rename('%s/%s' % (directory, file), '%s/%s' % (folder, file))
            else:
                try:
                    os.makedirs(folder)
                except OSError:
                    print("Create directory %s failed" % folder)
                    exit(0)
                os.rename('%s/%s' % (directory, file), '%s/%s' % (folder, file))


for d in input_directories:
    move_files(d)
