# file-randomizer

This Python script moves the content of a directory to another one. By default the filenames are randomized and all subfolder removed.  
All changes are stored in a dump file.

| option           | description                                                       |
|:-----------------|:------------------------------------------------------------------|
| -h, --help       | show this help message and exit                                   |
| -v, --verbose    | show the progress (recommended for large folders)                 |
| -d, --dry-run    | perform a trial run with no changes made. dump file is still made |
| -m, --move       | move instead of copy (pay attention)                              |
| -t, --keep-tree  | preserve the subdirectories                                       |
| -n, --keep-name  | preserve the original filenames                                   |
| -e, --remove-ext | remove the file extensions                                        |
