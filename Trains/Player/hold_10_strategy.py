from typing import Set

from Trains.Common.map import Destination, sort_destinations, sort_connections
from Trains.Common.player_game_state import PlayerGameState
from Trains.Player.strategy import IStrategy, Move, ConnectionRequest, CardRequest


class Hold10Strategy(IStrategy):
    def __init__(self):
        super().__init__()

    def pick(self, destinations: Set[Destination]) -> Set[Destination]:
        """
        Choose the first 2 destinations that come lexicographically.
        Return the rest.
        """
        return set(sort_destinations(destinations)[2:])

    def play(self, pgs: PlayerGameState) -> Move:
        """
        If player has more than 10 cards:
            Get the first sorted connection
            If no connections: ask for cards.
        If player has 10 or less cards:
            ask for cards
        """
        sorted_legal_connections = sort_connections(set(pgs.get_all_obtainable_connections_for_player(self.trains_map)))

        if pgs.get_num_cards() > 10 and len(sorted_legal_connections) > 0:
            desired_conn = sorted_legal_connections[0]
            return ConnectionRequest(desired_conn)
        else:
            return CardRequest()
