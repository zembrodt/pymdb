"""Module to test functionality of the PyMDbParser."""

import unittest
from pymdb.parser import (
    PyMDbParser,
    _NAME_BASICS,
    _TITLE_AKAS,
    _TITLE_BASICS,
    _TITLE_CREW,
    _TITLE_EPISODE,
    _TITLE_PRINCIPALS,
    _TITLE_RATINGS
)
from pymdb.exceptions import InvalidParseFormat
import gzip
import os
from tempfile import TemporaryDirectory


class TestGetTitleAkas(unittest.TestCase):
    title_id = 'titleId'
    ordering = '5'
    title = 'title'
    region = 'region'
    language = 'language'
    types = 'alternative,tv'
    attributes = 'attr1,attr2'
    is_original_title = '1'
    akas1 = f'{title_id}\t{ordering}\t{title}\t{region}\t{language}\t{types}\t{attributes}\t{is_original_title}'
    akas2 = f'{title_id}\t{ordering}\t{title}\t{region}\t{language}\ttype\tattr\t{is_original_title}'
    content = f'{akas1}\n{akas2}\n'

    def test_default_filenames(self):
        parser = PyMDbParser()
        with TemporaryDirectory() as tmpdir:
            filename = os.path.join(tmpdir, _TITLE_AKAS.default_filename)
            with open(filename, 'w+') as f:
                f.write(self.content)
            title_akas = []
            for title_aka in parser.get_title_akas(tmpdir, contains_headers=False):
                title_akas.append(title_aka)
        self.assertEqual(len(title_akas), 2)
        actual1, actual2 = title_akas
        self.assertEqual(actual1.title_id, self.title_id)
        self.assertEqual(actual1.ordering, int(self.ordering))
        self.assertEqual(actual1.localized_title, self.title)
        self.assertEqual(actual1.region, self.region)
        self.assertEqual(actual1.language, self.language)
        self.assertEqual(actual1.types, self.types.split(','))
        self.assertEqual(actual1.attributes, self.attributes.split(','))
        self.assertTrue(actual1.is_original_title)
        self.assertEqual(actual2.types, ['type'])
        self.assertEqual(actual2.attributes, ['attr'])

    def test_custom_filenames(self):
        parser = PyMDbParser(use_default_filenames=False)
        with TemporaryDirectory() as tmpdir:
            filename = os.path.join(tmpdir, 'test.tsv')
            with open(filename, 'w+') as f:
                f.write(self.content)
            title_akas = []
            for title_aka in parser.get_title_akas(filename, contains_headers=False):
                title_akas.append(title_aka)
        self.assertEqual(len(title_akas), 2)
        actual1, actual2 = title_akas
        self.assertEqual(actual1.title_id, self.title_id)
        self.assertEqual(actual1.ordering, int(self.ordering))
        self.assertEqual(actual1.localized_title, self.title)
        self.assertEqual(actual1.region, self.region)
        self.assertEqual(actual1.language, self.language)
        self.assertEqual(actual1.types, self.types.split(','))
        self.assertEqual(actual1.attributes, self.attributes.split(','))
        self.assertTrue(actual1.is_original_title)
        self.assertEqual(actual2.types, ['type'])
        self.assertEqual(actual2.attributes, ['attr'])

    def test_gunzip_default_filenames(self):
        parser = PyMDbParser(gunzip_files=True)
        with TemporaryDirectory() as tmpdir:
            filename = os.path.join(tmpdir, f'{_TITLE_AKAS.default_filename}.gz')
            with gzip.open(filename, 'wb') as f:
                f.write(self.content.encode('utf-8'))
            title_akas = []
            for title_aka in parser.get_title_akas(tmpdir, contains_headers=False):
                title_akas.append(title_aka)
            self.assertTrue(os.path.exists(filename))
        self.assertEqual(len(title_akas), 2)
        actual1, actual2 = title_akas
        self.assertEqual(actual1.title_id, self.title_id)
        self.assertEqual(actual1.ordering, int(self.ordering))
        self.assertEqual(actual1.localized_title, self.title)
        self.assertEqual(actual1.region, self.region)
        self.assertEqual(actual1.language, self.language)
        self.assertEqual(actual1.types, self.types.split(','))
        self.assertEqual(actual1.attributes, self.attributes.split(','))
        self.assertTrue(actual1.is_original_title)
        self.assertEqual(actual2.types, ['type'])
        self.assertEqual(actual2.attributes, ['attr'])

    def test_gunzip_custom_filenames(self):
        parser = PyMDbParser(use_default_filenames=False, gunzip_files=True)
        with TemporaryDirectory() as tmpdir:
            filename = os.path.join(tmpdir, 'test.gz')
            with gzip.open(filename, 'wb') as f:
                f.write(self.content.encode('utf-8'))
            title_akas = []
            for title_aka in parser.get_title_akas(filename, contains_headers=False):
                title_akas.append(title_aka)
            self.assertTrue(os.path.exists(filename))
        self.assertEqual(len(title_akas), 2)
        actual1, actual2 = title_akas
        self.assertEqual(actual1.title_id, self.title_id)
        self.assertEqual(actual1.ordering, int(self.ordering))
        self.assertEqual(actual1.localized_title, self.title)
        self.assertEqual(actual1.region, self.region)
        self.assertEqual(actual1.language, self.language)
        self.assertEqual(actual1.types, self.types.split(','))
        self.assertEqual(actual1.attributes, self.attributes.split(','))
        self.assertTrue(actual1.is_original_title)
        self.assertEqual(actual2.types, ['type'])
        self.assertEqual(actual2.attributes, ['attr'])

    def test_gunzip_delete_default_filenames(self):
        parser = PyMDbParser(gunzip_files=True, delete_gzip_files=True)
        with TemporaryDirectory() as tmpdir:
            filename = os.path.join(tmpdir, f'{_TITLE_AKAS.default_filename}.gz')
            with gzip.open(filename, 'wb') as f:
                f.write(self.content.encode('utf-8'))
            title_akas = []
            for title_aka in parser.get_title_akas(tmpdir, contains_headers=False):
                title_akas.append(title_aka)
            self.assertFalse(os.path.exists(filename))
        self.assertEqual(len(title_akas), 2)
        actual1, actual2 = title_akas
        self.assertEqual(actual1.title_id, self.title_id)
        self.assertEqual(actual1.ordering, int(self.ordering))
        self.assertEqual(actual1.localized_title, self.title)
        self.assertEqual(actual1.region, self.region)
        self.assertEqual(actual1.language, self.language)
        self.assertEqual(actual1.types, self.types.split(','))
        self.assertEqual(actual1.attributes, self.attributes.split(','))
        self.assertTrue(actual1.is_original_title)
        self.assertEqual(actual2.types, ['type'])
        self.assertEqual(actual2.attributes, ['attr'])

    def test_gunzip_delete_custom_filenames(self):
        parser = PyMDbParser(use_default_filenames=False, gunzip_files=True, delete_gzip_files=True)
        with TemporaryDirectory() as tmpdir:
            filename = os.path.join(tmpdir, 'test.gz')
            with gzip.open(filename, 'wb') as f:
                f.write(self.content.encode('utf-8'))
            title_akas = []
            for title_aka in parser.get_title_akas(filename, contains_headers=False):
                title_akas.append(title_aka)
            self.assertFalse(os.path.exists(filename))
        self.assertEqual(len(title_akas), 2)
        actual1, actual2 = title_akas
        self.assertEqual(actual1.title_id, self.title_id)
        self.assertEqual(actual1.ordering, int(self.ordering))
        self.assertEqual(actual1.localized_title, self.title)
        self.assertEqual(actual1.region, self.region)
        self.assertEqual(actual1.language, self.language)
        self.assertEqual(actual1.types, self.types.split(','))
        self.assertEqual(actual1.attributes, self.attributes.split(','))
        self.assertTrue(actual1.is_original_title)
        self.assertEqual(actual2.types, ['type'])
        self.assertEqual(actual2.attributes, ['attr'])

    def test_contains_headers(self):
        parser = PyMDbParser()
        headers_content = f'headers\n{self.content}'
        with TemporaryDirectory() as tmpdir:
            filename = os.path.join(tmpdir, _TITLE_AKAS.default_filename)
            with open(filename, 'w+') as f:
                f.write(headers_content)
            title_akas = []
            for title_aka in parser.get_title_akas(tmpdir):
                title_akas.append(title_aka)
        self.assertEqual(len(title_akas), 2)
        actual1, actual2 = title_akas
        self.assertEqual(actual1.title_id, self.title_id)
        self.assertEqual(actual1.ordering, int(self.ordering))
        self.assertEqual(actual1.localized_title, self.title)
        self.assertEqual(actual1.region, self.region)
        self.assertEqual(actual1.language, self.language)
        self.assertEqual(actual1.types, self.types.split(','))
        self.assertEqual(actual1.attributes, self.attributes.split(','))
        self.assertTrue(actual1.is_original_title)
        self.assertEqual(actual2.types, ['type'])
        self.assertEqual(actual2.attributes, ['attr'])

    def test_incorrect_column_count(self):
        with TemporaryDirectory() as tmpdir:
            filename = os.path.join(tmpdir, _TITLE_AKAS.default_filename)
            with open(filename, 'w+') as f:
                f.write('headers\ntest1\ttest2')
            with self.assertRaises(InvalidParseFormat):
                for _ in PyMDbParser().get_title_akas(tmpdir):
                    pass

