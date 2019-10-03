class Name:
    def __init__(
            self, name_id, primary_name, birth_year, death_year, primary_professions, birth_date, birth_location,
            death_date, death_location, alternate_names, height):
        self._name_id = name_id
        self._primary_name = primary_name
        self._birth_year = birth_year
        self._death_year = death_year
        self._primary_professions = primary_professions
        self._birth_date = birth_date
        self._birth_location = birth_location
        self._death_date = death_date
        self._death_location = death_location
        self._alternate_names = alternate_names
        self._height = height

    def __str__(self):
        return f'''
            {self._primary_name} ({self._name_id}): {self._birth_year} - 
            {"Present" if self._death_year is None else self._death_year}
        '''


class NameBasics:
    def __init__(self, name_id, primary_name, birth_year, death_year, primary_professions, known_for_titles):
        self._name_id = name_id
        self._primary_name = primary_name
        self._birth_year = birth_year
        self._death_year = death_year
        self._primary_professions = primary_professions
        self._known_for_titles = known_for_titles

    def __str__(self):
        return f'{self._primary_name} ({self._name_id}): ' + \
            f'{"???" if self._birth_year is None else self._birth_year} - ' + \
            f'{"Present" if self._death_year is None else self._death_year}'
