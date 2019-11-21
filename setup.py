import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name='py-mdb',
    version='0.1.1',
    author='Ryan Zembrodt',
    author_email='ryan.zembrodt@gmail.com',
    description='Package for parsing IMDb datasets and scraping web pages',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/zembrodt/pymdb',
    packages=setuptools.find_packages(),
    python_requires='>=3.6.0, <3.8.0',
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.6',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    keywords = ['imdb', 'pymdb', 'movie', 'film', 'tv', 'series', 'show', 'episode', 
    'database', 'db', 'dataset', 'web scrape', 'scrape', 'actor', 'actress', 'director',
    'writer', 'person', 'title', 'company', 'rating'
    ],
    install_requires=[
        'requests',
        'selectolax'
    ],
)
