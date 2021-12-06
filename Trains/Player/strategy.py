from abc import ABC, abstractmethod
from collections import Counter
from typing import List, Set, Optional, Any

from Trains.Common.map import Map, Color, Destination, Connection
from Trains.Common.player_game_state import PlayerGameState


class Move(ABC):
    @abstractmethod
    def get_connection(self) -> Optional[Connection]:
        """
        Return this move's connection, if the move is a connection request.
        """
        raise NotImplementedError()

    @abstractmethod
    def is_connection_request(self) -> bool:
        """
        Determine whether this move is a connection request.
        """
        raise NotImplementedError()

    def is_card_request(self) -> bool:
        """
        Determine whether this move is a card request.
        """
        return not self.is_connection_request()


class CardRequest(Move):
    def get_connection(self) -> Optional[Connection]:
        return None

    def is_connection_request(self) -> bool:
        return False

    def __eq__(self, other: Any) -> bool:
        return isinstance(other, CardRequest)


class ConnectionRequest(Move):
    def __init__(self, c: Connection):
        if not isinstance(c, Connection):
            raise ValueError("connection must be of type Connection.")
        self.__connection = c

    def get_connection(self) -> Optional[Connection]:
        return self.__connection.copy()

    def is_connection_request(self) -> bool:
        return True

    def __eq__(self, other: Any) -> bool:
        return (
            isinstance(other, ConnectionRequest)
            and other.get_connection() == self.__connection
        )

    def __hash__(self) -> int:
        return hash(self.__connection)


class IStrategy(ABC):
    def __init__(self):
        self.trains_map = None
        self.num_rails = None
        self.cards = None

    def setup(self, trains_map: Map, num_rails: int, cards: List[Color]) -> None:
        """
        Default functionality to setup(). stores all game information for the strategy to be able to use later.
        """
        self.__trains_map = trains_map
        self.num_rails = num_rails
        self.cards = Counter(cards)

    @abstractmethod
    def pick(self, destinations: Set[Destination]) -> Set[Destination]:
        """
        Choose 2 destinations, and return the rest.
        """
        raise NotImplementedError()

    def more(self, cards: List[Color]) -> None:
        """
        Update cards given additional cards from the referee.
        """
        card_map = Counter(cards)
        for color, count in card_map.items():
            self.cards[color] += count

    @abstractmethod
    def play(self, pgs: PlayerGameState) -> Move:
        """
        Return some action, given the player game state.
        """
        raise NotImplementedError()

    def win(self, win_or_not: bool) -> None:
        """
        Do some action if the player has won or not.
        """
        pass
