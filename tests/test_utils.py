"""Module to test functionality of the various util functions."""

import unittest
from pymdb.utils import *


class TestAppendFilenameToPath(unittest.TestCase):
    def test_append_filename_to_path_unspecified(self):
        path = 'path'
        filename = 'myfile.txt'
        correct_result = 'path/myfile.txt'
        self.assertEqual(append_filename_to_path(path, filename), correct_result)

    def test_append_filename_to_path_unix(self):
        path1 = 'path/to/file/'
        path2 = 'path/to/file'
        filename = 'myfile.txt'
        correct_result = 'path/to/file/myfile.txt'
        self.assertEqual(append_filename_to_path(path1, filename), correct_result)
        self.assertEqual(append_filename_to_path(path2, filename), correct_result)

    def test_append_filename_to_path_windows(self):
        path1 = 'path\\to\\file\\'
        path2 = 'path\\to\\file'
        filename = 'myfile.txt'
        correct_result = 'path\\to\\file\\myfile.txt'
        self.assertEqual(append_filename_to_path(path1, filename), correct_result)
        self.assertEqual(append_filename_to_path(path2, filename), correct_result)


# TODO: test gunzip_file
class TestGunzipFile(unittest.TestCase):
    pass


class TestPreprocessList(unittest.TestCase):
    def test_preprocess_list_single(self):
        lst = ['a', 'test', '\\N']
        correct_result = ['a', 'test', None]
        self.assertEqual(preprocess_list(lst), correct_result)

    def test_preprocess_list_multiple(self):
        lst = ['\\N', 'a', '\\N', 'test', '\\N']
        correct_result = [None, 'a', None, 'test', None]
        self.assertEqual(preprocess_list(lst), correct_result)

    def test_preprocess_list_none(self):
        lst = ['a', 'test']
        correct_result = ['a', 'test']
        self.assertEqual(preprocess_list(lst), correct_result)

    def test_preprocess_list_empty(self):
        lst = []
        correct_result = []
        self.assertEqual(preprocess_list(lst), correct_result)


class TestSplitByBr(unittest.TestCase):
    pass


class TestRemoveDivs(unittest.TestCase):
    pass


class TestRemoveTags(unittest.TestCase):
    pass


class TestGetCompanyId(unittest.TestCase):
    pass


class TestGetNameId(unittest.TestCase):
    pass


class TestGetTitleId(unittest.TestCase):
    pass


class TestGetCategory(unittest.TestCase):
    pass


class TestGetRefMarker(unittest.TestCase):
    pass


class TestTrimYear(unittest.TestCase):
    pass


class TestIsMoneyString(unittest.TestCase):
    pass


class TestTrimMoneyString(unittest.TestCase):
    pass


class TestIsBool(unittest.TestCase):
    def test_is_bool_boolean(self):
        b1 = True
        b2 = False
        self.assertTrue(is_bool(b1))
        self.assertTrue(is_bool(b2))

    def test_is_bool_string_correct(self):
        b = 'True'
        self.assertTrue(is_bool(b))

    def test_is_bool_string_incorrect(self):
        b = 'is this true?'
        self.assertFalse(is_bool(b))


class TestIsFloat(unittest.TestCase):
    def test_is_float_float(self):
        f = 1.23
        self.assertTrue(is_float(f))

    def test_is_float_string_correct(self):
        f = '1.23'
        self.assertTrue(is_float(f))

    def test_is_float_string_incorrect(self):
        f = 'one point two three'
        self.assertFalse(is_float(f))


class TestIsInt(unittest.TestCase):
    def test_is_int_integer(self):
        i = 5
        self.assertTrue(is_int(i))

    def test_is_int_string_correct(self):
        i = '5'
        self.assertTrue(is_int(i))

    def test_is_int_string_incorrect(self):
        i = 'five'
        self.assertFalse(is_int(i))


class TestIsDatetime(unittest.TestCase):
    pass


class TestToDatetime(unittest.TestCase):
    pass