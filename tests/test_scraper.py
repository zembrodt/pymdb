"""Module to test functionality of the PyMDbScraper."""

import unittest
import re
from collections import defaultdict
from datetime import datetime
from requests.exceptions import HTTPError
from pymdb.exceptions import InvalidCompanyId
from pymdb.scraper import PyMDbScraper


class TestGetTitle(unittest.TestCase):
    def test_get_title_movie(self):
        title_id = 'tt0076759'
        scraper = PyMDbScraper()
        title = scraper.get_title(title_id, include_taglines=True)

        # Correct values
        title_text = 'Star Wars: Episode IV - A New Hope'
        title_parent_id = None
        mpaa_rating = 'PG'
        country = 'USA'
        language = 'English'
        release_date = datetime(1977, 5, 25)
        end_year = None
        season_number = None
        episode_number = None
        taglines = [
            'It\'s Back! The Force will be with you for three weeks only. (1979 Reissue Poster)',
            'May the Force be with you. One year old today. (Star Wars Happy Birthday Poster)',
            'The force will be with you (re-release)',
            'Somewhere, in space, this could all be happening right now.',
            'The original is back. (1982 Reissue)',
            'A long time ago in a galaxy far, far away...',
            'Coming to your galaxy this summer.  (Teaser poster)'
        ]
        plot = '''
            Luke Skywalker joins forces with a Jedi Knight, a cocky pilot, a Wookiee and two 
            droids to save the galaxy from the Empire's world-destroying battle station, 
            while also attempting to rescue Princess Leia from the mysterious Darth Vader.
            '''
        storyline = '''
            The Imperial Forces, under orders from cruel Darth Vader, hold Princess Leia hostage 
            in their efforts to quell the rebellion against the Galactic Empire. Luke Skywalker 
            and Han Solo, captain of the Millennium Falcon, work together with the companionable 
            droid duo R2-D2 and C-3PO to rescue the beautiful princess, help the Rebel Alliance 
            and restore freedom and justice to the Galaxy.
            '''
        production_companies = ['co0071326', 'co0000756']
        top_cast = [
            'nm0000434',
            'nm0000148',
            'nm0000402',
            'nm0001088',
            'nm0000027',
            'nm0000355',
            'nm0048652',
            'nm0562679',
            'nm0001190',
            'nm0114436',
            'nm0292235',
            'nm0701023',
            'nm0567018',
            'nm0125952',
            'nm0377120'
        ]
        budget = 11000000
        opening_weekend_gross = 1554475
        opening_weekend_date = datetime(1977, 5, 30)
        usa_gross = 460998507
        worldwide_gross = 775512064

        self.assertEqual(title.title_id, title_id)
        self.assertEqual(title.title_text, title_text)
        self.assertEqual(title.title_parent_id, title_parent_id)
        self.assertEqual(title.mpaa_rating, mpaa_rating)
        self.assertEqual(title.country, country)
        self.assertEqual(title.language, language)
        self.assertEqual(title.release_date, release_date)
        self.assertEqual(title.end_year, end_year)
        self.assertEqual(title.season_number, season_number)
        self.assertEqual(title.episode_number, episode_number)
        self.assertEqual(sorted(title.taglines), sorted(taglines))
        self.assertEqual(re.sub(r'\s+', '', title.plot), re.sub(r'\s+', '', plot))
        self.assertEqual(re.sub(r'\s+', '', title.storyline), re.sub(r'\s+', '', storyline))
        self.assertEqual(sorted(title.production_companies), sorted(production_companies))
        self.assertEqual(sorted(title.top_cast), sorted(top_cast))
        self.assertEqual(title.budget, budget)
        self.assertEqual(title.opening_weekend_gross, opening_weekend_gross)
        self.assertEqual(title.opening_weekend_date, opening_weekend_date)
        self.assertEqual(title.usa_gross, usa_gross)
        self.assertEqual(title.worldwide_gross, worldwide_gross)

    def test_get_title_tv_series(self):
        title_id = 'tt0149460'
        scraper = PyMDbScraper()
        title = scraper.get_title(title_id, include_taglines=True)

        # Correct values
        title_text = 'Futurama'
        title_parent_id = None
        mpaa_rating = 'TV-14'
        country = 'USA'
        language = 'English'
        release_date = datetime(1999, 3, 28)
        end_year = datetime(2013, 1, 1)
        season_number = None
        episode_number = None
        taglines = [
            'The future is here!',
            '1000 years in the making!'
        ]
        plot = '''
            Philip J. Fry, a pizza delivery boy, is accidentally frozen in 1999 and thawed out 
            on New Year's Eve 2999.
            '''
        storyline = '''
            Philip J. Fry is a twenty-five-year-old pizza delivery boy whose life is going nowhere. 
            When he accidentally freezes himself on December 31, 1999, he wakes up one thousand 
            years in the future, and has a chance to make a fresh start. He goes to work for the 
            Planet Express Corporation, a futuristic delivery service that transports packages to 
            all five quadrants of the universe. His companions include the delivery ship's Captain, 
            Leela, a beautiful one-eyed female alien who kicks some serious butt, and Bender, a 
            robot with very human flaws.
            '''
        production_companies = ['co0223402', 'co0056447', 'co0159275']
        top_cast = [
            'nm0921942',
            'nm0005408',
            'nm0224007',
            'nm0534134',
            'nm0482851',
            'nm0866300',
            'nm0005606',
            'nm0379114'
        ]
        budget = None
        opening_weekend_gross = None
        opening_weekend_date = None
        usa_gross = None
        worldwide_gross = None

        self.assertEqual(title.title_id, title_id)
        self.assertEqual(title.title_text, title_text)
        self.assertEqual(title.title_parent_id, title_parent_id)
        self.assertEqual(title.mpaa_rating, mpaa_rating)
        self.assertEqual(title.country, country)
        self.assertEqual(title.language, language)
        self.assertEqual(title.release_date, release_date)
        self.assertEqual(title.end_year, end_year)
        self.assertEqual(title.season_number, season_number)
        self.assertEqual(title.episode_number, episode_number)
        self.assertEqual(sorted(title.taglines), sorted(taglines))
        self.assertEqual(re.sub(r'\s+', '', title.plot), re.sub(r'\s+', '', plot))
        self.assertEqual(re.sub(r'\s+', '', title.storyline), re.sub(r'\s+', '', storyline))
        self.assertEqual(sorted(title.production_companies), sorted(production_companies))
        self.assertEqual(sorted(title.top_cast), sorted(top_cast))
        self.assertEqual(title.budget, budget)
        self.assertEqual(title.opening_weekend_gross, opening_weekend_gross)
        self.assertEqual(title.opening_weekend_date, opening_weekend_date)
        self.assertEqual(title.usa_gross, usa_gross)
        self.assertEqual(title.worldwide_gross, worldwide_gross)

    def test_get_title_tv_episode(self):
        title_id = 'tt4283088'
        scraper = PyMDbScraper()
        title = scraper.get_title(title_id, include_taglines=True)

        # Correct values
        title_text = 'Battle of the Bastards'
        title_parent_id = 'tt0944947'
        mpaa_rating = 'TV-MA'
        country = 'USA'
        language = 'English'
        release_date = datetime(2016, 6, 19)
        end_year = None
        season_number = 6
        episode_number = 9
        taglines = []
        plot = '''
            Jon and Sansa face Ramsay Bolton on the fields of Winterfell. Daenerys strikes back at
            her enemies. Theon and Yara arrive in Meereen.
            '''
        storyline = '''
            Meereen is under siege and the fleet of the masters is attacking the city. Daenerys wants 
            to destroy their cities but Tyrion convinces her to not incur in the same mistake of her 
            father in King's Landing. They schedule a meeting with the masters to discuss the terms of 
            surrender. However the masters misunderstand and believe Daenerys want to surrender. She 
            rides Drogon and together with the two other dragons, they burn part of the fleet. Meanwhile 
            Daario and the Dothraki attack the Sons of the Harpy. Then Yara and Theon team up with 
            Daenerys to accept the independence of the Iron Isles and to overthrow Euron. In Winterfell, 
            Jon Snow, Sansa, Davos and Tormund meet with Ramsay, and Jon Snow proposes a dispute between 
            them instead of sacrificing lives in a battle. Ramsay does not accept and they schedule the 
            battle in the morning. Jon Snow plots a scheme with Davos and Tormund and Sansa warns that 
            Ramsay plays dirty. When both armies are ready to battle, Ramsay brings a surprise that ...
            '''
        production_companies = ['co0335036', 'co0418998', 'co0343278']
        top_cast = [
            'nm0227759',
            'nm3229685',
            'nm3592338',
            'nm0192377',
            'nm3849842',
            'nm0318821',
            'nm0396924',
            'nm2812026',
            'nm1970465',
            'nm3701064',
            'nm0654295',
            'nm0401264',
            'nm2760664',
            'nm2247629',
            'nm1613839'
        ]
        budget = 10000000
        opening_weekend_gross = None
        opening_weekend_date = None
        usa_gross = None
        worldwide_gross = None

        self.assertEqual(title.title_id, title_id)
        self.assertEqual(title.title_text, title_text)
        self.assertEqual(title.title_parent_id, title_parent_id)
        self.assertEqual(title.mpaa_rating, mpaa_rating)
        self.assertEqual(title.country, country)
        self.assertEqual(title.language, language)
        self.assertEqual(title.release_date, release_date)
        self.assertEqual(title.end_year, end_year)
        self.assertEqual(title.season_number, season_number)
        self.assertEqual(title.episode_number, episode_number)
        self.assertEqual(sorted(title.taglines), sorted(taglines))
        self.assertEqual(re.sub(r'\s+', '', title.plot), re.sub(r'\s+', '', plot))
        self.assertEqual(re.sub(r'\s+', '', title.storyline), re.sub(r'\s+', '', storyline))
        self.assertEqual(sorted(title.production_companies), sorted(production_companies))
        self.assertEqual(sorted(title.top_cast), sorted(top_cast))
        self.assertEqual(title.budget, budget)
        self.assertEqual(title.opening_weekend_gross, opening_weekend_gross)
        self.assertEqual(title.opening_weekend_date, opening_weekend_date)
        self.assertEqual(title.usa_gross, usa_gross)
        self.assertEqual(title.worldwide_gross, worldwide_gross)

    def test_get_title_bad_request(self):
        title_id = 'nm123456789'
        scraper = PyMDbScraper()
        with self.assertRaises(HTTPError):
            scraper.get_title(title_id)


