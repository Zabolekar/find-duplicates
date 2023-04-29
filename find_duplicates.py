#!/usr/bin/env python

from os import walk, path, stat
from sys import argv
dir = argv[1]
min_size = int(argv[2])

def add_sizes_to_files(where, files):
    for file in sorted(files):
        size = stat(path.join(where, file)).st_size
        yield file, size

class Candidate:
    def __init__(self, where, files):
        self.where = where
        self.files_with_sizes = tuple(add_sizes_to_files(where, files))
        self.size = sum(size for _, size in self.files_with_sizes)

def candidates():
    for where, dirs, files in walk(dir):
        if files:
            yield Candidate(where, files)

files_where = dict()
for candidate in candidates():
    # TODO: progress bar
    # TODO: DO NOT IGNORE SUBFOLDERS!
    # TODO: and also just single files (identical name and size)
    # TODO: and also deeply nested structures, where files themselves are not large
    # TODO: optionally consider inexact matches, like, if some names are missing or changed here or there...
    # test for common subsets of names? in percent of whoever is smaller? hmm
    
    if candidate.size < min_size:
        continue

    where, files = candidate.where, candidate.files_with_sizes

    if files in files_where:
        files_where[files].append(where)
    else:
        files_where[files] = [where]

for where in files_where.values():
    if len(where) > 1:
        print(where)
