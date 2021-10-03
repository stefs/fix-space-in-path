# Fix space in path

Some programs cannot deal with directory or file names, that start or end with a whitespace. File explorers usually fix 
this on the fly, but other applications might still create such malformed names. This can happen for example when 
unpacking a file archive. This script scans directories recursively, and offers to remove the spaces.

## Dependencies

* [Python 3.8](https://www.python.org/) - Programming language

## Usage
Set the directory you want to scan inside the script, then execute without arguments.

    RECURSIVE_FIX_DIRECTORY_NAMES_HERE = 'C:\\path'

Example output:

     BROKEN: "C:\path\ dir \"
        FIX: "C:\path\dir\"
    Rename this? y
    Fixed.

     BROKEN: "C:\path\ file . jpg "
        FIX: "C:\path\file.jpg"
    Rename this? n
    Not fixed.

## Author and license

Copyright © 2021 Stefan Schindler  
MIT License
