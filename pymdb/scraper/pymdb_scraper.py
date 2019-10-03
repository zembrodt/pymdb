import re, requests
from selectolax.parser import HTMLParser


class PyMDbScraper:
    _headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36',
        'accept': 'text/html,application/xhtml+xml,application/xml'
    }

    def __init__(self):
        self.blah = 5

    def get_title(self, title_id):
        response = requests.get(f'https://www.imdb.com/title/{title_id}', headers=self._headers)

        print(response.status_code)
        tree = HTMLParser(response.text)

        plot = tree.css_first('div.summary_text').text().strip()
        storyline_node = tree.css_first('div#titleStoryLine')
        description = storyline_node.css_first('div > p > span').text().strip()
        tagline = 'EMPTY'
        tagline_nodes = storyline_node.css('div.txt-block > h4')
        for node in tagline_nodes:
            if 'Taglines' in node.text():
                tagline = node.parent.text().strip()
                break
        title_node = tree.css_first('div.title_block > div > div > div.title_wrapper > div.subtext')

        release_date = None
        for link in title_node.css('a'):
            if 'title' in link.attributes and link.attributes['title'] == 'See more release dates':
                release_date = re.search(r'\d+\s\w+\s\d+', link.text().strip()).group(0)
                break

        title_node.strip_tags(['span', 'a', 'time'])
        rating = title_node.text().strip()

        print('plot: '+plot)
        print('desc:'+ description)
        print('tagline:'+tagline)
        print('rating:'+rating)
        print('release date:' +release_date)

        '''
        return Title(
            title_id=title_id,
            sub_title_id=None,
            title_type=None,
            primary_title=None,
            original_title=None,
            is_adult=None,
            start_year=None,
            end_year=None,
            runtime_minutes=None,
            plot=plot,
            description=description,
            release_date=release_date,
            tagline=tagline,
            rating=rating,
            title_localized=None,
            region=None,
            language=None,
            is_original_title=None

        )
        credits = tree.css_first('div#fullcredits_content')
        i = 0
        found_title = False
        curr_title = None
        credits_dict = {}
        for node in credits.iter():
            # if i > 4:
            # break
            if not found_title:
                if node.tag == 'h4' and node.id is None:
                    title = node.text().strip()
                    if len(title) > 0:
                        found_title = True
                        print(title)
                        curr_title = title
                        credits_dict[title] = []
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
                                name = f'{name_text} ({name_id})'
                                credit_node = item.css_first('td.credit')
                                credit = credit_node.text().strip() if credit_node is not None else ''
                                credits = [credit] if len(credit) > 0 else []
                                print(f'\t{name}: {credit}')
                                credits_dict[curr_title].append(Name(name_id, name_text, credits))
                    else:
                        print('\t[EMPTY]')
            # i += 1
            found_title = False  # only because we use continue when set to True for now...

        cast = tree.css_first('table.cast_list').css('tr')
        cast_members = []
        print('CAST:')
        for cast_member in cast:
            actor_node = cast_member.css_first('td.primary_photo + td')
            if actor_node is not None:
                actor_node = actor_node.css_first('a')
                actor_id = re.search(r'nm\d+', actor_node.attributes['href']).group(0)
                actor_text = actor_node.text().strip()
                actor = f'{actor_text} ({actor_id})'
                character_node = cast_member.css_first('td.character')
                credits = []
                if character_node is not None:
                    character_links = character_node.css('a')
                    if character_links is not None and len(character_links) > 0:
                        characters = ', '.join([c.text().strip() for c in character_links])
                        print(f'\t{actor}: {characters}')
                        credits = [c.text().strip() for c in character_links]
                    else:
                        print(f'\t{actor}: {" ".join(character_node.text().split())}')
                        credits = [" ".join(character_node.text().split())]
                else:
                    print(f'\t{actor}: [NO CREDITS]')
                cast_members.append(Name(actor_id, actor_text, credits))

        title_node = tree.css_first('div.parent > h3')
        title = title_node.css_first('a')
        title_id = re.search(r'tt\d+', title.attributes['href']).group(0)
        title_text = title.text().strip()
        year = re.search(r'\d+', title_node.css_first('span').text()).group(0)

        movie = Title(title_id, title_text, year, cast_members, credits_dict)

        print(movie)
        '''

    def get_name(self, title):
        pass
