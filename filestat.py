#! /usr/bin/python3

"""Recursively read files in a directory and calculate its statistics."""

# Scripted by Carl di Ortus | reklamukibiras@gmail.com
# Available in MIT license (see LICENCE)


import argparse
import copy
import mimetypes
import os
import tempfile


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
    # TODO: not possible, must convert to list or tuple!
    
    words = {}
    chars = {}
    
    f = open(filename)
    
    for line in f.readlines():
        line = line.strip()
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


def dictadd(dict1, dict2):
    """Adds two dictionaries like in set algebra.
        Returns new dictionary."""
    
    result = copy.deepcopy(dict1)
    
    for key in dict2.keys():
        if key in result.keys():
            result[key] += dict2[key]
        else:
            result[key] = dict2[key]
    
    return result


def write_stats(words, chars, filehandle, context):
    """Writes the dictionaries to a file."""
    
    filehandle.write(bytes('\n'+context+'\n\nWords usage:\n', 'UTF-8'))
    for key in words:
        filehandle.write(bytes('\"'+key+'\": %d\n' % words[key], 'UTF-8'))
    filehandle.write(bytes('\nChars usage:\n', 'UTF-8'))
    for key in chars:
        filehandle.write(bytes('\"'+key+'\": %d\n' % chars[key], 'UTF-8'))
    
    return


def main():
    parser = argparse.ArgumentParser(description="""
        Recursively read files in a directory and calculate its statistics.
        Statistics are written to a provided filename.
        (Always overwritten if file is present)""")
    parser.add_argument('filename', metavar='<filename>', type=str,
                        help='location to save the statistics')
    parser.add_argument('directory', metavar='<dir>', type=str,
                        help='root directory for recursive file search')
    args = parser.parse_args()
    
    filelist = get_file_list(args.directory)
    tmp = tempfile.TemporaryFile()
    totalwords = {}
    totalchars = {}
    
    for f in filelist:
        words, chars = calc_file_stats(f)
        write_stats(words, chars, tmp, f)
        totalwords = dictadd(totalwords, words)
        totalchars = dictadd(totalchars, chars)
    
    handle = open(args.filename, 'wb')
    write_stats(totalwords, totalchars, handle, "TOTAL")
    tmp.seek(0, 0)
    for line in tmp.readlines():
        handle.write(line)
    
    tmp.close
    handle.close()
    
    print('%d files treated\n' % len(filelist))
    print('%d total different words\n' % len(totalwords))
    print('%d total different chars\n' % len(totalchars))
    return


if __name__ == '__main__':
    main()
