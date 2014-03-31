#! /usr/bin/python3

"""Recursive reads of files in a directory and calculates their statistics."""

# Scripted by Carl di Ortus | reklamukibiras@gmail.com
# Available in MIT license (see LICENCE)


import mimetypes
import os
import re


def get_file_list(directory):
    """Returns a list of file paths in a given directory.
        Hidden directories and hidden files are ommited.
        File is accepted if its mimetype is None or text."""
    
    filelist = []
    
    for root, dirs, files in os.walk(directory):
        dirs[:] = [d for d in dirs if not d[0] == '.']
        for filename in files:
            if (not filename.startswith('.') and 
                    mimetypes.guess_type(filename)[0] is None):
                filelist.append(os.path.join(root, filename))
            elif (not filename.startswith('.') and
                    mimetypes.guess_type(filename)[0].startswith('text')):
                filelist.append(os.path.join(root, filename))
    
    return filelist


def calc_file_stats(filename):
    """Calculates file statistics and returns two dictionaries
        with words and chars usage."""
    # TODO: sort dicts (by count or by abc)
    
    words = {}
    chars = {}
    
    f = open(filename)
    
    for line in f.readlines():
        for char in line:
            if not char in chars.keys():
                chars[char] = 1
            else:
                chars[char] += 1
        # TODO: other separators & is it necessary
        for word in line.split(' '):
            if not word in words.keys():
                words[word] = 1
            else:
                words[word] += 1
    
    f.close()
    return words, chars

