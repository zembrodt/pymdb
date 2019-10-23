"""The classes used to represent various information about titles on IMDb.

This will contain classes for both information gathered from the datasets provided by IMDb
and information scraped from IMDb web pages. Class names ending with 'Scrape' are scraped
from the web pages, otherwise they are gathered from the datasets.
"""

from pymdb.utils import (
    is_float,
    is_int,
    to_bool,
    to_datetime
)


class TitleAkas:
    """Class to store the row information from IMDb's 'title.akas.tsv' dataset.
    
    Provides additional information for a title.
    """

    def __init__(self, title_id, ordering, localized_title, region, language, types, attributes, is_original_title):
        """Initialize the object with all values in the row.

        Args:
            title_id: A string of the title's ID used by IMDb prefixed with 'tt'.
            ordering: An integer or string representation to unqiuely identify the row for
                a given title_id.
            localized_title: A string of the localized title.
            region: A string of the region for this version of the title.
            language: A string for the language of this title.
            types: A list of strings for the different types attributed to this title.
            attributes: A list of strings for terms to describe this title.
            is_original_title:  A boolean or string representation of if this title is
                the original title.
        """

        self._title_id = title_id
        self._ordering = None
        self._localized_title = localized_title
        self._region = region
        self._language = language
        self._types = []
        self._attributes = []
        self._is_original_title = None

        self.ordering = ordering
        self.types = types
        self.attributes = attributes
        self.is_original_title = is_original_title

    @property
    def title_id(self):
        return self._title_id

    @property
    def ordering(self):
        return self._ordering

    @ordering.setter
    def ordering(self, value):
        if is_int(value):
            self._ordering = int(value)

    @property
    def localized_title(self):
        return self._localized_title

    @property
    def region(self):
        return self._region

    @property
    def language(self):
        return self._language

    @property
    def types(self):
        return self._types

    @types.setter
    def types(self, value):
        if value is not None:
            self._types = value

    @property
    def attributes(self):
        return self._attributes

    @attributes.setter
    def attributes(self, value):
        if value is not None:
            self._attributes = value

    @property
    def is_original_title(self):
        return self._is_original_title

    @is_original_title.setter
    def is_original_title(self, value):
        self._is_original_title = to_bool(value)

    def __str__(self):
        ret_str = f'{self.localized_title} ({self.title_id}) {f": {self.region}" if self.region is not None else ""}'
        if self.language:
            if self.region:
                ret_str += f' - {self.language}'
            else:
                ret_str += f': {self.language}'


class TitleBasics:
    """Class to store the row information from IMDb's 'title.basics.tsv' dataset.
    
    Basic information for a title.
    """

    def __init__(self, title_id, title_type, primary_title, original_title, is_adult, start_year, end_year,
                 runtime_minutes, genres):
        """Initialize the object with all values in the row.

        Args:
            title_id: A string of the title's ID used by IMDb prefixed with 'tt'.
            title_type: A string for the type/format of the title (ex: movie, short,
                tvseries, tvepisode, video, etc).
            primary_title: A string for the popular title used.
            original_title: A string for the original title in the original langauge.
            is_adult: A boolean or string representation of if this is an adult title.
            start_year: An integer or string representation of the year this title
                was released, or for TV series, the year the series started.
            end_year: An integer or string representation for the year this TV series
                ended, otherwise None.
            runtime_minutes: An integer or string representation for the length of the
                title's runtime in minutes.
            genres: An array of strings that includes up to three genres associated with
                this title.
        """

        self._title_id = title_id
        self._title_type = title_type
        self._primary_title = primary_title
        self._original_title = original_title
        self._is_adult = None
        self._start_year = None
        self._end_year = None
        self._runtime_minutes = None
        self._genres = []

        self.is_adult = is_adult
        self.start_year = start_year
        self.end_year = end_year
        self.runtime_minutes = runtime_minutes
        self.genres = genres

    @property
    def title_id(self):
        return self._title_id

    @property
    def title_type(self):
        return self._title_type

    @property
    def primary_title(self):
        return self._primary_title

    @property
    def original_title(self):
        return self._original_title

    @property
    def is_adult(self):
        return self._is_adult

    @is_adult.setter
    def is_adult(self, value):
        self._is_adult = to_bool(value)

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

    @property
    def runtime_minutes(self):
        return self._runtime_minutes

    @runtime_minutes.setter
    def runtime_minutes(self, value):
        if is_int(value):
            self._runtime_minutes = int(value)

    @property
    def genres(self):
        return self._genres

    @genres.setter
    def genres(self, value):
        if value is not None:
            self._genres = value

    def __str__(self):
        return f'{self.primary_title} ({self.title_id}): {self.title_type}, ' + \
            f'{self.start_year if self.start_year is not None else "????"}' + \
            f'{f" - {self.end_year}" if self.end_year is not None else ""}'


