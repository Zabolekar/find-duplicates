#!/usr/bin/env python

import os
import re
from sys import argv

dir = argv[1].rstrip(os.sep)

def parse_size(s: str) -> int:
    ok = re.match("^(\d+)(\w?)$", s)
    if not ok:
        raise ValueError(f"{s} is not a valid minimum size")
    count, suffix = ok.groups()
    powers = dict(K=1024, M=1024**2, G=1024**3)
    try:
        return int(count) * powers[suffix]
    except KeyError:
        valid_suffixes = ', '.join(powers.keys())
        message = f"valid suffixes are {valid_suffixes}; got {suffix}"
        raise ValueError(message) from None

min_size = parse_size(argv[2])

def add_sizes_to_files(where, files):
    for file in sorted(files):
        size = os.stat(os.path.join(where, file)).st_size
        yield file, size

class Candidate:
    def __init__(self, where, files):
        self.where = where
        self.files_with_sizes = tuple(add_sizes_to_files(where, files))
        self.size = sum(size for _, size in self.files_with_sizes)

def candidates():
    for where, dirs, files in os.walk(dir):
        if files:
            yield Candidate(where, files)

def print_nice_result(paths: list[str]) -> None:
    assert len(paths) > 1
    common_prefix = dir + os.sep
    split_paths = []
    for path in paths:
        assert path.startswith(common_prefix)
        split_paths.append(path[len(common_prefix):].split(os.sep))
    upper_bound = min(len(path) for path in split_paths)
    for suffix_length in range(upper_bound):
        index = - 1 - suffix_length
        unique_names = { path[- 1 - suffix_length] for path in split_paths }
        if len(unique_names) > 1:
            break
    common_suffix = os.path.join(*split_paths[0][-suffix_length:])
    print(common_suffix)
    for path in split_paths:
        path_section = os.path.join(*path[:-suffix_length])
        print(f"- {path_section}")


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


for paths in files_where.values():
    if len(paths) > 1:
        print_nice_result(paths)