class TestGetFullCast(unittest.TestCase):
    def test_get_full_cast_movie(self):
        pass

    def test_get_full_cast_tv_series(self):
        pass

    def test_get_full_cast_tv_series_and_episodes(self):
        pass

    def test_get_full_cast_episode(self):
        pass

    def test_get_full_cast_bad_request(self):
        title_id = 'nm123456789'
        scraper = PyMDbScraper()
        with self.assertRaises(HTTPError):
            for c in scraper.get_full_cast(title_id):
                pass


class TestGetFullCredits(unittest.TestCase):
    def test_get_full_credits_movie(self):
        pass

    def test_get_full_credits_tv_series(self):
        pass

    def test_get_full_credits_tv_episode(self):
        pass

    def test_get_full_credits_bad_request(self):
        title_id = 'nm123456789'
        scraper = PyMDbScraper()
        with self.assertRaises(HTTPError):
            for c in scraper.get_full_credits(title_id):
                pass


class TestGetName(unittest.TestCase):
    def test_get_name_actor_alive(self):
        name_id = 'nm0000375'
        scraper = PyMDbScraper()
        name = scraper.get_name(name_id)

        # Correct values
        display_name = 'Robert Downey Jr.'
        birth_date = datetime(1965, 4, 4)
        birth_city = 'Manhattan, New York City, New York, USA'
        death_date = None
        death_city = None
        death_cause = None
        birth_name = 'Robert John Downey Jr'
        nicknames = ['Bob', 'RDJ']
        height = 1.74

        self.assertEqual(name.name_id, name_id)
        self.assertEqual(name.display_name, display_name)
        self.assertEqual(name.birth_date, birth_date)
        self.assertEqual(name.birth_city, birth_city)
        self.assertEqual(name.death_date, death_date)
        self.assertEqual(name.death_city, death_city)
        self.assertEqual(name.death_cause, death_cause)
        self.assertEqual(name.birth_name, birth_name)
        self.assertEqual(sorted(name.nicknames), sorted(nicknames))
        self.assertEqual(name.height, height)

    def test_get_name_actor_deceased(self):
        name_id = 'nm0000122'
        scraper = PyMDbScraper()
        name = scraper.get_name(name_id)

        # Correct values
        display_name = 'Charles Chaplin'
        birth_date = datetime(1889, 4, 16)
        birth_city = 'Walworth, London, England, UK'
        death_date = datetime(1977, 12, 25)
        death_city = 'Vevey, Vaud, Switzerland'
        death_cause = 'stroke'
        birth_name = 'Charles Spencer Chaplin'
        nicknames = ['Charlie', 'Charlot', 'The Little Tramp']
        height = 1.63

        self.assertEqual(name.name_id, name_id)
        self.assertEqual(name.display_name, display_name)
        self.assertEqual(name.birth_date, birth_date)
        self.assertEqual(name.birth_city, birth_city)
        self.assertEqual(name.death_date, death_date)
        self.assertEqual(name.death_city, death_city)
        self.assertEqual(name.death_cause, death_cause)
        self.assertEqual(name.birth_name, birth_name)
        self.assertEqual(sorted(name.nicknames), sorted(nicknames))
        self.assertEqual(name.height, height)

    def test_get_name_director(self):
        name_id = 'nm0796117'
        scraper = PyMDbScraper()
        name = scraper.get_name(name_id)

        # Correct values
        display_name = 'M. Night Shyamalan'
        birth_date = datetime(1970, 8, 6)
        birth_city = 'Mahé, Pondicherry, India'
        death_date = None
        death_city = None
        death_cause = None
        birth_name = 'Manoj Nelliyattu Shyamalan'
        nicknames = []
        height = 1.78

        self.assertEqual(name.name_id, name_id)
        self.assertEqual(name.display_name, display_name)
        self.assertEqual(name.birth_date, birth_date)
        self.assertEqual(name.birth_city, birth_city)
        self.assertEqual(name.death_date, death_date)
        self.assertEqual(name.death_city, death_city)
        self.assertEqual(name.death_cause, death_cause)
        self.assertEqual(name.birth_name, birth_name)
        self.assertEqual(sorted(name.nicknames), sorted(nicknames))
        self.assertEqual(name.height, height)

    def test_get_name_crew_member(self):
        name_id = 'nm2361112'
        scraper = PyMDbScraper()
        name = scraper.get_name(name_id)

        # Correct values
        display_name = 'James Sled'
        birth_date = None
        birth_city = None
        death_date = None
        death_city = None
        death_cause = None
        birth_name = None
        nicknames = []
        height = None

        self.assertEqual(name.name_id, name_id)
        self.assertEqual(name.display_name, display_name)
        self.assertEqual(name.birth_date, birth_date)
        self.assertEqual(name.birth_city, birth_city)
        self.assertEqual(name.death_date, death_date)
        self.assertEqual(name.death_city, death_city)
        self.assertEqual(name.death_cause, death_cause)
        self.assertEqual(name.birth_name, birth_name)
        self.assertEqual(sorted(name.nicknames), sorted(nicknames))
        self.assertEqual(name.height, height)

    def test_get_name_bad_request(self):
        name_id = 'tt123456789'
        scraper = PyMDbScraper()
        with self.assertRaises(HTTPError):
            scraper.get_name(name_id)


