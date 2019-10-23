"""The classes used to represent various information about companies on IMDb.

All information for the classes here will be scraped from IMDb web pages.
"""

from pymdb.utils import is_int


class CompanyScrape:
    """Stores a title a company is credited in on IMDb.

    This information is taken from IMDb's search by company ID for titles
    that include it in their credits.
    """

    def __init__(self, company_id, title_id, start_year, end_year, notes):
        """Initialize a CompanyScrape object with all information it will store.

        Args:
            company_id: A string of the companys's ID used by IMDb prefixed with 'co'.
            title_id: A string of the titles's ID used by IMDb prefixed with 'tt'.
            start_year: An integer or string representation of the year the title released,
                or the year the company started being credited if a TV series.
            end_year: An integer or string representation of the year the company stopped
                being credited if a TV series, or None otherwise.
            notes: A list of strings for further notes IMDb gives about the credit.
        """

        self._company_id = company_id
        self._title_id = title_id
        self._start_year = None
        self._end_year = None
        self._notes = notes

        self.start_year = start_year
        self.end_year = end_year

    @property
    def company_id(self):
        return self._company_id

    @property
    def title_id(self):
        return self._title_id

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
    def notes(self):
        return self._notes

    def __str__(self):
        return f'{self.company_id} produced {self.title_id} ({self.start_year}' + \
               f'{f"-{self.end_year}" if self.end_year is not None else ""}). Notes: {self.notes}'


class CompanyCreditScrape:
    """Stores a company that is credited on a title's IMDb page.

    This information is taken from a title's IMDb company credits page, and contains
    more information on what a company is credited on a title for.
    """

    def __init__(self, company_id, title_id, company_name, category, notes):
        """Initialize a CompanyCreditScrape object with all information it will store.

        Args:
            company_id: A string of the company's ID used by IMDb prefixed with 'co'.
            title_id: A string of the titles's ID used by IMDb prefixed with 'tt'.
            company_name: A string of the company's name it was credited under.
            category: A string of the category the company was credited for.
            notes: A list of strings for further notes IMDb gives about the credit.
        """

        self._company_id = company_id
        self._title_id = title_id
        self._company_name = company_name
        self._category = category
        self._notes = notes

    @property
    def company_id(self):
        return self._company_id

    @property
    def title_id(self):
        return self._title_id

    @property
    def company_name(self):
        return self._company_name

    @property
    def category(self):
        return self._category

    @property
    def notes(self):
        return self._notes

    def __str__(self):
        return f'{self.company_name} ({self.company_id}) is a {self.category} for {self.title_id}. Notes: {self.notes}'
