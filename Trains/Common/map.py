import re
from collections import defaultdict
from enum import Enum
from typing import Optional, Set, Tuple, Any, Iterable, List, Dict

from Trains.Common.constants import CONNECTION, MAP
from Trains.Utils.utils import bfs


class Color(Enum):
    """
    Represents the colors in the board game.
    """

    RED = "red"
    GREEN = "green"
    BLUE = "blue"
    WHITE = "white"

    @staticmethod
    def get_all_color_enums() -> Set["Color"]:
        """
        Get the enum of every possible Color in the game.
        """
        return {Color.RED, Color.GREEN, Color.BLUE, Color.WHITE}

    def get_hex(self) -> Optional[str]:
        """
        Returns a hex representation of the color, as a str.
        Color.NULL is yellow.
        Returns None the color is not defined in this mapping yet.
        """
        color_map = {
            Color.GREEN: "#00FF00",
            Color.BLUE: "#4974ff",
            Color.RED: "#ff4949",
            Color.WHITE: "#ffffff",
        }
        return color_map.get(self)

    @staticmethod
    def string_to_color(s: str) -> Optional["Color"]:
        """
        Returns the proper enumeration given the string representation for the desired color.
        Returns None if no such color is defined.

        :param s: String representation of desired color.

        :return: Desired enumeration of color.
        """
        color_map = {
            "red": Color.RED,
            "green": Color.GREEN,
            "blue": Color.BLUE,
            "white": Color.WHITE,
        }
        return color_map.get(s.lower())


class City:
    """
    Represents a city in the game.
    City.x, City.y represents the location of the city on the map, in pixels.
    If the City's coordinates are bigger than what the Map class allows, then a new city with updated coordinates
    will have to be made.
    City.name represents the name of the City.
    """

    def __init__(self, name: str, x: int, y: int):
        """
        Creates a City class with given name and (x, y) position.
        (x, y) can be any combination of integers, but if this City will be used in a Map,
        then the Map will validate that this City is within its bounds.
        """
        self.__name = self.__validate_name(name)
        self.__x, self.__y = self.__validate_coords(x, y)

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, City):
            return False

        return (
            self.__name == other.__name
            and self.__x == other.__x
            and self.__y == other.__y
        )

    def __hash__(self) -> int:
        return hash(self.__repr__())

    def __repr__(self) -> str:
        return f"City {self.__name} at ({self.__x}, {self.__y})"

    @staticmethod
    def __validate_name(name: str):
        """
        Ensures the name of the city only contains letters and numbers, along with spaces, commas,
        and/or periods.
        Also ensures the length of the name is, at maximum, 25.

        :param name: City name to validate.

        :return: City name iff city name fits all the requirements.
        """
        regex = re.compile("^[a-zA-Z0-9 .,]+$")
        if not isinstance(name, str):
            raise ValueError("City name must be str")
        if len(name) <= 25 and regex.match(name):
            return name
        raise ValueError(
            "City name must be at least 25 characters and must match regex "
            "pattern " + r"[a-zA-Z0-9 .,]+"
        )

    @staticmethod
    def __validate_coords(x: int, y: int) -> Tuple[int, int]:
        if not (
            isinstance(x, int)
            and isinstance(y, int)
        ):
            raise ValueError("x and y must both be integers.")
        return x, y

    def get_name(self) -> str:
        """
        Gets the name of the city.

        :return: The city's name.
        """
        return self.__name

    def get_x(self) -> int:
        """
        Gets the x-coordinate value for the City.

        :return: an int representing the x coordinate value.
        """
        return self.__x

    def get_y(self) -> int:
        """
        Gets the y-coordinate value for the City.

        :return: an int representing the y coordinate value.
        """
        return self.__y

    def copy(self) -> "City":
        """
        Returns a copy of a City.
        """
        return City(self.__name, self.__x, self.__y)


def sort_cities(cities: Iterable[City]) -> List[City]:
    """
    Sort cities based on name; uses Racket predicate string<?.
    """
    return sorted(cities, key=lambda city: city.get_name())


