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
_SUPPORTED_DENOMINATIONS = '|'.join((r'\$', 'GBP'))


def append_filename_to_path(path, filename):
    """Append a filename to a system file path.

    This method correctly appends a filename to a file path with the
    correct path separators used within the path string.

    Args:
        path (:obj:`str`): The system file path.
        filename (:obj:`str`): The filename to append.

    Returns:
        :obj:`str`: The filename correctly appended to the file path.
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
    outfile name. If the infile's filename ends with "`.gz`", the oufile
    will be the same filename with the gzip extension removed. The function is
    also capable of deleteing the gzipped infile afterwards.

    Args:
        infile (:obj:`str`): The gzipped file's filename.
        outfile (:obj:`str`, optional): The filename to unzip the infile to, or `None` to use
            the default filename.
        delete_infile (:obj:`bool`, optional): Determine if the gzipped infile should be deleted
            after it is unzipped to the outfile.

    Returns:
        :obj:`str`: The outfile's filename for the case when the default filename was used.
    """

    if outfile is None:
        if infile[-3:] == '.gz':
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
    r"""Process a row of data from the IMDb datasets.

    Replaces all "`\\N`" characters in the IMDb dataset with `None`.

    Args:
        lst (:obj:`list` of :obj:`str`): A list of strings to process.

    Returns:
        :obj:`list` of :obj:`str`: A list of strings with all "`\\N`" strings being set to `None`.
    """

    for i, item in enumerate(lst):
        if item == '\\N':
            lst[i] = None
    return lst


def split_by_br(s):
    r"""Split a string by `<br>` tags.

    Splits by replacing each `<br>` tag with a "`\\t`" character
    and then splitting.

    Args:
        s (:obj:`str`): A string containing `<br>` tags.    

    Returns:
        :obj:`list`: A list of strings split around the `<br>` tags.
    """

    return re.sub(r'<\s*b\s*r\s*/?\s*>', '\t', s).split('\t')


def remove_tags(s, tag):
    """Removes the specified opening and closing tags of the given type.

    This method does not remove content between the tags, rather just
    the tags themselves. For example: "`td`" to remove all table column tags.

    Args:
        s (:obj:`str`): The HTML to parse.
        tag (:obj:`str`): The tag to be removed.

    Returns:
        :obj:`str`: A string with all of the given tags removed, but other
        HTML information intact.
    """

    return re.sub(rf'(<\s*{tag}.*?>|<\s*/\s*{tag}\s*>)', '', s)


def remove_tags_and_content(s, tag):
    """Removes all of the specified tags from the string including their children.

    Greedily finds an opening and closing of specified tag and removes all content
    between the two. 
    **Note**: Not intended to remove multiple sibling nodes with content in between.

    Args:
        s (:obj:`str`): The HTML to parse.
        tag (:obj:`str`): The tag to be removed.

    Returns:
        :obj:`str`: A string with all of the specified tags and their content removed.
    """

    return re.sub(rf'<\s*{tag}.*?>(.|\r|\n)*<\s*/\s*{tag}\s*>', '', s)


def _get_id(node, prefix):
    """Private function to find an IMDb ID within a link node.

    Will only look for the IMDb ID within the "`href`" attribute of a
    selectolax `Node`.

    Args:
        node (:class:`Node`): A `Node` containing the "`href`" attribute.
        prefix (:obj:`str`): The IMDb ID prefix (`co`, `nm`, or `tt`).

    Returns:
        :obj:`str`: The IMDb ID, or `None` if none was found.
    """
    if node and 'href' in node.attributes:
        id_match = re.search(rf'{prefix}\d+', node.attributes['href'])
        if id_match:
            return id_match.group(0)
    return None


def get_company_id(node):
    """Find the IMDb company ID within a selectolax `Node`.

    Expects the ID to be within the `Node`'s "`href`" attribute.

    Args:
        node (:class:`Node`): A `Node` containing the ID.

    Returns:
        :obj:`str`: The IMDb company ID.
    """

    return _get_id(node, 'co')


def get_name_id(node):
    """Find the IMDb name ID within a selectolax `Node`.

    Expects the ID to be within the `Node`'s "`href`" attribute.

    Args:
        node (:class:`Node`): A `Node` containing the ID.

    Returns:
        :obj:`str`: The IMDb name ID.
    """

    return _get_id(node, 'nm')


def get_title_id(node):
    """Find the IMDb title ID within a selectolax `Node`.

    Expects the ID to be within the `Node`'s "`href`" attribute.

    Args:
        node (:obj:`Node`): A `Node` containing the ID.

    Returns:
        :obj:`str`: The IMDb title ID.
    """

    return _get_id(node, 'tt')


def _get_from_onclick(node, index):
    """Private function to grab a value in the "`onclick`" attribute.

    Grabs the value in the specified index of the "`onclick`" attribute
    of a selectolax `Node`.

    Args:
        node (:class:`Node`): A `Node` containing the "`onclick`" attribute.
        index (:obj:`int`): The index of the value to grab.
    
    Returns:
        :obj:`str`: The value found within the "`onclick`" attribute,
        or `None` if it was not found.
    """

    if node and 'onclick' in node.attributes:
        onclick_split = node.attributes['onclick'].split(',')
        if len(onclick_split) > index:
            return onclick_split[index].strip('\'')
    return None


def get_category(node):
    """Gets the category value from a selectolax `Node`.

    Grabs the value from the `Node`'s "`onclick`" attribute.

    Args:
        node (:class:`Node`): A `Node` containing the "`onclick`" attribute.

    Returns:
        :obj:`str`: The category.
    """

    return _get_from_onclick(node, _CATEGORY_INDEX)


