from pymdb.utils import is_int

class CompanyScrape:
    def __init__(self, company_id, title_id, start_year, end_year, notes):
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
        if value is not None and is_int(value):
            self._start_year = int(value)

    @property
    def end_year(self):
        return self._end_year

    @end_year.setter
    def end_year(self, value):
        if value is not None and is_int(value):
            self._end_year = int(value)

    @property
    def notes(self):
        return self._notes

    def __str__(self):
        return f'{self.company_id} produced {self.title_id} ({self.start_year}{f"-{self.end_year}" if self.end_year is not None else ""}). Notes: {self.notes}'

class CompanyCreditScrape:
    def __init__(self, company_id, title_id, company_name, category, notes):
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