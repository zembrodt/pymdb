"""Module to test functionality of the various util functions."""

import unittest
from pymdb.utils import *
from pymdb.utils import _get_id, _get_from_onclick
from datetime import datetime
import gzip
import os
from selectolax.parser import HTMLParser
from tempfile import TemporaryDirectory


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


class TestGunzipFile(unittest.TestCase):
    content = b'test content'

    def test_gunzip_file_gz_extension(self):
        with TemporaryDirectory() as tmpdir:
            infile = os.path.join(tmpdir, 'test.csv.gz')
            with gzip.open(infile, 'wb') as f:
                f.write(self.content)
            actual_result = gunzip_file(infile)
            correct_result = os.path.join(tmpdir, 'test.csv')
            self.assertTrue(os.path.exists(infile))
            self.assertTrue(os.path.exists(correct_result))
            with open(actual_result, 'rb') as f:
                self.assertEqual(self.content, f.read())
        self.assertEqual(actual_result, correct_result)

    def test_gunzip_file_gz_extension_delete_infile(self):
        with TemporaryDirectory() as tmpdir:
            infile = os.path.join(tmpdir, 'test.csv.gz')
            with gzip.open(infile, 'wb') as f:
                f.write(self.content)
            actual_result = gunzip_file(infile, delete_infile=True)
            correct_result = os.path.join(tmpdir, 'test.csv')
            self.assertFalse(os.path.exists(infile))
            self.assertTrue(os.path.exists(correct_result))
            with open(actual_result, 'rb') as f:
                self.assertEqual(self.content, f.read())
        self.assertEqual(actual_result, correct_result)

    def test_gunzip_file_custom_outfile(self):
        with TemporaryDirectory() as tmpdir:
            infile = os.path.join(tmpdir, 'test.csv.gz')
            outfile = os.path.join(tmpdir, 'test2.csv')
            with gzip.open(infile, 'wb') as f:
                f.write(self.content)
            actual_result = gunzip_file(infile, outfile=outfile)
            self.assertTrue(os.path.exists(infile))
            self.assertTrue(os.path.exists(outfile))
            with open(actual_result, 'rb') as f:
                self.assertEqual(self.content, f.read())
        self.assertEqual(actual_result, outfile)

    def test_gunzip_file_custom_outfile_delete_infile(self):
        with TemporaryDirectory() as tmpdir:
            infile = os.path.join(tmpdir, 'test.csv.gz')
            outfile = os.path.join(tmpdir, 'test2.csv')
            with gzip.open(infile, 'wb') as f:
                f.write(self.content)
            actual_result = gunzip_file(infile, outfile=outfile, delete_infile=True)
            self.assertFalse(os.path.exists(infile))
            self.assertTrue(os.path.exists(outfile))
            with open(actual_result, 'rb') as f:
                self.assertEqual(self.content, f.read())
        self.assertEqual(actual_result, outfile)

    def test_gunzip_file_no_gz_extension_no_outfile(self):
        with TemporaryDirectory() as tmpdir:
            infile = os.path.join(tmpdir, 'test.csv')
            with gzip.open(infile, 'wb') as f:
                f.write(self.content)
            actual_result = gunzip_file(infile)
            correct_result = os.path.join(tmpdir, 'test.csv.out')
            self.assertTrue(os.path.exists(infile))
            self.assertTrue(os.path.exists(correct_result))
            with open(actual_result, 'rb') as f:
                self.assertEqual(self.content, f.read())
        self.assertEqual(actual_result, correct_result)

    def test_gunzip_file_no_gz_extension_no_outfile_delete_infile(self):
        with TemporaryDirectory() as tmpdir:
            infile = os.path.join(tmpdir, 'test.csv')
            with gzip.open(infile, 'wb') as f:
                f.write(self.content)
            actual_result = gunzip_file(infile, delete_infile=True)
            correct_result = os.path.join(tmpdir, 'test.csv.out')
            self.assertFalse(os.path.exists(infile))
            self.assertTrue(os.path.exists(correct_result))
            with open(actual_result, 'rb') as f:
                self.assertEqual(self.content, f.read())
        self.assertEqual(actual_result, correct_result)    


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
    def test_split_by_br(self):
        html1 = 'this is <br> a test'
        html2 = 'this is < br > a test'
        html3 = 'this is < br / > a test'
        html4 = 'this is <br/> a test'
        correct_split = ['this is ', ' a test']
        self.assertEqual(split_by_br(html1), correct_split)
        self.assertEqual(split_by_br(html2), correct_split)
        self.assertEqual(split_by_br(html3), correct_split)
        self.assertEqual(split_by_br(html4), correct_split)

    def test_split_by_br_no_br(self):
        html = 'this is a test'
        correct_split = ['this is a test']
        self.assertEqual(split_by_br(html), correct_split)

    def test_split_by_br_other_tags(self):
        html = '<a>this is</a><br><span>a test</span>'
        correct_split = ['<a>this is</a>', '<span>a test</span>']
        self.assertEqual(split_by_br(html), correct_split)


