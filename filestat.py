#! /usr/bin/python3

"""Recursive reads of files in a directory and calculates their statistics."""

# Scripted by Carl di Ortus | reklamukibiras@gmail.com
# Available in MIT license (see LICENCE)


import os


def get_file_list(directory):
    """Returns a list of file paths in a given directory.
        Hidden directories and hidden files are ommited."""
    
    filelist = []
    
    for root, dirs, files in os.walk(directory):
        dirs[:] = [d for d in dirs if not d[0] == '.']
        for filename in files:
            if not filename.startswith('.'):
                filelist.append(os.path.join(root, filename))
    
    return filelist


