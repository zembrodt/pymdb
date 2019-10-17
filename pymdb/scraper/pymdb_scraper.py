import re, requests
from selectolax.parser import HTMLParser
from pymdb.models import (
    CreditScrape,
    NameScrape,
    NameCreditScrape,
    TitleScrape,
)
from pymdb.utils.util import split_by_br, trim_year, remove_divs

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
        tagline = tree.css_first('#titleStoryLine > div:nth-of-type(3)').text()
        tagline = re.sub(r'(Taglines:|See more.*)', '', tagline).strip()
        title_node = tree.css_first('div.title_block > div > div > div.title_wrapper > div.subtext')

        release_date = None
        end_date = None
        for link in title_node.css('a'):
            if 'title' in link.attributes and link.attributes['title'] == 'See more release dates':
                link = link.text().strip()
                try:
                    release_date = re.search(r'\d+\s\w+\s\d+', link).group(0)
                except AttributeError:
                    if 'TV Series' in link:
                        release_date, end_date = re.sub(r'(\(|\))*', '', link).split('-')
                break

        title_node.strip_tags(['span', 'a', 'time'])
        rating = tree.css_first('div.titleBar > div.title_wrapper > div.subtext').text()
        rating = re.sub(r'(\s|,)*', '', rating).strip()

        company_id = ''
        company_name = ''
        prod_company_nodes = tree.css('div#titleDetails > div.txt-block')
        for n in prod_company_nodes:
            if n.css_first('h4.inline') is not None and 'Production Co' in n.css_first('h4.inline').text().strip():
                company = n.css_first('a')
                company_id = re.search(r'co\d+', company.attributes['href']).group(0)
                company_name = company.text().strip()

        cast = tree.css_first('table.cast_list')
        cast_members = []
        for cast_member in cast.css('tr.odd, tr.even'):
            cast_member_node = cast_member.css_first('td:nth-of-type(2) > a')
            cast_member_id = re.search(r'nm\d+', cast_member_node.attributes['href']).group(0)
            cast_member_name = cast_member_node.text().strip()
            character_nodes = cast_member.css('td.character > a')
            characters = []
            for c in character_nodes:
                characters.append(c.text().strip())
            cast_members.append(f'{cast_member_name} ({cast_member_id}): {", ".join(characters)}')

        return TitleScrape(
            title_id=title_id,
            mpaa_rating=rating,
            release_date=release_date,
            end_date=end_date,
            tagline=tagline,
            plot=plot,
            storyline=storyline,
            production_company=company_id,
            top_cast=cast_members
        )

    # Get full credits of all actors
    def get_full_cast(self, title_id):
        response = requests.get(f'https://www.imdb.com/title/{title_id}/fullcredits', headers=self._headers)
        tree = HTMLParser(response.text)

        cast = tree.css_first('table.cast_list').css('tr')
        for cast_member in cast:
            actor_node = cast_member.css_first('td.primary_photo + td')
            if actor_node is not None:
                actor_node = actor_node.css_first('a')
                actor_id = re.search(r'nm\d+', actor_node.attributes['href']).group(0)
                actor_text = actor_node.text().strip()
                character_node = cast_member.css_first('td.character')
                credits = []
                if character_node is not None:
                    character_links = character_node.css('a')
                    if character_links is not None and len(character_links) > 0:
                        credits = [c.text().strip() for c in character_links]
                    else:
                        credits = [" ".join(character_node.text().split())]

                yield CreditScrape(
                    name_id=actor_id,
                    name=actor_text,
                    title_id=title_id,
                    job_title='actor',
                    credit=credits
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
                                name_text = name_node.text().strip()
                                credit_node = item.css_first('td.credit')
                                credit = credit_node.text().strip() if credit_node is not None else ''
                                credits = [credit] if len(credit) > 0 else []

                                yield CreditScrape(
                                    name_id=name_id,
                                    name=name_text,
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
        birth_date = None
        birth_city = None
        death_date = None
        death_city = None
        death_cause = None
        birth_name = None
        nicknames = []
        height = None
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
    def get_name_credits(self, name_id):
        response = requests.get(f'https://www.imdb.com/name/{name_id}/', headers=self._headers)
        tree = HTMLParser(response.text)

        filmography_node = tree.css_first('div#filmography')
        for row_node in filmography_node.css('div.filmo-row'):
            category, title_id = row_node.attributes['id'].split('-')
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

        