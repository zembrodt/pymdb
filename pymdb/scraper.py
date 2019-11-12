"""Module containing the PyMDbScraper class."""

import re
import requests
from selectolax.parser import HTMLParser
from pymdb.exceptions import InvalidCompanyId
from pymdb.models import (
    CompanyScrape,
    CompanyCreditScrape,
    CreditScrape,
    NameCreditScrape,
    NameScrape,
    TitleScrape,
    TitleTechSpecsScrape,
)
from pymdb.utils import (
    get_category,
    get_company_id,
    get_name_id,
    get_ref_marker,
    get_title_id,
    is_money_string,
    remove_tags,
    remove_tags_and_content,
    split_by_br,
    trim_year,
    trim_money_string,
)


class PyMDbScraper:
    """Scrapes various information from IMDb web pages.

    Contains functions for various IMDb pages and scrapes information into Python classes.
    """

    _headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) ' +
                      'Chrome/77.0.3865.90 Safari/537.36',
        'accept': 'text/html,application/xhtml+xml,application/xml'
    }

    def __init__(self):
        pass

    def get_title(self, title_id, include_taglines=False):
        """Scrapes information from the IMDb web page for the specified title.

        Uses the given title ID to request the IMDb page for the title and scrapes
        the page's information into a new `TitleScrape` object.

        Args:
            title_id (:obj:`str`): The title's ID used by IMDb prefixed with `tt`.
            include_taglines (:obj:`bool`, optional): Specify if an extra request should be
                made to get all the taglines for the title

        Returns:
            :class:`~.models.title.TitleScrape`: An object containing the page's information.

        Raises:
            HTTPError: If the request failed.
        """

        request = f'https://www.imdb.com/title/{title_id}/'
        tree = self._get_tree(request)

        title_text = None
        title_parent_id = None
        rating = None
        country = None
        language = None
        release_date = None
        end_year = None
        season_number = None
        episode_number = None
        taglines = []
        plot = None
        storyline = None
        production_companies = []
        cast_members = []
        budget = None
        opening_weekend_gross = None
        opening_weekend_date = None
        usa_gross = None
        worldwide_gross = None

        # Get title text
        title_text_node = tree.css_first('div.title_wrapper > h1')
        if title_text_node:
            # Remove title year
            title_year_node = title_text_node.css_first('span#titleYear')
            if title_year_node:
                title_year_node.decompose()
            title_text = title_text_node.text().strip()

        # Get title parent (if TV episode)
        title_parent_node = tree.css_first('div.titleParent > a')
        if title_parent_node:
            title_parent_id = get_title_id(title_parent_node)

        # Get plot
        plot_node = tree.css_first('div.summary_text')
        if plot_node:
            plot = plot_node.text().strip()

        # Get storyline
        storyline_node = tree.css_first('div#titleStoryLine')
        if storyline_node:
            storyline_node = storyline_node.css_first('div > p > span')
            if storyline_node:
                storyline = storyline_node.text().strip()

        # Get taglines
        if include_taglines:
            tagline_request = f'https://www.imdb.com/title/{title_id}/taglines'
            tagline_tree = self._get_tree(tagline_request)
            if not tagline_tree.css_first('div#no_content'):
                for tagline_node in tagline_tree.css('div.soda'):
                    # TODO: should a Tagline object be created that stores the note for each tagline separately?
                    taglines.append(tagline_node.text().strip())

        title_node = tree.css_first('div.title_block > div > div > div.title_wrapper > div.subtext')
        if title_node:
            # If this is a TV series, get the year the show ended
            for link_node in title_node.css('a'):
                if 'href' in link_node.attributes and 'releaseinfo' in link_node.attributes['href']:
                    series_dates_match = re.search(r'[\d]{4}[-–][\d]{4}', link_node.text())
                    if series_dates_match:
                        end_year_split = re.sub(r'[-–]', '\t', series_dates_match.group(0)).split('\t')
                        if len(end_year_split) > 1:
                            end_year = end_year_split[1]
                            break

            # Get MPAA Rating
            title_node.strip_tags(['span', 'a', 'time'])
            rating_node = tree.css_first('div.titleBar > div.title_wrapper > div.subtext')
            if rating_node:
                rating = re.sub(r'(\s|,)*', '', rating_node.text()).strip()

        # Parse through text blocks
        text_block_nodes = tree.css('div#titleDetails > div.txt-block')
        for text_block_node in text_block_nodes:
            text_block_id = text_block_node.css_first('h4.inline')
            if text_block_id:
                text_block_id = text_block_id.text().lower().strip()
                text_block_text = text_block_node.text()
                if 'country' in text_block_id:
                    country_node = text_block_node.css_first('a')
                    if country_node:
                        country = country_node.text().strip()
                elif 'language' in text_block_id:
                    language_node = text_block_node.css_first('a')
                    if language_node:
                        language = language_node.text().strip()
                elif 'release date' in text_block_id:
                    release_date_match = re.search(r'\d+?\s*\w+?\s*[\d]{4}', text_block_text)
                    if release_date_match:
                        release_date = release_date_match.group(0)
                elif 'production co' in text_block_id:
                    companies = text_block_node.css('a')
                    for company in companies:
                        company_id = get_company_id(company)
                        if company_id:
                            production_companies.append(company_id)
                # Box office info
                elif 'budget' in text_block_id:
                    if is_money_string(text_block_text):
                        budget = trim_money_string(text_block_text)
                elif 'opening weekend' in text_block_id:
                    if is_money_string(text_block_text):
                        opening_weekend_gross = trim_money_string(text_block_text)
                    opening_weekend_date_node = text_block_node.css_first('span')
                    if opening_weekend_date_node:
                        opening_weekend_date = opening_weekend_date_node.text().strip()
                elif 'gross usa' in text_block_id:
                    if is_money_string(text_block_text):
                        usa_gross = trim_money_string(text_block_text)
                elif 'worldwide gross' in text_block_id:
                    if is_money_string(text_block_text):
                        worldwide_gross = trim_money_string(text_block_text)

        # Get top cast members
        cast_node = tree.css_first('table.cast_list')
        if cast_node:
            for cast_member in cast_node.css('tr.odd, tr.even'):
                cast_member_node = cast_member.css_first('td:nth-of-type(2) > a')
                if cast_member_node:
                    cast_member_id = get_name_id(cast_member_node)
                    # TODO: should this be modified to store a list of Credit objects?
                    #cast_member_name = cast_member_node.text().strip()
                    #character_nodes = cast_member.css('td.character > a')
                    #characters = []
                    #for c_node in character_nodes:
                    #    characters.append(c_node.text().strip())
                    #cast_members.append(f'{cast_member_name} ({cast_member_id}): {", ".join(characters)}')
                    cast_members.append(cast_member_id)

        # Get season and episode numbers if TV episode
        heading_nodes = tree.css('div.bp_heading')
        for heading_node in heading_nodes:
            if 'Season' in heading_node.text():
                heading_node_text = heading_node.text().lower()
                season_number_match = re.search(r'season\s*\d+', heading_node_text)
                if season_number_match:
                    season_number_match = re.search(r'\d+', season_number_match.group(0))
                    if season_number_match:
                        season_number = season_number_match.group(0)
                episode_number_match = re.search(r'episode\s*\d+', heading_node_text)
                if episode_number_match:
                    episode_number_match = re.search(r'\d+', episode_number_match.group(0))
                    if episode_number_match:
                        episode_number = episode_number_match.group(0)

        return TitleScrape(
            title_id=title_id,
            title_text=title_text,
            title_parent_id=title_parent_id,
            mpaa_rating=rating,
            country=country,
            language=language,
            release_date=release_date,
            end_year=end_year,
            season_number=season_number,
            episode_number=episode_number,
            taglines=taglines,
            plot=plot,
            storyline=storyline,
            production_companies=production_companies,
            top_cast=cast_members,
            budget=budget,
            opening_weekend_gross=opening_weekend_gross,
            opening_weekend_date=opening_weekend_date,
            usa_gross=usa_gross,
            worldwide_gross=worldwide_gross
        )

    def get_full_cast(self, title_id, include_episodes=False):
        """Scrapes the full cast of actors for a specified title.

        Will scrape the full cast of actors for a title, each into their own `CreditScrape` object.
        An optional argument `include_episodes` will also scrape each episode an actor is in
        if the title is a TV series.

        Args:
            title_id (:obj:`str`): The title's ID used by IMDb prefixed with `tt`.
            include_episodes (:obj:`bool`, optional): Specify if individual episodes of a 
                TV series should also be scraped.

        Yields:
            :class:`~.models.title.CreditScrape`: An object for each cast member in the title.

        Raises:
            HTTPError: If a request failed.
        """

        request = f'https://www.imdb.com/title/{title_id}/fullcredits'
        tree = self._get_tree(request)

        cast_node = tree.css_first('table.cast_list').css('tr')
        for cast_member in cast_node:
            actor_node = cast_member.css_first('td.primary_photo + td > a')
            if actor_node:
                name_id = get_name_id(actor_node)
                credit = None
                episode_count = None
                episode_year_start = None
                episode_year_end = None

                # Check if this is a TV series
                toggle_episodes_node = cast_member.css_first('a.toggle-episodes')
                if toggle_episodes_node:
                    episode_info = re.sub(
                        r'<\s*span.*?<\s*/\s*span\s*>', '', toggle_episodes_node.text()
                    ).strip().split(',')
                    if len(episode_info) > 1:
                        episode_count, episode_year_info = episode_info
                        episode_year_info = episode_year_info.split('-')
                        if len(episode_year_info) > 1:
                            episode_year_start, episode_year_end = episode_year_info
                        else:
                            episode_year_start, = episode_year_info
                    else:
                        episode_count, = episode_info
                    episode_count_match = re.search(r'\d+', episode_count)
                    if episode_count_match:
                        episode_count = episode_count_match.group(0)
                
                    # Include all individual episodes an actor is in
                    if include_episodes:
                        ref_marker = get_ref_marker(toggle_episodes_node)
                        request = f'https://www.imdb.com/name/{name_id}/episodes/_ajax?title={title_id}' + \
                                  f'&category=actor&ref_marker={ref_marker}&start_index=0'
                        episodes_tree = self._get_tree(request)

                        episode_nodes = episodes_tree.css('div.filmo-episodes')
                        for episode_node in episode_nodes:
                            episode_id = None
                            episode_year = None
                            episode_credit = None

                            episode_title_info = episode_node.css_first('a')
                            if episode_title_info and 'href' in episode_title_info:
                                episode_id_match = re.search(r'tt\d+', episode_title_info.attributes['href'])
                                if episode_id_match:
                                    episode_id = episode_id_match.group(0)
                            
                            episode_info = episode_node.text().strip().split('...')
                            if len(episode_info) > 1:
                                episode_year_info = episode_info[0]
                                episode_credit = '...'.join(episode_info[1:])
                            else:
                                episode_year_info, = episode_info

                            episode_year_match = re.search(r'\([\d]{4}\)', episode_year_info)
                            if episode_year_match:
                                episode_year = episode_year_match.group(0).strip('()')

                            yield CreditScrape(
                                name_id=name_id,
                                title_id=episode_id,
                                job_title='actor',
                                credit=episode_credit,
                                episode_count=None,
                                episode_year_start=episode_year,
                                episode_year_end=None
                            )

                # Remove the TV series info from character node if exists
                if toggle_episodes_node:
                    toggle_episodes_node.decompose()

                # Get the actor's credits
                character_node = cast_member.css_first('td.character')
                if character_node:
                    credit = re.sub(r'(\s|\r|\n)+', ' ', character_node.text().strip())

                yield CreditScrape(
                    name_id=name_id,
                    title_id=title_id,
                    job_title='actor',
                    credit=credit,
                    episode_count=episode_count,
                    episode_year_start=episode_year_start,
                    episode_year_end=episode_year_end
                )

    def get_full_credits(self, title_id):
        """Scrapes the full list of credited people for a title, not including actors.

        Will scrape the all credited members of a title, without the actors. For example, this will
        include all directors, writers, producers, cinematographers, etc.

        Args:
            title_id (:obj:`str`): The title's ID used by IMDb prefixed with `tt`.

        Yields:
            :class:`~.models.title.CreditScrape`: An object for each credited member in the title.

        Raises:
            HTTPError: If the request failed.
        """

        request = f'https://www.imdb.com/title/{title_id}/fullcredits'
        tree = self._get_tree(request)

        credits_node = tree.css_first('div#fullcredits_content')
        if credits_node:
            found_title = False
            curr_title = None
            for node in credits_node.iter():
                if not found_title:
                    if node.tag == 'h4' and node.id is None:
                        title = node.text().strip()
                        if len(title) > 0:
                            found_title = True
                            curr_title = title
                            continue
                else:
                    if node.tag == 'table':
                        content = node.css('tr')
                        for item in content:
                            name_node = item.css_first('td.name > a')
                            if name_node:
                                name_id = get_name_id(name_node)
                                credit = None
                                episode_count = None
                                episode_year_start = None
                                episode_year_end = None
                                credit_node = item.css_first('td.credit')
                                if credit_node:
                                    credit = credit_node.text().strip()
                                    # Grab episode count and years if TV series
                                    episode_details_regex = r'\(\d+\s*episodes?,\s*\d{4}(-\d{4})?\)'
                                    episode_details_match = re.search(episode_details_regex, credit)
                                    if episode_details_match:
                                        episode_count_details, episode_year_details = episode_details_match.group(0).strip('()').split(',')
                                        episode_count_match = re.search(r'\d+', episode_count_details)
                                        if episode_count_match:
                                            episode_count = episode_count_match.group(0)
                                        episode_year_split = episode_year_details.strip().split('-')
                                        episode_year_start = episode_year_split[0]
                                        if len(episode_year_split) > 1:
                                            episode_year_end = episode_year_split[1]
                                        credit = re.sub(episode_details_regex, '', credit).strip()
                                    # Strip ending 'and' for a credit
                                    if credit[-3:] == 'and':
                                        credit = credit[:-3].strip()
                                    # Remove surrounding parentheses
                                    parentheses_match = re.search(r'^\(.*\)$', credit)
                                    if parentheses_match:
                                        credit = credit.strip('()')
                                    # Final catch for empty credit
                                    if len(credit.strip()) == 0:
                                        credit = None

                                yield CreditScrape(
                                    name_id=name_id,
                                    title_id=title_id,
                                    job_title=curr_title,
                                    credit=credit,
                                    episode_count=episode_count,
                                    episode_year_start=episode_year_start,
                                    episode_year_end=episode_year_end
                                )
                found_title = False  # only because we use continue when set to True for now...

    def get_name(self, name_id):
        """Scrapes detailed information from a person's personal IMDb web page.

        Will scrape detailed information on a person's IMDb page into a new
        `NameScrape` object.

        Args:
            name_id (:obj:`str`): The person's ID used by IMDb prefixed with `nm`.

        Returns:
            :class:`~.models.name.NameScrape`: An object with the person's information.

        Raises:
            HTTPError: If the request failed.
        """
        request = f'https://www.imdb.com/name/{name_id}/bio'
        tree = self._get_tree(request)

        display_name = None
        birth_date = None
        birth_city = None
        death_date = None
        death_city = None
        death_cause = None
        birth_name = None
        nicknames = []
        height = None

        display_name_node = tree.css_first('div#main > div:nth-of-type(1) > div:nth-of-type(1) > div > h3 > a')
        if display_name_node:
            display_name = display_name_node.text().strip()

        bio_node = tree.css_first('div#bio_content')
        if bio_node:
            overview_node = bio_node.css_first('table#overviewTable')
            if overview_node:
                for row_node in overview_node.css('tr'):
                    label_node = row_node.css_first('td.label')
                    if label_node:
                        label = label_node.text().lower().strip()
                        if label == 'born':
                            birth_date_node = row_node.css_first('td > time')
                            if birth_date_node and 'datetime' in birth_date_node.attributes:
                                birth_date = birth_date_node.attributes['datetime']
                            birth_city_node = row_node.css_first('td > a')
                            if birth_city_node:
                                birth_city = birth_city_node.text().strip()
                        elif label == 'died':
                            death_date_node = row_node.css_first('td > time')
                            if death_date_node and 'datetime' in death_date_node.attributes:
                                death_date = death_date_node.attributes['datetime']
                            death_city_node = row_node.css_first('td > a')
                            if death_city_node:
                                death_city = death_city_node.text().strip()
                            death_cause_node = row_node.css_first('td ~ td')
                            if death_cause_node:
                                death_cause_match = re.search(r'\(.*\)', death_cause_node.text())
                                if death_cause_match:
                                    death_cause = death_cause_match.group(0).strip('()')
                        elif label == 'birth name':
                            birth_name_node = row_node.css_first('td ~ td')
                            if birth_name_node:
                                birth_name = birth_name_node.text().strip()
                        elif label == 'nicknames':
                            nicknames_node = row_node.css_first('td ~ td')
                            if nicknames_node:
                                nicknames = split_by_br(re.sub(r'</*td>', '', nicknames_node.html).strip())
                        elif label == 'height':
                            height_node = row_node.css_first('td ~ td')
                            if height_node:
                                height_match = re.search(r'\(\d+\.*\d*', height_node.text().strip())
                                if height_match:
                                    height = height_match.group(0).strip('(')

        return NameScrape(
            name_id=name_id,
            display_name=display_name,
            birth_name=birth_name,
            birth_date=birth_date,
            birth_city=birth_city,
            death_date=death_date,
            death_city=death_city,
            death_cause=death_cause,
            nicknames=nicknames,
            height=height
        )

    def get_name_credits(self, name_id, include_episodes=False):
        """Scrapes all title credits a person is included in.

        Scrapes the full filmography from a person's IMDb page to get each
        title they are credited in, and what category that credit is under.
        Each credit is created with a new `NameCreditScrape` object.

        Args:
            name_id (:obj:`str`): The person's ID used by IMDb prefixed with `nm`.
            include_episodes (:obj:`bool`, optional): Specify if individual episodes of a TV series
                should also be scraped.

        Yields: 
            :class:`~.models.name.NameCreditScrape`: An object for each credit in the person's filmography.

        Raises:
            HTTPError: If a request failed.
        """

        request = f'https://www.imdb.com/name/{name_id}/'
        tree = self._get_tree(request)
        
        filmography_node = tree.css_first('div#filmography')
        if not filmography_node:
            return None

        for row_node in filmography_node.css('div.filmo-row'):
            category, title_id = row_node.id.split('-')
            category = '_'.join(category.split()).lower()
            start_year = None
            end_year = None
            title_info = None
            role = None
            years_node = row_node.css_first('span.year_column')
            if years_node:
                years = years_node.text().strip()
                if len(years) > 0:
                    if '-' in years:
                        start_year, end_year = years.split('-')
                    else:
                        start_year = years
            info = split_by_br(row_node.html)
            if len(info) > 1:
                title_info, role = info
                role = re.sub(r'<.*?>', '', remove_tags_and_content(role, 'div')).strip()
                if include_episodes and row_node.css_first('div.filmo-episodes'):
                    # Send AJAX request if a "show all" link exists
                    more_episodes_node = row_node.css_first(
                        f'div#more-episodes-{title_id}-{category} ~ div.filmo-episodes'
                    )
                    episode_nodes = row_node
                    if more_episodes_node:
                        onclick_node = more_episodes_node.css_first('div > a')
                        ref_marker = get_ref_marker(onclick_node)
                        category_req = get_category(onclick_node)
                        request = f'https://www.imdb.com/name/{name_id}/episodes/_ajax?title={title_id}' + \
                                  f'&category={category_req}&ref_marker={ref_marker}&start_index=0'
                        try:
                            episode_nodes = self._get_tree(request)
                        except requests.exceptions.HTTPError as e:
                            # Some AJAX calls seem to 404, so ignore them and remove the "show all" link
                            if e.response.status_code == 404:
                                more_episodes_node.decompose()
                            else:
                                raise e

                    episode_nodes = episode_nodes.css('div.filmo-episodes')
                    for episode_node in episode_nodes:
                        episode_info_node = episode_node.css_first('a')
                        episode_id = None
                        if episode_info_node:
                            episode_id = get_title_id(episode_info_node)
                        episode_info = episode_node.text().split('...')
                        episode_year = None
                        episode_role = None
                        if len(episode_info) > 1:
                            year_info = episode_info[0]
                            episode_role = '...'.join(episode_info[1:]).strip()
                            if len(episode_role) == 0:
                                episode_role = None
                        else:
                            year_info, = episode_info
                        year_info_match = re.search(r'\([\d]{4}\)', year_info)
                        if year_info_match:
                            episode_year = year_info_match.group(0).strip('()')

                        yield NameCreditScrape(
                            name_id=name_id,
                            title_id=episode_id,
                            category=category,
                            start_year=episode_year,
                            end_year=None,
                            role=episode_role,
                            title_notes=[]
                        )
            else:
                title_info, = info
            title_info = re.sub(r'(<\s*a.*?>|<.*?a\s*>)', '', title_info)
            title_notes = [note.strip('()') for note in re.findall(r'\(.*?\)', title_info)]
            if role is not None and len(role) == 0:
                role = None

            yield NameCreditScrape(
                name_id=name_id,
                title_id=title_id,
                category=category,
                start_year=trim_year(start_year),
                end_year=trim_year(end_year),
                role=role,
                title_notes=title_notes
            )

    def get_company(self, company_id):
        """Scrapes all titles a company is credited for on IMDb.

        Will scrape all titles listed under a company on IMDb by going through each page
        in IMDb's company search. This only gives the year(s) the company was involved with
        each title and 'notes' for each listed on IMDb.

        Args:
            company_id (:obj:`str`): The company's ID used by IMDb prefixed with `co`.

        Yields:
            :class:`~.models.company.CompanyScrape`: An object for each title the company is credited for.

        Raises:
            HTTPError: If a request failed.
            InvalidCompanyId: If an invalid company ID was given.
        """

        index = 1
        finding_titles = True
        while finding_titles:
            request = f'https://www.imdb.com/search/title/?companies={company_id}&view=simple&start={index}'
            try:
                tree = self._get_tree(request)
            except requests.exceptions.HTTPError as e:
                if e.response.status_code == 404:
                    finding_titles = False
                else:
                    raise e
            # Check if this was a valid company ID
            company_title_node = tree.css_first('div.article > h1.header')
            if company_title_node:
                company_title = company_title_node.text().replace('(Sorted by Popularity Ascending)', '').strip()
                if len(company_title) == 0:
                    raise InvalidCompanyId(f'Invalid company ID: {company_id}')

            title_list_node = tree.css_first('div.lister-list')
            if not title_list_node:
                finding_titles = False
            else:
                for title_info_node in title_list_node.css('span.lister-item-header'):
                    title_id = None
                    start_year = None
                    end_year = None
                    notes = None

                    year_info_node = None
                    # Check if this is a TV episode
                    episode_node = title_info_node.css_first('small')
                    if episode_node and 'Episode' in episode_node.text():
                        episode_link_node = title_info_node.css_first('small ~ a')
                        title_id = get_title_id(episode_link_node)
                        year_info_node = title_info_node.css_first('small ~ a ~ span.lister-item-year')
                    else:
                        title_info_node = title_info_node.css_first('span.lister-item-index ~ span')
                        if title_info_node:
                            title_link_node = title_info_node.css_first('a')
                            title_id = get_title_id(title_link_node)
                            year_info_node = title_info_node.css_first('span.lister-item-year')

                    if year_info_node:
                        year_info_text = year_info_node.text().strip('()')
                        years_match = re.search(r'(\d|–|-)+', year_info_text)
                        notes_match = re.search(r'([A-Za-z]+\s*)+', year_info_text)
                        if years_match:
                            year_info = re.sub(r'[–\-]+', '\t', years_match.group(0)).split('\t')
                            if len(year_info) > 1:
                                start_year, end_year = year_info
                                # Handle shows that are still on-air (ex: '2005- ')
                                if len(end_year.strip()) == 0:
                                    end_year = None
                            else:
                                start_year, = year_info
                        if notes_match:
                            notes = notes_match.group(0)

                    yield CompanyScrape(
                        company_id=company_id,
                        title_id=title_id,
                        start_year=start_year,
                        end_year=end_year,
                        notes=notes
                    )
            index += 50

    def get_company_credits(self, title_id):
        """Gets all companies credited for a title.

        Scrapes a title's company credits page on IMDb to find information for each
        company that was credited. Each company creates a new `CompanyCreditScrape` object.

        Args:
            title_id (:obj:`str`): The title's ID used by IMDb prefixed with `tt`.

        Yields:
            :class:`~.models.company.CompanyCreditScrape`: An object for each company.

        Raises:
            HTTPError: If the request failed.
        """

        request = f'https://www.imdb.com/title/{title_id}/companycredits'
        tree = self._get_tree(request)

        credits_content_node = tree.css_first('div#company_credits_content')
        if credits_content_node:
            company_category_nodes = credits_content_node.css('h4.dataHeaderWithBorder')
            for category_node in company_category_nodes:
                category = category_node.id
                company_nodes = category_node.next.next.css('li')
                for company_node in company_nodes:
                    company_id = None
                    company_name = None
                    notes = [note.strip('()') for note in re.findall(r'\(.*?\)', company_node.text())]

                    # Get company id and name
                    link_node = company_node.css_first('a')
                    if link_node:
                        company_id = get_company_id(link_node)
                        company_name = link_node.text().strip()

                    yield CompanyCreditScrape(
                        company_id=company_id,
                        title_id=title_id,
                        company_name=company_name,
                        category=category,
                        notes=notes
                    )

    def get_tech_specs(self, title_id):
        """Gets information for all tech specs for a title.

        Uses a title's technical web page on IMDb to scrape all technical
        specifications listed. Each tech spec creates a new `TitleTechSpecScrape` object.

        Args:
            title_id (:obj:`str`): The title's ID used by IMDb prefixed with `tt`.

        Returns:
            :class:`~.models.title.TitleTechSpecScrape`: An object containing the information.

        Raises:
            HTTPError: If the request failed.
        """

        request = f'https://www.imdb.com/title/{title_id}/technical/'
        tree = self._get_tree(request)

        runtime = None
        sound_mix = []
        color = None
        aspect_ratio = []
        camera = []
        laboratory = []
        negative_format = None
        cinematographic_process = []
        printed_film_format = None

        tech_content_node = tree.css_first('div#technical_content')
        if tech_content_node:
            for tech_spec_node in tech_content_node.css('tr.even, tr.odd'):
                label_node = tech_spec_node.css_first('td.label')
                content_node = tech_spec_node.css_first('td.label ~ td')
                if label_node and content_node:
                    label = label_node.text().lower().strip()
                    if 'runtime' in label:
                        runtime_regex = r'\d+.*min'
                        content_node_text = content_node.text()
                        if '(' in content_node_text:
                            runtime_regex = rf'\({runtime_regex}\)'
                        runtime_match = re.search(runtime_regex, content_node_text)
                        if runtime_match:
                            runtime = re.sub(r'[()\smin]+', '', runtime_match.group(0))
                    elif 'sound mix' in label:
                        sound_mix = [
                            sound.strip() for sound in re.sub(r'\s+', ' ', content_node.text().strip()).split('|')
                        ]
                    elif 'color' in label:
                        color = re.sub(r'\s+', ' ', content_node.text().strip())
                    elif 'aspect' in label:
                        aspect_ratio = [
                            asp.strip() for asp in split_by_br(
                                re.sub(r'\s+', ' ', remove_tags(content_node.html, 'td')))
                        ]
                    elif 'camera' in label:
                        camera = [
                            cam.strip() for cam in re.sub(r'(and|,)', '\t', content_node.text().strip()).split('\t')
                        ]
                    elif 'laboratory' in label:
                        laboratory = [
                            lab.strip() for lab in split_by_br(
                                re.sub(r'\s+', ' ', remove_tags(content_node.html, 'td')))
                        ]
                    elif 'negative' in label:
                        negative_format = content_node.text().strip()
                    elif 'cinematographic' in label:
                        cinematographic_process = [
                            cin.strip() for cin in split_by_br(
                                re.sub(r'\s+', ' ', remove_tags(content_node.html, 'td')))
                        ]
                    elif 'printed film' in label:
                        printed_film_format = re.sub(r'\s+', ' ', content_node.text().strip())

        return TitleTechSpecsScrape(
            title_id=title_id,
            runtime=runtime,
            sound_mix=sound_mix,
            color=color,
            aspect_ratio=aspect_ratio,
            camera=camera,
            laboratory=laboratory,
            negative_format=negative_format,
            cinematographic_process=cinematographic_process,
            printed_film_format=printed_film_format
        )

    def _get_tree(self, request):
        """Get the selectolax HTML tree given a request.

        Args:
            request (:obj:`str`): The HTTP GET request.

        Returns:
            :class:`HTMLTree`: The HTML tree from the GET request.
        
        Raises:
            HTTPError: If a non successful response was returned.
        """

        response = requests.get(request, headers=self._headers)
        response.raise_for_status()
        return HTMLParser(response.text)