class Destination:
    """
    Represents a Destination in the game, Trains.
    """
    def __init__(self, cities: Set[City]):
        self.__cities = self.__validate_cities(cities)

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, Destination):
            return False
        return (
            self.__cities == other.__cities
        )

    def __hash__(self) -> int:
        from_city, to_city = sort_cities(self.__cities)
        return hash(f"Destination from {from_city.__repr__()} to {to_city.__repr__()}")

    def __repr__(self) -> str:
        from_city, to_city = sort_cities(self.__cities)
        return f"Destination from {from_city.get_name()} to {to_city.get_name()}"

    @staticmethod
    def __validate_cities(cities: Set[City]) -> Set[City]:
        e = ValueError("Cities supplied must be a set of two City.")
        if not (isinstance(cities, set) and len(cities) == 2):
            raise e
        for city in cities:
            if not isinstance(city, City):
                raise e
        return cities

    def get_cities(self) -> Set[City]:
        """
        Return a set of both cities in this Destination.
        :return:
        """
        return set([c.copy() for c in self.__cities])

    def copy(self) -> "Destination":
        """
        Returns a deep copy of this Destination.
        """
        return Destination(self.get_cities())


class Connection:
    """
    Represents a Connection in the game, Trains.
    Each connection has a pair of cities, some length, and some color.
    """
    def __init__(
        self,
        cities: Set[City],
        *,
        length: int,
        color: Color
    ):
        self.__cities = cities
        self.__length = length
        self.__color = color
        self.__validate_connection()

    def __eq__(self, other: Any) -> bool:
        """
        Determines whether this Connection is equal to another.
        """
        if not isinstance(other, Connection):
            return False
        return (
            self.__cities == other.__cities
            and self.__length == other.__length
            and self.__color == other.__color
        )

    def __hash__(self) -> int:
        sorted_cities = sort_cities(self.__cities)
        from_city = sorted_cities[0]
        to_city = sorted_cities[1]
        color = self.__color.value
        representation = f"{from_city.__repr__()} -> {to_city.__repr__()} {color}, {self.__length}"
        return hash(representation)

    def __repr__(self) -> str:
        sorted_cities = sort_cities(self.__cities)
        from_city = sorted_cities[0].get_name()
        to_city = sorted_cities[1].get_name()
        color = self.__color.value
        return f"Connection from {from_city} to {to_city} ({color}, {self.__length})"

    def __validate_connection(self) -> None:
        """
        Ensures each Connection is well-formed.
        Checks whether the Connection has a pair of cities as a set,
        whether the color is an enumeration,
        and whether the length is within the acceptable lengths as defined in the constants file.
        """
        cities_error = ValueError("Cities provided must be a set of City.")
        if not (isinstance(self.__cities, set) and len(self.__cities) == 2):
            raise cities_error
        for city in self.__cities:
            if not isinstance(city, City):
                raise cities_error
        if not (isinstance(self.__length, int) and self.__length in CONNECTION.LENGTHS):
            raise ValueError(f"Connection length must be in: {CONNECTION.LENGTHS}")
        if not isinstance(self.__color, Color):
            raise ValueError(f"Connection color must be enum Color.")

    def get_cities(self) -> Set[City]:
        """
        Returns a deep copy of the cities in this connection.
        """
        return set([c.copy() for c in self.__cities])

    def get_length(self) -> int:
        """
        Returns the length of this Connection.
        """
        return self.__length

    def get_color(self) -> Color:
        """
        Returns the color of this connection.
        """
        return self.__color

    def copy(self) -> "Connection":
        cities = set([c.copy() for c in self.__cities])
        return Connection(cities, length=self.__length, color=self.__color)


