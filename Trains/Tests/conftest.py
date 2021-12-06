import pytest

from Trains.Common.map import City, Connection, Color, Map, Destination


@pytest.fixture(name="boston")
def make_boston() -> City:
    return City("boston", 100, 300)


@pytest.fixture(name="nyc")
def make_nyc() -> City:
    return City("nyc", 100, 100)


@pytest.fixture(name="la")
def make_la() -> City:
    return City("la", 0, 100)


@pytest.fixture(name="dc")
def make_dc() -> City:
    return City("dc", 10, 100)


@pytest.fixture(name="nyc_to_dc")
def make_nyc_to_dc(nyc: City, dc: City) -> Connection:
    return Connection({nyc, dc}, length=3, color=Color.BLUE)


@pytest.fixture(name="nyc_to_boston")
def make_nyc_to_boston(nyc: City, boston: City) -> Connection:
    return Connection({nyc, boston}, length=3, color=Color.GREEN)


@pytest.fixture(name="la_island_map")
def make_small_map(
    nyc: City,
    boston: City,
    la: City,
    dc: City,
    nyc_to_dc: Connection,
    nyc_to_boston: Connection
) -> Map:
    cities = {nyc, boston, la, dc}
    conns = {nyc_to_dc, nyc_to_boston}
    return Map(cities, conns, width=800, height=700)


@pytest.fixture(name="choose_from_dests")
def get_5_destinations(boston: City, nyc: City, la: City, dc: City):
    return {
        Destination({boston, nyc}),
        Destination({boston, la}),
        Destination({boston, dc}),
        Destination({nyc, la}),
        Destination({nyc, dc})
    }