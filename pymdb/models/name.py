"""The classes used to represent various information about persons on IMDb.

This will contain classes for both information gathered from the datasets provided by IMDb
and information scraped from IMDb web pages. Class names ending with "`Scrape`" are scraped
from the web pages. Otherwise, they are gathered from the datasets.
"""

from pymdb.utils import (
    is_float,
    is_int,
    to_datetime
)


class NameBasics:
    """Class to store the row information from IMDb's "`name.basics.tsv`" dataset.
    
    Args:
        name_id (:obj:`str`): The person's ID used by IMDb prefixed with `nm`.
        primary_name(:obj:`str`): The person's name.
        birth_year (:obj:`int`): The person's birth year.
        death_year (:obj:`int`): The person's death year, or `None` otherwise.
        primary_professions (:obj:`list` of :obj:`str`): A list of all the person's primary professions.
        known_for_titles (:obj:`list` of :obj:`str`): A list of title IDs for each title the person is known for.
    """

    def __init__(self, name_id, primary_name, birth_year, death_year, primary_professions, known_for_titles):
        self._name_id = name_id
        self._primary_name = primary_name
        self._birth_year = None
        self._death_year = None
        self._primary_professions = []
        self._known_for_titles = []

        self.birth_year = birth_year
        self.death_year = death_year
        self.primary_professions = primary_professions
        self.known_for_titles = known_for_titles

    @property
    def name_id(self):
        return self._name_id

    @property
    def primary_name(self):
        return self._primary_name

    @property
    def birth_year(self):
        return self._birth_year

    @birth_year.setter
    def birth_year(self, value):
        if is_int(value):
            self._birth_year = int(value)

    @property
    def death_year(self):
        return self._death_year

    @death_year.setter
    def death_year(self, value):
        if is_int(value):
            self._death_year = int(value)

    @property
    def primary_professions(self):
        return self._primary_professions

    @primary_professions.setter
    def primary_professions(self, value):
        if value is not None:
            self._primary_professions = value

    @property
    def known_for_titles(self):
        return self._known_for_titles

    @known_for_titles.setter
    def known_for_titles(self, value):
        if value is not None:
            self._known_for_titles = value

    def __str__(self):
        return f'{self._primary_name} ({self._name_id}): ' + \
            f'{"???" if self._birth_year is None else self._birth_year} - ' + \
            f'{"" if self._death_year is None else self._death_year}'


class CreditScrape:
    """Object to represent information for each person scraped from IMDb's `fullcredits` page for a title.

    This information is scraped from the `fullcredits` IMDb web page, and will either represent an actor or
    another crew member.

    Args:
        name_id (:obj:`str`): The person's ID used by IMDb prefixed with `nm`.
        title_id (:obj:`str`): The title's ID used by IMDb prefixed with `tt`.
        job_title (:obj:`str`): The job title the person is credited for on the title.
        credit (:obj:`str`): Further credits for the person on the title.
        episode_count (:obj:`int`): How many episodes the person is credited for if a
            TV series, otherwise `None`.
        episode_year_start (:obj:`int`): The year the person began being credited in the
            title if the title is a TV series, otherwise `None`.
        episode_year_end (:obj:`int`): The year the person stopped being credited in the
            title if the title is a TV series, otherwise `None`.
    """

    def __init__(self, name_id, title_id, job_title, credit, episode_count, episode_year_start, episode_year_end):
        self._name_id = name_id
        self._title_id = title_id
        self._job_title = job_title
        self._credit = credit
        self._episode_count = None
        self._episode_year_start = None
        self._episode_year_end = None

        self.episode_count = episode_count
        self.episode_year_start = episode_year_start
        self.episode_year_end = episode_year_end

    @property
    def name_id(self):
        return self._name_id

    @property
    def title_id(self):
        return self._title_id

    @property
    def job_title(self):
        return self._job_title

    @property
    def credit(self):
        return self._credit

    @property
    def episode_count(self):
        return self._episode_count

    @episode_count.setter
    def episode_count(self, value):
        if is_int(value):
            self._episode_count = int(value)

    @property
    def episode_year_start(self):
        return self._episode_year_start

    @episode_year_start.setter
    def episode_year_start(self, value):
        if is_int(value):
            self._episode_year_start = int(value)

    @property
    def episode_year_end(self):
        return self._episode_year_end

    @episode_year_end.setter
    def episode_year_end(self, value):
        if is_int(value):
            self._episode_year_end = int(value)

    def __str__(self):
        return f'{self.name_id}: {self.job_title} in {self.title_id} as {self.credit}'