class TestGetTitleBasics(unittest.TestCase):
    title_id = 'titleId'
    title_type = 'titleType'
    primary_title = 'primaryTitle'
    original_title = 'originalTitle'
    is_adult = '0'
    start_year = '1999'
    end_year = '2013'
    runtime = '30'
    genres = 'comedy,action,drama'
    basics1 = f'{title_id}\t{title_type}\t{primary_title}\t{original_title}\t{is_adult}\t{start_year}\t{end_year}\t{runtime}\t{genres}'
    basics2 = f'{title_id}\t{title_type}\t{primary_title}\t{original_title}\t{is_adult}\t{start_year}\t\\N\t{runtime}\t{genres}'
    content = f'{basics1}\n{basics2}\n'

    def test_default_filenames(self):
        parser = PyMDbParser()
        with TemporaryDirectory() as tmpdir:
            filename = os.path.join(tmpdir, _TITLE_BASICS.default_filename)
            with open(filename, 'w+') as f:
                f.write(self.content)
            title_basics = []
            for title_basic in parser.get_title_basics(tmpdir, contains_headers=False):
                title_basics.append(title_basic)
        self.assertEqual(len(title_basics), 2)
        actual1, actual2 = title_basics
        self.assertEqual(actual1.title_id, self.title_id)
        self.assertEqual(actual1.title_type, self.title_type)
        self.assertEqual(actual1.primary_title, self.primary_title)
        self.assertEqual(actual1.original_title, self.original_title)
        self.assertFalse(actual1.is_adult)
        self.assertEqual(actual1.start_year, int(self.start_year))
        self.assertEqual(actual1.end_year, int(self.end_year))
        self.assertEqual(actual1.runtime_minutes, int(self.runtime))
        self.assertEqual(actual1.genres, self.genres.split(','))
        self.assertIsNone(actual2.end_year)

    def test_custom_filenames(self):
        parser = PyMDbParser(use_default_filenames=False)
        with TemporaryDirectory() as tmpdir:
            filename = os.path.join(tmpdir, 'test_file.tsv')
            with open(filename, 'w+') as f:
                f.write(self.content)
            title_basics = []
            for title_basic in parser.get_title_basics(filename, contains_headers=False):
                title_basics.append(title_basic)
        self.assertEqual(len(title_basics), 2)
        actual1, actual2 = title_basics
        self.assertEqual(actual1.title_id, self.title_id)
        self.assertEqual(actual1.title_type, self.title_type)
        self.assertEqual(actual1.primary_title, self.primary_title)
        self.assertEqual(actual1.original_title, self.original_title)
        self.assertFalse(actual1.is_adult)
        self.assertEqual(actual1.start_year, int(self.start_year))
        self.assertEqual(actual1.end_year, int(self.end_year))
        self.assertEqual(actual1.runtime_minutes, int(self.runtime))
        self.assertEqual(actual1.genres, self.genres.split(','))
        self.assertIsNone(actual2.end_year)

    def test_gunzip_default_filenames(self):
        parser = PyMDbParser(gunzip_files=True)
        with TemporaryDirectory() as tmpdir:
            filename = os.path.join(tmpdir, f'{_TITLE_BASICS.default_filename}.gz')
            with gzip.open(filename, 'wb') as f:
                f.write(self.content.encode('utf-8'))
            title_basics = []
            for title_basic in parser.get_title_basics(tmpdir, contains_headers=False):
                title_basics.append(title_basic)
            self.assertTrue(os.path.exists(filename))
        self.assertEqual(len(title_basics), 2)
        actual1, actual2 = title_basics
        self.assertEqual(actual1.title_id, self.title_id)
        self.assertEqual(actual1.title_type, self.title_type)
        self.assertEqual(actual1.primary_title, self.primary_title)
        self.assertEqual(actual1.original_title, self.original_title)
        self.assertFalse(actual1.is_adult)
        self.assertEqual(actual1.start_year, int(self.start_year))
        self.assertEqual(actual1.end_year, int(self.end_year))
        self.assertEqual(actual1.runtime_minutes, int(self.runtime))
        self.assertEqual(actual1.genres, self.genres.split(','))
        self.assertIsNone(actual2.end_year)

    def test_gunzip_custom_filenames(self):
        parser = PyMDbParser(use_default_filenames=False, gunzip_files=True)
        with TemporaryDirectory() as tmpdir:
            filename = os.path.join(tmpdir, 'test.gz')
            with gzip.open(filename, 'wb') as f:
                f.write(self.content.encode('utf-8'))
            title_basics = []
            for title_basic in parser.get_title_basics(filename, contains_headers=False):
                title_basics.append(title_basic)
            self.assertTrue(os.path.exists(filename))
        self.assertEqual(len(title_basics), 2)
        actual1, actual2 = title_basics
        self.assertEqual(actual1.title_id, self.title_id)
        self.assertEqual(actual1.title_type, self.title_type)
        self.assertEqual(actual1.primary_title, self.primary_title)
        self.assertEqual(actual1.original_title, self.original_title)
        self.assertFalse(actual1.is_adult)
        self.assertEqual(actual1.start_year, int(self.start_year))
        self.assertEqual(actual1.end_year, int(self.end_year))
        self.assertEqual(actual1.runtime_minutes, int(self.runtime))
        self.assertEqual(actual1.genres, self.genres.split(','))
        self.assertIsNone(actual2.end_year)

    def test_gunzip_delete_default_filenames(self):
        parser = PyMDbParser(gunzip_files=True, delete_gzip_files=True)
        with TemporaryDirectory() as tmpdir:
            filename = os.path.join(tmpdir, f'{_TITLE_BASICS.default_filename}.gz')
            with gzip.open(filename, 'wb') as f:
                f.write(self.content.encode('utf-8'))
            title_basics = []
            for title_basic in parser.get_title_basics(tmpdir, contains_headers=False):
                title_basics.append(title_basic)
            self.assertFalse(os.path.exists(filename))
        self.assertEqual(len(title_basics), 2)
        actual1, actual2 = title_basics
        self.assertEqual(actual1.title_id, self.title_id)
        self.assertEqual(actual1.title_type, self.title_type)
        self.assertEqual(actual1.primary_title, self.primary_title)
        self.assertEqual(actual1.original_title, self.original_title)
        self.assertFalse(actual1.is_adult)
        self.assertEqual(actual1.start_year, int(self.start_year))
        self.assertEqual(actual1.end_year, int(self.end_year))
        self.assertEqual(actual1.runtime_minutes, int(self.runtime))
        self.assertEqual(actual1.genres, self.genres.split(','))
        self.assertIsNone(actual2.end_year)

    def test_gunzip_delete_custom_filenames(self):
        parser = PyMDbParser(use_default_filenames=False, gunzip_files=True, delete_gzip_files=True)
        with TemporaryDirectory() as tmpdir:
            filename = os.path.join(tmpdir, 'test.gz')
            with gzip.open(filename, 'wb') as f:
                f.write(self.content.encode('utf-8'))
            title_basics = []
            for title_basic in parser.get_title_basics(filename, contains_headers=False):
                title_basics.append(title_basic)
            self.assertFalse(os.path.exists(filename))
        self.assertEqual(len(title_basics), 2)
        actual1, actual2 = title_basics
        self.assertEqual(actual1.title_id, self.title_id)
        self.assertEqual(actual1.title_type, self.title_type)
        self.assertEqual(actual1.primary_title, self.primary_title)
        self.assertEqual(actual1.original_title, self.original_title)
        self.assertFalse(actual1.is_adult)
        self.assertEqual(actual1.start_year, int(self.start_year))
        self.assertEqual(actual1.end_year, int(self.end_year))
        self.assertEqual(actual1.runtime_minutes, int(self.runtime))
        self.assertEqual(actual1.genres, self.genres.split(','))
        self.assertIsNone(actual2.end_year)

    def test_contains_headers(self):
        parser = PyMDbParser()
        headers_content = f'headers\n{self.content}'
        with TemporaryDirectory() as tmpdir:
            filename = os.path.join(tmpdir, _TITLE_BASICS.default_filename)
            with open(filename, 'w+') as f:
                f.write(headers_content)
            title_basics = []
            for title_basic in parser.get_title_basics(tmpdir):
                title_basics.append(title_basic)
        self.assertEqual(len(title_basics), 2)
        actual1, actual2 = title_basics
        self.assertEqual(actual1.title_id, self.title_id)
        self.assertEqual(actual1.title_type, self.title_type)
        self.assertEqual(actual1.primary_title, self.primary_title)
        self.assertEqual(actual1.original_title, self.original_title)
        self.assertFalse(actual1.is_adult)
        self.assertEqual(actual1.start_year, int(self.start_year))
        self.assertEqual(actual1.end_year, int(self.end_year))
        self.assertEqual(actual1.runtime_minutes, int(self.runtime))
        self.assertEqual(actual1.genres, self.genres.split(','))
        self.assertIsNone(actual2.end_year)

    def test_incorrect_column_count(self):
        with TemporaryDirectory() as tmpdir:
            filename = os.path.join(tmpdir, _TITLE_BASICS.default_filename)
            with open(filename, 'w+') as f:
                f.write('headers\ntest1\ttest2')
            with self.assertRaises(InvalidParseFormat):
                for _ in PyMDbParser().get_title_basics(tmpdir):
                    pass


