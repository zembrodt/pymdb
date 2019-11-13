# PyMDb  
  
PyMDb is a package for both parsing the datasets provided by IMDb and scraping information from their web pages.  
  
This package is able to gather information on people, titles, and companies provided by IMDb and is split into two separate modules: one for parsing the IMDb datasets, and one for scraping webpages on [imdb.com](http://imdb.com/).  
  
## Installation  
  
The latest release of PyMDb can be installed from PyPI with:  
  
```pip install py-mdb```  
  
If downloading the source from GitHub, PyMDb requires the following packages:  
  
- [requests](https://github.com/psf/requests)  
- [selectolax](https://github.com/rushter/selectolax)  
  
## Usage  
  
```python 
import pymdb
from collections import defaultdict

parser = pymdb.PyMDbParser(gunzip_files=True)  
genre_count = defaultdict(int)  
for title in parser.get_title_basics('path/to/files'):  
    for genre in title.genres:  
        genre_count[genre] += 1
for genre in genre_count:  
    print(f'{genre}: {genre_count[genre]}')
  
scraper = pymdb.PyMDbScraper()  
title = scraper.get_title('tt0076759')  
print(f'{title.title_text} came out in {title.release_date.year}!')  
```  
  
## Documentation  
  
Full documentation can be found at the [PyMDb Read the Docs](https://pymdb.readthedocs.io/) page.  
  
## License

This project is licensed under the MIT License. Please see the [LICENSE](https://github.com/zembrodt/pymdb/blob/master/LICENSE) file for details.