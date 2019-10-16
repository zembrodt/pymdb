import gzip, os, shutil
from datetime import datetime

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
            return False

def to_datetime(d):
    try:
        return datetime.strptime(d, '%d %B %Y')
    except ValueError:
        try:
            return datetime.strptime(d, '%Y')
        except ValueError as e:
            raise e