class TestRemoveTags(unittest.TestCase):
    _tag = 'td'

    def test_remove_tags_empty(self):
        html = '<td></td>'
        correct_result = ''
        self.assertEqual(remove_tags(html, self._tag), correct_result)

    def test_remove_tags_no_class(self):
        html = '<td>test</td>'
        correct_result = 'test'
        self.assertEqual(remove_tags(html, self._tag), correct_result)

    def test_remove_tags_class(self):
        html = '<td class="testClass">test</td>'
        correct_result = 'test'
        self.assertEqual(remove_tags(html, self._tag), correct_result)

    def test_remove_tags_spaces(self):
        html = '< td  class="testClass" >test< /  td >'
        correct_result = 'test'
        self.assertEqual(remove_tags(html, self._tag), correct_result)

    def test_remove_tags_multiple(self):
        html = '<td class="testClass">test</td ><div>blah</div><td>test2</td>'
        correct_result = 'test<div>blah</div>test2'
        self.assertEqual(remove_tags(html, self._tag), correct_result)

    def test_remove_tags_none(self):
        html = 'test'
        correct_result = 'test'
        self.assertEqual(remove_tags(html, self._tag), correct_result)


class TestRemoveDivs(unittest.TestCase):
    _tag = 'div'

    def test_remove_divs_empty(self):
        html = '<div></div><td>test</td>'
        correct_result = '<td>test</td>'
        self.assertEqual(remove_tags_and_content(html, self._tag), correct_result)

    def test_remove_divs_no_class(self):
        html = '<div>this should be <strong>removed</strong></div><td>test</td>'
        correct_result = '<td>test</td>'
        self.assertEqual(remove_tags_and_content(html, self._tag), correct_result)

    def test_remove_divs_class(self):
        html = '<div class="testClass">this should be <strong>removed</strong></div><td>test</td>'
        correct_result = '<td>test</td>'
        self.assertEqual(remove_tags_and_content(html, self._tag), correct_result)

    def test_remove_divs_spaces(self):
        html = '<  div   class="testClass"  >this should be <strong>removed</strong>< /  div ><td>test</td>'
        correct_result = '<td>test</td>'
        self.assertEqual(remove_tags_and_content(html, self._tag), correct_result)

    def test_remove_divs_no_divs(self):
        html = '<td>test</td>'
        correct_result = '<td>test</td>'
        self.assertEqual(remove_tags_and_content(html, self._tag), correct_result)

    def test_remove_divs_multiple(self):
        html = '''
        <div class="testClass">this should be <strong>removed</strong></div>
        <div>also this should be removed</div>
        <td>test</td>
        '''
        correct_result = '<td>test</td>'
        self.assertEqual(remove_tags_and_content(html, self._tag).strip(), correct_result)

    def test_remove_divs_with_children(self):
        html = '''
        <div class="testClass">this should be <strong>removed</strong>
            <div>also this should be removed</div>
        </div>
        <td>test</td>
        '''
        correct_result = '<td>test</td>'
        self.assertEqual(remove_tags_and_content(html, self._tag).strip(), correct_result)


class TestGetId(unittest.TestCase):
    _prefix = 'tt'

    def test_get_id_correct(self):
        html = '<a href="www.blah.com/blah/tt123456/blah/" onclick="test">my link</a>'
        node = HTMLParser(html).css_first('a')
        correct_result = 'tt123456'
        self.assertEqual(_get_id(node, self._prefix), correct_result)

    def test_get_id_no_id(self):
        html = '<a href="www.blah.com/blah/" onclick="test">my link</a>'
        node = HTMLParser(html).css_first('a')
        self.assertIsNone(_get_id(node, self._prefix))

    def test_get_id_no_href(self):
        html = '<a onclick="test">my link</a>'
        node = HTMLParser(html).css_first('a')
        self.assertIsNone(_get_id(node, self._prefix))

    def test_get_id_none(self):
        self.assertIsNone(_get_id(None, self._prefix))


class TestGetCompanyId(unittest.TestCase):
    def test_get_company_id(self):
        html = '<a href="www.blah.com/blah/co123456/blah/" onclick="test">my link</a>'
        node = HTMLParser(html).css_first('a')
        correct_result = 'co123456'
        self.assertEqual(get_company_id(node), correct_result)


class TestGetNameId(unittest.TestCase):
    def test_get_name_id(self):
        html = '<a href="www.blah.com/blah/nm123456/blah/" onclick="test">my link</a>'
        node = HTMLParser(html).css_first('a')
        correct_result = 'nm123456'
        self.assertEqual(get_name_id(node), correct_result)


class TestGetTitleId(unittest.TestCase):
    def test_get_name_id(self):
        html = '<a href="www.blah.com/blah/tt123456/blah/" onclick="test">my link</a>'
        node = HTMLParser(html).css_first('a')
        correct_result = 'tt123456'
        self.assertEqual(get_title_id(node), correct_result)