class TitleCrew:
    """Class to store the row information from IMDb's 'title.crew.tsv' dataset.
    
    Director(s) and writer(s) for a title.
    """

    def __init__(self, title_id, director_ids, writer_ids):
        """Initialize the object with all values in the row.

        Args:
            title_id: A string of the title's ID used by IMDb prefixed with 'tt'.
            director_ids: An array of strings of IDs used by IMDb for people, prefixed
                with 'nm', represents the director(s) of the title.
            writer_ids: An array of strings of IDs used by IMDb for people, prefixed
                with 'nm', represents the writer(s) of the title.
        """

        self._title_id = title_id
        self._director_ids = []
        self._writer_ids = []

        self.director_ids = director_ids
        self.writer_ids = writer_ids

    @property
    def title_id(self):
        return self._title_id

    @property
    def director_ids(self):
        return self._director_ids

    @director_ids.setter
    def director_ids(self, value):
        if value is not None:
            self._director_ids = value

    @property
    def writer_ids(self):
        return self._writer_ids

    @writer_ids.setter
    def writer_ids(self, value):
        if value is not None:
            self._writer_ids = value

    def __str__(self):
        ret_str = f'{self._title_id}{f" directed by {self.director_ids}" if self.director_ids is not None else ""}'
        if self.writer_ids:
            if self.director_ids:
                ret_str += f' and written by {self.writer_ids}'
            else:
                ret_str += f' written by {self.writer_ids}'
        return ret_str


class TitleEpisode:
    """Class to store the row information from IMDb's 'title.episodes.tsv' dataset."""

    def __init__(self, title_id, parent_title_id, season_number, episode_number):
        """Initialize the object with all values in the row.

        Args:
            title_id: A string of the title's ID used by IMDb prefixed with 'tt'.
            parent_title_id: A string of the title's ID used by IMDb prefixed with 'tt',
                represents the parent TV series to the episode.
            season_number: An integer or string representation of the season this episode
                was aired in.
            episode_number: An integer or string representation of the episode number
                it was aired as in the season.
        """

        self._title_id = title_id
        self._parent_title_id = parent_title_id
        self._season_number = None
        self._episode_number = None

        self.season_number = season_number
        self.episode_number = episode_number

    @property
    def title_id(self):
        return self._title_id

    @property
    def parent_title_id(self):
        return self._parent_title_id

    @property
    def season_number(self):
        return self._season_number

    @season_number.setter
    def season_number(self, value):
        if is_int(value):
            self._season_number = int(value)

    @property
    def episode_number(self):
        return self._episode_number

    @episode_number.setter
    def episode_number(self, value):
        if is_int(value):
            self._episode_number = int(value)

    def __str__(self):
        return f'{self.parent_title_id} {f"S{self.season_number}" if self._season_number is not None else ""}' + \
            f'{f"E{self.episode_number}" if self.episode_number is not None else ""}: {self.title_id}'


class TitlePrincipalCrew:
    """Class to store the row information from IMDb's 'title.principals.tsv' dataset.
    
    Principal cast/crew for a title.
    """

    def __init__(self, title_id, ordering, name_id, category, job, characters):
        """Initialize the object with all values in the row.

        Args:
            title_id: A string of the title's ID used by IMDb prefixed with 'tt'.
            ordering: An integer or string representation to unqiuely identify the row for
                a given title_id.
            name_id: A string of the person's ID used by IMDb prefixed with 'nm'.
            category: A string for the category of job the person was in.
            job: A string for the specific job title if available, otherwise None.
            characters: A list of characters the person played, if applicable.
        """

        self._title_id = title_id
        self._ordering = None
        self._name_id = name_id
        self._category = category
        self._job = job
        self._characters = []

        self.ordering = ordering
        self.characters = characters

    @property
    def title_id(self):
        return self._title_id

    @property
    def ordering(self):
        return self._ordering

    @ordering.setter
    def ordering(self, value):
        if is_int(value):
            self._ordering = int(value)

    @property
    def name_id(self):
        return self._name_id

    @property
    def category(self):
        return self._category

    @property
    def job(self):
        return self._job

    @property
    def characters(self):
        return self._characters

    @characters.setter
    def characters(self, value):
        if value is not None:
            self._characters = value

    def __str__(self):
        return f'{self.name_id} ({self.title_id}): {self.category}' + \
            f'{f" as {self.job}" if self.job is not None else ""}' + \
            f'{f" playing {self.characters}" if len(self.characters) > 0 else ""}'