class TestGetTitleCrew(unittest.TestCase):
    title_id = 'title_id'
    directors = 'director1,director2'
    writers = 'writer1,writer2'
    crew1 = f'{title_id}\t{directors}\t{writers}'
    crew2 = f'{title_id}\tdirector\twriter'
    content = f'{crew1}\n{crew2}\n'

    def test_default_filenames(self):
        parser = PyMDbParser()
        with TemporaryDirectory() as tmpdir:
            filename = os.path.join(tmpdir, _TITLE_CREW.default_filename)
            with open(filename, 'w+') as f:
                f.write(self.content)
            title_crew = []
            for title_crew_member in parser.get_title_crew(tmpdir, contains_headers=False):
                title_crew.append(title_crew_member)
        self.assertEqual(len(title_crew), 2)
        actual1, actual2 = title_crew
        self.assertEqual(actual1.title_id, self.title_id)
        self.assertEqual(actual1.director_ids, self.directors.split(','))
        self.assertEqual(actual1.writer_ids, self.writers.split(','))
        self.assertEqual(actual2.director_ids, ['director'])
        self.assertEqual(actual2.writer_ids, ['writer'])

    def test_custom_filenames(self):
        parser = PyMDbParser(use_default_filenames=False)
        with TemporaryDirectory() as tmpdir:
            filename = os.path.join(tmpdir, 'test.tsv')
            with open(filename, 'w+') as f:
                f.write(self.content)
            title_crew = []
            for title_crew_member in parser.get_title_crew(filename, contains_headers=False):
                title_crew.append(title_crew_member)
        self.assertEqual(len(title_crew), 2)
        actual1, actual2 = title_crew
        self.assertEqual(actual1.title_id, self.title_id)
        self.assertEqual(actual1.director_ids, self.directors.split(','))
        self.assertEqual(actual1.writer_ids, self.writers.split(','))
        self.assertEqual(actual2.director_ids, ['director'])
        self.assertEqual(actual2.writer_ids, ['writer'])

    def test_gunzip_default_filenames(self):
        parser = PyMDbParser(gunzip_files=True)
        with TemporaryDirectory() as tmpdir:
            filename = os.path.join(tmpdir, f'{_TITLE_CREW.default_filename}.gz')
            with gzip.open(filename, 'wb') as f:
                f.write(self.content.encode('utf-8'))
            title_crew = []
            for title_crew_member in parser.get_title_crew(tmpdir, contains_headers=False):
                title_crew.append(title_crew_member)
            self.assertTrue(os.path.exists(filename))
        self.assertEqual(len(title_crew), 2)
        actual1, actual2 = title_crew
        self.assertEqual(actual1.title_id, self.title_id)
        self.assertEqual(actual1.director_ids, self.directors.split(','))
        self.assertEqual(actual1.writer_ids, self.writers.split(','))
        self.assertEqual(actual2.director_ids, ['director'])
        self.assertEqual(actual2.writer_ids, ['writer'])

    def test_gunzip_custom_filenames(self):
        parser = PyMDbParser(use_default_filenames=False, gunzip_files=True)
        with TemporaryDirectory() as tmpdir:
            filename = os.path.join(tmpdir, 'test.gz')
            with gzip.open(filename, 'wb') as f:
                f.write(self.content.encode('utf-8'))
            title_crew = []
            for title_crew_member in parser.get_title_crew(filename, contains_headers=False):
                title_crew.append(title_crew_member)
            self.assertTrue(os.path.exists(filename))
        self.assertEqual(len(title_crew), 2)
        actual1, actual2 = title_crew
        self.assertEqual(actual1.title_id, self.title_id)
        self.assertEqual(actual1.director_ids, self.directors.split(','))
        self.assertEqual(actual1.writer_ids, self.writers.split(','))
        self.assertEqual(actual2.director_ids, ['director'])
        self.assertEqual(actual2.writer_ids, ['writer'])

    def test_gunzip_delete_default_filenames(self):
        parser = PyMDbParser(gunzip_files=True, delete_gzip_files=True)
        with TemporaryDirectory() as tmpdir:
            filename = os.path.join(tmpdir, f'{_TITLE_CREW.default_filename}.gz')
            with gzip.open(filename, 'wb') as f:
                f.write(self.content.encode('utf-8'))
            title_crew = []
            for title_crew_member in parser.get_title_crew(tmpdir, contains_headers=False):
                title_crew.append(title_crew_member)
            self.assertFalse(os.path.exists(filename))
        self.assertEqual(len(title_crew), 2)
        actual1, actual2 = title_crew
        self.assertEqual(actual1.title_id, self.title_id)
        self.assertEqual(actual1.director_ids, self.directors.split(','))
        self.assertEqual(actual1.writer_ids, self.writers.split(','))
        self.assertEqual(actual2.director_ids, ['director'])
        self.assertEqual(actual2.writer_ids, ['writer'])

    def test_gunzip_delete_custom_filenames(self):
        parser = PyMDbParser(use_default_filenames=False, gunzip_files=True, delete_gzip_files=True)
        with TemporaryDirectory() as tmpdir:
            filename = os.path.join(tmpdir, 'test.gz')
            with gzip.open(filename, 'wb') as f:
                f.write(self.content.encode('utf-8'))
            title_crew = []
            for title_crew_member in parser.get_title_crew(filename, contains_headers=False):
                title_crew.append(title_crew_member)
            self.assertFalse(os.path.exists(filename))
        self.assertEqual(len(title_crew), 2)
        actual1, actual2 = title_crew
        self.assertEqual(actual1.title_id, self.title_id)
        self.assertEqual(actual1.director_ids, self.directors.split(','))
        self.assertEqual(actual1.writer_ids, self.writers.split(','))
        self.assertEqual(actual2.director_ids, ['director'])
        self.assertEqual(actual2.writer_ids, ['writer'])

    def test_contains_headers(self):
        parser = PyMDbParser()
        headers_content = f'headers\n{self.content}'
        with TemporaryDirectory() as tmpdir:
            filename = os.path.join(tmpdir, _TITLE_CREW.default_filename)
            with open(filename, 'w+') as f:
                f.write(headers_content)
            title_crew = []
            for title_crew_member in parser.get_title_crew(tmpdir):
                title_crew.append(title_crew_member)
        self.assertEqual(len(title_crew), 2)
        actual1, actual2 = title_crew
        self.assertEqual(actual1.title_id, self.title_id)
        self.assertEqual(actual1.director_ids, self.directors.split(','))
        self.assertEqual(actual1.writer_ids, self.writers.split(','))
        self.assertEqual(actual2.director_ids, ['director'])
        self.assertEqual(actual2.writer_ids, ['writer'])

    def test_incorrect_column_count(self):
        with TemporaryDirectory() as tmpdir:
            filename = os.path.join(tmpdir, _TITLE_CREW.default_filename)
            with open(filename, 'w+') as f:
                f.write('headers\ntest1\ttest2')
            with self.assertRaises(InvalidParseFormat):
                for _ in PyMDbParser().get_title_crew(tmpdir):
                    pass


