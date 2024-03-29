"""Module to test functionality of the PyMDbScraper."""

import unittest
import re
from collections import defaultdict
from datetime import datetime
from requests.exceptions import HTTPError
from pymdb.exceptions import InvalidCompanyId
from pymdb.scraper import PyMDbScraper
from pymdb import CreditScrape, NameCreditScrape, SearchResultName, SearchResultTitle
from pymdb.models.name import (
    ACTOR,
    ART_DEPARTMENT,
    ASSISTANT_DIRECTOR,
    CAMERA_AND_ELECTRICAL_DEPARTMENT,
    CINEMATOGRAPHY,
    DIRECTOR,
    MUSIC,
    MUSIC_DEPARTMENT,
    OTHER_CREW,
    ADDITIONAL_CREW,
    PRODUCER,
    THANKS,
    WRITER,
)


class TestGetTitle(unittest.TestCase):
    def test_get_title_movie(self):
        title_id = 'tt0076759'
        scraper = PyMDbScraper()
        title = scraper.get_title(title_id, include_taglines=True)

        # Correct values
        display_title = 'Star Wars: Episode IV - A New Hope'
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
            CreditScrape('nm0000434', title_id, ACTOR, 'Luke Skywalker', None, None, None),
            CreditScrape('nm0000148', title_id, ACTOR, 'Han Solo', None, None, None),
            CreditScrape('nm0000402', title_id, ACTOR, 'Princess Leia Organa', None, None, None),
            CreditScrape('nm0001088', title_id, ACTOR, 'Grand Moff Tarkin', None, None, None),
            CreditScrape('nm0000027', title_id, ACTOR, 'Ben Obi-Wan Kenobi', None, None, None),
            CreditScrape('nm0000355', title_id, ACTOR, 'C-3PO', None, None, None),
            CreditScrape('nm0048652', title_id, ACTOR, 'R2-D2', None, None, None),
            CreditScrape('nm0562679', title_id, ACTOR, 'Chewbacca', None, None, None),
            CreditScrape('nm0001190', title_id, ACTOR, 'Darth Vader', None, None, None),
            CreditScrape('nm0114436', title_id, ACTOR, 'Uncle Owen', None, None, None),
            CreditScrape('nm0292235', title_id, ACTOR, 'Aunt Beru', None, None, None),
            CreditScrape('nm0701023', title_id, ACTOR, 'Chief Jawa', None, None, None),
            CreditScrape('nm0567018', title_id, ACTOR, 'General Dodonna', None, None, None),
            CreditScrape('nm0125952', title_id, ACTOR, 'General Willard', None, None, None),
            CreditScrape('nm0377120', title_id, ACTOR, 'Red Leader (as Drewe Hemley)', None, None, None)
        ]
        budget = 11000000
        budget_denomination = 'USD'
        opening_weekend_gross = 1554475
        opening_weekend_date = datetime(1977, 5, 30)
        usa_gross = 460998507
        worldwide_gross = 775398007

        self.assertEqual(title.title_id, title_id)
        self.assertEqual(title.display_title, display_title)
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
        self.assertEqual(title.budget_denomination, budget_denomination)
        self.assertEqual(title.opening_weekend_gross, opening_weekend_gross)
        self.assertEqual(title.opening_weekend_date, opening_weekend_date)
        self.assertEqual(title.usa_gross, usa_gross)
        self.assertEqual(title.worldwide_gross, worldwide_gross)

    def test_get_title_tv_series(self):
        title_id = 'tt0149460'
        scraper = PyMDbScraper()
        title = scraper.get_title(title_id, include_taglines=True)

        # Correct values
        display_title = 'Futurama'
        title_parent_id = None
        mpaa_rating = 'TV-14'
        country = 'USA'
        language = 'English'
        release_date = datetime(1999, 3, 28)
        end_year = 2013
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
            CreditScrape('nm0921942', title_id, ACTOR, 'Philip J. Fry / ...', 140, 1999, 2013),
            CreditScrape('nm0005408', title_id, ACTOR, 'Turanga Leela / ...', 140, 1999, 2013),
            CreditScrape('nm0224007', title_id, ACTOR, 'Bender / ...', 140, 1999, 2013),
            CreditScrape('nm0534134', title_id, ACTOR, 'Linda / ...', 137, 1999, 2013),
            CreditScrape('nm0482851', title_id, ACTOR, 'Hermes Conrad / ...', 133, 1999, 2013),
            CreditScrape('nm0866300', title_id, ACTOR, 'Amy Wong / ...', 131, 1999, 2013),
            CreditScrape('nm0005606', title_id, ACTOR, 'Morbo / ...', 127, 1999, 2013),
            CreditScrape('nm0379114', title_id, ACTOR, 'Scruffy / ...', 119, 1999, 2013)
        ]
        budget = None
        budget_denomination = None
        opening_weekend_gross = None
        opening_weekend_date = None
        usa_gross = None
        worldwide_gross = None

        self.assertEqual(title.title_id, title_id)
        self.assertEqual(title.display_title, display_title)
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
        self.assertEqual(title.budget_denomination, budget_denomination)
        self.assertEqual(title.opening_weekend_gross, opening_weekend_gross)
        self.assertEqual(title.opening_weekend_date, opening_weekend_date)
        self.assertEqual(title.usa_gross, usa_gross)
        self.assertEqual(title.worldwide_gross, worldwide_gross)

    def test_get_title_tv_episode(self):
        title_id = 'tt4283088'
        scraper = PyMDbScraper()
        title = scraper.get_title(title_id, include_taglines=True)

        # Correct values
        display_title = 'Battle of the Bastards'
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
            CreditScrape('nm0227759', title_id, ACTOR, 'Tyrion Lannister', None, None, None),
            CreditScrape('nm3229685', title_id, ACTOR, 'Jon Snow', None, None, None),
            CreditScrape('nm3592338', title_id, ACTOR, 'Daenerys Targaryen', None, None, None),
            CreditScrape('nm0192377', title_id, ACTOR, 'Davos Seaworth', None, None, None),
            CreditScrape('nm3849842', title_id, ACTOR, 'Sansa Stark', None, None, None),
            CreditScrape('nm0318821', title_id, ACTOR, 'Petyr \'Littlefinger\' Baelish', None, None, None),
            CreditScrape('nm0396924', title_id, ACTOR, 'Melisandre (as Carice Van Houten)', None, None, None),
            CreditScrape('nm2812026', title_id, ACTOR, 'Missandei', None, None, None),
            CreditScrape('nm1970465', title_id, ACTOR, 'Tormund Giantsbane', None, None, None),
            CreditScrape('nm3701064', title_id, ACTOR, 'Ramsay Bolton', None, None, None),
            CreditScrape('nm0654295', title_id, ACTOR, 'Theon Greyjoy', None, None, None),
            CreditScrape('nm0401264', title_id, ACTOR, 'Daario Naharis', None, None, None),
            CreditScrape('nm2760664', title_id, ACTOR, 'Grey Worm', None, None, None),
            CreditScrape('nm2247629', title_id, ACTOR, 'Yara Greyjoy', None, None, None),
            CreditScrape('nm1613839', title_id, ACTOR, 'Wun Wun', None, None, None)
        ]
        budget = 10000000
        budget_denomination = 'GBP'
        opening_weekend_gross = None
        opening_weekend_date = None
        usa_gross = None
        worldwide_gross = None

        self.assertEqual(title.title_id, title_id)
        self.assertEqual(title.display_title, display_title)
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
        self.assertEqual(title.budget_denomination, budget_denomination)
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
        title_id = 'tt4154796'
        scraper = PyMDbScraper()

        # Correct values
        job_title = ACTOR
        actor1_id = 'nm0421822'
        actor1_credit = 'Security Guard'
        actor2_id = 'nm0000982'
        actor2_credit = 'Thanos'
        actor3_id = 'nm1165110'
        actor3_credit = 'Thor'
        actor4_id = 'nm9320991'
        actor4_credit = 'Security Guard (uncredited)'
        actor_ids = {actor1_id, actor2_id, actor3_id, actor4_id}
        actor_count = 0

        for credit in scraper.get_full_cast(title_id):
            actor_count += 1
            if credit.name_id in actor_ids:
                self.assertEqual(credit.title_id, title_id)
                self.assertEqual(credit.job_title, job_title)
                self.assertIsNone(credit.episode_count)
                self.assertIsNone(credit.episode_year_start)
                self.assertIsNone(credit.episode_year_end)

                if credit.name_id == actor1_id:
                    self.assertEqual(credit.credit, actor1_credit)
                elif credit.name_id == actor2_id:
                    self.assertEqual(credit.credit, actor2_credit)
                elif credit.name_id == actor3_id:
                    self.assertEqual(credit.credit, actor3_credit)
                elif credit.name_id == actor4_id:
                    self.assertEqual(credit.credit, actor4_credit)
        self.assertGreaterEqual(actor_count, 162)

    def test_get_full_cast_tv_series(self):
        title_id = 'tt0149460'
        scraper = PyMDbScraper()

        # Correct values
        job_title = ACTOR
        actor1_id = 'nm0224007'
        actor1_credit = 'Bender / ...'
        actor1_episode_count = 140
        actor1_start_year = 1999
        actor1_end_year = 2013
        actor2_id = 'nm0005277'
        actor2_credit = 'Conan O\'Brien'
        actor2_episode_count = 1
        actor2_start_year = 1999
        actor2_end_year = None
        actor3_id = 'nm0065059'
        actor3_credit = 'Beck'
        actor3_episode_count = 1
        actor3_start_year = 2001
        actor3_end_year = None
        actor4_id = 'nm2858163'
        actor4_credit = 'Self (uncredited)'
        actor4_episode_count = None
        actor4_start_year = None
        actor4_end_year = None
        actor_ids = {actor1_id, actor2_id, actor3_id, actor4_id}
        actor_count = 0

        for credit in scraper.get_full_cast(title_id):
            actor_count += 1
            if credit.name_id in actor_ids:
                self.assertEqual(credit.title_id, title_id)
                self.assertEqual(credit.job_title, job_title)

                if credit.name_id == actor1_id:
                    self.assertEqual(credit.credit, actor1_credit)
                    self.assertEqual(credit.episode_count, actor1_episode_count)
                    self.assertEqual(credit.episode_year_start, actor1_start_year)
                    self.assertEqual(credit.episode_year_end, actor1_end_year)
                elif credit.name_id == actor2_id:
                    self.assertEqual(credit.credit, actor2_credit)
                    self.assertEqual(credit.episode_count, actor2_episode_count)
                    self.assertEqual(credit.episode_year_start, actor2_start_year)
                    self.assertEqual(credit.episode_year_end, actor2_end_year)
                elif credit.name_id == actor3_id:
                    self.assertEqual(credit.credit, actor3_credit)
                    self.assertEqual(credit.episode_count, actor3_episode_count)
                    self.assertEqual(credit.episode_year_start, actor3_start_year)
                    self.assertEqual(credit.episode_year_end, actor3_end_year)
                elif credit.name_id == actor4_id:
                    self.assertEqual(credit.credit, actor4_credit)
                    self.assertEqual(credit.episode_count, actor4_episode_count)
                    self.assertEqual(credit.episode_year_start, actor4_start_year)
                    self.assertEqual(credit.episode_year_end, actor4_end_year)
        self.assertGreaterEqual(actor_count, 85)

    def test_get_full_cast_tv_series_and_episodes(self):
        title_id = 'tt7366338'
        scraper = PyMDbScraper()

        # Correct values
        job_title = ACTOR
        actor1_id = 'nm0364813'
        actor1_ep1_credit = 'Valery Legasov'
        actor1_ep1_start_year = 2019
        actor1_ep1_title_id = 'tt9166696'
        actor1_ep2_credit = 'Valery Legasov'
        actor1_ep2_start_year = 2019
        actor1_ep2_title_id = 'tt8162428'
        actor2_id = 'nm2523072'
        actor2_ep1_credit = 'Mikhail'
        actor2_ep1_start_year = 2019
        actor2_ep1_title_id = 'tt9166696'
        actor2_ep2_credit = 'Mikhail'
        actor2_ep2_start_year = 2019
        actor2_ep2_title_id = 'tt8162428'
        episode_count = 4

        episodes_found = 0
        for credit in scraper.get_full_cast(title_id, include_episodes=True):
            self.assertEqual(credit.job_title, job_title)

            if credit.title_id == actor1_ep1_title_id and credit.name_id == actor1_id:
                episodes_found += 1
                self.assertEqual(credit.name_id, actor1_id)
                self.assertEqual(credit.credit, actor1_ep1_credit)
                self.assertIsNone(credit.episode_count)
                self.assertEqual(credit.episode_year_start, actor1_ep1_start_year)
                self.assertIsNone(credit.episode_year_end)
            elif credit.title_id == actor1_ep2_title_id and credit.name_id == actor1_id:
                episodes_found += 1
                self.assertEqual(credit.name_id, actor1_id)
                self.assertEqual(credit.credit, actor1_ep2_credit)
                self.assertIsNone(credit.episode_count)
                self.assertEqual(credit.episode_year_start, actor1_ep2_start_year)
                self.assertIsNone(credit.episode_year_end)
            elif credit.title_id == actor2_ep1_title_id and credit.name_id == actor2_id:
                episodes_found += 1
                self.assertEqual(credit.name_id, actor2_id)
                self.assertEqual(credit.credit, actor2_ep1_credit)
                self.assertIsNone(credit.episode_count)
                self.assertEqual(credit.episode_year_start, actor2_ep1_start_year)
                self.assertIsNone(credit.episode_year_end)
            elif credit.title_id == actor2_ep2_title_id and credit.name_id == actor2_id:
                episodes_found += 1
                self.assertEqual(credit.name_id, actor2_id)
                self.assertEqual(credit.credit, actor2_ep2_credit)
                self.assertIsNone(credit.episode_count)
                self.assertEqual(credit.episode_year_start, actor2_ep2_start_year)
                self.assertIsNone(credit.episode_year_end)
        self.assertGreaterEqual(episodes_found, episode_count)

    def test_get_full_cast_episode(self):
        title_id = 'tt4283088'
        scraper = PyMDbScraper()

        # Correct values
        job_title = ACTOR
        actor1_id = 'nm0227759'
        actor1_credit = 'Tyrion Lannister'
        actor2_id = 'nm0654295'
        actor2_credit = 'Theon Greyjoy'
        actor3_id = 'nm8256997'
        actor3_credit = 'Stark Soldier (uncredited)'
        actor4_id = 'nm2502703'
        actor4_credit = 'Meereen Guard (uncredited)'
        actor_ids = {actor1_id, actor2_id, actor3_id, actor4_id}
        actor_count = 0

        for credit in scraper.get_full_cast(title_id):
            actor_count += 1
            if credit.name_id in actor_ids:
                self.assertEqual(credit.title_id, title_id)
                self.assertEqual(credit.job_title, job_title)
                self.assertIsNone(credit.episode_count)
                self.assertIsNone(credit.episode_year_start)
                self.assertIsNone(credit.episode_year_end)

                if credit.name_id == actor1_id:
                    self.assertEqual(credit.credit, actor1_credit)
                elif credit.name_id == actor2_id:
                    self.assertEqual(credit.credit, actor2_credit)
                elif credit.name_id == actor3_id:
                    self.assertEqual(credit.credit, actor3_credit)
                elif credit.name_id == actor4_id:
                    self.assertEqual(credit.credit, actor4_credit)
        self.assertGreaterEqual(actor_count, 36)

    def test_get_full_cast_bad_request(self):
        title_id = 'nm123456789'
        scraper = PyMDbScraper()
        with self.assertRaises(HTTPError):
            for c in scraper.get_full_cast(title_id):
                pass


