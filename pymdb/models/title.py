class Title:
    def __init__(
            self, title_id, sub_title_id, title_type, primary_title, original_title, is_adult, start_year, end_year, 
            runtime_minutes, plot, description, release_date, tagline, rating, title_localized, region, language, 
            is_original_title):
        self._title_id = title_id
        self._sub_title_id = sub_title_id
        self._title_type = title_type
        self._primary_title = primary_title
        self._original_title = original_title
        self._is_adult = is_adult
        self._start_year = start_year
        self._end_year = end_year
        self._runtime_minutes = runtime_minutes
        self._plot = plot
        self._description = description
        self._release_date = release_date
        self._tagline = tagline
        self._rating = rating
        self._title_localized = title_localized
        self._region = region
        self._language = language
        self._is_original_title = is_original_title

    def __str__(self):
        return f'{self._primary_title} ({self._title_id}-{self._sub_title_id}): {self._title_type}'


# Additional information for a title
class TitleAkas:
    def __init__(self, title_id, sub_title_id, localized_title, region, language, types, attributes, is_original_title):
        self._title_id = title_id
        self._sub_title_id = sub_title_id
        self._localized_title = localized_title
        self._region = region
        self._language = language
        self._types = types
        self._attributes = attributes
        self._is_original_title = is_original_title

    def __str__(self):
        return f'{self._localized_title} ({self._title_id}_{self._sub_title_id})' + \
            f'{": " + self._region if self._region is not None else ""}' + \
            f'{" - " + self._language if self._language is not None and self._region is not None else ": " + self._language if self._language is not None else ""}'


# Basic information for a title
class TitleBasics:
    def __init__(self, title_id, title_type, primary_title, original_title, is_adult, start_year, end_year,
                 runtime_minutes, genres):
        self._title_id = title_id
        self._title_type = title_type
        self._primary_title = primary_title
        self._original_title = original_title
        self._is_adult = is_adult
        self._start_year = start_year
        self._end_year = end_year
        self._runtime_minutes = runtime_minutes
        self._genres = genres

    def __str__(self):
        return f'{self._primary_title} ({self._title_id}): {self._title_type}, ' + \
            f'{self._start_year if self._start_year is not None else "????"}' + \
            f'{" - " + str(self._end_year) if self._end_year is not None else ""}'


# Director(s) and writer(s) for a title
class TitleCrew:
    def __init__(self, title_id, director_ids, writer_ids):
        self._title_id = title_id
        self._director_ids = director_ids
        self._writer_ids = writer_ids

    def __str__(self):
        return f'{self._title_id}' + \
            f'{" directed by " + str(self._director_ids) if self._director_ids is not None else ""}' + \
            f'{" and written by " + str(self._writer_ids) if self._writer_ids is not None and self._director_ids is not None else " written by" + str(self._writer_ids) if self._director_ids is None else ""}'


class TitleEpisode:
    def __init__(self, title_id, parent_title_id, season_number, episode_number):
        self._title_id = title_id
        self._parent_title_id = parent_title_id
        self._season_number = season_number
        self._episode_number = episode_number

    def __str__(self):
        return f'{self._parent_title_id} {"S" + str(self._season_number) if self._season_number is not None else ""}' + \
            f'{"E" + str(self._episode_number) if self._episode_number is not None else ""}: {self._title_id}'


# Principal cast/crew for a title
class TitlePrincipalCrew:
    def __init__(self, title_id, sub_title_id, name_id, category, job, characters):
        self._title_id = title_id
        self._sub_title_id = sub_title_id
        self._name_id = name_id
        self._category = category
        self._job = job
        self._characters = characters

    def __str__(self):
        return f'{self._name_id} ({self._title_id}_{self._sub_title_id}): {self._category}' + \
            f'{" as " + self._job if self._job is not None else ""}' + \
            f'{" playing " + str(self._characters) if self._characters is not None else ""}'


class TitleRating:
    def __init__(self, title_id, average_rating, num_votes):
        self._title_id = title_id
        self._average_rating = average_rating
        self._num_votes = num_votes

    def __str__(self):
        return f'{self._title_id}: Rated {self._average_rating} with {self._num_votes} votes'
