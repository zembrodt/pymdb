"""The classes used to represent search results on IMDb.

This information is gathered from the JSON responses IMDb uses
for various GET requests for their search results.
"""

from ..utils import (
    is_int
)
from functools import total_ordering

@total_ordering
class SearchResult:
    """The base search result class.

    Contains the basic search result information both `SearchResultName`
    and `SearchResultTitle` use.

    Args:
        imdb_id (:obj:`str`): The ID used by IMDb. Prefixed with `nm` for names
            and `tt` for titles.
        search_rank (:obj:`int`): The ranking of the result by IMDb.
    """

    def __init__(self, imdb_id, search_rank):
        self._imdb_id = imdb_id
        self._search_rank = None

        self.search_rank = search_rank
    
    @property
    def imdb_id(self):
        return self._imdb_id
    
    @property
    def search_rank(self):
        return self._search_rank

    @search_rank.setter
    def search_rank(self, value):
        if is_int(value):
            self._search_rank = int(value)

    def __eq__(self, other):
        return self.imdb_id == other.imdb_id

    def __lt__(self, other):
        return self.imdb_id < other.imdb_id

    def __str__(self):
        return f'{self._imdb_id}, {self._search_rank}'

    def __repr__(self):
        return self.__str__()


class SearchResultName(SearchResult):
    """Search result for a person within IMDb.

    Contains the rest of the information IMDb provides within a search
    result when the ID is for a person.

    Args:
        imdb_id (:obj:`str`): The ID used by IMDb prefixed with `nm`.
        search_rank (:obj:`int`): The ranking of the result by IMDb.
        name (:obj:`str`): The name of the person.
        known_for (:obj:`str`): The blurb IMDb provides for what the person
            is known for to build the search results.
    """

    def __init__(self, imdb_id, search_rank, name, known_for):
        self._name = name
        self._known_for = known_for

        SearchResult.__init__(self, imdb_id, search_rank)
    
    @property
    def name(self):
        return self._name

    @property
    def known_for(self):
        return self._known_for

    def __str__(self):
        return f'{self._name} ({self._imdb_id}), known for: {self._known_for} (rank: {self._search_rank})'


class SearchResultTitle(SearchResult):
    """Search result for a title within IMDb.

    Contains the rest of the information IMDb provides within a search
    result when the ID is for a title.
    Note: If the `title_type` is a "`video game`", the `starring` list will be empty
    as IMDb provides the title's genres in its place.

    Args:
        imdb_id (:obj:`str`): The ID used by IMDb prefixed with `tt`.
        search_rank (:obj:`int`): The ranking of the result by IMDb.
        display_title (:obj:`str`): The title used by IMDb within search results.
        title_type (:obj:`str`): The type of title (ex: TV series, feature, etc).
        starring (:obj:`list` of :obj:`str`): A list of two actor names that are known
            for starring in the film.
        start_year(:obj:`int`): The year the title was released, or the start year if
            a TV series.
        end_year(:obj:`int`): The year a TV series was ended, or `None` if the series
            has not ended or is not a TV series.
    """

    def __init__(self, imdb_id, search_rank, display_title, title_type, starring, start_year, end_year):
        self._display_title = display_title
        self._title_type = title_type
        self._starring = []
        self._start_year = None
        self._end_year = None

        self.starring = starring
        self.start_year = start_year
        self.end_year = end_year

        SearchResult.__init__(self, imdb_id, search_rank)

    @property
    def display_title(self):
        return self._display_title

    @property
    def title_type(self):
        return self._title_type

    @property
    def starring(self):
        return self._starring

    @starring.setter
    def starring(self, value):
        if value is not None:
            self._starring = value

    @property
    def start_year(self):
        return self._start_year

    @start_year.setter
    def start_year(self, value):
        if is_int(value):
            self._start_year = int(value)

    @property
    def end_year(self):
        return self._end_year

    @end_year.setter
    def end_year(self, value):
        if is_int(value):
            self._end_year = int(value)

    def __str__(self):
        return f'{self._display_title} ({self._imdb_id}), {self._title_type}. Starring {self._starring} ' + \
            f'{f"{self._start_year}" if self._end_year is None else f"({self._start_year}-{self._end_year})"}' + \
                f' (rank: {self._search_rank})'