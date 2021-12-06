from typing import List

from Trains.Common.map import Map, Color, Connection
from Trains.Common.player_game_state import PlayerGameState


class RefereeGameState:
    def __init__(
        self,
        *,
        trains_map: Map,
        player_game_states: List[PlayerGameState],
        deck: List[Color],
        active_player_idx: int = 0
    ):
        self.__trains_map = self.__validate_map(trains_map)
        self.__player_game_states = self.__validate_player_game_states(player_game_states)
        self.__deck = self.__validate_card_deck(deck)
        self.__active_player_idx = self.__validate_player_idx(active_player_idx)

    @staticmethod
    def __validate_map(trains_map: Map) -> Map:
        """
        trains_map must be a Map.
        """
        if not isinstance(trains_map, Map):
            raise ValueError("Input map must be of Map type.")
        return trains_map

    def __validate_player_game_states(self, player_game_states: List[PlayerGameState]) -> List[PlayerGameState]:
        """
        Player game states must be a list of PlayerGameState.
        All connections must agree with the map's connections.
        pgs.get_acquired_connections() must be the exact same for all player game states. 
        """
        map_connections = self.__trains_map.get_connections()
        pgs_error = ValueError("Player game states must be list of PlayerGameState.")
        connection_error = ValueError("All connections must be a subset of those in the map.")
        all_connections_error = ValueError("All player connections must be consistent with all player game states.")
        player_connections = []

        if not isinstance(player_game_states, list):
            raise pgs_error
        for pgs in player_game_states:
            if not isinstance(pgs, PlayerGameState):
                raise pgs_error
            for connection in pgs.get_acquired_connections():
                if connection not in map_connections:
                    raise connection_error
            player_connections.append(pgs.get_acquired_connections())
        for pgs in player_game_states:
            if player_connections != pgs.get_all_player_connections():
                raise all_connections_error
        return player_game_states

    @staticmethod
    def __validate_card_deck(deck: List[Color]) -> List[Color]:
        """
        Card deck must be a list of Color.
        """
        deck_error = ValueError("Deck must be list of Color.")
        if not isinstance(deck, list):
            raise deck_error
        for card in deck:
            if not isinstance(card, Color):
                raise deck_error
        return deck

    def __validate_player_idx(self, player_idx: int) -> int:
        """
        Player index must be between 0 and the number of players.
        """
        if not (
            isinstance(player_idx, int)
            and 0 <= player_idx < len(self.__player_game_states)
        ):
            raise ValueError(f"Player index must be an integer between 0 and {len(self.__player_game_states)}, "
                             "exclusive.")
        return player_idx

    def get_active_player_idx(self) -> int:
        """
        Get the index of the active player.
        """
        return self.__active_player_idx

    def get_active_player_game_state(self) -> PlayerGameState:
        """
        Get the active player's game state.
        """
        return self.__player_game_states[self.__active_player_idx]

    def get_deck(self) -> List[Color]:
        """
        Get the referee deck.
        """
        return self.__deck

    def can_active_player_acquire_connection(self, c: Connection) -> bool:
        """
        Returns whether the active player can acquire the given connection, based on the game map.
        """
        active_pgs = self.get_active_player_game_state()
        return active_pgs.can_acquire_connection(c, self.__trains_map)
