# Settings for script to sort files by last modified date.
# author Ilya Matthew Kuvarzin <luceo2011@yandex.ru>
# version 1.2 dated January 21, 2020

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
# $year, $month, $day, $hour, $minute, $second - fragments of the date the file was last modified
output_directory_tree = '$extension_folder/$year/$month/$day'

# Dictionary with lists file extensions for move. 
# Syntax: {'folder': ['.ext1', 'ext2', ...], ...} 
# Example: {'images': ['.png', '.jpg', '.ico'], 'video': ['.mp4', '.avi']}
files_extensions = {
    'images': ['.jpg', '.png'],
    'video': ['.mp4', '.avi'],
    'text': ['.txt', '.doc']}  