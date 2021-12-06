from typing import Set

from Trains.Common.map import Destination, sort_connections, sort_destinations
from Trains.Common.player_game_state import PlayerGameState
from Trains.Player.strategy import IStrategy, Move, ConnectionRequest, CardRequest


class BuyNowStrategy(IStrategy):
    def __init__(self):
        super().__init__()

    def pick(self, destinations: Set[Destination]) -> Set[Destination]:
        """
        Pick the 2 destinations that come last lexicographically.
        Return the rest.
        """
        return set(sort_destinations(destinations)[:3])

    def play(self, pgs: PlayerGameState) -> Move:
        """
        If the player has legal connections they can acquire, acquire them.
        If not, ask for cards.
        """
        sorted_legal_connections = sort_connections(set(pgs.get_all_obtainable_connections_for_player(self.trains_map)))
        if len(sorted_legal_connections) > 0:
            return ConnectionRequest(sorted_legal_connections[0])
        else:
            return CardRequest()