class Map:
    def __init__(
        self,
        cities: Set[City],
        connections: Set[Connection],
        *,
        height: int = MAP.MAX_HEIGHT,
        width: int = MAP.MAX_WIDTH,
    ):
        self.__height, self.__width = self.__validate_height_width(height, width)
        self.__cities = self.__validate_cities(cities)
        self.__connections = self.__validate_connections(connections)
        self.__destinations = self.__calculate_all_destinations()

    @staticmethod
    def __validate_height_width(height: int, width: int) -> Tuple[int, int]:
        """
        Ensures heights and widths are within the max and min allowed.
        """
        if (
            isinstance(height, int)
            and isinstance(width, int)
            and MAP.MIN_WIDTH <= width <= MAP.MAX_WIDTH
            and MAP.MIN_HEIGHT <= height <= MAP.MAX_HEIGHT
        ):
            return height, width
        else:
            raise ValueError(f"Height must be an int between {MAP.MIN_HEIGHT} and {MAP.MAX_HEIGHT}. \n"
                             f"Width must be an int between {MAP.MIN_WIDTH} and {MAP.MAX_WIDTH}. ")

    def __validate_cities(self, cities: Set[City]) -> Set[City]:
        """
        Ensures all cities have unique names and coordinates, and all coordinates are within the bounds of the map.
        """
        cities_error = ValueError(f"Cities must be a set of City.")
        city_names = set()
        city_coord_map = defaultdict(set)

        if not isinstance(cities, set):
            raise cities_error
        for city in cities:
            if not isinstance(city, City):
                raise cities_error
            if not (0 <= city.get_x() <= self.__width):
                raise ValueError("City must have x coord between 0 and map width.")
            if not (0 <= city.get_y() <= self.__height):
                raise ValueError("City must have y coord between 0 and map height.")
            city_name = city.get_name()
            city_x = city.get_x()
            city_y = city.get_y()
            if city_name in city_names:
                raise ValueError(f"No duplicate city names ({city_name}).")
            else:
                city_names.add(city_name)
            if city_x in city_coord_map:
                if city_y in city_coord_map[city_x]:
                    raise ValueError(f"Two cities can't have the same coordinates of ({city_x}, {city_y}).")
                else:
                    city_coord_map[city_x].add(city_y)
            else:
                city_coord_map[city_x] = {city_y}

        return cities

    def __validate_connections(self, connections: Set[Connection]) -> Set[Connection]:
        """
        Ensures each city in the connections are already defined in the map's cities.
        """
        connection_error = ValueError("Connections supplied must be a set of Connection.")
        if not isinstance(connections, set):
            raise connection_error
        for connection in connections:
            if not isinstance(connection, Connection):
                raise connection_error
            cities = connection.get_cities()
            for city in cities:
                if city not in self.__cities:
                    raise ValueError("Cities in connections must be specified in the cities of the Map.")
        return connections

    def get_cities(self) -> Set[City]:
        """
        Gets all of the cities in this game map.
        """
        return set([c.copy() for c in self.__cities])

    def get_connections(self) -> Set[Connection]:
        """
        Gets all of the connections in this game map.
        """
        return set([c.copy() for c in self.__connections])

    def get_height(self) -> int:
        """
        Gets this map's height.
        """
        return self.__height

    def get_width(self) -> int:
        """
        Gets this map's width.
        """
        return self.__width

    def get_city_names(self) -> Set[str]:
        """
        Getter for all city names (set of strings).
        """
        return set([c.get_name() for c in self.__cities])

    def __calculate_all_destinations(self) -> Set[Destination]:
        """
        Uses the city mapping and BFS to find all possible Destinations in this game map.
        """
        destinations = set()
        cities = self.__cities
        city_map = self.__make_city_map()

        for city in cities:
            all_cities_reachable_from_city = bfs(city, city_map)
            for city_neighbor in all_cities_reachable_from_city:
                if city_neighbor != city:
                    destinations.add(Destination({city, city_neighbor}))
        return destinations

    def __make_city_map(self) -> Dict[City, Set[City]]:
        """
        Make a mapping between every city and the set of cities directly reachable from this city.
        Directly reachable from city1 to city2: there exists a Connection between city1 and city2 (or vice-versa).
        """
        city_map = defaultdict(set)
        for connection in self.__connections:
            city1, city2 = connection.get_cities()
            city_map[city1].add(city2)
            city_map[city2].add(city1)
        return city_map

    def get_destinations(self) -> Set[Destination]:
        """
        Returns all destinations from this map.
        A destination, in this context, is a pair of cities.
        """
        return set([d.copy() for d in self.__destinations])

    def copy(self) -> "Map":
        """
        Return a deep copy of this Map.
        """
        cities = set([c.copy() for c in self.__cities])
        conns = set([c.copy() for c in self.__connections])
        return Map(cities, conns, height=self.__height, width=self.__width)