class TestGetFullCrew(unittest.TestCase):
    def test_get_full_crew_movie(self):
        title_id = 'tt4154796'
        scraper = PyMDbScraper()

        # Correct values
        correct_credits = {
            'nm0751577': CreditScrape(
                'nm0751577',
                title_id,
                DIRECTOR,
                None,
                None,
                None,
                None
            ),
            'nm2757098': CreditScrape(
                'nm2757098',
                title_id,
                WRITER,
                'Rocket Raccoon created by',
                None,
                None,
                None
            ),
            'nm10724782': CreditScrape(
                'nm10724782',
                title_id,
                THANKS,
                'special thanks',
                None,
                None,
                None
            )
        }
        credit_types_count = 30

        credit_types = set()
        for crew_member in scraper.get_full_crew(title_id):
            if crew_member.job_title not in credit_types:
                credit_types.add(crew_member.job_title)

            self.assertEqual(crew_member.title_id, title_id)
            self.assertIsNone(crew_member.episode_count)
            self.assertIsNone(crew_member.episode_year_start)
            self.assertIsNone(crew_member.episode_year_end)
            self.assertIsNotNone(crew_member.name_id)
            self.assertIsNotNone(crew_member.job_title)

            if crew_member.name_id in correct_credits:
                correct_credit = correct_credits[crew_member.name_id]
                self.assertEqual(crew_member.name_id, correct_credit.name_id)
                self.assertEqual(crew_member.job_title, correct_credit.job_title)
                self.assertEqual(crew_member.credit, correct_credit.credit)
        self.assertEqual(credit_types_count, len(credit_types))

    def test_get_full_crew_tv_series(self):
        title_id = 'tt0149460'
        scraper = PyMDbScraper()

        # Correct values
        correct_credits = {
            'nm0547772': CreditScrape(
                'nm0547772',
                title_id,
                DIRECTOR,
                None,
                8,
                2010,
                2013
            ),
            'nm0592546': CreditScrape(
                'nm0592546',
                title_id,
                WRITER,
                'staff writer',
                26,
                2001,
                2003
            ),
            'nm0629628': CreditScrape(
                'nm0629628',
                title_id,
                MUSIC_DEPARTMENT,
                'stock music (uncredited) (unknown episodes)',
                None,
                None,
                None
            ),
            'nm4348107': CreditScrape(
                'nm4348107',
                title_id,
                ADDITIONAL_CREW,
                'production assistant',
                1,
                2012,
                None
            )
        }
        credit_types_count = 19

        credit_types = set()
        for crew_member in scraper.get_full_crew(title_id):
            if crew_member.job_title not in credit_types:
                credit_types.add(crew_member.job_title)

            self.assertEqual(crew_member.title_id, title_id)
            self.assertIsNotNone(crew_member.name_id)
            self.assertIsNotNone(crew_member.job_title)

            if crew_member.name_id in correct_credits:
                correct_credit = correct_credits[crew_member.name_id]
                self.assertEqual(crew_member.name_id, correct_credit.name_id)
                self.assertEqual(crew_member.job_title, correct_credit.job_title)
                self.assertEqual(crew_member.credit, correct_credit.credit)
                self.assertEqual(crew_member.episode_count, correct_credit.episode_count)
                self.assertEqual(crew_member.episode_year_start, correct_credit.episode_year_start)
                self.assertEqual(crew_member.episode_year_end, correct_credit.episode_year_end)
        self.assertEqual(credit_types_count, len(credit_types))

    def test_get_full_crew_tv_episode(self):
        title_id = 'tt4283088'
        scraper = PyMDbScraper()

        # Correct values
        correct_credits = {
            'nm0764601': CreditScrape(
                'nm0764601',
                title_id,
                DIRECTOR,
                None,
                None,
                None,
                None
            ),
            'nm2388673': CreditScrape(
                'nm2388673',
                title_id,
                PRODUCER,
                'co-producer',
                None,
                None,
                None
            ),
            'nm1268561': CreditScrape(
                'nm1268561',
                title_id,
                ART_DEPARTMENT,
                'head greensman (as Michael Gibson)',
                None,
                None,
                None
            )
        }
        credit_types_count = 28

        credit_types = set()
        for crew_member in scraper.get_full_crew(title_id):
            if crew_member.job_title not in credit_types:
                credit_types.add(crew_member.job_title)

            self.assertIsNone(crew_member.episode_count)
            self.assertIsNone(crew_member.episode_year_start)
            self.assertIsNone(crew_member.episode_year_end)
            self.assertIsNotNone(crew_member.name_id)
            self.assertIsNotNone(crew_member.job_title)

            if crew_member.name_id in correct_credits:
                correct_credit = correct_credits[crew_member.name_id]
                self.assertEqual(crew_member.name_id, correct_credit.name_id)
                self.assertEqual(crew_member.job_title, correct_credit.job_title)
                self.assertEqual(crew_member.credit, correct_credit.credit)
        self.assertEqual(credit_types_count, len(credit_types))

    def test_get_full_crew_bad_request(self):
        title_id = 'nm123456789'
        scraper = PyMDbScraper()
        with self.assertRaises(HTTPError):
            for c in scraper.get_full_crew(title_id):
                pass


