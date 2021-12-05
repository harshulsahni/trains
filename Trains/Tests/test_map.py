import pytest

from Trains.Common.map import City, Color, Destination


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


