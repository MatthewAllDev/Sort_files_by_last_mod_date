# Script to sort files by last modified date.
# author Ilya Matthew Kuvarzin <luceo2011@yandex.ru>
# version 1.1 dated January 20, 2020

import os.path
from datetime import datetime
from hashlib import md5

# SETTINGS
recursively = True  # Sort files from subfolders?
delete_duplicate_files = True  # Delete files with the same checksum?
delete_empty_directory = True  # Delete processed directory if empty?
input_directories = ['D:/FILES']  # List input directories. Example: ['/home/Images', '/home/Photos']
output_directories = 'D:/FILES SORTED'  # Output folder
files_extensions = ['.jpg', '.png']  # List file extensions. Example: ['.png', '.jpg', '.avi', '.txt']


def check_extension(file):
    for extension in files_extensions:
        if file.lower().endswith(extension.lower()):
            return True


def get_checksum(file):
    checksum = md5()
    with open(file, 'rb') as f:
        for chunk in iter(lambda: f.read(128* checksum.block_size), b''):
            checksum.update(chunk)
    f.close()
    return checksum.hexdigest()


def move_file(input_file, output_file):
    try:
        os.rename(input_file, output_file)
    except FileExistsError:
        if delete_duplicate_files:
            if get_checksum(input_file) == get_checksum(output_file):
                os.remove(input_file)
                return
        extension = output_file[output_file.lower().rfind('.'):]
        file_name = output_file[:output_file.lower().rfind('.')]
        move_file(input_file, '%s(1)%s' % (file_name, extension))
    except OSError:
        print('Move file %s failed' % input_file)
        return


def move_files(directory):
    try:
        files = os.listdir(directory)
    except FileNotFoundError:
        print('Directory %s not found' % directory)
        return
    except OSError:
        print('Processing directory %s failed' % directory)
        return
    for file in files:
        if os.path.isdir('%s/%s' % (directory, file)) and recursively:
            move_files('%s/%s' % (directory, file))
            continue
        if check_extension(file):
            date = datetime.fromtimestamp(os.path.getmtime('%s/%s' % (directory, file)))
            folder = '%s/%i/%i/%i' % (output_directories, date.year, date.month, date.day)
            input_file = '%s/%s' % (directory, file)
            output_file = '%s/%s' % (folder, file)
            if os.path.exists(folder):
                move_file(input_file, output_file)
            else:
                try:
                    os.makedirs(folder)
                except OSError:
                    print('Create directory %s failed' % folder)
                    return
                move_file(input_file, output_file)
    if (len(os.listdir(directory)) == 0) and delete_empty_directory:
        try:
            os.rmdir(directory)
        except OSError:
            print('Delete directory %s failed' % directory)
            return


for d in input_directories:
    move_files(d)