class TestGetTitleEpisodes(unittest.TestCase):
    title_id = 'titleId'
    parent_title_id = 'parentId'
    season_number = '5'
    episode_number = '4'
    episode = f'{title_id}\t{parent_title_id}\t{season_number}\t{episode_number}'
    content = f'{episode}\n{episode}\n'

    def test_default_filenames(self):
        parser = PyMDbParser()
        with TemporaryDirectory() as tmpdir:
            filename = os.path.join(tmpdir, _TITLE_EPISODE.default_filename)
            with open(filename, 'w+') as f:
                f.write(self.content)
            title_episodes = []
            for title_episode in parser.get_title_episodes(tmpdir, contains_headers=False):
                title_episodes.append(title_episode)
        self.assertEqual(len(title_episodes), 2)
        actual, _ = title_episodes
        self.assertEqual(actual.title_id, self.title_id)
        self.assertEqual(actual.parent_title_id, self.parent_title_id)
        self.assertEqual(actual.season_number, int(self.season_number))
        self.assertEqual(actual.episode_number, int(self.episode_number))

    def test_custom_filenames(self):
        parser = PyMDbParser(use_default_filenames=False)
        with TemporaryDirectory() as tmpdir:
            filename = os.path.join(tmpdir, 'test.tsv')
            with open(filename, 'w+') as f:
                f.write(self.content)
            title_episodes = []
            for title_episode in parser.get_title_episodes(filename, contains_headers=False):
                title_episodes.append(title_episode)
        self.assertEqual(len(title_episodes), 2)
        actual, _ = title_episodes
        self.assertEqual(actual.title_id, self.title_id)
        self.assertEqual(actual.parent_title_id, self.parent_title_id)
        self.assertEqual(actual.season_number, int(self.season_number))
        self.assertEqual(actual.episode_number, int(self.episode_number))

    def test_gunzip_default_filenames(self):
        parser = PyMDbParser(gunzip_files=True)
        with TemporaryDirectory() as tmpdir:
            filename = os.path.join(tmpdir, f'{_TITLE_EPISODE.default_filename}.gz')
            with gzip.open(filename, 'wb') as f:
                f.write(self.content.encode('utf-8'))
            title_episodes = []
            for title_episode in parser.get_title_episodes(tmpdir, contains_headers=False):
                title_episodes.append(title_episode)
            self.assertTrue(os.path.exists(filename))
        self.assertEqual(len(title_episodes), 2)
        actual, _ = title_episodes
        self.assertEqual(actual.title_id, self.title_id)
        self.assertEqual(actual.parent_title_id, self.parent_title_id)
        self.assertEqual(actual.season_number, int(self.season_number))
        self.assertEqual(actual.episode_number, int(self.episode_number))

    def test_gunzip_custom_filenames(self):
        parser = PyMDbParser(use_default_filenames=False, gunzip_files=True)
        with TemporaryDirectory() as tmpdir:
            filename = os.path.join(tmpdir, 'test.gz')
            with gzip.open(filename, 'wb') as f:
                f.write(self.content.encode('utf-8'))
            title_episodes = []
            for title_episode in parser.get_title_episodes(filename, contains_headers=False):
                title_episodes.append(title_episode)
            self.assertTrue(os.path.exists(filename))
        self.assertEqual(len(title_episodes), 2)
        actual, _ = title_episodes
        self.assertEqual(actual.title_id, self.title_id)
        self.assertEqual(actual.parent_title_id, self.parent_title_id)
        self.assertEqual(actual.season_number, int(self.season_number))
        self.assertEqual(actual.episode_number, int(self.episode_number))

    def test_gunzip_delete_default_filenames(self):
        parser = PyMDbParser(gunzip_files=True, delete_gzip_files=True)
        with TemporaryDirectory() as tmpdir:
            filename = os.path.join(tmpdir, f'{_TITLE_EPISODE.default_filename}.gz')
            with gzip.open(filename, 'wb') as f:
                f.write(self.content.encode('utf-8'))
            title_episodes = []
            for title_episode in parser.get_title_episodes(tmpdir, contains_headers=False):
                title_episodes.append(title_episode)
            self.assertFalse(os.path.exists(filename))
        self.assertEqual(len(title_episodes), 2)
        actual, _ = title_episodes
        self.assertEqual(actual.title_id, self.title_id)
        self.assertEqual(actual.parent_title_id, self.parent_title_id)
        self.assertEqual(actual.season_number, int(self.season_number))
        self.assertEqual(actual.episode_number, int(self.episode_number))

    def test_gunzip_delete_custom_filenames(self):
        parser = PyMDbParser(use_default_filenames=False, gunzip_files=True, delete_gzip_files=True)
        with TemporaryDirectory() as tmpdir:
            filename = os.path.join(tmpdir, 'test.gz')
            with gzip.open(filename, 'wb') as f:
                f.write(self.content.encode('utf-8'))
            title_episodes = []
            for title_episode in parser.get_title_episodes(filename, contains_headers=False):
                title_episodes.append(title_episode)
            self.assertFalse(os.path.exists(filename))
        self.assertEqual(len(title_episodes), 2)
        actual, _ = title_episodes
        self.assertEqual(actual.title_id, self.title_id)
        self.assertEqual(actual.parent_title_id, self.parent_title_id)
        self.assertEqual(actual.season_number, int(self.season_number))
        self.assertEqual(actual.episode_number, int(self.episode_number))

    def test_contains_headers(self):
        parser = PyMDbParser()
        headers_content = f'headers\n{self.content}'
        with TemporaryDirectory() as tmpdir:
            filename = os.path.join(tmpdir, _TITLE_EPISODE.default_filename)
            with open(filename, 'w+') as f:
                f.write(headers_content)
            title_episodes = []
            for title_episode in parser.get_title_episodes(tmpdir):
                title_episodes.append(title_episode)
        self.assertEqual(len(title_episodes), 2)
        actual, _ = title_episodes
        self.assertEqual(actual.title_id, self.title_id)
        self.assertEqual(actual.parent_title_id, self.parent_title_id)
        self.assertEqual(actual.season_number, int(self.season_number))
        self.assertEqual(actual.episode_number, int(self.episode_number))

    def test_incorrect_column_count(self):
        with TemporaryDirectory() as tmpdir:
            filename = os.path.join(tmpdir, _TITLE_EPISODE.default_filename)
            with open(filename, 'w+') as f:
                f.write('headers\ntest1\ttest2')
            with self.assertRaises(InvalidParseFormat):
                for _ in PyMDbParser().get_title_episodes(tmpdir):
                    pass