class TestGetFullCredits(unittest.TestCase):
    def test_get_full_credits_movie(self):
        title_id = 'tt4154796'
        scraper = PyMDbScraper()

        # Correct values
        correct_credits = {
            'nm0751577': CreditScrape(
                'nm0751577',
                title_id,
                DIRECTOR,
                None,
                None,
                None,
                None
            ),
            'nm2757098': CreditScrape(
                'nm2757098',
                title_id,
                WRITER,
                'Rocket Raccoon created by',
                None,
                None,
                None
            ),
            'nm0000982': CreditScrape(
                'nm0000982',
                title_id,
                ACTOR,
                'Thanos',
                None,
                None,
                None
            )
        }
        credit_types_count = 31

        credit_types = set()
        for credit in scraper.get_full_credits(title_id):
            if credit.job_title not in credit_types:
                credit_types.add(credit.job_title)

            self.assertEqual(credit.title_id, title_id)
            self.assertIsNone(credit.episode_year_end)
            self.assertIsNotNone(credit.name_id)
            self.assertIsNotNone(credit.job_title)

            if credit.name_id in correct_credits:
                correct_credit = correct_credits[credit.name_id]
                self.assertEqual(credit.name_id, correct_credit.name_id)
                self.assertEqual(credit.job_title, correct_credit.job_title)
                self.assertEqual(credit.credit, correct_credit.credit)
        self.assertEqual(credit_types_count, len(credit_types))

    def test_get_full_credits_tv_series(self):
        title_id = 'tt0149460'
        scraper = PyMDbScraper()

        # Correct values
        correct_credits = {
            'nm0547772': CreditScrape(
                'nm0547772',
                title_id,
                DIRECTOR,
                None,
                8,
                2010,
                2013
            ),
            'nm0592546': CreditScrape(
                'nm0592546',
                title_id,
                WRITER,
                'staff writer',
                26,
                2001,
                2003
            ),
            'nm0224007': CreditScrape(
                'nm0224007',
                title_id,
                ACTOR,
                'Bender / ...',
                140,
                1999,
                2013
            )
        }
        credit_types_count = 20

        credit_types = set()
        for credit in scraper.get_full_credits(title_id):
            if credit.job_title not in credit_types:
                credit_types.add(credit.job_title)

            self.assertEqual(credit.title_id, title_id)
            self.assertIsNotNone(credit.name_id)
            self.assertIsNotNone(credit.job_title)

            if credit.name_id in correct_credits:
                correct_credit = correct_credits[credit.name_id]
                self.assertEqual(credit.name_id, correct_credit.name_id)
                self.assertEqual(credit.job_title, correct_credit.job_title)
                self.assertEqual(credit.credit, correct_credit.credit)
                self.assertEqual(credit.episode_count, correct_credit.episode_count)
                self.assertEqual(credit.episode_year_start, correct_credit.episode_year_start)
                self.assertEqual(credit.episode_year_end, correct_credit.episode_year_end)
        self.assertEqual(credit_types_count, len(credit_types))

    def test_get_full_credits_tv_series_and_episodes(self):
        title_id = 'tt7366338'
        scraper = PyMDbScraper()

        # Correct values
        correct_credits = {
            'nm0269957': CreditScrape(
                'nm0269957',
                title_id,
                PRODUCER,
                'executive producer',
                5,
                2019,
                None
            ),
            'nm3723390': CreditScrape(
                'nm3723390',
                title_id,
                MUSIC,
                None,
                5,
                2019,
                None
            ),
            'nm0364813': CreditScrape(
                'nm0364813',
                'tt9166696',
                ACTOR,
                'Valery Legasov',
                None,
                2019,
                None
            )
        }
        credit_types_count = 30

        credit_types = set()
        for credit in scraper.get_full_credits(title_id, include_episodes=True):
            if credit.job_title not in credit_types:
                credit_types.add(credit.job_title)
            
            self.assertIsNotNone(credit.name_id)
            self.assertIsNotNone(credit.job_title)

            if credit.name_id in correct_credits:
                if credit.name_id == 'nm0364813' and title_id != 'tt9166696':
                    continue
                correct_credit = correct_credits[credit.name_id]
                self.assertEqual(credit.name_id, correct_credit.name_id)
                self.assertEqual(credit.job_title, correct_credit.job_title)
                self.assertEqual(credit.credit, correct_credit.credit)
                self.assertEqual(credit.episode_count, correct_credit.episode_count)
                self.assertEqual(credit.episode_year_start, correct_credit.episode_year_start)
                self.assertEqual(credit.episode_year_end, correct_credit.episode_year_end)
        self.assertEqual(credit_types_count, len(credit_types))

    def test_get_full_credits_tv_episode(self):
        title_id = 'tt4283088'
        scraper = PyMDbScraper()

        # Correct values
        correct_credits = {
            'nm0764601': CreditScrape(
                'nm0764601',
                title_id,
                DIRECTOR,
                None,
                None,
                None,
                None
            ),
            'nm2388673': CreditScrape(
                'nm2388673',
                title_id,
                PRODUCER,
                'co-producer',
                None,
                None,
                None
            ),
            'nm0227759': CreditScrape(
                'nm0227759',
                title_id,
                ACTOR,
                'Tyrion Lannister',
                None,
                None,
                None
            )
        }
        credit_types_count = 29

        credit_types = set()
        for credit in scraper.get_full_credits(title_id):
            if credit.job_title not in credit_types:
                credit_types.add(credit.job_title)

            self.assertEqual(credit.title_id, title_id)
            self.assertIsNone(credit.episode_count)
            self.assertIsNone(credit.episode_year_start)
            self.assertIsNone(credit.episode_year_end)
            self.assertIsNotNone(credit.name_id)
            self.assertIsNotNone(credit.job_title)

            if credit.name_id in correct_credits:
                correct_credit = correct_credits[credit.name_id]
                self.assertEqual(credit.name_id, correct_credit.name_id)
                self.assertEqual(credit.job_title, correct_credit.job_title)
                self.assertEqual(credit.credit, correct_credit.credit)
        self.assertEqual(credit_types_count, len(credit_types))

    def test_get_full_credits_as_dict(self):
        title_id = 'tt3359412'
        scraper = PyMDbScraper()

        # Correct results
        directors = ['nm6113438']
        writers = ['nm6113440']
        cast = ['nm4043618', 'nm6113439']
        cinematographers = ['nm6113438']
        assistant_directors = ['nm6113441']
        art_department = ['nm6294206']
        camera_department = ['nm6113442']

        actual_results = scraper.get_full_credits_as_dict(title_id)
        for director in actual_results[DIRECTOR]:
            self.assertTrue(director.name_id in directors)
        for writer in actual_results[WRITER]:
            self.assertTrue(writer.name_id in writers)
        for cast_member in actual_results[ACTOR]:
            self.assertTrue(cast_member.name_id in cast)
        for cinematographer in actual_results[CINEMATOGRAPHY]:
            self.assertTrue(cinematographer.name_id in cinematographers)
        for assistant_director in actual_results[ASSISTANT_DIRECTOR]:
            self.assertTrue(assistant_director.name_id in assistant_directors)
        for crew_member in actual_results[ART_DEPARTMENT]:
            self.assertTrue(crew_member.name_id in art_department)
        for crew_member in actual_results[CAMERA_AND_ELECTRICAL_DEPARTMENT]:
            self.assertTrue(crew_member.name_id in camera_department)
    
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
        name = scraper.get_name(name_id, include_known_for_titles=True)

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
        self.assertEqual(len(name.known_for_titles), 4)
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
        name = scraper.get_name(name_id, include_known_for_titles=True)

        # Correct values
        display_name = 'Charles Chaplin'
        known_for_titles = ['tt0032553', 'tt0044837', 'tt0027977', 'tt0018773']
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
        self.assertEqual(sorted(name.known_for_titles), sorted(known_for_titles))
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
        name = scraper.get_name(name_id, include_known_for_titles=True)

        # Correct values
        display_name = 'M. Night Shyamalan'
        known_for_titles = ['tt0452637', 'tt0286106', 'tt0368447', 'tt0167404']
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
        self.assertEqual(sorted(name.known_for_titles), sorted(known_for_titles))
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
        name = scraper.get_name(name_id, include_known_for_titles=True)

        # Correct values
        display_name = 'James Sled'
        known_for_titles_len = 4
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
        self.assertEqual(len(name.known_for_titles), known_for_titles_len)
        self.assertEqual(name.birth_date, birth_date)
        self.assertEqual(name.birth_city, birth_city)
        self.assertEqual(name.death_date, death_date)
        self.assertEqual(name.death_city, death_city)
        self.assertEqual(name.death_cause, death_cause)
        self.assertEqual(name.birth_name, birth_name)
        self.assertEqual(sorted(name.nicknames), sorted(nicknames))
        self.assertEqual(name.height, height)

    def test_get_name_known_for_stacked(self):
        name_id = 'nm2361234'
        scraper = PyMDbScraper()
        name = scraper.get_name(name_id, include_known_for_titles=True)

        # Correct values
        known_for_titles = ['tt0457201', 'tt5916418']

        self.assertEqual(sorted(name.known_for_titles), sorted(known_for_titles))

    def test_get_name_no_known_for(self):
        name_id = 'nm0000375'
        scraper = PyMDbScraper()
        name = scraper.get_name(name_id, include_known_for_titles=False)

        self.assertEqual(name.known_for_titles, [])

    def test_get_name_bad_request(self):
        name_id = 'tt123456789'
        scraper = PyMDbScraper()
        with self.assertRaises(HTTPError):
            scraper.get_name(name_id)