class TestGetNameCredits(unittest.TestCase):
    def test_get_name_credits_actor(self):
        pass

    def test_get_name_credits_actor_with_episodes(self):
        pass

    def test_get_name_credits_director(self):
        pass

    def test_get_name_credits_director_with_episodes(self):
        pass

    def test_get_name_credits_crew_member(self):
        pass

    def test_get_name_credits_crew_member_with_episodes(self):
        pass

    def test_get_name_credits_bad_request(self):
        name_id = 'tt123456789'
        scraper = PyMDbScraper()
        with self.assertRaises(HTTPError):
            for n in scraper.get_name_credits(name_id):
                pass


class TestGetCompany(unittest.TestCase):
    def test_get_company_single_page(self):
        company_id = 'co0102418'
        scraper = PyMDbScraper()
        valid_titles = {'tt0120737', 'tt0380510', 'tt0094184', 'tt0219858'}
        for company in scraper.get_company(company_id):
            self.assertEqual(company.company_id, company_id)
            if company.title_id in valid_titles:
                valid_titles.remove(company.title_id)
        self.assertEqual(len(valid_titles), 0)

    def test_get_company_multiple_pages(self):
        company_id = 'co0076091'
        scraper = PyMDbScraper()
        valid_titles = {
            'tt1856101', 'tt1219827', 'tt0338526', 'tt1136608', 'tt1596576', 'tt0477407', 'tt0806017', 'tt4656248'
        }
        for company in scraper.get_company(company_id):
            self.assertEqual(company.company_id, company_id)
            if company.title_id in valid_titles:
                valid_titles.remove(company.title_id)
        self.assertEqual(len(valid_titles), 0)

    def test_get_company_bad_request(self):
        company_id = 'tt123456789'
        scraper = PyMDbScraper()
        with self.assertRaises(InvalidCompanyId):
            for c in scraper.get_company(company_id):
                pass


