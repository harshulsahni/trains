import pytest

from Trains.Common.map import City, Color, Connection, Destination, Map


class TestColor:
    @staticmethod
    def test_color_to_enum():
        for color_enum in [Color.RED, Color.BLUE, Color.WHITE, Color.GREEN]:
            assert Color.string_to_color(color_enum.value) == color_enum


class TestCity:
    @staticmethod
    def test_invalid_city():
        with pytest.raises(ValueError):
            City("_)(*&^%$", 0, 0)
        with pytest.raises(ValueError):
            City("bostonbostonbostonbostonbostonbostonbostonbostonboston", 100, 100)
        with pytest.raises(ValueError):
            City(1, 100, 100)
        with pytest.raises(ValueError):
            City("boston", 'a', 100)
        with pytest.raises(ValueError):
            City("boston", 100, 'a')

    @staticmethod
    def test_getters():
        boston = City("boston", 100, 200)
        assert boston.get_name() == "boston"
        assert boston.get_x() == 100
        assert boston.get_y() == 200

    @staticmethod
    def test_equality():
        boston = City("boston", 130, 140)
        assert boston == City("boston", 130, 140)
        assert boston != City("boston", 130, 141)
        assert boston != City("boson", 130, 141)
        assert boston != City("boston", 131, 140)
        assert boston != 1

    @staticmethod
    def test_repr():
        assert City("boston", 0, 1).__repr__() == "City boston at (0, 1)"


class TestDestination:
    @staticmethod
    def test_bad_destinations(boston: City, nyc: City, la: City):
        with pytest.raises(ValueError):
            Destination({1, boston})

        with pytest.raises(ValueError):
            Destination(boston)

        with pytest.raises(ValueError):
            Destination({boston, nyc, la})

    @staticmethod
    def test_getters(boston: City, nyc: City):
        cities = {nyc, boston}
        assert Destination(cities).get_cities() == cities

    @staticmethod
    def test_equality(boston: City, nyc: City):
        assert Destination({boston, nyc}) == Destination({boston, nyc})

    @staticmethod
    def test_repr(nyc, boston):
        assert Destination({nyc, boston}).__repr__() == "Destination from boston to nyc"


class TestConnection:
    @staticmethod
    def test_bad_connections(boston: City, la: City):
        with pytest.raises(ValueError):
            Connection({boston, la}, length=3, color=1)
        with pytest.raises(ValueError):
            Connection({boston}, length=6, color=Color.RED)
        with pytest.raises(ValueError):
            Connection({boston}, length=3, color=Color.RED)
        with pytest.raises(ValueError):
            Connection([boston, la], length=3, color=Color.GREEN)
        with pytest.raises(ValueError):
            Connection(1, length=3, color=Color.GREEN)

    @staticmethod
    def test_getters(boston, la):
        c = Connection({boston, la}, length=3, color=Color.RED)
        assert c.get_cities() == {boston, la}
        assert c.get_color() == Color.RED
        assert c.get_length() == 3

    @staticmethod
    def test_equality(boston, la, nyc):
        c = Connection({boston, la}, length=3, color=Color.RED)

        assert c == Connection({boston, la}, length=3, color=Color.RED)
        assert c != Connection({boston, la}, length=4, color=Color.RED)
        assert c != Connection({boston, la}, length=3, color=Color.GREEN)
        assert c != Connection({boston, nyc}, length=3, color=Color.RED)


class TestMap:
    @staticmethod
    def test_bad_maps(la_island_map: Map):
        with pytest.raises(ValueError):
            Map(
                la_island_map.get_cities(),
                la_island_map.get_connections(),
                height=800,
                width=801
            )
        with pytest.raises(ValueError):
            Map(
                la_island_map.get_cities(),
                la_island_map.get_connections(),
                height=9,
                width=700
            )
        with pytest.raises(ValueError):
            Map(
                1,
                la_island_map.get_connections(),
                height=800,
                width=10
            )
        with pytest.raises(ValueError):
            Map(
                set(),
                la_island_map.get_connections(),
                height=800,
                width=801
            )
        with pytest.raises(ValueError):
            Map(
                {"boston", "la"},
                la_island_map.get_connections(),
                height=800,
                width=801
            )

    @staticmethod
    def test_getters(
        la_island_map: Map,
        nyc_to_dc: Connection,
        nyc_to_boston: Connection,
        nyc: City,
        boston: City,
        la: City,
        dc: City
    ):
        dests = {
            Destination({nyc, boston}),
            Destination({nyc, dc}),
            Destination({dc, boston})
        }
        city_names = {
            "boston", "nyc", "la", "dc"
        }
        assert la_island_map.get_width() == 800
        assert la_island_map.get_height() == 700
        assert la_island_map.get_connections() == {nyc_to_boston, nyc_to_dc}
        assert la_island_map.get_cities() == {nyc, boston, la, dc}
        assert la_island_map.get_destinations() == dests
        assert la_island_map.get_city_names() == city_names