class TestGetTitlePrincipals(unittest.TestCase):
    title_id = 'titleId'
    ordering = '5'
    name_id = 'nameId'
    category = 'category'
    job = 'jobTitle'
    character1 = 'character1'
    character2 = 'character2'
    characters = f'["{character1}","{character2}"]'
    principal1 = f'{title_id}\t{ordering}\t{name_id}\t{category}\t{job}\t{characters}'
    principal2 = f'{title_id}\t{ordering}\t{name_id}\t{category}\t\\N\t\\N'
    content = f'{principal1}\n{principal2}\n'

    def test_default_filenames(self):
        parser = PyMDbParser()
        with TemporaryDirectory() as tmpdir:
            filename = os.path.join(tmpdir, _TITLE_PRINCIPALS.default_filename)
            with open(filename, 'w+') as f:
                f.write(self.content)
            title_principals = []
            for title_principal in parser.get_title_principals(tmpdir, contains_headers=False):
                title_principals.append(title_principal)
        self.assertEqual(len(title_principals), 2)
        actual1, actual2 = title_principals
        self.assertEqual(actual1.title_id, self.title_id)
        self.assertEqual(actual1.ordering, int(self.ordering))
        self.assertEqual(actual1.name_id, self.name_id)
        self.assertEqual(actual1.category, self.category)
        self.assertEqual(actual1.job, self.job)
        self.assertEqual(actual1.characters, [self.character1, self.character2])
        self.assertIsNone(actual2.job)
        self.assertEqual(actual2.characters, [])

    def test_custom_filenames(self):
        parser = PyMDbParser(use_default_filenames=False)
        with TemporaryDirectory() as tmpdir:
            filename = os.path.join(tmpdir, 'test.tsv')
            with open(filename, 'w+') as f:
                f.write(self.content)
            title_principals = []
            for title_principal in parser.get_title_principals(filename, contains_headers=False):
                title_principals.append(title_principal)
        self.assertEqual(len(title_principals), 2)
        actual1, actual2 = title_principals
        self.assertEqual(actual1.title_id, self.title_id)
        self.assertEqual(actual1.ordering, int(self.ordering))
        self.assertEqual(actual1.name_id, self.name_id)
        self.assertEqual(actual1.category, self.category)
        self.assertEqual(actual1.job, self.job)
        self.assertEqual(actual1.characters, [self.character1, self.character2])
        self.assertIsNone(actual2.job)
        self.assertEqual(actual2.characters, [])

    def test_gunzip_default_filenames(self):
        parser = PyMDbParser(gunzip_files=True)
        with TemporaryDirectory() as tmpdir:
            filename = os.path.join(tmpdir, f'{_TITLE_PRINCIPALS.default_filename}.gz')
            with gzip.open(filename, 'wb') as f:
                f.write(self.content.encode('utf-8'))
            title_principals = []
            for title_principal in parser.get_title_principals(tmpdir, contains_headers=False):
                title_principals.append(title_principal)
            self.assertTrue(os.path.exists(filename))
        self.assertEqual(len(title_principals), 2)
        actual1, actual2 = title_principals
        self.assertEqual(actual1.title_id, self.title_id)
        self.assertEqual(actual1.ordering, int(self.ordering))
        self.assertEqual(actual1.name_id, self.name_id)
        self.assertEqual(actual1.category, self.category)
        self.assertEqual(actual1.job, self.job)
        self.assertEqual(actual1.characters, [self.character1, self.character2])
        self.assertIsNone(actual2.job)
        self.assertEqual(actual2.characters, [])

    def test_gunzip_custom_filenames(self):
        parser = PyMDbParser(use_default_filenames=False, gunzip_files=True)
        with TemporaryDirectory() as tmpdir:
            filename = os.path.join(tmpdir, 'test.gz')
            with gzip.open(filename, 'wb') as f:
                f.write(self.content.encode('utf-8'))
            title_principals = []
            for title_principal in parser.get_title_principals(filename, contains_headers=False):
                title_principals.append(title_principal)
            self.assertTrue(os.path.exists(filename))
        self.assertEqual(len(title_principals), 2)
        actual1, actual2 = title_principals
        self.assertEqual(actual1.title_id, self.title_id)
        self.assertEqual(actual1.ordering, int(self.ordering))
        self.assertEqual(actual1.name_id, self.name_id)
        self.assertEqual(actual1.category, self.category)
        self.assertEqual(actual1.job, self.job)
        self.assertEqual(actual1.characters, [self.character1, self.character2])
        self.assertIsNone(actual2.job)
        self.assertEqual(actual2.characters, [])

    def test_gunzip_delete_default_filenames(self):
        parser = PyMDbParser(gunzip_files=True, delete_gzip_files=True)
        with TemporaryDirectory() as tmpdir:
            filename = os.path.join(tmpdir, f'{_TITLE_PRINCIPALS.default_filename}.gz')
            with gzip.open(filename, 'wb') as f:
                f.write(self.content.encode('utf-8'))
            title_principals = []
            for title_principal in parser.get_title_principals(tmpdir, contains_headers=False):
                title_principals.append(title_principal)
            self.assertFalse(os.path.exists(filename))
        self.assertEqual(len(title_principals), 2)
        actual1, actual2 = title_principals
        self.assertEqual(actual1.title_id, self.title_id)
        self.assertEqual(actual1.ordering, int(self.ordering))
        self.assertEqual(actual1.name_id, self.name_id)
        self.assertEqual(actual1.category, self.category)
        self.assertEqual(actual1.job, self.job)
        self.assertEqual(actual1.characters, [self.character1, self.character2])
        self.assertIsNone(actual2.job)
        self.assertEqual(actual2.characters, [])

    def test_gunzip_delete_custom_filenames(self):
        parser = PyMDbParser(use_default_filenames=False, gunzip_files=True, delete_gzip_files=True)
        with TemporaryDirectory() as tmpdir:
            filename = os.path.join(tmpdir, 'test.gz')
            with gzip.open(filename, 'wb') as f:
                f.write(self.content.encode('utf-8'))
            title_principals = []
            for title_principal in parser.get_title_principals(filename, contains_headers=False):
                title_principals.append(title_principal)
            self.assertFalse(os.path.exists(filename))
        self.assertEqual(len(title_principals), 2)
        actual1, actual2 = title_principals
        self.assertEqual(actual1.title_id, self.title_id)
        self.assertEqual(actual1.ordering, int(self.ordering))
        self.assertEqual(actual1.name_id, self.name_id)
        self.assertEqual(actual1.category, self.category)
        self.assertEqual(actual1.job, self.job)
        self.assertEqual(actual1.characters, [self.character1, self.character2])
        self.assertIsNone(actual2.job)
        self.assertEqual(actual2.characters, [])

    def test_contains_headers(self):
        parser = PyMDbParser()
        headers_content = f'headers\n{self.content}'
        with TemporaryDirectory() as tmpdir:
            filename = os.path.join(tmpdir, _TITLE_PRINCIPALS.default_filename)
            with open(filename, 'w+') as f:
                f.write(headers_content)
            title_principals = []
            for title_principal in parser.get_title_principals(tmpdir):
                title_principals.append(title_principal)
        self.assertEqual(len(title_principals), 2)
        actual1, actual2 = title_principals
        self.assertEqual(actual1.title_id, self.title_id)
        self.assertEqual(actual1.ordering, int(self.ordering))
        self.assertEqual(actual1.name_id, self.name_id)
        self.assertEqual(actual1.category, self.category)
        self.assertEqual(actual1.job, self.job)
        self.assertEqual(actual1.characters, [self.character1, self.character2])
        self.assertIsNone(actual2.job)
        self.assertEqual(actual2.characters, [])

    def test_incorrect_column_count(self):
        with TemporaryDirectory() as tmpdir:
            filename = os.path.join(tmpdir, _TITLE_PRINCIPALS.default_filename)
            with open(filename, 'w+') as f:
                f.write('headers\ntest1\ttest2')
            with self.assertRaises(InvalidParseFormat):
                for _ in PyMDbParser().get_title_principals(tmpdir):
                    pass


