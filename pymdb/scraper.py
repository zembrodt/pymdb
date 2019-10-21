import re, requests
from selectolax.parser import HTMLParser
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
    remove_divs,
    remove_tags,
    split_by_br,
    trim_year,
)

'''
Object containing functions to scrape various information from IMDb based on the given ID
'''
class PyMDbScraper:
    _headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36',
        'accept': 'text/html,application/xhtml+xml,application/xml'
    }

    def __init__(self):
        pass

    # Get information on title scraped from IMDb page
    def get_title(self, title_id):
        request = f'https://www.imdb.com/title/{title_id}/'
        response = requests.get(request, headers=self._headers)
        status_code = response.status_code
        if status_code != 200:
            print(f'Bad request: {status_code}')
            print(request)
            print(self._headers)
            return None

        tree = HTMLParser(response.text)

        title_text = None
        title_parent_id = None
        rating = None
        country = None
        language = None
        release_date = None
        end_year = None
        season_number = None
        episode_number = None
        tagline = None
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

        # Get tagline
        tagline_node = tree.css_first('#titleStoryLine > div:nth-of-type(3)')
        if tagline_node and 'Taglines' in tagline_node.text():
            tagline = re.sub(r'(Taglines:|See more.*)', '', tagline_node.text()).strip()

        # Get MPAA Rating
        title_node = tree.css_first('div.title_block > div > div > div.title_wrapper > div.subtext')
        if title_node:
            title_node.strip_tags(['span', 'a', 'time'])
            rating_node = tree.css_first('div.titleBar > div.title_wrapper > div.subtext')
            if rating_node:
                rating = re.sub(r'(\s|,)*', '', rating_node.text()).strip()

        # If this is a TV series, get the year the show ended
        for link_node in title_node.css('a'):
            if 'title' in link_node.attributes and link_node.attributes['title'] == 'See more release dates' and 'TV Series' in link_node.text():
                series_dates_match = re.search(r'[\d]{4}(-|–)[\d]{4}', link_node.text())
                if series_dates_match:
                    end_year_split = re.sub(r'(-|–)', '\t', series_dates_match.group(0)).split('\t')
                    if len(end_year_split) > 1:
                        end_year = end_year_split[1]

        # Parse through text blocks
        text_block_nodes = tree.css('div#titleDetails > div.txt-block')
        for text_block_node in text_block_nodes:
            text_block_id = text_block_node.css_first('h4.inline')
            if text_block_id:
                text_block_id = text_block_id.text().lower().strip()
                if 'country' in text_block_id:
                    country_node = text_block_node.css_first('a')
                    if country_node:
                        country = country_node.text().strip()
                elif 'language' in text_block_id:
                    language_node = text_block_node.css_first('a')
                    if language_node:
                        language = language_node.text().strip()
                elif 'release date' in text_block_id:
                    release_date_match = re.search(r'\d+?\s*\w+?\s*[\d]{4}', text_block_node.text())
                    if release_date_match:
                        release_date = release_date_match.group(0)
                elif 'production co' in text_block_id:
                    companies = text_block_node.css('a')
                    for company in companies:
                        company_match = re.search(r'co\d+', company.attributes['href'])
                        if company_match:
                            production_companies.append(company_match.group(0))
                # Box office info
                elif 'budget' in text_block_id:
                    budget_match = re.search(r'\$(\d|,)+', text_block_node.text())
                    if budget_match:
                        budget = re.sub(r'(\$|,)+', '', budget_match.group(0))
                elif 'opening weekend' in text_block_id:
                    opening_weekend_gross_match = re.search(r'\$(\d|,)+', text_block_node.text())
                    if opening_weekend_gross_match:
                        opening_weekend_gross = re.sub(r'(\$|,)+', '', opening_weekend_gross_match.group(0))
                    opening_weekend_date_node = text_block_node.css_first('span')
                    if opening_weekend_date_node:
                        opening_weekend_date = opening_weekend_date_node.text().strip()
                elif 'gross usa' in text_block_id:
                    usa_gross_match = re.search(r'\$(\d|,)+', text_block_node.text())
                    if usa_gross_match:
                        usa_gross = re.sub(r'(\$|,)+', '', usa_gross_match.group(0))
                elif 'worldwide gross' in text_block_id:
                    worldwide_gross_match = re.search(r'\$(\d|,)+', text_block_node.text())
                    if worldwide_gross_match:
                        worldwide_gross = re.sub(r'(\$|,)+', '', worldwide_gross_match.group(0))

        # Get top cast members
        cast_node = tree.css_first('table.cast_list')
        if cast_node:
            for cast_member in cast_node.css('tr.odd, tr.even'):
                cast_member_node = cast_member.css_first('td:nth-of-type(2) > a')
                if cast_member_node:
                    cast_member_id = re.search(r'nm\d+', cast_member_node.attributes['href']).group(0)
                    cast_member_name = cast_member_node.text().strip()
                    character_nodes = cast_member.css('td.character > a')
                    characters = []
                    for c_node in character_nodes:
                        characters.append(c_node.text().strip())
                    cast_members.append(f'{cast_member_name} ({cast_member_id}): {", ".join(characters)}')

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
            tagline=tagline,
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

    # Get full credits of all actors
    def get_full_cast(self, title_id, include_episodes=False):
        request = f'https://www.imdb.com/title/{title_id}/fullcredits'
        response = requests.get(request, headers=self._headers)
        status_code = response.status_code
        if status_code != 200:
            print(f'Bad request: {status_code}')
            print(request)
            print(self._headers)
            return None

        tree = HTMLParser(response.text)

        cast_node = tree.css_first('table.cast_list').css('tr')
        for cast_member in cast_node:
            actor_node = cast_member.css_first('td.primary_photo + td > a')
            if actor_node:
                #actor_node = actor_node.css_first('a')

                name_id = None
                credit = None
                episode_count = None
                episode_year_start = None
                episode_year_end = None
                
                # Get actor's name id
                name_id = get_name_id(actor_node)

                # Check if this is a TV series
                toggle_episodes_node = cast_member.css_first('a.toggle-episodes')
                if toggle_episodes_node:
                    episode_info = re.sub(r'<\s*span.*?<\s*\/\s*span\s*>', '', toggle_episodes_node.text()).strip().split(',')
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
                        request = f'https://www.imdb.com/name/{actor_id}/episodes/_ajax?title={title_id}&category=actor&ref_marker={ref_marker}&start_index=0'
                        episodes_reponse = requests.get(request)
                        status_code = episodes_reponse.status_code

                        if status_code == 200:
                            episode_nodes = HTMLParser(episodes_reponse.text).css('div.filmo-episodes')
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
                        else:
                            print(f'Bad request: {status_code}')
                            print(request)

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

    # Get the full credits of all members minus actors
    def get_full_credits(self, title_id):
        request = f'https://www.imdb.com/title/{title_id}/fullcredits'
        response = requests.get(request, headers=self._headers)
        status_code = response.status_code
        if status_code != 200:
            print(f'Bad request: {status_code}')
            print(request)
            print(self._headers)
            return None

        tree = HTMLParser(response.text)

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
                                name_id = None
                                credit = None

                                #name_node = name_node.css_first('a')
                                name_id_match = re.search(r'nm\d+', name_node.attributes['href'])
                                if name_id_match:
                                    name_id = name_id_match.group(0)
                                credit_node = item.css_first('td.credit')
                                if credit_node:
                                    credit = credit_node.text().strip()
                                    #credits = [credit] if len(credit) > 0 else []

                                yield CreditScrape(
                                    name_id=name_id,
                                    title_id=title_id,
                                    job_title=curr_title,
                                    credit=credit,
                                    episode_count=None,
                                    episode_year_start=None,
                                    episode_year_end=None
                                )
                found_title = False  # only because we use continue when set to True for now...

    # Get information on a person scraped from IMDb page
    def get_name(self, name_id):
        request = f'https://www.imdb.com/name/{name_id}/bio'
        response = requests.get(request, headers=self._headers)
        status_code = response.status_code
        if status_code != 200:
            print(f'Bad request: {status_code}')
            print(request)
            print(self._headers)
            return None

        tree = HTMLParser(response.text)

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

    # Get full credited information on a person from IMDb page
    def get_name_credits(self, name_id, include_episodes=False):
        request = f'https://www.imdb.com/name/{name_id}/'
        response = requests.get(request, headers=self._headers)
        status_code = response.status_code
        if status_code != 200:
            print(f'Bad request: {status_code}')
            print(request)
            print(self._headers)
            return None

        tree = HTMLParser(response.text)
        
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
                role = re.sub(r'<.*?>', '', remove_divs(role)).strip()
                if include_episodes and row_node.css_first('div.filmo-episodes'):
                    # Send AJAX request if a "show all" link exists
                    more_episodes_node = row_node.css_first(f'div#more-episodes-{title_id}-{category} ~ div.filmo-episodes')
                    episode_nodes = row_node
                    if more_episodes_node:
                        onclick_node = more_episodes_node.css_first('div > a')
                        ref_marker = get_ref_marker(onclick_node)
                        category_req = get_category(onclick_node)
                        #ref_marker = re.search(r'\'nm_.*?\'', onclick_action).group(0).strip('\'')
                        #category_req = onclick_action.split(',')[3].strip('\'')
                        request = f'https://www.imdb.com/name/{name_id}/episodes/_ajax?title={title_id}&category={category_req}&ref_marker={ref_marker}&start_index=0'
                        episodes_reponse = requests.get(request)
                        status_code = episodes_reponse.status_code
                        if status_code == 200:
                            episode_nodes = HTMLParser(episodes_reponse.text)
                        elif status_code == 404:
                            # Some AJAX calls seem to 404, so ignore them and remove the "show all" link
                            more_episodes_node.decompose()
                        else:
                            # Log other responses
                            print(f'Bad request ({status_code}):')
                            print(request)
                    episode_nodes = episode_nodes.css('div.filmo-episodes')
                    for episode_node in episode_nodes:
                        episode_info_node = episode_node.css_first('a')
                        if episode_info_node:
                            episode_title = episode_info_node.text().strip()
                            episode_id = get_title_id(episode_info_node)
                        episode_info = episode_node.text().split('...')
                        episode_year = None
                        role = None
                        if len(episode_info) > 1:
                            year_info = episode_info[0]
                            role = '...'.join(episode_info[1:]).strip()
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
                            role=role,
                            title_notes=[]
                        )
            else:
                title_info, = info
            title_info = re.sub(r'(<\s*a.*?>|<.*?a\s*>)', '', title_info)
            title_notes = [note.strip('()') for note in re.findall(r'\(.*?\)', title_info)]

            yield NameCreditScrape(
                name_id=name_id,
                title_id=title_id,
                category=category,
                start_year=trim_year(start_year),
                end_year=trim_year(end_year),
                role=role,
                title_notes=title_notes
            )

    # Get all titles company has worked on
    def get_company(self, company_id):
        index = 1
        finding_titles = True
        while finding_titles:
            request = f'https://www.imdb.com/search/title/?companies={company_id}&view=simple&start={index}'
            response = requests.get(request, headers=self._headers)
            status_code = response.status_code
            if status_code == 200:
                tree = HTMLParser(response.text)
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
                                year_info = re.sub(r'(–|-)+', '\t', years_match.group(0)).split('\t')
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
            else:
                print(f'Bad request: {status_code}')
                print(request)
                print(self._headers)
                finding_titles = False
            index += 50

    # Get all companies credited for title
    def get_company_credits(self, title_id):
        request = f'https://www.imdb.com/title/{title_id}/companycredits'
        response = requests.get(request, headers=self._headers)
        status_code = response.status_code
        if status_code != 200:
            print(f'Bad request: {status_code}')
            print(request)
            print(self._headers)
            return None
        
        tree = HTMLParser(response.text)
        credits_content_node = tree.css_first('div#company_credits_content')
        if credits_content_node:
            company_category_nodes = credits_content_node.css('h4.dataHeaderWithBorder')
            for category_node in company_category_nodes:
                category = category_node.id
                company_nodes = category_node.next.next.css('li')
                for company_node in company_nodes:
                    company_id = None
                    company_name = None
                    notes = None

                    # Get company id and name
                    link_node = company_node.css_first('a')
                    if link_node:
                        company_id = get_company_id(link_node)
                        company_name = link_node.text().strip()

                    # Get company notes for current title
                    notes = [note.strip('()') for note in re.findall(r'\(.*?\)', company_node.text())]

                    yield CompanyCreditScrape(
                        company_id=company_id,
                        title_id=title_id,
                        company_name=company_name,
                        category=category,
                        notes=notes
                    )

    # Get full tech spec information for a title
    def get_tech_specs(self, title_id):
        request = f'https://www.imdb.com/title/{title_id}/technical/'
        response = requests.get(request, headers=self._headers)
        status_code = response.status_code
        if status_code != 200:
            print(f'Bad request: {status_code}')
            print(request)
            print(self._headers)
            return None
        
        tree = HTMLParser(response.text)

        runtime = None
        sound_mix = None
        color = None
        aspect_ratio = None
        camera = None
        laboratory = None
        negative_format = None
        cinematographic_process = None
        printed_film_format = None

        tech_content_node = tree.css_first('div#technical_content')
        if tech_content_node:
            for tech_spec_node in tech_content_node.css('tr.even, tr.odd'):
                label_node = tech_spec_node.css_first('td.label')
                content_node = tech_spec_node.css_first('td.label ~ td')
                if label_node and content_node:
                    label = label_node.text().lower().strip()
                    if 'runtime' in label:
                        runtime_match = re.search(r'\(\d+.*min\)', content_node.text())
                        if runtime_match:
                            runtime = re.sub(r'[\(\)\smin]+', '', runtime_match.group(0))
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
                        camera = [cam.strip() for cam in re.sub(r'(and|,)', '\t', content_node.text().strip()).split('\t')]
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