def get_ref_marker(node):
    """Gets the ref marker value from a selectolax `Node`.

    Grabs the value from the `Node`'s "`onclick`" attribute.

    Args:
        node (:class:`Node`): A `Node` containing the "`onclick`" attribute.

    Returns:
        :obj:`str`: The ref marker.
    """

    return _get_from_onclick(node, _REF_MARKER_INDEX)

def get_episode_info(node):
    """Gets the episode count, episode year start, and episode year end for an actor.

    Gets the episode information for an actor's credit within an IMDb TV series. The format
    the information is expected is: "`episode count` episodes, `episode year start`-`episode
    year end`". Single episodes/years are also handled. For example:

    - 124 episodes, 1999-2013
    - 2 episodes, 2010
    - 1 episode

    Args:
        node (:class:`Node`): A `Node` containing the episode information.

    Returns:
        (:obj:`int`, :obj:`int`, :obj:`int`): 
            The episode count, episode start year, and episode end year, or `None` if a value is not found.
    """

    episode_count = None
    episode_year_start = None
    episode_year_end = None

    if node:
        episode_count_str = None
        episode_year_start_str = None
        episode_year_end_str = None
        episode_info = re.sub(
            r'<\s*span.*?<\s*/\s*span\s*>', '', node.text()
        ).strip().split(',')
        if len(episode_info) > 1:
            episode_count_str, episode_year_info = episode_info
            episode_year_info = episode_year_info.strip().split('-')
            if len(episode_year_info) > 1:
                episode_year_start_str, episode_year_end_str = episode_year_info
            else:
                episode_year_start_str, = episode_year_info
        else:
            episode_count_str, = episode_info
        episode_count_match = re.search(r'\d+', episode_count_str)
        if episode_count_match:
            episode_count_str = episode_count_match.group(0)
        # Convert values to ints
        if is_int(episode_count_str):
            episode_count = int(episode_count_str)
        if is_int(episode_year_start_str):
            episode_year_start = int(episode_year_start_str)
        if is_int(episode_year_end_str):
            episode_year_end = int(episode_year_end_str)
    return episode_count, episode_year_start, episode_year_end


def trim_year(year):
    """Used to trim roman numerals from year values.

    IMDb differentiates movies of the same title and the same year with
    the format: `YYYY/<Roman numeral>`. This function removes the roman numerals
    and returns just the year value.

    Args:
        year (:obj:`str`): The year and roman numeral combination.

    Returns:
        :obj:`str`: The year with roman numerals removed, or `None` if year was `None`.
    """

    return re.sub(r'/\w*', '', year) if year is not None else None


def is_money_string(s):
    """Determine if a string is in a money format.

    Determines if the string represents a monetary value, for example: $123,456,789.

    Args:
        s (:obj:`str`): The monetary amount to check.

    Returns:
        :obj:`bool`: If the string does represent a monetary value for not.
    """

    return True if re.search(rf'({_SUPPORTED_DENOMINATIONS})[\d,]+', s) else False


def trim_money_string(s):
    """Trims excess characters from a monetary value.

    Only keeps the digits within a monetary value, such as trimming `$123,456` to `123456`. Trims dollar signs and commas.

    Args:
        s (:obj:`str`): The monetary amount to trim.

    Returns:
        :obj:`str`: The same monetary amount with excess characters removed.
    """

    money_match = re.search(rf'({_SUPPORTED_DENOMINATIONS})[\d,]+', s)
    if money_match:
        return re.sub(rf'({_SUPPORTED_DENOMINATIONS}|,)+', '', money_match.group(0))
    return s

def get_denomination(s):
    """Returns the monetary denomination for the given monetary value.

    Checks if the monetary value has one of the supported denominations. In the case it is a US dollar ($), the
    dollar sign character is replaced with "`USD`". Currently supported denominations:

    - `GBP`
    - `USD` ($)

    Args:
        s(:obj:`str`): The monetary amount to retrieve the denomination from.

    Returns:
        :obj:`str`: The denomination type, or `None` if not a monetary value or supported denomination.
    """

    if is_money_string(s):
        denomination_match = re.search(rf'({_SUPPORTED_DENOMINATIONS})', s)
        if denomination_match:
            denomination = denomination_match.group(0)
            if denomination == '$':
                denomination = 'USD'
            return denomination
    return None


def is_float(f):
    """Check if a variable is a `float` type.
    
    Args:
        f: The object to check.

    Returns:
        :obj:`bool`: If the object can be converted to a :obj:`float`.
    """

    if not f:
        return False
    try:
        float(f)
        return True
    except ValueError:
        return False


def is_int(i):
    """Check if a variable is an `int` type.
    
    Args:
        i: The object to check.

    Returns:
        :obj:`bool`: If the object can be converted to an :obj:`int`.
    """

    if not i:
        return False
    try:
        int(i)
        return True
    except ValueError:
        return False


def to_bool(b):
    """Convert a variable to a `boolean` type.
    
    Args:
        b: The object to convert.

    Returns:
        :obj:`bool`: The `boolean` representation of the object.
    """

    if is_int(b):
        return bool(int(b))
    return bool(b)


def to_datetime(d):
    """Convert a variable to a `datetime` object.

    Checks various formats used in IMDb to convert the variable to a
    `datetime` object under those formats. The formats include:

    - `%d %B %Y`
    - `%Y`
    - `%Y-%m-%d`

    Args:
        d (:obj:`str`): A string to convert to a `datetime` object.
    
    Returns:
        :obj:`datetime`: A `datetime` object that was represented by the string, or `None` if `d` is `None`.
    
    Raises:
        :class:`ValueError`: If the string could not be converted.
    """

    if not d:
        return None
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
