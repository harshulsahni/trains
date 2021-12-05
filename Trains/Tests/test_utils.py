from Trains.Common.map import City, sort_cities


class TestSortCities:
    @staticmethod
    def test_sort_cities_empty():
        assert sort_cities([]) == []
        assert sort_cities({}) == []

    @staticmethod
    def test_sort_cities_basic(nyc: City, boston: City, la: City):
        sorted_cities = [boston, la, nyc]
        assert sort_cities([nyc, boston, la]) == sorted_cities
        assert sort_cities({nyc, boston, la}) == sorted_cities
