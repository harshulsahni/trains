from typing import Dict, Union, List, Any, Set, Optional

# from Trains.Admin.board_state import BoardState
# from Trains.Admin.private_player_info import PrivatePlayerInfo
# from Trains.Admin.private_player_info import card_counter_from_dict
from Trains.Common.map import City, Connection, Destination, Map, Color, sort_cities

# from Trains.Common.player_game_state import PlayerGameState
# from Trains.Player.turn_type import TakeTurn, ActionType

WIDTH = "width"
HEIGHT = "height"
CITIES = "cities"
CONNECTIONS = "connections"
MORE_CARDS = "more cards"
ACTION = "action"
ACQUIRED = "acquired"
DEST1 = "destination1"
DEST2 = "destination2"
RAILS = "rails"
CARDS = "cards"
THIS = "this"


class CityTranslation:
    @staticmethod
    def is_city_json_valid(city_as_json: Any) -> bool:
        """
        Determines whether the JSON representation of a City is valid.
        Returns True if json looks like this: [str, [int, int]].
        """
        return (
            isinstance(city_as_json, list)
            and len(city_as_json) == 2
            and isinstance(city_as_json[0], str)
            and isinstance(city_as_json[1], list)
            and len(city_as_json[1]) == 2
            and isinstance(city_as_json[1][0], int)
            and isinstance(city_as_json[1][1], int)
        )

    @staticmethod
    def city_to_json(city: City) -> List[Union[str, List[int]]]:
        """
        Turns City into JSON representation of a City.
        """
        if not isinstance(city, City):
            raise ValueError("Input is not of City type.")
        return [city.get_name(), [city.get_x(), city.get_y()]]

    @staticmethod
    def json_to_city(city_as_json: List[Union[str, List[int]]]) -> City:
        """
        Turns a JSON representation of a City into a City.
        Errors out if the JSON is not valid.
        """
        if not CityTranslation.is_city_json_valid(city_as_json):
            raise ValueError("Invalid JSON representation for a city supplied")
        name, (x, y) = city_as_json
        return City(name, x, y)

    @staticmethod
    def find_city_from_str(city_name: str, cities: Set[City]) -> Optional[City]:
        """
        Given a set of City, returns the City with the same name as the input string.
        Returns None if the City is not found.
        """
        for city in cities:
            if city.get_name() == city_name:
                return city
        return None