class NameScrape:
    """Specific information on a person scraped from IMDb.

    This information is taken from IMDb's `bio` web page on a person to find detailed information.

    Args:
        name_id (:obj:`str`): The person's ID used by IMDb prefixed with `nm`.
        display_name (:obj:`str`): The name IMDb lists the person having currently. Usually
            how they are well known or credited.
        birth_name (:obj:`str`): The name IMDb lists the person born as.
        birth_date (:obj:`datetime`): The date the person was born.
        birth_city (:obj:`str`): The city the person was born in.
        death_date (:obj:`datetime`): The date the person died, or `None` otherwise.
        death_city (:obj:`str`): The city the person died in, or `None` otherwise.
        death_cause (:obj:`str`): The person's cause of death, or `None` otherwise.
        nicknames (:obj:`list` of :obj:`str`): All of the person's nicknames.
        height (:obj:`float`): How tall the person is in meters.
    """

    def __init__(self, name_id, display_name, birth_name, birth_date, birth_city,
            death_date, death_city, death_cause, nicknames, height):
        self._name_id = name_id
        self._display_name = display_name
        self._birth_name = birth_name
        self._birth_date = None
        self._birth_city = birth_city
        self._death_date = None
        self._death_city = death_city
        self._death_cause = death_cause
        self._nicknames = nicknames
        self._height = None

        self.birth_date = birth_date
        self.death_date = death_date
        self.height = height

    @property
    def name_id(self):
        return self._name_id

    @property
    def display_name(self):
        return self._display_name

    @property
    def birth_name(self):
        return self._birth_name

    @property
    def birth_date(self):
        return self._birth_date

    @birth_date.setter
    def birth_date(self, value):
        self._birth_date = to_datetime(value)

    @property
    def birth_city(self):
        return self._birth_city

    @property
    def death_date(self):
        return self._death_date

    @death_date.setter
    def death_date(self, value):
        self._death_date = to_datetime(value)

    @property
    def death_city(self):
        return self._death_city

    @property
    def death_cause(self):
        return self._death_cause

    @property
    def nicknames(self):
        return self._nicknames

    @property
    def height(self):
        return self._height

    @height.setter
    def height(self, value):
        if is_float(value):
            self._height = float(value)

    def __str__(self):
        return f'{self.display_name} [{self.name_id}] ({self.birth_date} - ' + \
               f'{self.death_date if self.death_date is not None else ""}): {self.height}m'


class NameCreditScrape:
    """Stores credit information from a person's `full filmography` on IMDb.

    This information is taken from IMDb's `full filmography` section of a person's
    personal web page.

    Args:
        name_id (:obj:`str`): The person's ID used by IMDb prefixed with `nm`.
        title_id (:obj:`str`): The titles's ID used by IMDb prefixed with `tt`.
        category (:obj:`str`): The category this credit is listed under in the filmography section.
        start_year (:obj:`int`): The year the title released, or the starting year they were credited
            for on a TV series.
        end_year (:obj:`int`): The year the person stopped being credited on a TV series, or `None` otherwise.
        role (:obj:`str`): A string of the role the person is credited for the title, such as character.
        title_notes (:obj:`list` of :obj:`str`): A list of further notes for a person's credit on a title.
    """

    def __init__(self, name_id, title_id, category, start_year, end_year, role, title_notes):
        self._name_id = name_id
        self._title_id = title_id
        self._category = category
        self._start_year = None
        self._end_year = None
        self._role = role
        self._title_notes = title_notes

        self.start_year = start_year
        self.end_year = end_year

    @property
    def name_id(self):
        return self._name_id

    @property
    def title_id(self):
        return self._title_id

    @property
    def category(self):
        return self._category

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
    def role(self):
        return self._role

    @property
    def title_notes(self):
        return self._title_notes

    def __str__(self):
        return f'{self.name_id} in {self.title_id} ({self.start_year}' + \
               f'{f" - {self.end_year}" if self.end_year is not None else ""}) as {self.category}. ' + \
               f'Role: {self.role}. {f"Notes: {self.title_notes}" if self.title_notes is not None else ""}'
