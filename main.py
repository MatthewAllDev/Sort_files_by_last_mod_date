# Script to sort files by last modified date.
# author Ilya Matthew Kuvarzin <luceo2011@yandex.ru>
# version 1.3 dated February 03, 2020

import os.path
from datetime import datetime
from hashlib import md5
import settings
import re


def get_group(file):
    if len(settings.files_extensions) == 0:
        return True
    for group in settings.files_extensions:
        for extension in settings.files_extensions[group]:
            if file.lower().endswith(extension.lower()):
                return group
    return False


def get_checksum(file):
    checksum = md5()
    with open(file, 'rb') as f:
        for chunk in iter(lambda: f.read(128 * checksum.block_size), b''):
            checksum.update(chunk)
    f.close()
    return checksum.hexdigest()


def move_file(input_file, output_file):
    if not os.path.exists(output_file):
        try:
            os.rename(input_file, output_file)
        except OSError:
            print('Move file %s failed' % input_file)
            return
    else:
        if settings.delete_duplicate_files:
            if get_checksum(input_file) == get_checksum(output_file):
                os.remove(input_file)
                return
        extension = output_file[output_file.lower().rfind('.'):]
        file_name = output_file[:output_file.lower().rfind('.')]
        move_file(input_file, '%s(1)%s' % (file_name, extension))


def get_output_directory_tree(file_name, folder_name, date, other_file):
    file_names = re.findall(r'\$file_name\[\d*:?\d*\]', settings.output_directory_tree)
    if not other_file:
        tree = settings.output_directory_tree
    else:
        tree = settings.output_directory_other_file_tree
    pos = file_name.rfind('.')
    extension = file_name[pos+1:]
    file_name = file_name[:pos]
    for file_name_variable in file_names:
        fragment = eval(file_name_variable.replace('$file_name', 'file_name'))
        tree = tree.replace(file_name_variable, fragment)
    if type(folder_name) != bool:
        tree = tree.replace('$extension_folder', folder_name)
    else:
        tree = re.sub(r'/?\$extension_folder/?', '/', tree)
    tree = tree.replace('$extension', extension)
    tree = tree.replace('$year', str(date.year))
    tree = tree.replace('$month', str(date.month))
    tree = tree.replace('$day', str(date.day))
    tree = tree.replace('$hour', str(date.hour))
    tree = tree.replace('$minute', str(date.minute))
    tree = tree.replace('$second', str(date.second))
    return tree


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
        if os.path.isdir('%s/%s' % (directory, file)) and settings.recursively:
            move_files('%s/%s' % (directory, file))
            continue
        group = get_group(file)
        if group or settings.move_other_files:
            date = datetime.fromtimestamp(os.path.getmtime('%s/%s' % (directory, file)))
            if not group:
                other = True
            else:
                other = False
            folder = '%s/%s' % (settings.output_directory, get_output_directory_tree(file, group, date, other))
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

    if (len(os.listdir(directory)) == 0) and settings.delete_empty_directory:
        try:
            os.rmdir(directory)
        except OSError:
            print('Delete directory %s failed' % directory)
            return


for d in settings.input_directories:
    move_files(d)