class ConnectionsTranslation:
    @staticmethod
    def is_acquired_valid(acquired_json: Any) -> bool:
        return (
            len(acquired_json) == 4
            and isinstance(acquired_json[0], str)
            and isinstance(acquired_json[1], str)
            and acquired_json[0] < acquired_json[1]
            and isinstance(acquired_json[2], str)
            and Color.string_to_color(acquired_json[2]) is not None
            and isinstance(acquired_json[3], int)
        )

    @staticmethod
    def are_connections_valid(connections: Any) -> bool:
        """
        Determines whether all connections, represented as JSON, are valid.
        JSON must be of form:
        {
            str: {
                str: {
                    str: int
                }
            }
        }
        where the first two strs represent city names (and must be string<?), and the third str represents a Color.
        the int represents the connection length.
        Both color and length must be valid, as well.
        """
        if not isinstance(connections, dict):
            return False
        for first_connection_name, second_connection_map in connections.items():
            if not (isinstance(first_connection_name, str) and isinstance(second_connection_map, dict)):
                return False
            for second_connection_name, color_length_map in second_connection_map.items():
                if not (
                    isinstance(second_connection_name, str)
                    and isinstance(color_length_map, dict)
                    and first_connection_name < second_connection_name
                ):
                    return False
                for color, length in color_length_map.items():
                    if not (
                        isinstance(color, str)
                        and Color.color_to_enum(color) is not None
                    ):
                        return False
        return True

    @staticmethod
    def connection_to_json(connection: Connection) -> Dict[str, Dict[str, Dict[str, int]]]:
        """
        Turns a Connection into the JSON representation for a Connection.
        """
        if not isinstance(connection, Connection):
            raise ValueError("Input is not of Connection type")

        color = connection.get_color().value
        length = connection.get_length()
        c1, c2 = sort_cities(connection.get_cities())
        return {
            c1.get_name(): {
                c2.get_name(): {
                    color: length
                }
            }
        }

    @staticmethod
    def acquired_to_json(connection: Connection) -> List[Union[str, int]]:
        if not isinstance(connection, Connection):
            raise ValueError("Input is not of type Connection")
        city1, city2 = sort_cities(connection.get_cities())
        c1 = city1.get_name()
        c2 = city2.get_name()
        color = connection.get_color().value
        length = connection.get_length()

        return [c1, c2, color, length]

    @staticmethod
    def json_to_acquired(
        connection_as_json: List[Union[str, int]],
        cities: Optional[Set[City]] = None
    ) -> Connection:
        cities = cities if cities else set()

        if not ConnectionsTranslation.is_acquired_valid(connection_as_json):
            raise ValueError("Invalid JSON representation for an acquired Connection supplied")

        c1_name, c2_name, color_name, length = connection_as_json
        c1_from_cities = CityTranslation.find_city_from_str(c1_name, cities)
        c1 = c1_from_cities if c1_from_cities else City(c1_name, 0, 0)

        c2_from_cities = CityTranslation.find_city_from_str(c2_name, cities)
        c2 = c2_from_cities if c2_from_cities else City(c2_name, 0, 0)

        return Connection(c1, c2, SegmentLength.length_to_enum(length), Color.color_to_enum(color_name))

    @staticmethod
    # TODO: DOESN'T WORK WITH 1 CITY HAVING MULTIPLE CONNECTIONS
    def connections_to_json(connections: Set[Connection]) -> Dict[str, Dict[str, Dict[str, int]]]:
        """
        Turns a set of connections into the JSON representation for Connections.
        """
        output = {}
        if not isinstance(connections, set):
            raise TypeError("not given a set of connections")
        for connection in connections:
            if not isinstance(connection, Connection):
                raise TypeError("not given a set of connections")
            c1 = connection.city_1.name
            c2 = connection.city_2.name
            color = connection.color.value
            length = connection.num_rails.value

            if c1 in output:
                if c2 in output[c1]:
                    output[c1][c2][color] = length
                else:
                    output[c1][c2] = {color: length}
            else:
                output[c1] = {c2: {color: length}}

        return output

    @staticmethod
    def json_to_connections(
        connections_as_json: Dict[str, Dict[str, Dict[str, int]]],
        cities: Optional[Set[City]] = None
    ) -> Set[Connection]:
        """
        Given a JSON representation for Connections, this function outputs a set of Connection.

        Optionally, the user can specify a set of City for the function to use if the user wishes to have accurate
        City coordinates. If not specified, then each city will be at (0, 0).
        """
        cities = cities if cities else set()
        output = set()

        if not ConnectionsTranslation.are_connections_valid(connections_as_json):
            raise ValueError("Invalid JSON representation for connections supplied.")

        for city1_name, city2_map in connections_as_json.items():
            city1_from_cities = CityTranslation.find_city_from_str(city1_name, cities)
            city1 = city1_from_cities if city1_from_cities else City(city1_name, 0, 0)

            for city2_name, color_length_map in city2_map.items():
                city2_from_cities = CityTranslation.find_city_from_str(city2_name, cities)
                city2 = city2_from_cities if city2_from_cities else City(city2_name, 0, 0)

                for color_name, length in color_length_map.items():
                    color = Color.color_to_enum(color_name)
                    num_rails = SegmentLength.length_to_enum(length)
                    output.add(Connection(city1, city2, num_rails, color))

        return output