class TestGetCompanyCredits(unittest.TestCase):
    def test_get_company_credits_movie(self):
        title_id = 'tt4154796'
        scraper = PyMDbScraper()
        company_credits = scraper.get_company_credits(title_id)

        # Correct results
        production_company_id = 'co0051941'
        production_company_name = 'Marvel Studios'
        production_companies = 'production'
        production_companies_num = 1
        distributors = 'distributors'
        distributors_num = 53
        special_effects = 'specialEffects'
        special_effects_num = 25
        special_effects_company_id = 'co0072491'
        special_effects_company_name = 'Industrial Light & Magic (ILM)'
        other_companies = 'other'
        other_companies_num = 59
        other_company_id = 'co0057495'
        other_company_name = 'IMAX'

        company_info = defaultdict(int)
        discovered_ids = 0
        for company_credit in company_credits:
            if company_credit.category not in company_info:
                company_info[company_credit.category] = 0
            company_info[company_credit.category] += 1

            if company_credit.company_id == production_company_id:
                discovered_ids += 1
                self.assertEqual(company_credit.company_id, production_company_id)
                self.assertEqual(company_credit.title_id, title_id)
                self.assertEqual(company_credit.company_name, production_company_name)
                self.assertEqual(company_credit.category, production_companies)
                self.assertEqual(company_credit.notes, [])
            elif company_credit.company_id == special_effects_company_id:
                discovered_ids += 1
                self.assertEqual(company_credit.company_id, special_effects_company_id)
                self.assertEqual(company_credit.title_id, title_id)
                self.assertEqual(company_credit.company_name, special_effects_company_name)
                self.assertEqual(company_credit.category, special_effects)
                self.assertEqual(sorted(company_credit.notes), sorted(['ILM', 'visual effects and animation']))
            elif company_credit.company_id == other_company_id:
                discovered_ids += 1
                self.assertEqual(company_credit.company_id, other_company_id)
                self.assertEqual(company_credit.title_id, title_id)
                self.assertEqual(company_credit.company_name, other_company_name)
                self.assertEqual(company_credit.category, other_companies)
                self.assertEqual(sorted(company_credit.notes), sorted(['specially formatted in',]))
        self.assertEqual(discovered_ids, 3)
        self.assertEqual(company_info[production_companies], production_companies_num)
        self.assertEqual(company_info[distributors], distributors_num)
        self.assertEqual(company_info[special_effects], special_effects_num)
        self.assertEqual(company_info[other_companies], other_companies_num)

    def test_get_company_credits_tv_series(self):
        title_id = 'tt0149460'
        scraper = PyMDbScraper()
        company_credits = scraper.get_company_credits(title_id)

        # Correct results
        production_company_id = 'co0223402'
        production_company_name = 'The Curiosity Company'
        production_companies = 'production'
        production_companies_num = 3
        distributors = 'distributors'
        distributors_num = 39
        special_effects = 'specialEffects'
        special_effects_num = 0
        other_companies = 'other'
        other_companies_num = 6
        other_company_id = 'co0055255'
        other_company_name = 'Rough Draft Studios'

        company_info = defaultdict(int)
        discovered_ids = 0
        for company_credit in company_credits:
            if company_credit.category not in company_info:
                company_info[company_credit.category] = 0
            company_info[company_credit.category] += 1

            if company_credit.company_id == production_company_id:
                discovered_ids += 1
                self.assertEqual(company_credit.company_id, production_company_id)
                self.assertEqual(company_credit.title_id, title_id)
                self.assertEqual(company_credit.company_name, production_company_name)
                self.assertEqual(company_credit.category, production_companies)
                self.assertEqual(company_credit.notes, [])
            elif company_credit.company_id == other_company_id:
                discovered_ids += 1
                self.assertEqual(company_credit.company_id, other_company_id)
                self.assertEqual(company_credit.title_id, title_id)
                self.assertEqual(company_credit.company_name, other_company_name)
                self.assertEqual(company_credit.category, other_companies)
                self.assertEqual(sorted(company_credit.notes), sorted(['animation produced by']))
        self.assertEqual(discovered_ids, 2)
        self.assertEqual(company_info[production_companies], production_companies_num)
        self.assertEqual(company_info[distributors], distributors_num)
        self.assertEqual(company_info[special_effects], special_effects_num)
        self.assertEqual(company_info[other_companies], other_companies_num)

    def test_get_company_credits_tv_episode(self):
        title_id = 'tt4283088'
        scraper = PyMDbScraper()
        company_credits = scraper.get_company_credits(title_id)

        # Correct results
        production_company_id = 'co0418998'
        production_company_name = 'Startling'
        production_companies = 'production'
        production_companies_num = 3
        distributors = 'distributors'
        distributors_num = 4
        special_effects = 'specialEffects'
        special_effects_num = 11
        special_effects_company_id = 'co0069055'
        special_effects_company_name = 'Image Engine Design'
        other_companies = 'other'
        other_companies_num = 33
        other_company_id = 'co0280563'
        other_company_name = 'Elastic'

        company_info = defaultdict(int)
        discovered_ids = 0
        for company_credit in company_credits:
            company_info[company_credit.category] += 1

            if company_credit.company_id == production_company_id:
                discovered_ids += 1
                self.assertEqual(company_credit.company_id, production_company_id)
                self.assertEqual(company_credit.title_id, title_id)
                self.assertEqual(company_credit.company_name, production_company_name)
                self.assertEqual(company_credit.category, production_companies)
                self.assertEqual(company_credit.notes, [])
            elif company_credit.company_id == special_effects_company_id:
                discovered_ids += 1
                self.assertEqual(company_credit.company_id, special_effects_company_id)
                self.assertEqual(company_credit.title_id, title_id)
                self.assertEqual(company_credit.company_name, special_effects_company_name)
                self.assertEqual(company_credit.category, special_effects)
                self.assertEqual(sorted(company_credit.notes), sorted(['additional visual effects', 'as Image Engine']))
            elif company_credit.company_id == other_company_id:
                discovered_ids += 1
                self.assertEqual(company_credit.company_id, other_company_id)
                self.assertEqual(company_credit.title_id, title_id)
                self.assertEqual(company_credit.company_name, other_company_name)
                self.assertEqual(company_credit.category, other_companies)
                self.assertEqual(sorted(company_credit.notes), sorted(['main title design',]))
        self.assertEqual(discovered_ids, 3)
        self.assertEqual(company_info[production_companies], production_companies_num)
        self.assertEqual(company_info[distributors], distributors_num)
        self.assertEqual(company_info[special_effects], special_effects_num)
        self.assertEqual(company_info[other_companies], other_companies_num)

    def test_get_company_credits_bad_request(self):
        title_id = 'nm123456789'
        scraper = PyMDbScraper()
        with self.assertRaises(HTTPError):
            for c in scraper.get_company_credits(title_id):
                pass


