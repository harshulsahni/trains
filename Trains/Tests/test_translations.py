from Trains.Common.map import City, Connection, Color
from Trains.Translations.translations import (
    CityTranslation, ConnectionsTranslation, DestinationTranslation, MapTranslation
)


class TestCityTranslation:
    @staticmethod
    def test_invalid_vs_valid_city_json():
        assert not CityTranslation.is_city_json_valid("boston")
        assert not CityTranslation.is_city_json_valid(["boston", 1, 1])
        assert not CityTranslation.is_city_json_valid(["boston", [1]])
        assert not CityTranslation.is_city_json_valid([1, [1, 1]])
        assert CityTranslation.is_city_json_valid(["boston", [1, 1]])

    @staticmethod
    def test_city_to_json(boston: City):
        assert CityTranslation.city_to_json(boston) == ["boston", [100, 300]]

    @staticmethod
    def test_json_to_city(boston: City):
        assert CityTranslation.json_to_city(["boston", [100, 300]]) == boston

    @staticmethod
    def test_json_equality(boston: City):
        json_data = ["boston", [100, 300]]
        assert CityTranslation.city_to_json(CityTranslation.json_to_city(json_data)) == json_data
        assert CityTranslation.json_to_city(CityTranslation.city_to_json(boston)) == boston

    @staticmethod
    def test_find_city_from_name(boston: City, la: City, nyc: City):
        cities = {boston, nyc}
        assert CityTranslation.find_city_from_str("boston", cities) == boston
        assert CityTranslation.find_city_from_str("la", cities) is None


class TestConnectionTranslation:
    @staticmethod
    def test_invalid_vs_valid_acquired_json(boston: City, nyc: City):
        assert not ConnectionsTranslation.is_acquired_valid(["boston", 1])
        assert not ConnectionsTranslation.is_acquired_valid([1, "boston"])
        assert not ConnectionsTranslation.is_acquired_valid(["boston", 1])
        assert not ConnectionsTranslation.is_acquired_valid([boston, nyc])
        assert not ConnectionsTranslation.is_acquired_valid(["boston", "nyc", "red", 400])
        assert not ConnectionsTranslation.is_acquired_valid(["else", "anything", "green", 4])
        assert ConnectionsTranslation.is_acquired_valid(["anything", "else", "green", 4])

    @staticmethod
    def test_invalid_vs_valid_connection_json():
        assert not ConnectionsTranslation.are_connections_valid("boston to nyc")
        assert not ConnectionsTranslation.are_connections_valid({"boston"})
        assert not ConnectionsTranslation.are_connections_valid({"boston": "nyc"})
        assert not ConnectionsTranslation.are_connections_valid({"boston": {"nyc": "red"}})
        assert not ConnectionsTranslation.are_connections_valid({"boston": {"nyc": {"REEEEDDDDD": 7}}})
        assert not ConnectionsTranslation.are_connections_valid({"boston": {"nyc": {"red": 7}}})
        assert ConnectionsTranslation.are_connections_valid({"boston": {"nyc": {"red": 5}}})
        assert ConnectionsTranslation.are_connections_valid({"boston": {"nyc": {"red": 5, "blue": 3}}})
        assert ConnectionsTranslation.are_connections_valid({"boston": {"nyc": {"red": 5},
                                                                        "la": {"green": 3}}})

    @staticmethod
    def test_connection_to_acquired_json(nyc_to_boston: Connection):
        assert ConnectionsTranslation.acquired_to_json(nyc_to_boston) == ["boston", "nyc", "green", 3]

    @staticmethod
    def test_acquired_json_to_connection(nyc_to_boston: Connection):
        no_cities_provided = ConnectionsTranslation.json_to_acquired(["boston", "nyc", "green", 3])
        cities_provided = ConnectionsTranslation.json_to_acquired(["boston", "nyc", "green", 3],
                                                                  cities=nyc_to_boston.get_cities())
        assert no_cities_provided == Connection({
            City("nyc", 0, 0), City("boston", 0, 0)
        }, color=Color.GREEN, length=3)
        assert cities_provided == nyc_to_boston

    @staticmethod
    def test_acquired_json_equality(nyc_to_boston: Connection):
        acquired_json = ["boston", "nyc", "green", 3]
        assert ConnectionsTranslation.acquired_to_json(
            ConnectionsTranslation.json_to_acquired(acquired_json)
        ) == acquired_json
        assert ConnectionsTranslation.acquired_to_json(
            ConnectionsTranslation.json_to_acquired(acquired_json, cities=nyc_to_boston.get_cities())
        ) == acquired_json
        assert ConnectionsTranslation.json_to_acquired(
            ConnectionsTranslation.acquired_to_json(nyc_to_boston)
        ) != nyc_to_boston
        assert ConnectionsTranslation.json_to_acquired(
            ConnectionsTranslation.acquired_to_json(nyc_to_boston),
            cities=nyc_to_boston.get_cities()
        ) == nyc_to_boston

    @staticmethod
    def test_connection_to_json(nyc_to_boston: Connection):
        assert ConnectionsTranslation.connection_to_json(nyc_to_boston) == {'boston': {'nyc': {'green': 3}}}

    @staticmethod
    def test_connections_to_json(nyc_to_boston: Connection, nyc_to_dc: Connection):
        assert ConnectionsTranslation.connections_to_json(
            {nyc_to_boston, nyc_to_dc}) == {'boston': {'nyc': {'green': 3}},
                                            'dc': {'nyc': {'blue': 3}}}

    @staticmethod
    def test_json_to_connections(nyc_to_boston: Connection, nyc_to_dc: Connection):
        cities = nyc_to_boston.get_cities().union(nyc_to_dc.get_cities())
        assert ConnectionsTranslation.json_to_connections(
            {'boston': {'nyc': {'green': 3}},
             'dc': {'nyc': {'blue': 3}}}
        ) != {nyc_to_dc, nyc_to_boston}
        assert ConnectionsTranslation.json_to_connections(
            {'boston': {'nyc': {'green': 3}},
             'dc': {'nyc': {'blue': 3}}},
            cities=cities
        ) == {nyc_to_dc, nyc_to_boston}

    # TODO test map JSON
