"""Module containing exception classes unique to PyMDb."""

class InvalidCompanyId(Exception):
    """Raised when an invalid company ID has been used in an IMDb request."""
    pass

class InvalidParseFormat(Exception):
    """Raised when PyMDbParser runs into a row with an incorrect column size."""
    pass