class TestGetTechSpecs(unittest.TestCase):
    def test_get_tech_specs_movie(self):
        title_id = 'tt4154796'
        scraper = PyMDbScraper()
        tech_specs = scraper.get_tech_specs(title_id)

        # Correct values
        runtime = 181
        sound_mix = [
            'Dolby Atmos',
            'Auro 11.1',
            'Dolby Surround 7.1',
            'DTS (DTS: X)',
            'Dolby Digital',
            'Sonics-DDP',
            '12-Track Digital Sound',
            'IMAX 6-Track',
            'SDDS'
        ]
        color = 'Color (ACES)'
        aspect_ratio = ['1.90 : 1 (IMAX)', '2.39 : 1']
        camera = [
            'Arri Alexa 65 IMAX',
            'Panavision Sphero 65',
            'APO Panatar Lenses'
        ]
        laboratory = [
            'Company 3 (digital intermediate)',
            'PIX System, San Francisco (CA), USA (additional dailies services)',
            'Pinewood Digital, London, UK (digital dailies)',
            'Technicolor, Hollywood (CA), USA (digital intermediate)'
        ]
        negative_format = 'Codex'
        cinematographic_process = [
            'ARRIRAW (6.5K) (source format)',
            'Digital Intermediate (2K) (master format)',
            'Ultra Panavision 70 (anamorphic) (source format)'
        ]
        printed_film_format = 'D-Cinema (also 3-D version)'

        self.assertEqual(tech_specs.title_id, title_id)
        self.assertEqual(tech_specs.runtime, runtime)
        self.assertEqual(sorted(tech_specs.sound_mix), sorted(sound_mix))
        self.assertEqual(tech_specs.color, color)
        self.assertEqual(sorted(tech_specs.aspect_ratio), sorted(aspect_ratio))
        self.assertEqual(sorted(tech_specs.camera), sorted(camera))
        self.assertEqual(sorted(tech_specs.laboratory), sorted(laboratory))
        self.assertEqual(tech_specs.negative_format, negative_format)
        self.assertEqual(sorted(tech_specs.cinematographic_process), sorted(cinematographic_process))
        self.assertEqual(tech_specs.printed_film_format, printed_film_format)

    def test_get_tech_specs_tv_series(self):
        title_id = 'tt0149460'
        scraper = PyMDbScraper()
        tech_specs = scraper.get_tech_specs(title_id)

        # Correct values
        runtime = 22
        sound_mix = [
            'Dolby',
            'Dolby Digital (seasons 6-)',
        ]
        color = 'Color'
        aspect_ratio = [
            '1.78 : 1 (seasons 6-)',
            '1.33 : 1 (seasons 1-5)'
        ]
        camera = []
        laboratory = []
        negative_format = None
        cinematographic_process = []
        printed_film_format = None

        self.assertEqual(tech_specs.title_id, title_id)
        self.assertEqual(tech_specs.runtime, runtime)
        self.assertEqual(sorted(tech_specs.sound_mix), sorted(sound_mix))
        self.assertEqual(tech_specs.color, color)
        self.assertEqual(sorted(tech_specs.aspect_ratio), sorted(aspect_ratio))
        self.assertEqual(sorted(tech_specs.camera), sorted(camera))
        self.assertEqual(sorted(tech_specs.laboratory), sorted(laboratory))
        self.assertEqual(tech_specs.negative_format, negative_format)
        self.assertEqual(sorted(tech_specs.cinematographic_process), sorted(cinematographic_process))
        self.assertEqual(tech_specs.printed_film_format, printed_film_format)

    def test_get_tech_specs_tv_episode(self):
        title_id = 'tt4283088'
        scraper = PyMDbScraper()
        tech_specs = scraper.get_tech_specs(title_id)

        # Correct values
        runtime = 60
        sound_mix = [
            'Dolby Digital',
            'Dolby Atmos (Blu-ray release)',
        ]
        color = 'Color'
        aspect_ratio = ['1.78 : 1']
        camera = []
        laboratory = []
        negative_format = None
        cinematographic_process = []
        printed_film_format = None

        self.assertEqual(tech_specs.title_id, title_id)
        self.assertEqual(tech_specs.runtime, runtime)
        self.assertEqual(sorted(tech_specs.sound_mix), sorted(sound_mix))
        self.assertEqual(tech_specs.color, color)
        self.assertEqual(sorted(tech_specs.aspect_ratio), sorted(aspect_ratio))
        self.assertEqual(sorted(tech_specs.camera), sorted(camera))
        self.assertEqual(sorted(tech_specs.laboratory), sorted(laboratory))
        self.assertEqual(tech_specs.negative_format, negative_format)
        self.assertEqual(sorted(tech_specs.cinematographic_process), sorted(cinematographic_process))
        self.assertEqual(tech_specs.printed_film_format, printed_film_format)

    def test_get_tech_specs_bad_request(self):
        title_id = 'nm123456789'
        scraper = PyMDbScraper()
        with self.assertRaises(HTTPError):
            scraper.get_tech_specs(title_id)