class TestGetFromOnclick(unittest.TestCase):
    _index = 1

    def test_get_from_onclick_correct(self):
        html = '<a href="www.blah.com" onclick="\'test1\',\'test2\',\'test3\'" class="testClass">my link</a>'
        node = HTMLParser(html).css_first('a')
        correct_result = 'test2'
        self.assertEqual(_get_from_onclick(node, self._index), correct_result)

    def test_get_from_onclick_too_few(self):
        html = '<a href="www.blah.com" onclick="\'test1\'" class="testClass">my link</a>'
        node = HTMLParser(html).css_first('a')
        self.assertIsNone(_get_from_onclick(node, self._index))

    def test_get_from_onclick_no_onclick(self):
        html = '<a href="www.blah.com" class="testClass">my link</a>'
        node = HTMLParser(html).css_first('a')
        self.assertIsNone(_get_from_onclick(node, self._index))

    def test_get_from_onclick_none(self):
        self.assertIsNone(_get_from_onclick(None, self._index))


class TestGetCategory(unittest.TestCase):
    def test_get_category(self):
        html = '<a href="www.blah.com" onclick="\'test1\',\'test2\',\'test3\',\'test4\',\'test5\',\'test6\'"' + \
                'class="testClass">my link</a>'
        node = HTMLParser(html).css_first('a')
        correct_result = 'test4'
        self.assertEqual(get_category(node), correct_result)


class TestGetRefMarker(unittest.TestCase):
    def test_get_category(self):
        html = '<a href="www.blah.com" onclick="\'test1\',\'test2\',\'test3\',\'test4\',\'test5\',\'test6\'"' + \
               'class="testClass">my link</a>'
        node = HTMLParser(html).css_first('a')
        correct_result = 'test5'
        self.assertEqual(get_ref_marker(node), correct_result)


class TestTrimYear(unittest.TestCase):
    def test_trim_year_None(self):
        self.assertIsNone(trim_year(None))

    def test_trim_year_no_roman_numerals(self):
        s = '1999'
        correct_result = '1999'
        self.assertEqual(trim_year(s), correct_result)

    def test_trim_year_roman_numerals(self):
        s1 = '1999/I'
        s2 = '1999/IV'
        s3 = '1999/VII'
        correct_result = '1999'
        self.assertEqual(trim_year(s1), correct_result)
        self.assertEqual(trim_year(s2), correct_result)
        self.assertEqual(trim_year(s3), correct_result)


class TestIsMoneyString(unittest.TestCase):
    def test_is_money_string_no_commas(self):
        s = '$123'
        self.assertTrue(is_money_string(s))

    def test_is_money_string_single_comma(self):
        s = '$123,456'
        self.assertTrue(is_money_string(s))

    def test_is_money_string_multiple_commas(self):
        s = '$123,456,789'
        self.assertTrue(is_money_string(s))

    def test_is_money_string_incorrect_format(self):
        s = '123,456'
        self.assertFalse(is_money_string(s))


class TestTrimMoneyString(unittest.TestCase):
    def test_trim_money_string_no_commas(self):
        s = '$123'
        correct_result = '123'
        self.assertEqual(trim_money_string(s), correct_result)

    def test_trim_money_string_single_comma(self):
        s = '$123,456'
        correct_result = '123456'
        self.assertEqual(trim_money_string(s), correct_result)

    def test_trim_money_string_multiple_commas(self):
        s = '$123,456,789'
        correct_result = '123456789'
        self.assertEqual(trim_money_string(s), correct_result)

    def test_trim_money_string_incorrect_format(self):
        s = '123,456'
        correct_result = '123,456'
        self.assertEqual(trim_money_string(s), correct_result)


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

    def test_is_float_none(self):
        self.assertFalse(is_float(None))


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

    def test_is_int_none(self):
        self.assertFalse(is_int(None))


class TestToBool(unittest.TestCase):
    def test_to_bool_boolean_true(self):
        b = True
        self.assertTrue(to_bool(b))

    def test_to_bool_boolean_false(self):
        b = False
        self.assertFalse(to_bool(b))

    def test_to_bool_string_true(self):
        b = '1'
        self.assertTrue(to_bool(b))

    def test_to_bool_string_false(self):
        b = '0'
        self.assertFalse(to_bool(b))

    def test_to_bool_int_true(self):
        b = 1
        self.assertTrue(to_bool(b))

    def test_to_bool_int_false(self):
        b = 0
        self.assertFalse(to_bool(b))

    def test_to_bool_none(self):
        self.assertFalse(to_bool(None))


class TestToDatetime(unittest.TestCase):
    _correct_date = datetime(1999, 8, 21)

    def test_to_datetime_format1(self):
        d = '21 August 1999'
        self.assertEqual(to_datetime(d), self._correct_date)

    def test_to_datetime_format2(self):
        d = '1999'
        self.assertEqual(to_datetime(d).year, self._correct_date.year)

    def test_to_datetime_format3(self):
        d = '1999-08-21'
        self.assertEqual(to_datetime(d), self._correct_date)

    def test_to_datetime_unsupported_format(self):
        d = 'August 21, 1999'
        with self.assertRaises(ValueError):
            to_datetime(d)

    def test_to_datetime_not_date(self):
        d = 'test'
        with self.assertRaises(ValueError):
            to_datetime(d)

    def test_to_datetime_none(self):
        self.assertIsNone(to_datetime(None))


if __name__ == '__main__':
    unittest.main()
