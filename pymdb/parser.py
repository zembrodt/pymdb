import re
from pymdb.utils import (
    append_filename_to_path,
    gunzip_file,
    preprocess_list
)
from pymdb.models.name import (
    NameBasics
)
from pymdb.models.title import (
    TitleAkas,
    TitleBasics,
    TitleCrew,
    TitleEpisode,
    TitlePrincipalCrew,
    TitleRating
)

class _IMDbDataset:
    """Private class to match dataset files with column counts."""

    def __init__(self, default_filename, column_count):
        """Initialize with the dataset's default filename and column count.

        Args:
            default_filename: A string of the default filename for the dataset provided by IMDb.
            column_count: An integer of the amount of columns in the dataset.
        """

        self.default_filename = default_filename
        self.column_count = column_count

_TITLE_AKAS = _IMDbDataset('title.akas.tsv', 8)
_TITLE_BASICS = _IMDbDataset('title.basics.tsv', 9)
_TITLE_CREW = _IMDbDataset('title.crew.tsv', 3)
_TITLE_EPISODE = _IMDbDataset('title.episode.tsv', 4)
_TITLE_PRINCIPALS = _IMDbDataset('title.principals.tsv', 6)
_TITLE_RATINGS = _IMDbDataset('title.ratings.tsv', 3)
_NAME_BASICS = _IMDbDataset('name.basics.tsv', 6)