class TitleRating:
    """Class to store the row information from IMDb's 'title.ratings.tsv' dataset."""

    def __init__(self, title_id, average_rating, num_votes):
        """Initialize the object with all values in the row.

        Args:
            title_id: A string of the title's ID used by IMDb prefixed with 'tt'.
            average_rating: A float or string representation for the weighted
                average of all user ratings on IMDb.
            num_votes: An integer or string representation for the number of user
                votes the title has received on IMDb.
        """

        self._title_id = title_id
        self._average_rating = None
        self._num_votes = None

        self.average_rating = average_rating
        self.num_votes = num_votes

    @property
    def title_id(self):
        return self._title_id

    @property
    def average_rating(self):
        return self._average_rating

    @average_rating.setter
    def average_rating(self, value):
        if is_float(value):
            self._average_rating = float(value)

    @property
    def num_votes(self):
        return self._num_votes

    @num_votes.setter
    def num_votes(self, value):
        if is_int(value):
            self._num_votes = int(value)

    def __str__(self):
        return f'{self.title_id}: Rated {self.average_rating} with {self.num_votes} votes'


class TitleScrape:
    """Object to represent detailed information for a title on its IMDb web page.

    This information is scraped from the main page for a title's IMDb web page.
    """

    def __init__(
            self, title_id, title_text, title_parent_id, mpaa_rating, country, language, release_date, end_year,
            season_number, episode_number, taglines, plot, storyline, production_companies, top_cast,
            budget, opening_weekend_gross, opening_weekend_date, usa_gross, worldwide_gross
    ):
        """Initialize a CreditScrape object with all information it will store.

        Args:
            title_id: A string of the title's ID used by IMDb prefixed with 'tt'.
            title_text: A string for the title's name on its IMDb page.
            title_parent_id: A string of the episode's TV series parent ID used
                by IMDb prefixed with 'tt', otherwise None.
            mpaa_rating: A string for the title's MPAA rating.
            country: A string for the title's country of origin.
            language: A string for the title's original language.
            release_date: A datetime object or formatted string for the title's
                original release date, or when the TV series began airing.
            end_year: A datetime object or formatted string for the year the
                TV series stopped airing, otherwise None.
            season_number: An integer or string representation for the season
                the episode is in, otherwise None.
            episode_number: An integer or string representation for the episode's
                number in the season, otherwise None.
            taglines: A list of strings for all of the title's taglines.
            plot: A string for the title's plot.
            storyline: A string for the title's storyline.
            production_companies: A list of strings of company IDs credited with
                producing the title. These IDs are used by IMDb and prefixed with 'co'.
            top_cast: A list of strings of person IDs for the top cast in the title.
                These IDs are used by IMDb and prefixed with 'nm'.
            budget: An integer or string representation for the budget of the title.
            opening_weekend_gross: An integer or string representation of the title's
                gross on opening weekend.
            opening_weekend_date: A datetime object or formatted string for the title's
                opening weekend date.
            usa_gross: An integer or string representation of the title's gross in the USA.
            worldwide_gross: An integer or string representation of the title's gross worldwide.
        """

        self._title_id = title_id
        self._title_text = title_text
        self._title_parent_id = title_parent_id
        self._mpaa_rating = mpaa_rating
        self._country = country
        self._language = language
        self._release_date = None
        self._end_year = None
        self._season_number = None
        self._episode_number = None
        self._taglines = taglines
        self._plot = plot
        self._storyline = storyline
        self._production_companies = production_companies
        self._top_cast = top_cast
        self._budget = None
        self._opening_weekend_gross = None
        self._opening_weekend_date = None
        self._usa_gross = None
        self._worldwide_gross = None

        self.release_date = release_date
        self.end_year = end_year
        self.season_number = season_number
        self.episode_number = episode_number
        self.budget = budget
        self.opening_weekend_gross = opening_weekend_gross
        self.opening_weekend_date = opening_weekend_date
        self.usa_gross = usa_gross
        self.worldwide_gross = worldwide_gross

    @property
    def title_id(self):
        return self._title_id

    @property
    def title_text(self):
        return self._title_text

    @property
    def title_parent_id(self):
        return self._title_parent_id

    @property
    def mpaa_rating(self):
        return self._mpaa_rating

    @property
    def country(self):
        return self._country

    @property
    def language(self):
        return self._language

    @property
    def release_date(self):
        return self._release_date

    @release_date.setter
    def release_date(self, value):
        self._release_date = to_datetime(value)

    @property
    def end_year(self):
        return self._end_year

    @end_year.setter
    def end_year(self, value):
        self._end_year = to_datetime(value)

    @property
    def season_number(self):
        return self._season_number

    @season_number.setter
    def season_number(self, value):
        if is_int(value):
            self._season_number = int(value)

    @property
    def episode_number(self):
        return self._episode_number

    @episode_number.setter
    def episode_number(self, value):
        if is_int(value):
            self._episode_number = int(value)

    @property
    def taglines(self):
        return self._taglines

    @property
    def plot(self):
        return self._plot

    @property
    def storyline(self):
        return self._storyline

    @property
    def production_companies(self):
        return self._production_companies

    @property
    def top_cast(self):
        return self._top_cast

    @property
    def budget(self):
        return self._budget

    @budget.setter
    def budget(self, value):
        if is_int(value):
            self._budget = int(value)

    @property
    def opening_weekend_gross(self):
        return self._opening_weekend_gross

    @opening_weekend_gross.setter
    def opening_weekend_gross(self, value):
        if is_int(value):
            self._opening_weekend_gross = int(value)

    @property
    def opening_weekend_date(self):
        return self._opening_weekend_date

    @opening_weekend_date.setter
    def opening_weekend_date(self, value):
        self._opening_weekend_date = to_datetime(value)

    @property
    def usa_gross(self):
        return self._usa_gross

    @usa_gross.setter
    def usa_gross(self, value):
        if is_int(value):
            self._usa_gross = int(value)

    @property
    def worldwide_gross(self):
        return self._worldwide_gross

    @worldwide_gross.setter
    def worldwide_gross(self, value):
        if is_int(value):
            self._worldwide_gross = int(value)

    def __str__(self):
        return f'{self.title_text} ({self.title_id}): {self.mpaa_rating}, {self.release_date} by ' + \
               f'{self.production_companies}. {f"Ended {self.end_year}" if self.end_year is not None else ""} ' + \
               f'{self.taglines} {f" S{self.season_number}" if self.season_number is not None else ""}' + \
               f'{f"E{self.episode_number}" if self.episode_number is not None else ""}' + \
                '\n\t' + f'Budget: ${self.budget}, grossed ${self.opening_weekend_gross} on opening weekend of ' + \
               f'{self.opening_weekend_date}. USA total: ${self.usa_gross}, World total: ${self.worldwide_gross}'


