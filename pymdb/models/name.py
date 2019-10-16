from pymdb.utils.util import is_int

class NameBasics:
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
        if value is not None and is_int(value):
            self._birth_year = int(value)

    @property
    def death_year(self):
        return self._death_year

    @death_year.setter
    def death_year(self, value):
        if value is not None and is_int(value):
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
    def __init__(self, name_id, name, title_id, job_title, credit):
        self._name_id = name_id
        self._name = name
        self._title_id = title_id
        self._job_title = job_title
        self._credit = credit

    @property
    def name_id(self):
        return self._name_id

    @property
    def name(self):
        return self._name

    @property
    def title_id(self):
        return self._title_id

    @property
    def job_title(self):
        return self._job_title

    @property
    def credit(self):
        return self._credit

    def __str__(self):
        return f'{self.name} ({self.name_id}): {self.job_title} in {self.title_id} as {self.credit}'