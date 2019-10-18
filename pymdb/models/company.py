from pymdb.utils.util import is_int

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