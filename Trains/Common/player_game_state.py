from collections import Set
from typing import Dict, List

from Trains.Common.constants import GAME
from Trains.Common.map import Connection, Destination, Color, Map


class PlayerGameState:
    def __init__(
        self,
        *,
        acquired_connections: Set[Connection],
        destinations: Set[Destination],
        num_rails: int,
        cards: Dict[Color: int],
        total_acquired_connections: List[Set[Connection]]
    ):
        """
        Represents the state of the game of this player.

        :param acquired_connections: This player's connections so far.
        :param destinations: This player's destinations, to be held constant throughout the game.
        :param num_rails: The number of rails this player currently has.
        :param cards: Colors mapped to integers indicating this player's cards.
        :param total_acquired_connections: A list of sets of acquired connections. The list is in order of the players
        playing.

        ASSUMPTION: This assumes that the length of the total_acquired_connections is the same as the number of players.
        Therefore, if a player does not have connections, this assumes that there will be an empty set in this list.
        """
        self.__acquired_connections = self.__validate_acquired_connections(acquired_connections)
        self.__destinations = self.__validate_destinations(destinations)
        self.__num_rails = self.__validate_num_rails(num_rails)
        self.__cards = self.__put_all_colors_in_cards(self.__validate_cards(cards))
        self.__total_acquired_connections = self.__validate_total_acquired_connections(total_acquired_connections)
        self.__num_players = len(total_acquired_connections)
        self.__index = self.__get_this_player_index()

    @staticmethod
    def __validate_acquired_connections(acquired_connections: Set[Connection]):
        """
        Ensures connections must be a set of Connection.
        """
        acquired_error = ValueError("This player's acquired connections must be a set of Connection.")
        if not isinstance(acquired_connections, set):
            raise acquired_error
        for c in acquired_connections:
            if not isinstance(c, Connection):
                raise acquired_error
        return acquired_connections

    @staticmethod
    def __validate_destinations(destinations: Set[Destination]) -> Set[Destination]:
        """
        Ensures a pair of destinations for this player.
        """
        num_dests_per_player = GAME.NUM_DESTINATIONS_PER_PLAYER
        dest_error = ValueError(f"This player's destinations must be a set of {num_dests_per_player} Destination.")
        if not (
            isinstance(destinations, set)
            and len(destinations) == num_dests_per_player
        ):
            raise dest_error
        for d in destinations:
            if not isinstance(d, Destination):
                raise dest_error
        return destinations

    @staticmethod
    def __validate_num_rails(rails: int) -> int:
        """
        Ensures that rails represent an integer greater than 0.
        """
        if not (
            isinstance(rails, int)
            and rails >= 0
        ):
            raise ValueError("This player's number of rails must be a non-negative integer.")
        return rails

    @staticmethod
    def __validate_cards(cards: Dict[Color, int]) -> Dict[Color, int]:
        """
        Ensures all cards are a mapping of Color to count.
        Each count can't be higher than the total number of cards the referee starts with.
        The total count can't be higher than this either.
        """
        cards_error = ValueError("Cards must be a mapping between Color enum and integer.")
        total_cards = 0

        if not isinstance(cards, dict):
            raise cards_error
        for color, count in cards.items():
            if not (
                isinstance(color, Color)
                and isinstance(count, int)
                and 0 <= count <= GAME.NUM_TOTAL_CARDS
            ):
                raise cards_error
            total_cards += count
        if total_cards > GAME.NUM_TOTAL_CARDS:
            raise cards_error
        return cards

    @staticmethod
    def __put_all_colors_in_cards(cards: Dict[Color, int]) -> Dict[Color, int]:
        """
        Return a new mapping between each Color and its count such that every Color represented in the game has
        a value (0 if the color was not in the mapping previously).
        """
        cards = cards.copy()
        for color_enum in Color.get_all_color_enums():
            cards[color_enum] = cards.get(color_enum, 0)
        return cards

    def __validate_total_acquired_connections(self, player_connections: List[Set[Connection]]) -> List[Set[Connection]]:
        """
        Ensures each set in this list is a valid set of Connection.
        Also ensures this player's connections are somewhere in this list.
        """
        player_conn_error = ValueError("Player connections must be a list of set of Connection.")
        if not isinstance(player_connections, list):
            raise player_conn_error
        if len(player_connections) == 0:
            raise ValueError("Player connections cannot be empty; this player's connections must be in here.")
        found_players_conns = False
        for one_player_connections in player_connections:
            self.__validate_acquired_connections(one_player_connections)
            if one_player_connections == self.__acquired_connections:
                found_players_conns = True
        if not found_players_conns:
            raise ValueError("This player's connections must be stored in here.")
        return player_connections

    def __find_connection_in_total_acquired(self, c: Connection) -> int:
        """
        Returns the index of the player who owns this connection, and -1 if no one does.
        """
        for i, player_connections in enumerate(self.__total_acquired_connections):
            if c in player_connections:
                return i
        return -1

    def __get_this_player_index(self) -> int:
        """
        Return the index of this player.
        Returns -1 if the index cannot be found, but this is never possible given player state validation.
        """
        for i, player_connections in enumerate(self.__total_acquired_connections):
            if player_connections == self.__acquired_connections:
                return i
        return -1

    def can_acquire_connection(self, c: Connection, trains_map: Map):
        """
        Determine whether this player can acquire the given connection given the game map.

        Can acquire:
            - has enough rails
            - has enough same colored cards
            - the connection is in the Map
            - the connection is not owned by anyone else
        """
        has_enough_rails = self.__num_rails >= c.get_length()
        has_enough_colored_cards = self.__cards[c.get_color()] >= c.get_length()
        connection_in_map = c in trains_map.get_connections()
        is_connection_unacquired = self.__find_connection_in_total_acquired(c) == -1
        return (
            has_enough_rails
            and has_enough_colored_cards
            and connection_in_map
            and is_connection_unacquired
        )

    def get_index(self) -> int:
        """
        Return the index of this player in the game.
        The 0th indexed player goes first in the game.
        """
        return self.__index

    def get_acquired_connections(self) -> Set[Connection]:
        """
        Return a deep copy of this player's connections.
        """
        return set([c.copy() for c in self.__acquired_connections])

    def get_destinations(self) -> Set[Destination]:
        """
        Return a deep copy of this player's destinations.
        :return:
        """
        return set([d.copy() for d in self.__destinations])

    def get_cards(self) -> Dict[Color, int]:
        """
        Return a deep copy of this player's cards.
        """
        return {k: v for k, v in self.__cards.items()}

    def get_num_rails(self) -> int:
        """
        Get the number of rails this player has.
        """
        return self.__num_rails

    def get_all_player_connections(self) -> List[Set[Connection]]:
        """
        Return a deep copy of all of the players' Connections.
        """
        return [
            set([c.copy() for c in player_conns])
            for player_conns in self.__total_acquired_connections
        ]

    def copy(self) -> "PlayerGameState":
        """
        Return a deep copy of this player game state.
        """
        acquired_conns = self.get_acquired_connections()
        dests = self.get_destinations()
        cards = self.get_cards()
        total_conns = self.get_all_player_connections()

        return PlayerGameState(
            acquired_connections=acquired_conns,
            destinations=dests,
            num_rails=self.__num_rails,
            cards=cards,
            total_acquired_connections=total_conns
        )

    def obtain_connection(self, c: Connection) -> "PlayerGameState":
        """
        Obtains the given Connection. Assumes the Connection can be obtained.
        """
        new_acquired_connections = set(self.get_acquired_connections()).union({c})
        dests = self.get_destinations()
        cards = self.get_cards()
        cards[c.get_color()] -= c.get_length()
        total_conns = self.get_all_player_connections()
        total_conns[self.__index] = new_acquired_connections
        return PlayerGameState(
            acquired_connections=new_acquired_connections,
            destinations=dests,
            num_rails=self.__num_rails - c.get_length(),
            cards=cards,
            total_acquired_connections=total_conns
        )

    def get_all_obtainable_connections_for_player(self, trains_map: Map) -> Set[Connection]:
        """
        Gets all of the Connections this player can acquire given a trains map.
        """
        obtainable_connections = set()
        for conn in trains_map.get_connections():
            if self.can_acquire_connection(conn, trains_map):
                obtainable_connections.add(conn)
        return obtainable_connections
