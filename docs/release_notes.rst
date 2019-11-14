Release Notes
=============

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