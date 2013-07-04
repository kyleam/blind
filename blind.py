import sys
import os
import csv
import random

from four_letters import fours

__version__ = '0.9.0'


def name_by_shuffled_numbers(files):
    """Return generator that provides original file name and a file name
    drawn from the range of the number of files

    For example, files ['one.txt', 'two.txt', 'three.txt'] could yield

      one.txt, 2.txt
      two.txt, 1.txt
      three.txt, 3.txt
    """
    files = list(files)

    nfiles = len(files)
    digits = list(range(nfiles))
    width = len(str(nfiles))  # for 0-padding

    random.shuffle(digits)

    for f, digit in zip(files, digits):
        path, ext = _get_path_and_extension(f)
        yield f, os.path.join(path, str(digit).zfill(width) + ext)


def name_by_random_fours(files):
    """Return generator that provides original file name and a file name
    drawn from four letter words

    For example, files ['one.txt', 'two.txt', 'three.txt'] could yield

      one.txt, yurt.txt
      two.txt, clog.txt
      three.txt, fava.txt
    """
    if len(files) > len(fours):
        raise ValueError("Cannot process more than {} files".format(len(fours)))

    random.shuffle(fours)
    for f, four in zip(files, fours):
        path, ext = _get_path_and_extension(f)
        yield f, os.path.join(path, four + ext)


def _get_path_and_extension(f):
    """/path/to/file.ext -> (/path/to, .ext)"""
    path = os.path.split(f)[0]
    ext = os.path.splitext(f)[1]
    return path, ext


def write_map(file_map, ofh):
    """Write `file_map` to `ofh` in format of "original, masked" rows
    """
    writer = csv.writer(ofh)
    for original, masked in file_map.items():
        writer.writerow([original, masked])


def read_map(ifh):
    """Read original-masked mapping from `ifh`

    Each row of `ifh` should have a comma-delimited pair of original and
    masked file names
    """
    reader = csv.reader(ifh)
    return {original: masked for original, masked in reader}


def mask_files(files, masker):
    """Mask `files` with `masker`

    `masker` should be a function that produces an iterable providing
    the original file name and the masked file name

    Returns dictionary that maps the original file names to the sha1
    file names.
    """
    file_map = {}
    for original, masked in masker(files):
        os.rename(original, masked)
        file_map[original] = masked
    return file_map


def unmask_files(file_map):
    """Unmask files by renaming them back to the original file name provided
    by `file_map`.

    `file_map` is a dictionary with the original file names as keys and
    the masked file names as values. In almost all cases, this would have
    come from `mask_files`.
    """
    for original, masked in file_map.items():
        os.rename(masked, original)
