import pytest

from Trains.Common.map import City


@pytest.fixture(name="boston")
def make_boston() -> City:
    return City("boston", 100, 300)


@pytest.fixture(name="nyc")
def make_nyc() -> City:
    return City("nyc", 100, 100)


@pytest.fixture(name="la")
def make_la() -> City:
    return City("la", 0, 100)
