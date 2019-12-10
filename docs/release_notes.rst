Release Notes
=============

* Release 0.2.1 (10 December 2019)

   - Fixed import of utils methods within the pymdb.models modules (`#8`_)

* Release 0.2.0 (29 November 2019)

   - Mapped :class:`~.models.name.CreditScrape`'s member variable `job_title` into key values (`#5`_)
   - Added module :obj:`~.models.search` to store different IMDb search results (`#1`_)
   - Added method `~.scraper.PyMDbScraper.get_search_results` to :class:`~.scraper.PyMDbScraper`
     to retrieve search results from IMDb based on keywords (`#1`_)
   - Added utils method :obj:`~.utils.trim_name` to trim names within IMDb search results (`#1`_)
   - Added method :obj:`~.scraper.PyMDbScraper.get_full_credits_as_dict` to :class:`~.scraper.PyMDbScraper`
     to return a dictionary with `job_title` as the key for a list of :class:`~.models.name.CreditScrape`
     objects (`#4`_)
   - Added support for Python 3.8 by updating `selectolax` version to 0.2.3 (`#7`_)

* Release 0.1.1 (21 November 2019)

   - Changed the type of :class:`~.models.title.TitleScrape`'s member variable `end_year`
     from :obj:`datetime` to :obj:`int` to be more consistent with other classes
   - Changed the name of :class:`~.models.title.TitleScrape`'s member variable `title_text`
     to `display_title`
   - Added the member variable `known_for_titles` to :class:`~.models.name.NameScrape` to
     store a person's known for titles as listed on their IMDb page
   - Added an optional parameter `include_known_for_titles` to :class:`~.scraper.PyMDbScraper`'s
     method :obj:`~.scraper.PyMDbScraper.get_name` since an extra request needs to be sent to retrieve data for
     `known_for_titles`
   - Renamed :obj:`get_full_credits` to :obj:`~.scraper.PyMDbScraper.get_full_crew` (`#3`_)
   - Combined :obj:`~.scraper.PyMDbScraper.get_full_cast` and :obj:`~.scraper.PyMDbScraper.get_full_crew` into
     a single helper method of the previously used name :obj:`~.scraper.PyMDbScraper.get_full_credits` (`#3`_)
   - Added new utils function :obj:`~.utils.get_episode_info` to parse the episode information for an actor's
     credits on a TV series' IMDb page
   - Modified :class:`~.models.title.TitleScrape`'s `top_cast` member variable to be a list of :class:`~.models.name.CreditScrape`
     objects instead of a list of name IDs (`#6`_)

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

.. _#1: https://github.com/zembrodt/pymdb/issues/1
.. _#3: https://github.com/zembrodt/pymdb/issues/3
.. _#4: https://github.com/zembrodt/pymdb/issues/4
.. _#5: https://github.com/zembrodt/pymdb/issues/5
.. _#6: https://github.com/zembrodt/pymdb/issues/6
.. _#7: https://github.com/zembrodt/pymdb/issues/7
.. _#8: https://github.com/zembrodt/pymdb/issues/8