"""Module containing various utility functions used within other PyMDb modules.

The functions within here are not intended to be used outside of the PyMDb package.
"""

import gzip
import os
import re
import shutil
from datetime import datetime

_CATEGORY_INDEX = 3
_REF_MARKER_INDEX = 4


# TODO: add all error checking
def append_filename_to_path(path, filename):
    """Append a filename to a system file path.

    This method correctly appends a filename to a file path with the
    correct path separators used within the path string.

    Args:
        path: A string representing the system file path.
        filename: A string representing the filename.

    Returns:
        A string of the filename correctly appended to the file path.
    """

    if len(path) > 0 and path[-1] in ('/', '\\'):
        return f'{path}{filename}'
    else:
        if '\\' in path:
            return f'{path}\\{filename}'
        else:
            return f'{path}/{filename}'


def gunzip_file(infile, outfile=None, delete_infile=False):
    """Unzips a gzip file and returns the unzipped filename.

    Unzips the given gzipped file into the specified outfile, or a default
    outfile name. If the infile's filename ends with '.gz', the oufile
    will be the same filename with the gzip extension removed. The function is
    also capable of deleteing the gzipped infile afterwards.

    Args:
        infile: A string of the gzipped file's filename.
        outfile: A string of the filename to unzip the infile to, or None to use
            the default filename.
        delete_infile: A boolean to determine if the gzipped infile should be deleted
            after it is unzipped to the outfile.

    Returns:
        A string of the outfile's filename for the case when the default filename was used.
    """

    if outfile is None and len(infile) > 3 and infile[-3:] == '.gz':
        outfile = infile[:-3]
    else:
        outfile = f'{infile}.out'
    with gzip.open(infile, mode='rb') as f_in:
        with open(outfile, mode='wb') as f_out:
            shutil.copyfileobj(f_in, f_out)
    if delete_infile:
        os.remove(infile)
    return outfile


def preprocess_list(lst):
    """Process a row of data from the IMDb datasets.

    Replaces all '\N' characters in the IMDb dataset with None.

    Args:
        lst: A list of strings after the row has been tab-split.

    Returns:
        A list of strings with all '\N' strings being set to None.
    """

    for i, item in enumerate(lst):
        if item == '\\N':
            lst[i] = None
    return lst


def split_by_br(s):
    """Split a string by <br> tags.

    Splits by replacing each <br> tag with a '\t' character
    and then splitting.

    Args:
        s: A string containing <br> tags.    

    Returns:
        A list of strings split around the <br> tags.
    """

    return re.sub(r'<\s*b\s*r\s*/?\s*>', '\t', s).split('\t')


def remove_divs(s):
    """Removes all <div> tags from the string including their children.

    Greedily finds an opening and closing <div> tag and removes all content
    between the two.

    Args:
        s: A string containing HTML information.

    Returns:
        A string with all <div> tags and their content removed.
    """

    return re.sub(r'<\s*div.*>(.|\r|\n)*<\s*/\s*div\s*>', '', s)


def remove_tags(s, tag):
    """Removes the specified opening and closing tags of the given type.

    This method does not remove content between the tags, rather just
    the tags themselves. An example for tag would be: 'td' to remove
    all table column tags.

    Args:
        s: A string containing HTML information.
        tag: A string with the tagname to be removed.

    Returns:
        A string with all of the given tags removed, but other
        HTML information intact.
    """

    return re.sub(rf'(<\s*{tag}.*>|<\s*/{tag}\s*>)', '', s)


def _get_id(node, prefix):
    """Private function to find an IMDb ID within a link node

    Will only look for the IMDb ID within the 'href' attribute of a
    selectolax Node.

    Args:
        node: A selectolax Node containing the 'href' attribute.
        prefix: A string of the IMDb ID prefix ('co', 'nm', or 'tt').

    Returns:
        A string of the IMDb ID, or None if none was found.
    """
    if node and 'href' in node.attributes:
        id_match = re.search(rf'{prefix}\d+', node.attributes['href'])
        if id_match:
            return id_match.group(0)
    return None


def get_company_id(node):
    """Find the IMDb company ID within a selectolax Node.

    Expects the ID to be within the Node's 'href' attribute.

    Args:
        node: A selectolax Node containing the ID.

    Returns:
        A string representing the IMDb company ID.
    """

    return _get_id(node, 'co')


def get_name_id(node):
    """Find the IMDb name ID within a selectolax Node.

    Expects the ID to be within the Node's 'href' attribute.

    Args:
        node: A selectolax Node containing the ID.

    Returns:
        A string representing the IMDb name ID.
    """

    return _get_id(node, 'nm')