class TestGetTitleRatings(unittest.TestCase):
    title_id = 'titleId'
    average_rating = '1.25'
    num_votes = '10'
    rating = f'{title_id}\t{average_rating}\t{num_votes}'
    content = f'{rating}\n{rating}\n'

    def test_default_filenames(self):
        parser = PyMDbParser()
        with TemporaryDirectory() as tmpdir:
            filename = os.path.join(tmpdir, _TITLE_RATINGS.default_filename)
            with open(filename, 'w+') as f:
                f.write(self.content)
            title_ratings = []
            for title_rating in parser.get_title_ratings(tmpdir, contains_headers=False):
                title_ratings.append(title_rating)
        self.assertEqual(len(title_ratings), 2)
        actual1, actual2 = title_ratings
        self.assertEqual(actual1.title_id, self.title_id)
        self.assertEqual(actual1.average_rating, float(self.average_rating))
        self.assertEqual(actual1.num_votes, int(self.num_votes))

    def test_custom_filenames(self):
        parser = PyMDbParser(use_default_filenames=False)
        with TemporaryDirectory() as tmpdir:
            filename = os.path.join(tmpdir, _TITLE_RATINGS.default_filename)
            with open(filename, 'w+') as f:
                f.write(self.content)
            title_ratings = []
            for title_rating in parser.get_title_ratings(filename, contains_headers=False):
                title_ratings.append(title_rating)
        self.assertEqual(len(title_ratings), 2)
        actual1, actual2 = title_ratings
        self.assertEqual(actual1.title_id, self.title_id)
        self.assertEqual(actual1.average_rating, float(self.average_rating))
        self.assertEqual(actual1.num_votes, int(self.num_votes))

    def test_gunzip_default_filenames(self):
        parser = PyMDbParser(gunzip_files=True)
        with TemporaryDirectory() as tmpdir:
            filename = os.path.join(tmpdir, f'{_TITLE_RATINGS.default_filename}.gz')
            with gzip.open(filename, 'wb') as f:
                f.write(self.content.encode('utf-8'))
            title_ratings = []
            for title_rating in parser.get_title_ratings(tmpdir, contains_headers=False):
                title_ratings.append(title_rating)
            self.assertTrue(os.path.exists(filename))
        self.assertEqual(len(title_ratings), 2)
        actual1, actual2 = title_ratings
        self.assertEqual(actual1.title_id, self.title_id)
        self.assertEqual(actual1.average_rating, float(self.average_rating))
        self.assertEqual(actual1.num_votes, int(self.num_votes))

    def test_gunzip_custom_filenames(self):
        parser = PyMDbParser(use_default_filenames=False, gunzip_files=True)
        with TemporaryDirectory() as tmpdir:
            filename = os.path.join(tmpdir, f'{_TITLE_RATINGS.default_filename}.gz')
            with gzip.open(filename, 'wb') as f:
                f.write(self.content.encode('utf-8'))
            title_ratings = []
            for title_rating in parser.get_title_ratings(filename, contains_headers=False):
                title_ratings.append(title_rating)
            self.assertTrue(os.path.exists(filename))
        self.assertEqual(len(title_ratings), 2)
        actual1, actual2 = title_ratings
        self.assertEqual(actual1.title_id, self.title_id)
        self.assertEqual(actual1.average_rating, float(self.average_rating))
        self.assertEqual(actual1.num_votes, int(self.num_votes))

    def test_gunzip_delete_default_filenames(self):
        parser = PyMDbParser(gunzip_files=True, delete_gzip_files=True)
        with TemporaryDirectory() as tmpdir:
            filename = os.path.join(tmpdir, f'{_TITLE_RATINGS.default_filename}.gz')
            with gzip.open(filename, 'wb') as f:
                f.write(self.content.encode('utf-8'))
            title_ratings = []
            for title_rating in parser.get_title_ratings(tmpdir, contains_headers=False):
                title_ratings.append(title_rating)
            self.assertFalse(os.path.exists(filename))
        self.assertEqual(len(title_ratings), 2)
        actual1, actual2 = title_ratings
        self.assertEqual(actual1.title_id, self.title_id)
        self.assertEqual(actual1.average_rating, float(self.average_rating))
        self.assertEqual(actual1.num_votes, int(self.num_votes))

    def test_gunzip_delete_custom_filenames(self):
        parser = PyMDbParser(use_default_filenames=False, gunzip_files=True, delete_gzip_files=True)
        with TemporaryDirectory() as tmpdir:
            filename = os.path.join(tmpdir, f'{_TITLE_RATINGS.default_filename}.gz')
            with gzip.open(filename, 'wb') as f:
                f.write(self.content.encode('utf-8'))
            title_ratings = []
            for title_rating in parser.get_title_ratings(filename, contains_headers=False):
                title_ratings.append(title_rating)
            self.assertFalse(os.path.exists(filename))
        self.assertEqual(len(title_ratings), 2)
        actual1, actual2 = title_ratings
        self.assertEqual(actual1.title_id, self.title_id)
        self.assertEqual(actual1.average_rating, float(self.average_rating))
        self.assertEqual(actual1.num_votes, int(self.num_votes))

    def test_contains_headers(self):
        parser = PyMDbParser()
        headers_content = f'headers\n{self.content}'
        with TemporaryDirectory() as tmpdir:
            filename = os.path.join(tmpdir, _TITLE_RATINGS.default_filename)
            with open(filename, 'w+') as f:
                f.write(headers_content)
            title_ratings = []
            for title_rating in parser.get_title_ratings(tmpdir):
                title_ratings.append(title_rating)
        self.assertEqual(len(title_ratings), 2)
        actual1, actual2 = title_ratings
        self.assertEqual(actual1.title_id, self.title_id)
        self.assertEqual(actual1.average_rating, float(self.average_rating))
        self.assertEqual(actual1.num_votes, int(self.num_votes))

    def test_incorrect_column_count(self):
        with TemporaryDirectory() as tmpdir:
            filename = os.path.join(tmpdir, _TITLE_RATINGS.default_filename)
            with open(filename, 'w+') as f:
                f.write('headers\ntest1\ttest2')
            with self.assertRaises(InvalidParseFormat):
                for _ in PyMDbParser().get_title_ratings(tmpdir):
                    pass