class TestGetNameCredits(unittest.TestCase):
    def test_get_name_credits_actor(self):
        name_id = 'nm0000375'
        scraper = PyMDbScraper()

        # Correct values
        correct_name_credits = {
            'tt0942385': NameCreditScrape(
                name_id,
                'tt0942385',
                'actor',
                2008,
                None,
                'Kirk Lazarus - Hot LZ',
                []
            ),
            'tt2094116': NameCreditScrape(
                name_id,
                'tt2094116',
                'actor',
                None,
                None,
                'Sherlock Holmes',
                ['pre-production']
            ),
            'tt3447362': NameCreditScrape(
                name_id,
                'tt3447362',
                'actor',
                2004,
                None,
                'Traveller (uncredited)',
                ['Short']
            )
        }
        actor_credits = 92

        category_count = defaultdict(int)
        for name_credit in scraper.get_name_credits(name_id):
            self.assertEqual(name_credit.name_id, name_id)
            self.assertIsNotNone(name_credit.title_id)
            self.assertIsNotNone(name_credit.category)
            self.assertIsNotNone(name_credit.title_notes)
            category_count[name_credit.category] += 1

            if name_credit.title_id in correct_name_credits:
                correct_credit = correct_name_credits[name_credit.title_id]
                self.assertEqual(name_credit.title_id, correct_credit.title_id)
                self.assertEqual(name_credit.category, correct_credit.category)
                self.assertEqual(name_credit.start_year, correct_credit.start_year)
                self.assertEqual(name_credit.end_year, correct_credit.end_year)
                self.assertEqual(name_credit.role, correct_credit.role)
                self.assertEqual(name_credit.title_notes, correct_credit.title_notes)
        self.assertGreaterEqual(category_count[ACTOR], actor_credits)

    def test_get_name_credits_actor_with_episodes(self):
        name_id = 'nm3229685'
        scraper = PyMDbScraper()

        # Correct values
        correct_name_credits = {
            'tt0944947': NameCreditScrape(
                name_id,
                'tt0944947',
                'actor',
                2011,
                2019,
                'Jon Snow',
                ['TV Series']
            ),
            'tt6027914': NameCreditScrape(
                name_id,
                'tt6027914',
                'actor',
                2019,
                None,
                'Jon Snow',
                []
            ),
            'tt2070135': NameCreditScrape(
                name_id,
                'tt2070135',
                'actor',
                2012,
                None,
                'Jon Snow',
                []
            )
        }
        actor_credits = 78

        category_count = defaultdict(int)
        for name_credit in scraper.get_name_credits(name_id, include_episodes=True):
            self.assertEqual(name_credit.name_id, name_id)
            self.assertIsNotNone(name_credit.title_id)
            self.assertIsNotNone(name_credit.category)
            self.assertIsNotNone(name_credit.title_notes)
            category_count[name_credit.category] += 1

            if name_credit.title_id in correct_name_credits and name_credit.category == 'actor':
                correct_credit = correct_name_credits[name_credit.title_id]
                self.assertEqual(name_credit.title_id, correct_credit.title_id)
                self.assertEqual(name_credit.category, correct_credit.category)
                self.assertEqual(name_credit.start_year, correct_credit.start_year)
                self.assertEqual(name_credit.end_year, correct_credit.end_year)
                self.assertEqual(name_credit.role, correct_credit.role)
                self.assertEqual(name_credit.title_notes, correct_credit.title_notes)
        self.assertGreaterEqual(category_count['actor'], actor_credits)

    def test_get_name_credits_director(self):
        name_id = 'nm0796117'
        scraper = PyMDbScraper()

        # Correct values
        correct_name_credits = {
            'tt4972582': NameCreditScrape(
                name_id,
                'tt4972582',
                'director',
                2016,
                None,
                None,
                ['directed by']
            ),
            'tt0167404': NameCreditScrape(
                name_id,
                'tt0167404',
                'director',
                1999,
                None,
                None,
                []
            ),
            'tt2618986': NameCreditScrape(
                name_id,
                'tt2618986',
                'director',
                2015,
                None,
                None,
                ['TV Series', '1 episode']
            )
        }
        director_credits = 16

        category_count = defaultdict(int)
        for name_credit in scraper.get_name_credits(name_id):
            self.assertEqual(name_credit.name_id, name_id)
            self.assertIsNotNone(name_credit.title_id)
            self.assertIsNotNone(name_credit.category)
            self.assertIsNotNone(name_credit.title_notes)
            category_count[name_credit.category] += 1

            if name_credit.title_id in correct_name_credits and name_credit.category == 'director':
                correct_credit = correct_name_credits[name_credit.title_id]
                self.assertEqual(name_credit.title_id, correct_credit.title_id)
                self.assertEqual(name_credit.category, correct_credit.category)
                self.assertEqual(name_credit.start_year, correct_credit.start_year)
                self.assertEqual(name_credit.end_year, correct_credit.end_year)
                self.assertEqual(name_credit.role, correct_credit.role)
                self.assertEqual(name_credit.title_notes, correct_credit.title_notes)
        self.assertGreaterEqual(category_count['director'], director_credits)

    def test_get_name_credits_director_with_episodes(self):
        name_id = 'nm0764601'
        scraper = PyMDbScraper()

        # Correct values
        correct_name_credits = {
            'tt0944947': NameCreditScrape(
                name_id,
                'tt0944947',
                'director',
                2015,
                2019,
                None,
                ['TV Series', '6 episodes']
            ),
            'tt3866846': NameCreditScrape(
                name_id,
                'tt3866846',
                'director',
                2015,
                None,
                None,
                []
            ),
            'tt2121964': NameCreditScrape(
                name_id,
                'tt2121964',
                'director',
                2012,
                None,
                None,
                []
            )
        }

        for name_credit in scraper.get_name_credits(name_id, include_episodes=True):
            self.assertEqual(name_credit.name_id, name_id)
            self.assertIsNotNone(name_credit.title_id)
            self.assertIsNotNone(name_credit.category)
            self.assertIsNotNone(name_credit.title_notes)

            if name_credit.title_id in correct_name_credits and name_credit.category == 'director':
                correct_credit = correct_name_credits[name_credit.title_id]
                self.assertEqual(name_credit.title_id, correct_credit.title_id)
                self.assertEqual(name_credit.category, correct_credit.category)
                self.assertEqual(name_credit.start_year, correct_credit.start_year)
                self.assertEqual(name_credit.end_year, correct_credit.end_year)
                self.assertEqual(name_credit.role, correct_credit.role)
                self.assertEqual(name_credit.title_notes, correct_credit.title_notes)

    def test_get_name_credits_crew_member(self):
        name_id = 'nm1014697'
        scraper = PyMDbScraper()

        # Correct values
        correct_name_credits = {
            'tt0944947': NameCreditScrape(
                name_id,
                'tt0944947',
                'composer',
                2011,
                2019,
                None,
                ['TV Series', '73 episodes']
            ),
            'tt8801880': NameCreditScrape(
                name_id,
                'tt8801880',
                'composer',
                2019,
                None,
                None,
                ['Video Game', 'music composed by']
            ),
            'tt2034800': NameCreditScrape(
                name_id,
                'tt2034800',
                'composer',
                2016,
                None,
                None,
                []
            )
        }
        composer_credits = 63

        category_count = defaultdict(int)
        for name_credit in scraper.get_name_credits(name_id):
            self.assertEqual(name_credit.name_id, name_id)
            self.assertIsNotNone(name_credit.title_id)
            self.assertIsNotNone(name_credit.category)
            self.assertIsNotNone(name_credit.title_notes)
            category_count[name_credit.category] += 1

            if name_credit.title_id in correct_name_credits and name_credit.category == 'composer':
                correct_credit = correct_name_credits[name_credit.title_id]
                self.assertEqual(name_credit.title_id, correct_credit.title_id)
                self.assertEqual(name_credit.category, correct_credit.category)
                self.assertEqual(name_credit.start_year, correct_credit.start_year)
                self.assertEqual(name_credit.end_year, correct_credit.end_year)
                self.assertEqual(name_credit.role, correct_credit.role)
                self.assertEqual(name_credit.title_notes, correct_credit.title_notes)
        self.assertGreaterEqual(category_count['composer'], composer_credits)

    def test_get_name_credits_crew_member_with_episodes(self):
        name_id = 'nm1014697'
        scraper = PyMDbScraper()

        # Correct values
        correct_name_credits = {
            'tt6027920': NameCreditScrape(
                name_id,
                'tt6027920',
                'composer',
                2019,
                None,
                None,
                []
            ),
            'tt3866846': NameCreditScrape(
                name_id,
                'tt3866846',
                'composer',
                2015,
                None,
                None,
                []
            ),
            'tt0723054': NameCreditScrape(
                name_id,
                'tt0723054',
                'composer',
                2005,
                None,
                None,
                []
            )
        }

        for name_credit in scraper.get_name_credits(name_id):
            self.assertEqual(name_credit.name_id, name_id)
            self.assertIsNotNone(name_credit.title_id)
            self.assertIsNotNone(name_credit.category)
            self.assertIsNotNone(name_credit.title_notes)

            if name_credit.title_id in correct_name_credits and name_credit.category == 'composer':
                correct_credit = correct_name_credits[name_credit.title_id]
                self.assertEqual(name_credit.title_id, correct_credit.title_id)
                self.assertEqual(name_credit.category, correct_credit.category)
                self.assertEqual(name_credit.start_year, correct_credit.start_year)
                self.assertEqual(name_credit.end_year, correct_credit.end_year)
                self.assertEqual(name_credit.role, correct_credit.role)
                self.assertEqual(name_credit.title_notes, correct_credit.title_notes)

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
            'tt1856101', 'tt1219827', 'tt0338526', 'tt1136608', 'tt0477407', 'tt0806017', 'tt4656248'
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
        production_companies_num = 2
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
        self.assertGreaterEqual(company_info[distributors], distributors_num)
        self.assertGreaterEqual(company_info[special_effects], special_effects_num)
        self.assertGreaterEqual(company_info[other_companies], other_companies_num)

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
        self.assertGreaterEqual(company_info[distributors], distributors_num)
        self.assertGreaterEqual(company_info[special_effects], special_effects_num)
        self.assertGreaterEqual(company_info[other_companies], other_companies_num)

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
        self.assertGreaterEqual(company_info[production_companies], production_companies_num)
        self.assertGreaterEqual(company_info[distributors], distributors_num)
        self.assertGreaterEqual(company_info[special_effects], special_effects_num)
        self.assertGreaterEqual(company_info[other_companies], other_companies_num)

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
        aspect_ratio = ['1.90 : 1 (IMAX version)', '2.39 : 1']
        camera = [
            'Arri Alexa 65 IMAX',
            'Panavision Sphero 65',
            'Ultra Panatar Lenses'
        ]
        laboratory = [
            'Company 3, Los Angeles (CA), USA (digital intermediate)',
            'PIX System, San Francisco (CA), USA (additional dailies services)',
            'Pinewood Digital, London, UK (digital dailies)'
        ]
        negative_format = 'Codex'
        cinematographic_process = [
            'ARRIRAW (6.5K) (source format)',
            'Digital Intermediate (2K) (master format)',
            'Dolby Vision',
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


class TestGetSearchResults(unittest.TestCase):
    def test_get_search_results_names(self):
        keyword = 'rob'
        scraper = PyMDbScraper()
        actual_results = scraper.get_search_results(keyword)

        self.assertEqual(len(actual_results), 8)
        for result in actual_results:
            self.assertIsNotNone(result.imdb_id) 
            self.assertIsInstance(result, SearchResultName)
    
    def test_get_search_results_titles(self):
        keyword = 'futuram'
        scraper = PyMDbScraper()
        actual_results = scraper.get_search_results(keyword)

        self.assertEqual(len(actual_results), 8)
        for result in actual_results:
            self.assertIsNotNone(result.imdb_id)
            self.assertIsInstance(result, (SearchResultTitle, SearchResultName))

    def test_get_search_results_mixed(self):
        keyword = 'bo'
        scraper = PyMDbScraper()
        actual_results = scraper.get_search_results(keyword)

        self.assertGreaterEqual(len(actual_results), 7)
        for result in actual_results:
            self.assertIsNotNone(result.imdb_id)
            self.assertIsInstance(result, (SearchResultName, SearchResultTitle))

    def test_get_search_results_empty(self):
        keyword = 'callmefreddiegordyonthemforties'
        scraper = PyMDbScraper()
        actual_results = scraper.get_search_results(keyword)

        self.assertEqual(len(actual_results), 0)

    def test_get_search_results_no_keyword(self):
        keyword = ''
        scraper = PyMDbScraper()
        actual_results = scraper.get_search_results(keyword)

        self.assertEqual(len(actual_results), 0)

    def test_get_search_results_none_keyword(self):
        keyword = None
        scraper = PyMDbScraper()
        actual_results = scraper.get_search_results(keyword)

        self.assertEqual(len(actual_results), 0)

    def test_get_search_results_bad_request(self):
        keyword = 'test?'
        with self.assertRaises(HTTPError):
            PyMDbScraper().get_search_results(keyword)

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