class PyMDbParser:
    """Object used to parse the tsv datasets provided by IMDb.

    Parses each row in the tsv file into a specific PyMDb object.
    """

    def __init__(self, use_default_filenames=True, gunzip_files=False, delete_gzip_files=False):
        """Initialized with optional booleans on how the IMDb datasets are formatted.

        Args:
            use_default_filenames: A boolean for whether the filenames for each dataset are the same as
                when they are provided by IMDb.
            gunzip_files: A boolean to notify if the files are gzipped or not.
            delete_gzip_files: A boolean to determine if gzip files should be deleted after gunzipped.
        """

        self._use_default_filenames = use_default_filenames
        self._gunzip_files = gunzip_files
        self._delete_gzip_files = delete_gzip_files

    def get_title_akas(self, path, contains_headers=True):
        """Parse the 'title.akas.tsv' dataset provided by IMDb.

        Args:
            path: A string for the system path to the dataset file. If not using
                default filenames, this string will include the dataset file.
            contains_headers: A boolean to determine if the first line is column titles or a data row.

        Yields:
            A TitleAkas object for each row in the dataset.
        """

        path = self._build_path(path, _TITLE_AKAS.default_filename)

        with open(path, mode='r', encoding='utf8') as f:
            is_first_line = contains_headers
            for line in f:
                if is_first_line:
                    is_first_line = False
                else:
                    line = line.strip().split('\t')
                    if len(line) == _TITLE_AKAS.column_count:
                        line = preprocess_list(line)
                        title_id, ordering, title, region, language, types, attributes, is_original_title = line
                        if types is not None:
                            types = [typ for typ in types.split(',')]
                        if attributes is not None:
                            attributes = [a for a in attributes.split(',')]
                        yield TitleAkas(title_id, ordering, title, region, language, types, attributes,
                                        is_original_title)
                    else:
                        print('Found title akas in incorrect format')

    def get_title_basics(self, path, contains_headers=True):
        """Parse the 'title.basics.tsv' dataset provided by IMDb.

        Args:
            path: A string for the system path to the dataset file. If not using
                default filenames, this string will include the dataset file.
            contains_headers: A boolean to determine if the first line is column titles or a data row.

        Yields:
            A TitleBasics object for each row in the dataset.
        """

        path = self._build_path(path, _TITLE_BASICS.default_filename)

        with open(path, mode='r', encoding='utf8') as f:
            is_first_line = contains_headers
            for line in f:
                if is_first_line:
                    is_first_line = False
                else:
                    line = line.strip().split('\t')
                    if len(line) == _TITLE_BASICS.column_count:
                        line = preprocess_list(line)
                        title_id, title_type, primary_title, original_title, is_adult, start_year, end_year, runtime, genres = line
                        if genres is not None:
                            genres = [genre for genre in genres.split(',')]
                        yield TitleBasics(title_id, title_type, primary_title, original_title, is_adult, start_year,
                                          end_year, runtime, genres)
                    else:
                        print('Found title basic in incorrect format')

    def get_title_crew(self, path, contains_headers=True):
        """Parse the 'title.crew.tsv' dataset provided by IMDb.

        Args:
            path: A string for the system path to the dataset file. If not using
                default filenames, this string will include the dataset file.
            contains_headers: A boolean to determine if the first line is column titles or a data row.

        Yields:
            A TitleCrew object for each row in the dataset.
        """

        path = self._build_path(path, _TITLE_CREW.default_filename)

        with open(path, mode='r', encoding='utf8') as f:
            is_first_line = contains_headers
            for line in f:
                if is_first_line:
                    is_first_line = False
                else:
                    line = line.strip().split('\t')
                    if len(line) == _TITLE_CREW.column_count:
                        line = preprocess_list(line)
                        title_id, director_ids, writer_ids = line
                        if director_ids is not None:
                            director_ids = [director_id for director_id in director_ids.split(',')]
                        if writer_ids is not None:
                            writer_ids = [writer_id for writer_id in writer_ids.split(',')]
                        yield TitleCrew(title_id, director_ids, writer_ids)
                    else:
                        print('Found title crew in incorrect format')

    def get_title_episodes(self, path, contains_headers=True):
        """Parse the 'title.episodes.tsv' dataset provided by IMDb.

        Args:
            path: A string for the system path to the dataset file. If not using
                default filenames, this string will include the dataset file.
            contains_headers: A boolean to determine if the first line is column titles or a data row.

        Yields:
            A TitleEpisode object for each row in the dataset.
        """

        path = self._build_path(path, _TITLE_EPISODE.default_filename)
        
        with open(path, mode='r', encoding='utf8') as f:
            is_first_line = contains_headers
            for line in f:
                if is_first_line:
                    is_first_line = False
                else:
                    line = line.strip().split('\t')
                    if len(line) == _TITLE_EPISODE.column_count:
                        line = preprocess_list(line)
                        title_id, parent_title_id, season_number, episode_number = line
                        yield TitleEpisode(title_id, parent_title_id, season_number, episode_number)
                    else:
                        print('Found title episode in incorrect format')

    def get_title_principals(self, path, contains_headers=True):
        """Parse the 'title.principals.tsv' dataset provided by IMDb.

        Args:
            path: A string for the system path to the dataset file. If not using
                default filenames, this string will include the dataset file.
            contains_headers: A boolean to determine if the first line is column titles or a data row.

        Yields:
            A TitlePrincipalCrew object for each row in the dataset.
        """

        path = self._build_path(path, _TITLE_PRINCIPALS.default_filename)

        with open(path, mode='r', encoding='utf8') as f:
            is_first_line = contains_headers
            for line in f:
                if is_first_line:
                    is_first_line = False
                else:
                    line = line.strip().split('\t')
                    if len(line) == _TITLE_PRINCIPALS.column_count:
                        line = preprocess_list(line)
                        title_id, ordering, name_id, category, job, characters = line
                        if characters is not None and len(characters) > 0 and characters[0] == '[' and characters[-1] == ']':
                                characters = [result.group(0).replace('"', '') for result in
                                              re.finditer(r'".+?"', characters)]
                        yield TitlePrincipalCrew(title_id, ordering, name_id, category, job, characters)
                    else:
                        print('Found title principals in incorrect format')

    def get_title_ratings(self, path, contains_headers=True):
        """Parse the 'title.ratings.tsv' dataset provided by IMDb.

        Args:
            path: A string for the system path to the dataset file. If not using
                default filenames, this string will include the dataset file.
            contains_headers: A boolean to determine if the first line is column titles or a data row.

        Yields:
            A TitleRating object for each row in the dataset.
        """

        path = self._build_path(path, _TITLE_RATINGS.default_filename)

        with open(path, mode='r', encoding='utf8') as f:
            is_first_line = contains_headers
            for line in f:
                if is_first_line:
                    is_first_line = False
                else:
                    line = line.strip().split('\t')
                    if len(line) == _TITLE_RATINGS.column_count:
                        line = preprocess_list(line)
                        title_id, average_rating, num_votes = line
                        yield TitleRating(title_id, average_rating, num_votes)
                    else:
                        print('Found title rating in incorrect format')

    def get_name_basics(self, path, contains_headers=True):
        """Parse the 'name.basics.tsv' dataset provided by IMDb.

        Args:
            path: A string for the system path to the dataset file. If not using
                default filenames, this string will include the dataset file.
            contains_headers: A boolean to determine if the first line is column titles or a data row.

        Yields:
            A NameBasics object for each row in the dataset.
        """

        path = self._build_path(path, _NAME_BASICS.default_filename)
        
        with open(path, 'r', encoding='utf8') as f:
            is_first_line = contains_headers
            for line in f:
                if is_first_line:
                    is_first_line = False
                else:
                    line = line.split('\t')
                    if len(line) == _NAME_BASICS.column_count:
                        line = preprocess_list(line)
                        # Build the NameBasics
                        name_id, primary_name, birth_year, death_year, primary_professions, known_for_titles = line
                        if primary_professions is not None:
                            primary_professions = [profession.strip() for profession in primary_professions.split(',')]
                        if known_for_titles is not None:
                            known_for_titles = [title.strip() for title in known_for_titles.split(',')]
                        yield NameBasics(
                            name_id, primary_name, birth_year, death_year, primary_professions, known_for_titles)
                    else:
                        # TODO: throw error
                        print('UNKNOWN NAME BASICS FORMAT!')

    def _build_path(self, path, default_filename):
        """Private function to combine a system path with a default filename.

        This method will append the default filename of a dataset to the given path
        it is located in. If the files are to be gunzipped, it will also append the correct
        gzip extension used by IMDb.

        Args:
            path: A string for the system path to the directory where the dataset is located.
            default_filename: A string for the default filename of the dataset.
        
        Returns:
            A string path and default filename combined correctly.
        """

        if self._use_default_filenames:
            path = append_filename_to_path(path, default_filename)
        if self._gunzip_files:
            if self._use_default_filenames:
                path = f'{path}.gz'
            path = gunzip_file(path, delete_infile=self._delete_gzip_files)
        return path