class TestGetNameBasics(unittest.TestCase):
    name_id = 'nameId'
    primary_name = 'primaryName'
    birth_year = '1930'
    death_year = '2010'
    primary_professions = 'actor,director,writer'
    known_for_titles = 'title1,title2'
    name1 = f'{name_id}\t{primary_name}\t{birth_year}\t{death_year}\t{primary_professions}\t{known_for_titles}'
    name2 = f'{name_id}\t{primary_name}\t{birth_year}\t\\N\tactor\ttitle'
    content = f'{name1}\n{name2}\n'

    def test_default_filenames(self):
        parser = PyMDbParser()
        with TemporaryDirectory() as tmpdir:
            filename = os.path.join(tmpdir, _NAME_BASICS.default_filename)
            with open(filename, 'w+') as f:
                f.write(self.content)
            name_basics = []
            for name_basic in parser.get_name_basics(tmpdir, contains_headers=False):
                name_basics.append(name_basic)
        self.assertEqual(len(name_basics), 2)
        actual1, actual2 = name_basics
        self.assertEqual(actual1.name_id, self.name_id)
        self.assertEqual(actual1.primary_name, self.primary_name)
        self.assertEqual(actual1.birth_year, int(self.birth_year))
        self.assertEqual(actual1.death_year, int(self.death_year))
        self.assertEqual(actual1.primary_professions, self.primary_professions.split(','))
        self.assertEqual(actual1.known_for_titles, self.known_for_titles.split(','))
        self.assertIsNone(actual2.death_year)
        self.assertEqual(actual2.primary_professions, ['actor'])
        self.assertEqual(actual2.known_for_titles, ['title'])

    def test_custom_filenames(self):
        parser = PyMDbParser(use_default_filenames=False)
        with TemporaryDirectory() as tmpdir:
            filename = os.path.join(tmpdir, 'test.tsv')
            with open(filename, 'w+') as f:
                f.write(self.content)
            name_basics = []
            for name_basic in parser.get_name_basics(filename, contains_headers=False):
                name_basics.append(name_basic)
        self.assertEqual(len(name_basics), 2)
        actual1, actual2 = name_basics
        self.assertEqual(actual1.name_id, self.name_id)
        self.assertEqual(actual1.primary_name, self.primary_name)
        self.assertEqual(actual1.birth_year, int(self.birth_year))
        self.assertEqual(actual1.death_year, int(self.death_year))
        self.assertEqual(actual1.primary_professions, self.primary_professions.split(','))
        self.assertEqual(actual1.known_for_titles, self.known_for_titles.split(','))
        self.assertIsNone(actual2.death_year)
        self.assertEqual(actual2.primary_professions, ['actor'])
        self.assertEqual(actual2.known_for_titles, ['title'])

    def test_gunzip_default_filenames(self):
        parser = PyMDbParser(gunzip_files=True)
        with TemporaryDirectory() as tmpdir:
            filename = os.path.join(tmpdir, f'{_NAME_BASICS.default_filename}.gz')
            with gzip.open(filename, 'wb') as f:
                f.write(self.content.encode('utf-8'))
            name_basics = []
            for name_basic in parser.get_name_basics(tmpdir, contains_headers=False):
                name_basics.append(name_basic)
            self.assertTrue(os.path.exists(filename))
        self.assertEqual(len(name_basics), 2)
        actual1, actual2 = name_basics
        self.assertEqual(actual1.name_id, self.name_id)
        self.assertEqual(actual1.primary_name, self.primary_name)
        self.assertEqual(actual1.birth_year, int(self.birth_year))
        self.assertEqual(actual1.death_year, int(self.death_year))
        self.assertEqual(actual1.primary_professions, self.primary_professions.split(','))
        self.assertEqual(actual1.known_for_titles, self.known_for_titles.split(','))
        self.assertIsNone(actual2.death_year)
        self.assertEqual(actual2.primary_professions, ['actor'])
        self.assertEqual(actual2.known_for_titles, ['title'])

    def test_gunzip_custom_filenames(self):
        parser = PyMDbParser(use_default_filenames=False, gunzip_files=True)
        with TemporaryDirectory() as tmpdir:
            filename = os.path.join(tmpdir, 'test.gz')
            with gzip.open(filename, 'wb') as f:
                f.write(self.content.encode('utf-8'))
            name_basics = []
            for name_basic in parser.get_name_basics(filename, contains_headers=False):
                name_basics.append(name_basic)
            self.assertTrue(os.path.exists(filename))
        self.assertEqual(len(name_basics), 2)
        actual1, actual2 = name_basics
        self.assertEqual(actual1.name_id, self.name_id)
        self.assertEqual(actual1.primary_name, self.primary_name)
        self.assertEqual(actual1.birth_year, int(self.birth_year))
        self.assertEqual(actual1.death_year, int(self.death_year))
        self.assertEqual(actual1.primary_professions, self.primary_professions.split(','))
        self.assertEqual(actual1.known_for_titles, self.known_for_titles.split(','))
        self.assertIsNone(actual2.death_year)
        self.assertEqual(actual2.primary_professions, ['actor'])
        self.assertEqual(actual2.known_for_titles, ['title'])

    def test_gunzip_delete_default_filenames(self):
        parser = PyMDbParser(gunzip_files=True, delete_gzip_files=True)
        with TemporaryDirectory() as tmpdir:
            filename = os.path.join(tmpdir, f'{_NAME_BASICS.default_filename}.gz')
            with gzip.open(filename, 'wb') as f:
                f.write(self.content.encode('utf-8'))
            name_basics = []
            for name_basic in parser.get_name_basics(tmpdir, contains_headers=False):
                name_basics.append(name_basic)
            self.assertFalse(os.path.exists(filename))
        self.assertEqual(len(name_basics), 2)
        actual1, actual2 = name_basics
        self.assertEqual(actual1.name_id, self.name_id)
        self.assertEqual(actual1.primary_name, self.primary_name)
        self.assertEqual(actual1.birth_year, int(self.birth_year))
        self.assertEqual(actual1.death_year, int(self.death_year))
        self.assertEqual(actual1.primary_professions, self.primary_professions.split(','))
        self.assertEqual(actual1.known_for_titles, self.known_for_titles.split(','))
        self.assertIsNone(actual2.death_year)
        self.assertEqual(actual2.primary_professions, ['actor'])
        self.assertEqual(actual2.known_for_titles, ['title'])

    def test_gunzip_delete_custom_filenames(self):
        parser = PyMDbParser(use_default_filenames=False, gunzip_files=True, delete_gzip_files=True)
        with TemporaryDirectory() as tmpdir:
            filename = os.path.join(tmpdir, 'test.gz')
            with gzip.open(filename, 'wb') as f:
                f.write(self.content.encode('utf-8'))
            name_basics = []
            for name_basic in parser.get_name_basics(filename, contains_headers=False):
                name_basics.append(name_basic)
            self.assertFalse(os.path.exists(filename))
        self.assertEqual(len(name_basics), 2)
        actual1, actual2 = name_basics
        self.assertEqual(actual1.name_id, self.name_id)
        self.assertEqual(actual1.primary_name, self.primary_name)
        self.assertEqual(actual1.birth_year, int(self.birth_year))
        self.assertEqual(actual1.death_year, int(self.death_year))
        self.assertEqual(actual1.primary_professions, self.primary_professions.split(','))
        self.assertEqual(actual1.known_for_titles, self.known_for_titles.split(','))
        self.assertIsNone(actual2.death_year)
        self.assertEqual(actual2.primary_professions, ['actor'])
        self.assertEqual(actual2.known_for_titles, ['title'])

    def test_contains_headers(self):
        parser = PyMDbParser()
        headers_content = f'headers\n{self.content}'
        with TemporaryDirectory() as tmpdir:
            filename = os.path.join(tmpdir, _NAME_BASICS.default_filename)
            with open(filename, 'w+') as f:
                f.write(headers_content)
            name_basics = []
            for name_basic in parser.get_name_basics(tmpdir):
                name_basics.append(name_basic)
        self.assertEqual(len(name_basics), 2)
        actual1, actual2 = name_basics
        self.assertEqual(actual1.name_id, self.name_id)
        self.assertEqual(actual1.primary_name, self.primary_name)
        self.assertEqual(actual1.birth_year, int(self.birth_year))
        self.assertEqual(actual1.death_year, int(self.death_year))
        self.assertEqual(actual1.primary_professions, self.primary_professions.split(','))
        self.assertEqual(actual1.known_for_titles, self.known_for_titles.split(','))
        self.assertIsNone(actual2.death_year)
        self.assertEqual(actual2.primary_professions, ['actor'])
        self.assertEqual(actual2.known_for_titles, ['title'])

    def test_incorrect_column_count(self):
        with TemporaryDirectory() as tmpdir:
            filename = os.path.join(tmpdir, _NAME_BASICS.default_filename)
            with open(filename, 'w+') as f:
                f.write('headers\ntest1\ttest2')
            with self.assertRaises(InvalidParseFormat):
                for _ in PyMDbParser().get_name_basics(tmpdir):
                    pass


