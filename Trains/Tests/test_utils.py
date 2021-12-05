from Trains.Common.map import City, sort_cities
from Trains.Utils.utils import bfs


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


class TestBFS:
    @staticmethod
    def test_bfs_empty():
        assert bfs("c1", dict()) == {"c1"}

    @staticmethod
    def test_bfs_1_neighbor():
        assert bfs("c1", {"c1": {"c2"},
                          "c2": {"c1"}}
                   ) == {"c1", "c2"}

    @staticmethod
    def test_bfs_some_cities_not_in_map():
        result = bfs("c1", {"c1": {"c2"}})
        expected = {"c1", "c2"}
        assert result == expected

    @staticmethod
    def test_bfs_show_directed_graph_assumption():
        # you can go from 3 -> 1, but NOT the other way around. so, since the root is 1,
        # 3 won't show up in the final output
        root = 1
        mapping = {
            1: {2},
            2: {1, 6},
            3: {1, 4},
            100: {},
            101: {102, 103, 104},
        }
        if_undirected_expected = {1, 2, 6, 3}
        directed_expected = {1, 2, 6}
        result = bfs(root, mapping)
        assert result != if_undirected_expected
        assert result == directed_expected
