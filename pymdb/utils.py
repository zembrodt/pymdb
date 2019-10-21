import gzip, os, re, shutil
from datetime import datetime

_CATEGORY_INDEX = 3
_REF_MARKER_INDEX = 4

# TODO: add all error checking
def append_filename_to_path(path, filename):
    if len(path) > 0 and path[-1] in ('/', '\\'):
        return f'{path}{filename}'
    else:
        if '\\' in path:
            return f'{path}\\{filename}'
        else:
            return f'{path}/{filename}'

def gunzip_file(infile, outfile=None, delete_infile=False):
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
    for i, item in enumerate(lst):
        if item == '\\N':
            lst[i] = None
    return lst

# Split a string of HTML by <br> tag
def split_by_br(s):
    return re.sub(r'<\s*b\s*r\s*\/?\s*>', '\t', s).split('\t')

def remove_divs(s):
    return re.sub(r'<\s*div.*>(.|\r|\n)*<\s*\/\s*div\s*>', '', s)

def remove_tags(s, tag):
    return re.sub(f'(<\s*{tag}.*>|<\s*\/{tag}\s*>)', '', s)

# IMDb IDs
def _get_id(node, prefix):
    if node and 'href' in node.attributes:
        id_match = re.search(f'{prefix}\d+', node.attributes['href'])
        if id_match:
            return id_match.group(0)
    return None

def get_company_id(node):
    return _get_id(node, 'co')

def get_name_id(node):
    return _get_id(node, 'nm')

def get_title_id(node):
    return _get_id(node, 'tt')

# Get value from onclick
def _get_from_onclick(node, index):
    if 'onclick' in node.attributes:
        onclick_split = node.attributes['onclick'].split(',')
        if len(onclick_split) >= index:
            return onclick_split[index].strip('\'')
    return None

# Get a category
def get_category(node):
    return _get_from_onclick(node, _CATEGORY_INDEX)

# Get a ref marker
def get_ref_marker(node):
    return _get_from_onclick(node, _REF_MARKER_INDEX)

# Duplicate movies of the same year are differentiated by YYYY/<Roman numeral>
# This function removes the roman numerals
def trim_year(year):
    return re.sub(r'\/\w*', '', year) if year is not None else None

def is_bool(b):
    try:
        bool(b)
        return True
    except ValueError:
        return False

def is_float(f):
    try:
        float(f)
        return True
    except ValueError:
        return False

def is_int(i):
    try:
        int(i)
        return True
    except ValueError:
        return False

def is_datetime(d):
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
    try:
        return datetime.strptime(d, '%d %B %Y')
    except ValueError:
        try:
            return datetime.strptime(d, '%Y')
        except ValueError as e:
            try:
                return datetime.strptime(d, '%Y-%m-%d')
            except ValueError as e:
                raise e