class TestBuildPath(unittest.TestCase):
    test_path = 'test_dir'
    default_filename = 'test.tsv'
    content = 'test'

    def test_default_filenames(self):
        parser = PyMDbParser()
        correct_result = f'{self.test_path}/{self.default_filename}'
        actual_result = parser._build_path(self.test_path, self.default_filename)
        
        self.assertEqual(actual_result, correct_result)

    def test_custom_filenames(self):
        parser = PyMDbParser(use_default_filenames=False)
        correct_result = self.test_path
        actual_result = parser._build_path(self.test_path, self.default_filename)
        
        self.assertEqual(actual_result, correct_result)

    def test_gunzip_default_filenames(self):
        with TemporaryDirectory() as tmpdir:
            parser = PyMDbParser(gunzip_files=True)
            gzip_path = os.path.join(tmpdir, f'{self.default_filename}.gz')
            with gzip.open(gzip_path, 'wb') as f:
                f.write(self.content.encode('utf-8'))
            correct_result = os.path.join(tmpdir, self.default_filename)
            actual_result = parser._build_path(tmpdir, self.default_filename)
            
            self.assertEqual(actual_result, correct_result)
            with open(actual_result, 'r') as f:
                self.assertEqual(f.read(), self.content)

    def test_gunzip_custom_filenames_gz(self):
        with TemporaryDirectory() as tmpdir:
            parser = PyMDbParser(use_default_filenames=False, gunzip_files=True)
            gzip_path = os.path.join(tmpdir, 'test.gz')
            with gzip.open(gzip_path, 'wb') as f:
                f.write(self.content.encode('utf-8'))
            correct_result = os.path.join(tmpdir, 'test')
            actual_result = parser._build_path(gzip_path, self.default_filename)
            
            self.assertEqual(actual_result, correct_result)
            with open(actual_result, 'r') as f:
                self.assertEqual(f.read(), self.content)

    def test_gunzip_custom_filenames_no_gz(self):
        with TemporaryDirectory() as tmpdir:
            parser = PyMDbParser(use_default_filenames=False, gunzip_files=True)
            gzip_path = os.path.join(tmpdir, 'test.txt')
            with gzip.open(gzip_path, 'wb') as f:
                f.write(self.content.encode('utf-8'))
            correct_result = os.path.join(tmpdir, 'test.txt.out')
            actual_result = parser._build_path(gzip_path, self.default_filename)
            
            self.assertEqual(actual_result, correct_result)
            with open(actual_result, 'r') as f:
                self.assertEqual(f.read(), self.content)