class MapTranslation:
    @staticmethod
    def is_map_json_valid(map_as_json: Any) -> bool:
        """
        Determines whether the JSON representation of a Map is valid.
        Map must be a mapping of four things:
            cities -> list of City
            connections -> mapping of all connections
            height -> integer representing height
            width -> integer representing width
        """
        is_map_dict = isinstance(map_as_json, dict)
        is_width_valid = WIDTH in map_as_json and isinstance(map_as_json.get(WIDTH), int)
        is_height_valid = HEIGHT in map_as_json and isinstance(map_as_json.get(HEIGHT), int)
        are_cities_valid = CITIES in map_as_json and isinstance(map_as_json.get(CITIES), list)
        are_connections_valid = CONNECTIONS in map_as_json and isinstance(map_as_json.get(CONNECTIONS), dict)
        return (
            is_map_dict
            and is_width_valid
            and is_height_valid
            and are_cities_valid
            and are_connections_valid
        )

    @staticmethod
    def map_to_json(trains_map: Map) -> Dict[str, Union[int, List[City], Dict[str, Dict[str, Dict[Color, int]]]]]:
        """
        Turns a Map into its JSON representation.
        """
        if not isinstance(trains_map, Map):
            raise ValueError("Input is not of Map type.")
        width = trains_map.get_width()
        height = trains_map.get_height()
        cities = sorted([CityTranslation.city_to_json(c) for c in trains_map.get_cities()])
        connections = ConnectionsTranslation.connections_to_json(trains_map.get_connections())

        return {
            WIDTH: width,
            HEIGHT: height,
            CITIES: cities,
            CONNECTIONS: connections
        }

    @staticmethod
    def json_to_map(map_as_json: Dict[str, Union[int, List[str], Dict[str, Dict[str, Dict[str, int]]]]]) -> TrainsMap:
        """
        Takes the JSON representation of a TrainsMap and turns it into a TrainsMap.
        Errors out if the JSON is not valid for a TrainsMap.
        """
        if not MapTranslation.is_map_json_valid(map_as_json):
            raise ValueError("Invalid JSON representation for a game map supplied.")
        width = map_as_json[WIDTH]
        height = map_as_json[HEIGHT]
        cities = set([CityTranslation.json_to_city(c) for c in map_as_json[CITIES]])
        connections = ConnectionsTranslation.json_to_connections(map_as_json[CONNECTIONS], cities)
        return TrainsMap(cities, connections, width, height)


class DestinationTranslation:
    @staticmethod
    def is_destination_json_valid(dest_as_json: Any) -> bool:
        """
        Determines whether the JSON representation for a Destination is valid.
        Destinations must look like: [str, str]
        where both strs represent city names, and the first str must be less than the second.
        """
        return (
            isinstance(dest_as_json, list)
            and len(dest_as_json) == 2
            and isinstance(dest_as_json[0], str)
            and isinstance(dest_as_json[1], str)
            and dest_as_json[0] < dest_as_json[1]
        )

    @staticmethod
    def destination_to_json(destination: Destination) -> List[str]:
        """
        Turns a Destination into its JSON form.
        """
        if not isinstance(destination, Destination):
            raise ValueError("Input is not destination type.")
        sorted_cities = sorted([destination.city_1, destination.city_2], key=lambda c: c.name)
        return [sorted_cities[0].name, sorted_cities[1].name]

    @staticmethod
    def json_to_destination(
        destination_as_json: List[str],
        cities: Optional[Set[City]] = None
    ) -> Destination:
        """
        Turns a JSON representation of a Destination into a Destination.
        Errors if the JSON is invalid.

        Optionally, the user can specify a set of cities so that the cities in the Destination have correct coords.
        If not specified, then the cities will all be at location (0, 0).
        """
        cities = cities if cities else set()

        if not DestinationTranslation.is_destination_json_valid(destination_as_json):
            raise ValueError("Invalid JSON representation for a destination supplied.")

        city1_from_cities = CityTranslation.find_city_from_str(destination_as_json[0], cities)
        city1 = city1_from_cities if city1_from_cities else City(destination_as_json[0], 0, 0)

        city2_from_cities = CityTranslation.find_city_from_str(destination_as_json[1], cities)
        city2 = city2_from_cities if city2_from_cities else City(destination_as_json[1], 0, 0)

        return Destination(city1, city2)