class TestGetTree(unittest.TestCase):
    def test_get_tree_200(self):
        request = 'https://www.imdb.com/'
        tree = PyMDbScraper()._get_tree(request)
        self.assertIsNotNone(tree)

    def test_get_tree_400(self):
        request = 'https://postman-echo.com/status/400'
        with self.assertRaises(HTTPError):
            PyMDbScraper()._get_tree(request)

    def test_get_tree_401(self):
        request = 'https://postman-echo.com/status/401'
        with self.assertRaises(HTTPError):
            PyMDbScraper()._get_tree(request)

    def test_get_tree_403(self):
        request = 'https://postman-echo.com/status/403'
        with self.assertRaises(HTTPError):
            PyMDbScraper()._get_tree(request)

    def test_get_tree_404(self):
        request = 'https://postman-echo.com/status/404'
        with self.assertRaises(HTTPError):
            PyMDbScraper()._get_tree(request)

    def test_get_tree_500(self):
        request = 'https://postman-echo.com/status/500'
        with self.assertRaises(HTTPError):
            PyMDbScraper()._get_tree(request)

    def test_get_tree_501(self):
        request = 'https://postman-echo.com/status/501'
        with self.assertRaises(HTTPError):
            PyMDbScraper()._get_tree(request)

    def test_get_tree_502(self):
        request = 'https://postman-echo.com/status/502'
        with self.assertRaises(HTTPError):
            PyMDbScraper()._get_tree(request)

    def test_get_tree_503(self):
        request = 'https://postman-echo.com/status/503'
        with self.assertRaises(HTTPError):
            PyMDbScraper()._get_tree(request)

    def test_get_tree_522(self):
        request = 'https://postman-echo.com/status/522'
        with self.assertRaises(HTTPError):
            PyMDbScraper()._get_tree(request)

    def test_get_tree_524(self):
        request = 'https://postman-echo.com/status/524'
        with self.assertRaises(HTTPError):
            PyMDbScraper()._get_tree(request)
