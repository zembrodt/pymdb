Release Notes
=============

* Release 0.1.1 (21 November 2019)

   - Changed the type of :class:`~.models.title.TitleScrape`'s member variable `end_year`
     from :obj:`datetime` to :obj:`int` to be more consistent with other classes
   - Changed the name of :class:`~.models.title.TitleScrape`'s member variable `title_text`
     to `display_title`
   - Added the member variable `known_for_titles` to :class:`~.models.name.NameScrape` to
     store a person's known for titles as listed on their IMDb page
   - Added an optional parameter `include_known_for_titles` to :class:`~.scraper.PyMDbScraper`'s
     method :obj:`~.scraper.PyMDbScraper.get_name` since an extra request needs to be sent to retrieve data for
     `known_for_titles`.
   - Renamed :obj:`get_full_credits` to :obj:`~.scraper.PyMDbScraper.get_full_crew`
   - Combined :obj:`~.scraper.PyMDbScraper.get_full_cast` and :obj:`~.scraper.PyMDbScraper.get_full_crew` into
     a single helper method of the previously used name :obj:`~.scraper.PyMDbScraper.get_full_credits`
   - Added new utils function :obj:`~.utils.get_episode_info` to parse the episode information for an actor'scraper
     credits on a TV series' IMDb page
   - Modified :class:`~.models.title.TitleScrape`'s `top_cast` member variable to be a list of :class:`~.models.name.CreditScrape`
     objects instead of a list of name IDs

* Release 0.1.0 (14 November 2019)

    - Initial pre-release of PyMDb
    - Introduction of Travis-CI at https://travis-ci.com/zembrodt/pymdb
    - Modification of unit tests to execute more quickly

* Release 0.0.3 (14 November 2019)

    - Renaming of :class:`~.models.title.TitleBasics`'s member variable `runtime_minutes` to `runtime`
      to be more consistent with the naming in :class:`~.models.title.TitleTechSpecsScrape`

* Release 0.0.2 (13 Novemer 2019)

    - Introduction of member variable `budget_denomination` in :class:`~.models.title.TitleScrape` to
      specify the monetary denomination of member variable `budget`
    - Additional `utils` method :obj:`~.utils.get_denomination`
    - Introduction of full documentation via Sphinx

* Release 0.0.1 (11 November 2019)

    - Initial stable release of PyMDb to PyPI with completed unit tests