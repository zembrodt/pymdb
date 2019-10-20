import re, requests
from selectolax.parser import HTMLParser
from pymdb.models import (
    CompanyScrape,
    CompanyCreditScrape,
    CreditScrape,
    NameScrape,
    NameCreditScrape,
    TitleScrape,
    TitleTechSpecsScrape
)
from pymdb.utils.util import split_by_br, trim_year, remove_divs, remove_tags

class PyMDbScraper:
    _headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36',
        'accept': 'text/html,application/xhtml+xml,application/xml'
    }

    def __init__(self):
        pass

    # Get information on title scraped from IMDb page
    def get_title(self, title_id):
        response = requests.get(f'https://www.imdb.com/title/{title_id}', headers=self._headers)
        tree = HTMLParser(response.text)

        plot = tree.css_first('div.summary_text').text().strip()
        storyline_node = tree.css_first('div#titleStoryLine')
        storyline = storyline_node.css_first('div > p > span').text().strip()
        tagline_node = tree.css_first('#titleStoryLine > div:nth-of-type(3)')
        tagline = None
        if tagline_node and 'Taglines' in tagline_node.text():
            tagline = re.sub(r'(Taglines:|See more.*)', '', tagline_node.text()).strip()
        title_node = tree.css_first('div.title_block > div > div > div.title_wrapper > div.subtext')

        # If this is a TV series, get the year the show ended
        end_year = None
        for link_node in title_node.css('a'):
            if 'title' in link_node.attributes and link_node.attributes['title'] == 'See more release dates' and 'TV Series' in link_node.text():
                series_dates_match = re.search(r'[\d]{4}(-|–)[\d]{4}', link_node.text())
                if series_dates_match:
                    end_year_split = re.sub(r'(-|–)', '\t', series_dates_match.group(0)).split('\t')
                    if len(end_year_split) > 1:
                        end_year = end_year_split[1]

        title_node.strip_tags(['span', 'a', 'time'])
        rating = tree.css_first('div.titleBar > div.title_wrapper > div.subtext').text()
        rating = re.sub(r'(\s|,)*', '', rating).strip()

        country = None
        language = None
        release_date = None
        production_companies = []
        budget = None
        opening_weekend_gross = None
        opening_weekend_date = None
        usa_gross = None
        worldwide_gross = None
        text_block_nodes = tree.css('div#titleDetails > div.txt-block')
        for text_block_node in text_block_nodes:
            text_block_id = text_block_node.css_first('h4.inline')
            if text_block_id:
                text_block_id = text_block_id.text().lower().strip()
                if 'country' in text_block_id:
                    country = text_block_node.css_first('a').text().strip()
                elif 'language' in text_block_id:
                    language = text_block_node.css_first('a').text().strip()
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
                    opening_weekend_date = text_block_node.css_first('span').text().strip()
                elif 'gross usa' in text_block_id:
                    usa_gross_match = re.search(r'\$(\d|,)+', text_block_node.text())
                    if usa_gross_match:
                        usa_gross = re.sub(r'(\$|,)+', '', usa_gross_match.group(0))
                elif 'worldwide gross' in text_block_id:
                    worldwide_gross_match = re.search(r'\$(\d|,)+', text_block_node.text())
                    if worldwide_gross_match:
                        worldwide_gross = re.sub(r'(\$|,)+', '', worldwide_gross_match.group(0))

        cast = tree.css_first('table.cast_list')
        cast_members = []
        for cast_member in cast.css('tr.odd, tr.even'):
            cast_member_node = cast_member.css_first('td:nth-of-type(2) > a')
            if cast_member_node:
                cast_member_id = re.search(r'nm\d+', cast_member_node.attributes['href']).group(0)
                cast_member_name = cast_member_node.text().strip()
                character_nodes = cast_member.css('td.character > a')
                characters = []
                for c in character_nodes:
                    characters.append(c.text().strip())
                cast_members.append(f'{cast_member_name} ({cast_member_id}): {", ".join(characters)}')

        season_number = None
        episode_number = None
        heading_nodes = tree.css('div.bp_heading')
        for heading_node in heading_nodes:
            if 'Season' in heading_node.text():
                heading_node_text = heading_node.text().lower()
                season_number_match = re.search(r'season\s*\d+', heading_node_text)
                if season_number_match:
                    season_number = re.search(r'\d+', season_number_match.group(0)).group(0)
                episode_number_match = re.search(r'episode\s*\d+', heading_node_text)
                if episode_number_match:
                    episode_number = re.search(r'\d+', episode_number_match.group(0)).group(0)

        return TitleScrape(
            title_id=title_id,
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
        response = requests.get(f'https://www.imdb.com/title/{title_id}/fullcredits', headers=self._headers)
        tree = HTMLParser(response.text)

        cast = tree.css_first('table.cast_list').css('tr')
        for cast_member in cast:
            actor_node = cast_member.css_first('td.primary_photo + td')
            if actor_node is not None:
                actor_node = actor_node.css_first('a')
                actor_id = re.search(r'nm\d+', actor_node.attributes['href']).group(0)

                # Check if this is a TV series
                toggle_episodes_node = cast_member.css_first('a.toggle-episodes')
                episode_count = None
                episode_year_start = None
                episode_year_end = None
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
                    episode_count = re.search(r'\d+', episode_count).group(0)
                
                    if include_episodes:
                        ref_marker = toggle_episodes_node.attributes['onclick'].split(',')[4].strip('\'')
                        request = f'https://www.imdb.com/name/{actor_id}/episodes/_ajax?title={title_id}&category=actor&ref_marker={ref_marker}&start_index=0'
                        episodes_reponse = requests.get(request)
                        status_code = episodes_reponse.status_code

                        if status_code == 200:
                            episode_nodes = HTMLParser(episodes_reponse.text).css('div.filmo-episodes')
                            for episode_node in episode_nodes:
                                episode_title_info = episode_node.css_first('a')
                                episode_id = re.search(r'tt\d+', episode_title_info.attributes['href']).group(0)
                                episode_info = episode_node.text().strip().split('...')
                                episode_year = None
                                episode_credit = None
                                if len(episode_info) > 1:
                                    episode_year_info = episode_info[0]
                                    episode_credit = '...'.join(episode_info[1:])
                                else:
                                    episode_year_info, = episode_info
                                episode_year_match = re.search(r'\([\d]{4}\)', episode_year_info)
                                if episode_year_match:
                                    episode_year = episode_year_match.group(0).strip('()')

                                yield CreditScrape(
                                    name_id=actor_id,
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

                character_node = cast_member.css_first('td.character')
                credit = None
                if character_node is not None:
                    credit = re.sub(r'(\s|\r|\n)+', ' ', character_node.text().strip())

                yield CreditScrape(
                    name_id=actor_id,
                    title_id=title_id,
                    job_title='actor',
                    credit=credit,
                    episode_count=episode_count,
                    episode_year_start=episode_year_start,
                    episode_year_end=episode_year_end
                )

    # Get the full credits of all members minus actors
    def get_full_credits(self, title_id):
        response = requests.get(f'https://www.imdb.com/title/{title_id}/fullcredits', headers=self._headers)
        tree = HTMLParser(response.text)

        credits_node = tree.css_first('div#fullcredits_content')
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
                    if content is not None and len(content) > 0:
                        for item in content:
                            name_node = item.css_first('td.name')
                            if name_node is not None:
                                name_node = name_node.css_first('a')
                                name_id = re.search(r'nm\d+', name_node.attributes['href']).group(0)
                                credit_node = item.css_first('td.credit')
                                credit = credit_node.text().strip() if credit_node is not None else ''
                                credits = [credit] if len(credit) > 0 else []

                                yield CreditScrape(
                                    name_id=name_id,
                                    title_id=title_id,
                                    job_title=curr_title,
                                    credit=credits
                                )
            found_title = False  # only because we use continue when set to True for now...

    # Get information on a person scraped from IMDb page
    def get_name(self, name_id):
        response = requests.get(f'https://www.imdb.com/name/{name_id}/bio', headers=self._headers)
        tree = HTMLParser(response.text)

        bio_node = tree.css_first('div#bio_content')
        overview_node = bio_node.css_first('table#overviewTable')
        display_name = tree.css_first('div#main > div:nth-of-type(1) > div:nth-of-type(1) > div > h3 > a').text().strip()
        birth_date = None
        birth_city = None
        death_date = None
        death_city = None
        death_cause = None
        birth_name = None
        nicknames = []
        height = None
        if overview_node:
            for row_node in overview_node.css('tr'):
                label = row_node.css_first('td.label').text().strip()
                if label == 'Born':
                    birth_date = row_node.css_first('td > time').attributes['datetime']
                    birth_city = row_node.css_first('td > a').text().strip()
                elif label == 'Died':
                    death_date = row_node.css_first('td > time').attributes['datetime']
                    death_city = row_node.css_first('td > a').text().strip()
                    death_cause = row_node.css_first('td ~ td').text()
                    death_cause = re.search(r'\(.*\)', death_cause).group(0).strip('()')
                elif label == 'Birth Name':
                    birth_name = row_node.css_first('td ~ td').text().strip()
                elif label == 'Nicknames':
                    nicknames = row_node.css_first('td ~ td').html
                    nicknames = re.sub(r'</*td>', '', nicknames).strip()
                    nicknames = split_by_br(nicknames)
                elif label == 'Height':
                    height = row_node.css_first('td ~ td').text().strip()
                    height = re.search(r'\(\d+\.*\d*', height).group(0).strip('(')

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
        response = requests.get(f'https://www.imdb.com/name/{name_id}/', headers=self._headers)
        tree = HTMLParser(response.text)
        
        filmography_node = tree.css_first('div#filmography')
        for row_node in filmography_node.css('div.filmo-row'):
            category, title_id = row_node.attributes['id'].split('-')
            category = '_'.join(category.split()).lower()
            start_year = None
            end_year = None
            title_info = None
            role = None
            years = row_node.css_first('span.year_column').text().strip()
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
                        onclick_action = more_episodes_node.css_first('div > a').attributes['onclick']
                        ref_marker = re.search(r'\'nm_.*?\'', onclick_action).group(0).strip('\'')
                        category_req = onclick_action.split(',')[3].strip('\'')
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
                        episode_info = episode_node.css_first('a')
                        episode_title = episode_info.text().strip()
                        episode_id = re.search(r'tt\d+', episode_info.attributes['href']).group(0)
                        episode_year = None
                        episode_info = episode_node.text().split('...')
                        role = None
                        if len(episode_info) > 1:
                            year_info = episode_info[0]
                            role = '...'.join(episode_info[1:])
                            role = role.strip()
                        else:
                            year_info, = episode_info
                        year_info = re.search(r'\([\d]{4}\)', year_info)
                        if year_info:
                            episode_year = year_info.group(0).strip('()')

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
                            title_id = re.search(r'tt\d+', episode_link_node.attributes['href']).group(0)
                            year_info_node = title_info_node.css_first('small ~ a ~ span.lister-item-year')
                        else:
                            title_info_node = title_info_node.css_first('span.lister-item-index ~ span')
                            title_id = re.search(r'tt\d+', title_info_node.css_first('a').attributes['href']).group(0)
                            year_info_node = title_info_node.css_first('span.lister-item-year')

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
        company_category_nodes = tree.css_first('div#company_credits_content').css('h4.dataHeaderWithBorder')
        for category_node in company_category_nodes:
            category = category_node.attributes['id']
            company_nodes = category_node.next.next.css('li')
            for company_node in company_nodes:
                link_node = company_node.css_first('a')
                company_id = re.search(r'co\d+', link_node.attributes['href']).group(0)
                company_name = link_node.text().strip()
                notes = [note.strip('()') for note in re.findall(r'\(.*?\)', company_node.text())]
                yield CompanyCreditScrape(
                    company_id=company_id,
                    title_id=title_id,
                    company_name=company_name,
                    category=category,
                    notes=notes
                )

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

        for tech_spec_node in tree.css_first('div#technical_content').css('tr.even, tr.odd'):
            label = tech_spec_node.css_first('td.label').text().lower().strip()
            if 'runtime' in label:
                runtime_match = re.search(r'\(\d+.*min\)', tech_spec_node.css_first('td.label ~ td').text())
                if runtime_match:
                    runtime = re.sub(r'[\(\)\smin]+', '', runtime_match.group(0))
            elif 'sound mix' in label:
                sound_mix = [
                    sound.strip() for sound in re.sub(r'\s+', ' ', tech_spec_node.css_first('td.label ~ td').text().strip()).split('|')
                ]
            elif 'color' in label:
                color = re.sub(r'\s+', ' ', tech_spec_node.css_first('td.label ~ td').text().strip())
            elif 'aspect' in label:
                aspect_ratio = [
                    asp.strip() for asp in split_by_br(
                        re.sub(r'\s+', ' ', remove_tags(tech_spec_node.css_first('td.label ~ td').html, 'td')))
                ]
            elif 'camera' in label:
                camera = [cam.strip() for cam in re.sub(r'(and|,)', '\t', tech_spec_node.css_first('td.label ~ td').text().strip()).split('\t')]
            elif 'laboratory' in label:
                laboratory = [
                    lab.strip() for lab in split_by_br(
                        re.sub(r'\s+', ' ', remove_tags(tech_spec_node.css_first('td.label ~ td').html, 'td')))
                ]
            elif 'negative' in label:
                negative_format = tech_spec_node.css_first('td.label ~ td').text().strip()
            elif 'cinematographic' in label:
                cinematographic_process = [
                    cin.strip() for cin in split_by_br(
                        re.sub(r'\s+', ' ', remove_tags(tech_spec_node.css_first('td.label ~ td').html, 'td')))
                ]
            elif 'printed film' in label:
                printed_film_format = re.sub(r'\s+', ' ', tech_spec_node.css_first('td.label ~ td').text().strip())

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