def get_title_id(node):
    """Find the IMDb title ID within a selectolax Node.

    Expects the ID to be within the Node's 'href' attribute.

    Args:
        node: A selectolax Node containing the ID.

    Returns:
        A string representing the IMDb title ID.
    """

    return _get_id(node, 'tt')


def _get_from_onclick(node, index):
    """Private function to grab a value in the 'onclick' attribute.

    Grabs the value in the specified index of the 'onclick' attribute
    of a selectolax Node.

    Args:
        node: A selectolax Node containing the 'onclick' attribute.
        index: An integer of the index of the value to grab.
    
    Returns:
        A string of the value grabbed within the 'onclick' attribute,
        or None if it was not found.
    """

    if 'onclick' in node.attributes:
        onclick_split = node.attributes['onclick'].split(',')
        if len(onclick_split) >= index:
            return onclick_split[index].strip('\'')
    return None


def get_category(node):
    """Gets the category value from a selectolax Node.

    Grabs the value from the Node's 'onclick' attribute.

    Args:
        node: A selectolax Node containing the 'onclick' attribute.

    Returns:
        A string representing the category.
    """

    return _get_from_onclick(node, _CATEGORY_INDEX)


def get_ref_marker(node):
    """Gets the ref marker value from a selectolax Node.

    Grabs the value from the Node's 'onclick' attribute.

    Args:
        node: A selectolax Node containing the 'onclick' attribute.

    Returns:
        A string representing the ref marker.
    """

    return _get_from_onclick(node, _REF_MARKER_INDEX)


def trim_year(year):
    """Used to trim roman numerals from year values.

    IMDb differentiates movies of the same title and the same year with
    the format: YYYY/<Roman numeral>. This function removes the roman numerals
    and returns just the year value.

    Args:
        year: A string representing the year and roman numeral combination.

    Returns:
        A string representation of the year, or None if year was None.
    """

    return re.sub(r'/\w*', '', year) if year is not None else None


def is_money_string(s):
    """Determine if a string is in a money format.

    Determines if the string represents a monetary value, for example: $123,456,789.

    Args:
        s: A string representation of the monetary amount.

    Returns:
        A boolean for if the string does represent a monetary value for not.
    """

    return True if re.search(r'\$[\d,]+', s) else False


def trim_money_string(s):
    """Trims excess characters from a monetary value

    Only keeps the digits within a monetary value, such as $123,456 to 123456. Trims dollar signs and commas.

    Args:
        s: A string representation of the monetary amount.

    Returns:
        A string of the same amount with excess characters removed.
    """

    money_match = re.search(r'\$[\d,]+', s)
    if money_match:
        return re.sub(r'[$,]+', '', money_match.group(0))
    return None


def is_bool(b):
    """Check if a variable is a boolean type."""

    try:
        bool(b)
        return True
    except ValueError:
        return False


def is_float(f):
    """Check if a variable is a float type."""

    try:
        float(f)
        return True
    except ValueError:
        return False


def is_int(i):
    """Check if a variable is an int type."""

    try:
        int(i)
        return True
    except ValueError:
        return False


def is_datetime(d):
    """Check if a variable can be converted to a datetime object.

    Checks various formats used in IMDb if the variable can be
    formatted to a datetime object under those types. The types include:
    - %d %B %Y
    - %Y
    - %Y-%m-%d

    Args:
        d: A variable to check.
    
    Returns:
        A boolean determining the variable can be converted or not.
    """

    try:
        datetime.strptime(d, '%d %B %Y')
        return True
    except ValueError:
        try:
            datetime.strptime(d, '%Y')
            return True
        except ValueError:
            try:
                datetime.strptime(d, '%Y-%m-%d')
                return True
            except ValueError:
                return False


def to_datetime(d):
    """Convert a variable can be converted to a datetime object.

    Checks various formats used in IMDb to convert the variable to a
    datetime object under those types. The types include:
    - %d %B %Y
    - %Y
    - %Y-%m-%d

    Args:
        d: A string to convert to a datetime object.
    
    Returns:
        A datetime object that was represented by the string.
    
    Raises:
        ValueError: If the string could not be converted.
    """

    try:
        return datetime.strptime(d, '%d %B %Y')
    except ValueError:
        try:
            return datetime.strptime(d, '%Y')
        except ValueError:
            try:
                return datetime.strptime(d, '%Y-%m-%d')
            except ValueError as e:
                raise e
