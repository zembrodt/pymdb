import re
from pymdb.utils.util import (
    append_filename_to_path,
    gunzip_file)
from pymdb.models.name import (
    NameBasics)
from pymdb.models.title import (
    TitleAkas,
    TitleBasics,
    TitleCrew,
    TitleEpisode,
    TitlePrincipalCrew,
    TitleRating
)

class PyMDbParser:
    _DEFAULT_TITLE_AKAS_FILE = 'title.akas.tsv'
    _DEFAULT_TITLE_BASICS_FILE = 'title.basics.tsv'
    _DEFAULT_TITLE_CREW_FILE = 'title.crew.tsv'
    _DEFAULT_TITLE_EPISODE_FILE = 'title.episode.tsv'
    _DEFAULT_TITLE_PRINCIPALS_FILE = 'title.principals.tsv'
    _DEFAULT_TITLE_RATINGS_FILE = 'title.ratings.tsv'
    _DEFAULT_NAME_BASICS_FILE = 'name.basics.tsv'

    def __init__(self, use_default_filenames=True, gunzip_files=False, delete_gzip_files=False):
        self._use_default_filenames = use_default_filenames
        self._gunzip_files = gunzip_files
        self._delete_gzip_files = delete_gzip_files

    def get_title_akas(self, path, contains_headers=True):
        if self._use_default_filenames:
            path = append_filename_to_path(path, self._DEFAULT_TITLE_AKAS_FILE)

        if self._gunzip_files:
            if self._use_default_filenames:
                path = f'{path}.gz'
            path = gunzip_file(path, delete_infile=self._delete_gzip_files)

        with open(path, mode='r', encoding='utf8') as f:
            is_first_line = contains_headers
            for line in f:
                if is_first_line:
                    is_first_line = False
                else:
                    line = line.strip().split('\t')
                    if len(line) == 8:
                        title_id, ordering, title, region, language, types, attributes, is_original_title = line
                        region = region if region != '\\N' else None
                        language = language if language != '\\N' else None
                        types = [t for t in types.split(',')]
                        attributes = [a for a in attributes.split(',')]
                        is_original_title = bool(is_original_title)
                        yield TitleAkas(title_id, ordering, title, region, language, types, attributes,
                                        is_original_title)
                    else:
                        print('Found title akas in incorrect format')

    def get_title_basics(self, path, contains_headers=True):
        if self._use_default_filenames:
            path = append_filename_to_path(path, self._DEFAULT_TITLE_BASICS_FILE)

        if self._gunzip_files:
            if self._use_default_filenames:
                path = f'{path}.gz'
            path = gunzip_file(path, delete_infile=self._delete_gzip_files)

        with open(path, mode='r', encoding='utf8') as f:
            is_first_line = contains_headers
            for line in f:
                if is_first_line:
                    is_first_line = False
                else:
                    line = line.strip().split('\t')
                    if len(line) == 9:
                        title_id, title_type, primary_title, original_title, is_adult, start_year, end_year, runtime, genres = line
                        is_adult = bool(is_adult)
                        start_year = int(start_year) if start_year != '\\N' else None
                        end_year = int(end_year) if end_year != '\\N' else None
                        runtime = int(runtime) if runtime != '\\N' else None
                        genres = [genre for genre in genres.split(',')]
                        yield TitleBasics(title_id, title_type, primary_title, original_title, is_adult, start_year,
                                          end_year, runtime, genres)
                    else:
                        print('Found title basic in incorrect format')

    def get_title_crew(self, path, contains_headers=True):
        if self._use_default_filenames:
            path = append_filename_to_path(path, self._DEFAULT_TITLE_CREW_FILE)

        if self._gunzip_files:
            if self._use_default_filenames:
                path = f'{path}.gz'
            path = gunzip_file(path, delete_infile=self._delete_gzip_files)

        with open(path, mode='r', encoding='utf8') as f:
            is_first_line = contains_headers
            for line in f:
                if is_first_line:
                    is_first_line = False
                else:
                    line = line.strip().split('\t')
                    if len(line) == 3:
                        title_id, director_ids, writer_ids = line
                        director_ids = [director_id for director_id in director_ids.split(',')]
                        writer_ids = [writer_id for writer_id in writer_ids.split(',')]
                        yield TitleCrew(title_id, director_ids, writer_ids)
                    else:
                        print('Found title crew in incorrect format')

    def get_title_episodes(self, path, contains_headers=True):
        if self._use_default_filenames:
            path = append_filename_to_path(path, self._DEFAULT_TITLE_EPISODE_FILE)

        if self._gunzip_files:
            if self._use_default_filenames:
                path = f'{path}.gz'
            path = gunzip_file(path, delete_infile=self._delete_gzip_files)

        with open(path, mode='r', encoding='utf8') as f:
            is_first_line = contains_headers
            for line in f:
                if is_first_line:
                    is_first_line = False
                else:
                    line = line.strip().split('\t')
                    if len(line) == 4:
                        title_id, parent_title_id, season_number, episode_number = line
                        season_number = int(season_number) if season_number != '\\N' else None
                        episode_number = int(episode_number) if episode_number != '\\N' else None
                        yield TitleEpisode(title_id, parent_title_id, season_number, episode_number)
                    else:
                        print('Found title episode in incorrect format')

    def get_title_principals(self, path, contains_headers=True):
        if self._use_default_filenames:
            path = append_filename_to_path(path, self._DEFAULT_TITLE_PRINCIPALS_FILE)

        if self._gunzip_files:
            if self._use_default_filenames:
                path = f'{path}.gz'
            path = gunzip_file(path, delete_infile=self._delete_gzip_files)

        with open(path, mode='r', encoding='utf8') as f:
            is_first_line = contains_headers
            for line in f:
                if is_first_line:
                    is_first_line = False
                else:
                    line = line.strip().split('\t')
                    if len(line) == 6:
                        title_id, ordering, name_id, category, job, characters = line
                        job = job if job != '\\N' else None
                        if characters != '\\N':
                            if len(characters) > 0 and characters[0] == '[' and characters[-1] == ']':
                                characters = [result.group(0).replace('"', '') for result in
                                              re.finditer(r'".+?"', characters)]
                        else:
                            characters = None
                        yield TitlePrincipalCrew(title_id, ordering, name_id, category, job, characters)
                    else:
                        print('Found title principals in incorrect format')

    def get_title_ratings(self, path, contains_headers=True):
        if self._use_default_filenames:
            path = append_filename_to_path(path, self._DEFAULT_TITLE_RATINGS_FILE)

        if self._gunzip_files:
            if self._use_default_filenames:
                path = f'{path}.gz'
            path = gunzip_file(path, delete_infile=self._delete_gzip_files)

        with open(path, mode='r', encoding='utf8') as f:
            is_first_line = contains_headers
            for line in f:
                if is_first_line:
                    is_first_line = False
                else:
                    line = line.strip().split('\t')
                    if len(line) == 3:
                        title_id, average_rating, num_votes = line
                        average_rating = float(average_rating)
                        num_votes = int(num_votes)
                        yield TitleRating(title_id, average_rating, num_votes)
                    else:
                        print('Found title rating in incorrect format')

    def get_name_basics(self, path, contains_headers=True):
        if self._use_default_filenames:
            path = append_filename_to_path(path, self._DEFAULT_NAME_BASICS_FILE)

        if self._gunzip_files:
            if self._use_default_filenames:
                path = f'{path}.gz'
            path = gunzip_file(path, delete_infile=self._delete_gzip_files)

        with open(path, 'r', encoding='utf8') as f:
            is_first_line = contains_headers
            for line in f:
                if is_first_line:
                    is_first_line = False
                else:
                    line = line.split('\t')
                    if len(line) == 6:
                        # Build the NameBasics
                        name_id, primary_name, birth_year, death_year, primary_professions, known_for_titles = line
                        birth_year = int(birth_year) if birth_year != '\\N' else None
                        death_year = int(death_year) if death_year != '\\N' else None
                        primary_professions = [profession.strip() for profession in primary_professions.split(',')]
                        known_for_titles = [title.strip() for title in known_for_titles.split(',')]
                        yield NameBasics(
                            name_id, primary_name, birth_year, death_year, primary_professions, known_for_titles)
                    else:
                        # TODO: throw error
                        print('UNKNOWN NAME BASICS FORMAT!')
