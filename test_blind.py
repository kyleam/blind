import pytest
import mock
from StringIO import StringIO

import blind

## _get_path_and_extension


def test_get_path_and_extension_full_path_and_extension():
    result = blind._get_path_and_extension('/path/to/file.ext')
    assert result[0] == '/path/to'
    assert result[1] == '.ext'


def test_get_path_and_extension_full_path_and_no_extension():
    result = blind._get_path_and_extension('/path/to/file')
    assert result[0] == '/path/to'
    assert result[1] == ''


def test_get_path_and_extension_no_path_with_extension():
    result = blind._get_path_and_extension('file.ext')
    assert result[0] == ''
    assert result[1] == '.ext'


def test_get_path_and_extension_no_path_no_extension():
    result = blind._get_path_and_extension('file')
    assert result[0] == ''
    assert result[1] == ''


## name_by_shuffled_numbers


def test_name_by_shuffled_numbers_one_file():
    files = ['one.txt']
    result = list(blind.name_by_shuffled_numbers(files))
    assert result == [('one.txt', '0.txt')]


def test_name_by_shuffled_numbers_two_files():
    with mock.patch('random.shuffle'):
        files = ['one.txt', 'two.csv']
        result = list(blind.name_by_shuffled_numbers(files))
        assert result == [('one.txt', '0.txt'), ('two.csv', '1.csv')]


def test_name_by_shuffled_numbers_ten_files():
    with mock.patch('random.shuffle'):
        files = ['{}.txt'.format(i) for i in range(10)]
        result = list(blind.name_by_shuffled_numbers(files))
        assert result[0] == ('0.txt', '00.txt')


def test_name_by_shuffled_numbers_two_files_with_path():
    with mock.patch('random.shuffle'):
        files = ['/path/one.txt', '/path/two.csv']
        result = list(blind.name_by_shuffled_numbers(files))
        assert result == [('/path/one.txt', '/path/0.txt'),
                          ('/path/two.csv', '/path/1.csv')]


def test_name_by_shuffled_numbers_no_files():
    result = list(blind.name_by_shuffled_numbers([]))
    assert result == []


## name_by_random_fours

test_fours = ['aaaa', 'bbbb']


@mock.patch('random.shuffle')
@mock.patch.object(blind, 'fours', test_fours)
def test_name_by_random_fours_one_file(shuffle):
    files = ['one.txt']
    result = list(blind.name_by_random_fours(files))
    assert result == [('one.txt', 'aaaa.txt')]


@mock.patch('random.shuffle')
@mock.patch.object(blind, 'fours', test_fours)
def test_name_by_random_fours_two_files(shuffle):
    files = ['one.txt', 'two.csv']
    result = list(blind.name_by_random_fours(files))
    assert result == [('one.txt', 'aaaa.txt'), ('two.csv', 'bbbb.csv')]


@mock.patch('random.shuffle')
@mock.patch.object(blind, 'fours', test_fours)
def test_name_by_random_fours_two_files_with_path(shuffle):
    files = ['/path/one.txt', '/path/two.csv']
    result = list(blind.name_by_random_fours(files))
    assert result == [('/path/one.txt', '/path/aaaa.txt'),
                      ('/path/two.csv', '/path/bbbb.csv')]


## write_map


def test_write_map():
    file_map = {'one.txt': 'mask1.txt', 'two.txt': 'mask2.txt'}
    ofh = StringIO()
    blind.write_map(file_map, ofh)
    result = ofh.getvalue()
    assert 'one.txt,mask1.txt' in result
    assert 'two.txt,mask2.txt' in result


## read_map


def test_read_map():
    ifh = StringIO('one.txt,mask1.txt\r\ntwo.txt,mask2.txt\r\n')
    result = blind.read_map(ifh)
    assert result == {'one.txt': 'mask1.txt', 'two.txt': 'mask2.txt'}


## mask_files


def test_mask_files():
    def masker(files):
        for f in files:
            yield f, f + '.masked'

    with mock.patch('os.rename') as rename:
        files = ['one.txt', 'two.txt']
        result = blind.mask_files(files, masker)
        rename.assert_any_call('one.txt', 'one.txt.masked')
        rename.assert_any_call('two.txt', 'two.txt.masked')
    assert result['one.txt'] == 'one.txt.masked'
    assert result['two.txt'] == 'two.txt.masked'


## unmask files


def test_unmask_files():
    file_map = {'one.txt': 'one.txt.masked', 'two.txt': 'two.txt.masked'}
    with mock.patch('os.rename') as rename:
        blind.unmask_files(file_map)
        rename.assert_any_call('one.txt.masked', 'one.txt')
        rename.assert_any_call('two.txt.masked', 'two.txt')
