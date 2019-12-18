# PyMDb
[![PyPI](https://img.shields.io/pypi/v/py-mdb.svg)](https://pypi.org/project/py-mdb/)
[![Python Versions](https://img.shields.io/pypi/pyversions/py-mdb.svg)](https://pypi.org/project/py-mdb/)
[![License](https://img.shields.io/pypi/l/py-mdb.svg)](https://github.com/zembrodt/pymdb/blob/master/LICENSE)
[![Build Status](https://travis-ci.com/zembrodt/pymdb.svg?branch=master)](https://travis-ci.com/zembrodt/pymdb)

PyMDb is a package for both parsing the [datasets provided by IMDb](https://datasets.imdbws.com/) and scraping information from their web pages.

This package is able to gather information on people, titles, and companies provided by IMDb and is split into two separate modules: one for parsing the IMDb datasets, and one for scraping webpages on [imdb.com](http://imdb.com/).

## Installation

The latest release of PyMDb can be installed from PyPI with:

```pip install py-mdb```

If downloading the source from GitHub, PyMDb requires the following packages:

- [requests](https://github.com/psf/requests)
- [selectolax](https://github.com/rushter/selectolax)

## Usage

```python
>>> import pymdb
>>> from collections import defaultdict
>>>
>>> parser = pymdb.PyMDbParser(gunzip_files=True)
>>> genre_count = defaultdict(int)
>>> for title in parser.get_title_basics("path/to/files"):
...     for genre in title.genres:
...             genre_count[genre] += 1
...
>>> for genre in genre_count:
...     print(f"{genre}: {genre_count[genre]}")
...
Documentary: 600184
Short: 837912
Animation: 312227
    ...
Talk-Show: 584252
Reality-TV: 307037
Adult: 178493
>>>
>>> scraper = pymdb.PyMDbScraper()
>>> title = scraper.get_title("tt0076759")
>>> print(f"{title.display_title} came out in {title.release_date.year}!")
Star Wars: Episode IV - A New Hope came out in 1977!
```  

## Documentation

Full documentation can be found at the [PyMDb Read the Docs](https://pymdb.readthedocs.io/) page.

## Disclaimer

PyMDb is still in a pre-release state and has only been tested with a small amount of data found on [imdb.com](http://imdb.com/).
If any bugs or issues are found, please do not hesitate to create an issue or make a pull request on [GitHub](https://github.com/zembrodt/pymdb).
Suggestions for features to be added to PyMDb in future releases are also welcome!

## License

This project is licensed under the MIT License. Please see the [LICENSE](https://github.com/zembrodt/pymdb/blob/master/LICENSE) file for details.