# class PlayerStateTranslation:
#     @staticmethod
#     def are_cards_json_valid(cards_json: Any) -> bool:
#         """
#         Checks whether the JSON representation for cards are a mapping between Color and natural number.
#         Also checks whether the only colors used are the ones in the enumeration.
#         """
#         if not isinstance(cards_json, dict):
#             return False
#         for color, count in cards_json.items():
#             if Color.color_to_enum(color) is None:
#                 return False
#             if not (isinstance(count, int) and count >= 0):
#                 return False
#         return True
#
#     @staticmethod
#     def are_this_player_acquired_json_valid(this_player_acquired: Any) -> bool:
#         """
#         Check whether the JSON representation for a list of acquired connections is valid.
#         Must be of form:
#         [
#             [str, str, str, int]
#         ]
#         """
#         if not isinstance(this_player_acquired, list):
#             return False
#         for connection_as_json in this_player_acquired:
#             if not ConnectionsTranslation.is_acquired_valid(connection_as_json):
#                 return False
#         return True
#
#     @staticmethod
#     def is_this_player_json_valid(this_player_json: Any) -> bool:
#         """
#         Checks whether "this" in the JSON representation of PlayerState is valid.
#         Checks for all keys for destinations, num_rails, cards, and acquired connections and checks each value
#             accordingly.
#         """
#         return (
#             isinstance(this_player_json, dict)
#             and DEST1 in this_player_json
#             and DestinationTranslation.is_destination_json_valid(this_player_json[DEST1])
#             and DEST2 in this_player_json
#             and DestinationTranslation.is_destination_json_valid(this_player_json[DEST2])
#             and RAILS in this_player_json
#             and isinstance(this_player_json[RAILS], int)
#             and CARDS in this_player_json
#             and PlayerStateTranslation.are_cards_json_valid(this_player_json[CARDS])
#             and ACQUIRED in this_player_json
#             and PlayerStateTranslation.are_this_player_acquired_json_valid(this_player_json[ACQUIRED])
#         )
#
#     @staticmethod
#     def is_all_acquired_json_valid(all_acquired_connections_json: Any) -> bool:
#         """
#         Checks whether the JSON representation of ALL of the acquired connections (for all player, in order of their
#         turn) is valid.
#         """
#         for player_acquired_connections_json in all_acquired_connections_json:
#             if not PlayerStateTranslation.are_this_player_acquired_json_valid(player_acquired_connections_json):
#                 return False
#         return True
#
#     @staticmethod
#     def is_player_state_json_valid(pgs_as_json: Any) -> bool:
#         """
#         Checks whether the JSON representation for the PlayerState is valid. Checks both "this" player and all
#         "acquired" connections.
#         """
#
#         return (
#             isinstance(pgs_as_json, dict)
#             and THIS in pgs_as_json
#             and ACQUIRED in pgs_as_json
#             and PlayerStateTranslation.is_this_player_json_valid(pgs_as_json[THIS])
#             and PlayerStateTranslation.is_all_acquired_json_valid(pgs_as_json[ACQUIRED])
#         )
#
#     @staticmethod
#     def player_state_to_this_player_json(pgs: PlayerGameState, player_idx: int) -> Dict[str, Any]:
#         """
#         Turns a PlayerGameState into the JSON representation for "this" player.
#         FLAW: Since the code does not support getting this player's connections without an index, we needed to include
#         the player index to get the player's connections.
#         """
#         if not (isinstance(pgs, PlayerGameState) and isinstance(player_idx, int)):
#             raise ValueError("Inputs are not of types PlayerGameState and int.")
#
#         num_rails = pgs.get_num_rails()
#         cards = {k.value: v for k, v in pgs.get_cards_as_dict().items()}
#         acquired_conns = [
#             ConnectionsTranslation.acquired_to_json(c)
#             # ConnectionsTranslation.connections_to_json(c)
#             for c in pgs.get_acquired_connections_for_player(player_idx)
#         ]
#         destinations = [
#             DestinationTranslation.destination_to_json(destination)
#             for destination in sorted(pgs.get_destinations(), key=lambda d: (d.city_1.name, d.city_2.name))
#         ]
#         return {
#             DEST1: destinations[0],
#             DEST2: destinations[1],
#             RAILS: num_rails,
#             CARDS: cards,
#             ACQUIRED: acquired_conns
#         }
#
#     @staticmethod
#     def player_state_to_all_acquired_connections_json(pgs: PlayerGameState, num_players: int) -> List[List[List[Union[str, int]]]]:
#         """
#         Turns a PlayerGameState into a JSON representation of all the acquired connections for each player.
#         """
#         if not isinstance(pgs, PlayerGameState):
#             raise ValueError("Input is not of type PlayerGameState.")
#
#         output = []
#         all_acquired_connections = pgs.get_all_acquired_connections_in_order(num_players)
#         for connection_set in all_acquired_connections:
#             output.append([ConnectionsTranslation.acquired_to_json(acquired) for acquired in connection_set])
#         return output
#
#     @staticmethod
#     def player_state_to_json(
#         player_state: PlayerGameState,
#         player_idx: int,
#         num_players: int
#     ) -> Dict[str, Union[List[Dict[str, Any]], Dict[str, Any]]]:
#         """
#         Turns a PlayerGameState into its JSON representation.
#         """
#         if not isinstance(player_state, PlayerGameState):
#             raise ValueError("Input is not of PlayerGameState type.")
#         return {
#             THIS: PlayerStateTranslation.player_state_to_this_player_json(player_state, player_idx),
#             ACQUIRED: PlayerStateTranslation.player_state_to_all_acquired_connections_json(player_state, num_players)
#         }
#
#     @staticmethod
#     def make_connection_id_map_from_list_of_connections(
#         all_player_connections: List[List[Connection]]
#     ) -> Dict[Connection, int]:
#         """
#         Given a list of connections (in the order at which each player plays), make a mapping between each Connection
#         and the player_id that owns that Connection.
#         """
#         output = {}
#         for i, connections_for_player in enumerate(all_player_connections):
#             for connection in connections_for_player:
#                 output.update({connection: i})
#         return output
#
#     @staticmethod
#     def json_to_player_state(
#         player_state_as_json: Dict[str, Union[List[List[List[Union[str, int]]]], Dict[str, Any]]],
#         trains_map: TrainsMap,
#     ) -> PlayerGameState:
#         """
#         Takes the JSON representation of a PlayerGameState and turns it into PlayerState.
#         DESIGN DECISION: We decided to include the trains map in this function in order to provide it to the constructor
#         of the player game state.
#         """
#         if not PlayerStateTranslation.is_player_state_json_valid(player_state_as_json):
#             raise ValueError("Invalid JSON representation for a PlayerGameState supplied.")
#         cities = trains_map.get_cities()
#
#         all_connections_json = player_state_as_json[ACQUIRED]
#         all_connections = []
#         for player_connections in all_connections_json:
#             all_connections.append([ConnectionsTranslation.json_to_acquired(c, cities) for c in player_connections])
#         connection_to_id = PlayerStateTranslation.make_connection_id_map_from_list_of_connections(all_connections)
#
#         d1 = DestinationTranslation.json_to_destination(player_state_as_json[THIS][DEST1], cities)
#         d2 = DestinationTranslation.json_to_destination(player_state_as_json[THIS][DEST2], cities)
#         destinations = {d1, d2}
#
#         num_rails = player_state_as_json[THIS][RAILS]
#         cards = {Color.color_to_enum(color): num for color, num in player_state_as_json[THIS][CARDS].items()}
#
#         board_game_state = BoardState(trains_map, connection_to_id)
#         private_player_info = PrivatePlayerInfo(
#             cards_counter=card_counter_from_dict(cards),
#             destinations=destinations,
#             num_rails=num_rails
#         )
#         return PlayerGameState(board_game_state=board_game_state, player_info=private_player_info)
#
#
# class ActionTranslation:
#     @staticmethod
#     def is_action_valid(action_as_json: Any) -> bool:
#         """
#         Determines whether the JSON representation for a TakeTurn is valid.
#         Must be of form:
#         {"action": str}
#         OR
#         {"action": <acquired_as_JSON>}
#         """
#         if isinstance(action_as_json, dict) and ACTION in action_as_json:
#             if isinstance(action_as_json[ACTION], str):
#                 return action_as_json[ACTION] == MORE_CARDS
#             if isinstance(action_as_json[ACTION], list):
#                 return ConnectionsTranslation.is_acquired_valid(action_as_json[ACTION])
#         return False
#
#     @staticmethod
#     def action_to_json(action: TakeTurn) -> Dict[str, Union[str, List[Union[str, int]]]]:
#         """
#         Takes a TakeTurn action and turns it into a JSON representation
#         """
#         if not isinstance(action, TakeTurn):
#             raise ValueError("Input is not of TakeTurn type.")
#
#         if action.get_action_type() == ActionType.REQUEST_CARDS:
#             action_json = MORE_CARDS
#         else:
#             connection = action.get_connection()
#             c1_name = connection.city_1.name
#             c2_name = connection.city_2.name
#             color_name = connection.color.value
#             length = connection.num_rails.value
#
#             action_json = [c1_name, c2_name, color_name, length]
#         return {ACTION: action_json}
#
#     @staticmethod
#     def json_to_action(
#         action_as_json: Dict[str, Union[str, List[Union[str, int]]]],
#         cities: Optional[Set[City]] = None
#     ) -> TakeTurn:
#         """
#         Takes the JSON representation of an Action and turns it into a TakeTurn object.
#         """
#         if not ActionTranslation.is_action_valid(action_as_json):
#             raise ValueError("Invalid JSON representation for an action supplied.")
#         action = action_as_json[ACTION]
#         if isinstance(action, str):
#             return TakeTurn(ActionType.REQUEST_CARDS)
#         else:
#             connection = ConnectionsTranslation.json_to_acquired(action, cities)
#             return TakeTurn(ActionType.ACQUIRE_CONNECTION, connection=connection)
