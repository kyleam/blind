"""Library for masking and unmasking file names
"""
import sys
import os
import csv
import random
from datetime import datetime

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


def mask(files, masker):
    """Mask `files` with `masker`

    `masker` should be a function that produces an iterable providing
    the original file name and the masked file name

    Writes file "blind-map-*.csv" that associates the original file
    names to the masked file names.

    Returns name of the blind map file.
    """
    file_map = _create_map(files, masker)
    _collision_check(file_map)
    _mask(file_map)

    file_map_file = _get_map_filename(files)
    with open(file_map_file, 'w') as ofh:
        _write_map(file_map, ofh)
    return file_map_file


def _create_map(files, masker):
    file_map = {}
    for original, masked in masker(files):
        file_map[original] = masked
    return file_map


def _collision_check(file_map):
    """Check that masked file names don't conflict with existing files in
    directories
    """
    for masked in file_map.values():
        if os.path.exists(masked):
            raise ConflictError('{} already exists'.format(masked))


class ConflictError(Exception):
    pass


_conflict_message = ('Attempted to rename files, '
                     'but there was a renaming conflict. '
                     'If you are masking with words, '
                     'this is an unlikely conflict '
                     '(assuming you don\'t have a large number '
                     'of four-letter names in this directory), '
                     'so try again. '
                     'If you are masking with numbers, '
                     'check if any files in the directory '
                     'consist of just numbers.')


def _mask(file_map):
    for original, masked in file_map.items():
        os.rename(original, masked)


def _get_map_filename(files, map_id=None):
    """Generate blind map file name for `files`

    `map_id` is the ID to append to blind map file. If None, date
    and time are appended.
    """
    if map_id is None:
        map_id = datetime.now().strftime('%Y%m%d-%H%M%S')
    pwd = os.path.split(files[0])[0]
    return os.path.join(pwd, 'blind-map-{}.csv'.format(map_id))


def _write_map(file_map, ofh):
    """Write `file_map` to `ofh` in format of "original, masked" rows
    """
    writer = csv.writer(ofh)
    for original, masked in file_map.items():
        writer.writerow([original, masked])


def unmask(blind_map):
    """Unmask files by renaming them back to the original file name provided
    by `blind_map`.

    `blind_map` is the name of the file mapping the masked file names to
    the original file names as keys and the masked file names.
    """
    _unmask(_read_map(open(blind_map)))


def _unmask(file_map):
    for original, masked in file_map.items():
        os.rename(masked, original)


def _read_map(ifh):
    """Read original-masked mapping from `ifh`

    Each row of `ifh` should have a comma-delimited pair of original and
    masked file names
    """
    reader = csv.reader(ifh)
    return {original: masked for original, masked in reader}
