# Settings for script to sort files by last modified date.
# author Ilya Matthew Kuvarzin <luceo2011@yandex.ru>
# version 1.3 dated February 03, 2020

recursively = True  # Sort files from subfolders?

delete_duplicate_files = True  # Delete files with the same checksum?

delete_empty_directory = True  # Delete processed directory if empty?

# List input directories.
# Example: ['/home/Images', '/home/Photos']
input_directories = ['/home/matthew/Images/input']

output_directory = '/home/matthew/Images/sorted'  # Output folder

# Path to file in output directory.
# Variables:
# $extension_folder - folder name specified as the files_extensions dictionary key for this file extension
# $extension - file extension
# $year, $month, $day, $hour, $minute, $second - fragments of the date the file was last modified
# $file_name[*] - file name fragment.
# A symbol can be accessed by its index. Example for Abcd.txt: $file_name[0] = A, $file_name[-1] = d
# In addition to indexing, slicing is also supported. While indexing is used to obtain individual characters,
# slicing allows you to obtain substring. Example for Abcd.txt: $file_name[1:3]  = bc, $file_name[1:] = bcd,
# $file_name[:2] = Ab

output_directory_tree = '$extension_folder/$extension/$year/$month/$file_name[0]/'

# Dictionary with lists file extensions for move. If the dictionary is empty, all files are moved.
# Syntax: {'folder': ['.ext1', 'ext2', ...], ...} 
# Example: {'images': ['.png', '.jpg', '.ico'], 'video': ['.mp4', '.avi']}
files_extensions = {
    'images': ['.jpg', '.png'],
    'video': ['.mp4', '.avi'],
    'text': ['.txt', '.doc']}

move_other_files = True  # Move files whose extension is not specified in files_extensions?

# Path to other files in output directory. It is possible to use the variables specified for output_directory_tree
output_directory_other_file_tree = 'other/$extension/$extension_folder'