class TitleTechSpecsScrape:
    """Object to represent information for a title's technical specifications.

    This information is scraped from the technical IMDb web page for a title
    """

    def __init__(
            self, title_id, runtime, sound_mix, color, aspect_ratio, camera, laboratory, negative_format,
            cinematographic_process, printed_film_format
    ):
        """Initialize a CreditScrape object with all information it will store.

        Args:
            title_id: A string of the title's ID used by IMDb prefixed with 'tt'.
            runtime: An integer or string representation for the length of the
                title's runtime in minutes.
            sound_mix: A list of strings for each of the title's sound mixes
            color: A string for the color used in the title.
            aspect_ratio: A list of strings for each aspect ratio the title
                is available in.
            camera: A list of strings for each camera used for the title.
            laboratory: A list of strings for all the title's laboratories.
            negative_format: A string for the title's negative format.
            cinematographic_process: A list of strings for each of the title's
                cinematographic processes.
            printed_film_format: A string for the title's printed film format.
        """

        self._title_id = title_id
        self._runtime = None
        self._sound_mix = sound_mix
        self._color = color
        self._aspect_ratio = aspect_ratio
        self._camera = camera
        self._laboratory = laboratory
        self._negative_format = negative_format
        self._cinematographic_process = cinematographic_process
        self._printed_film_format = printed_film_format

        self.runtime = runtime

    @property
    def title_id(self):
        return self._title_id

    @property
    def runtime(self):
        return self._runtime

    @runtime.setter
    def runtime(self, value):
        if is_int(value):
            self._runtime = int(value)

    @property
    def sound_mix(self):
        return self._sound_mix

    @property
    def color(self):
        return self._color

    @property
    def aspect_ratio(self):
        return self._aspect_ratio

    @property
    def camera(self):
        return self._camera

    @property
    def laboratory(self):
        return self._laboratory

    @property
    def negative_format(self):
        return self._negative_format

    @property
    def cinematographic_process(self):
        return self._cinematographic_process

    @property
    def printed_film_format(self):
        return self._printed_film_format

    def __str__(self):
        return f'{self.title_id} tech specs: {self.runtime}m runtime, {self.aspect_ratio} ratio'
