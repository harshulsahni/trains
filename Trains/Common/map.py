import re
from enum import Enum
from typing import Optional, Set, Tuple, Any, Iterable, List


class Color(Enum):
    """
    Represents the colors in the board game.
    """

    RED = "red"
    GREEN = "green"
    BLUE = "blue"
    WHITE = "white"

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

    def __eq__(self, other: Any):
        if not isinstance(other, Destination):
            return False
        return (
            self.__cities == other.__cities
        )

    def __repr__(self) -> str:
        sorted_cities = sort_cities(self.__cities)
        from_city = sorted_cities[0]
        to_city = sorted_cities[1]

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
