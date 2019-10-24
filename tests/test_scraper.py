"""Module to test functionality of the PyMDbScraper."""

import unittest
import re
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
        pass

    def test_get_name_actor_deceased(self):
        pass

    def test_get_name_director(self):
        pass

    def test_get_name_crew_member(self):
        pass

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
        pass

    def test_get_company_credits_tv_series(self):
        pass

    def test_get_company_credits_tv_episode(self):
        pass

    def test_get_company_credits_bad_request(self):
        title_id = 'nm123456789'
        scraper = PyMDbScraper()
        with self.assertRaises(HTTPError):
            for c in scraper.get_company_credits(title_id):
                pass


class TestGetTechSpecs(unittest.TestCase):
    def test_get_tech_specs_movie(self):
        pass

    def test_get_tech_specs_tv_series(self):
        pass

    def test_get_tech_specs_tv_episode(self):
        pass

    def test_get_tech_specs_bad_request(self):
        title_id = 'nm123456789'
        scraper = PyMDbScraper()
        with self.assertRaises(HTTPError):
            scraper.get_tech_specs(title_id)
