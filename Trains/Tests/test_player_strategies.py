from typing import Set

import mock

from Trains.Common.map import Destination, City, Map, Connection
from Trains.Player.buy_now_strategy import BuyNowStrategy
from Trains.Player.hold_10_strategy import Hold10Strategy
from Trains.Player.strategy import ConnectionRequest, CardRequest


class TestHold10:
    @staticmethod
    def test_hold_10_pick(choose_from_dests: Set[Destination], boston: City, nyc: City, la: City, dc: City):
        strat = Hold10Strategy()
        picked_destinations = {Destination({boston, dc}), Destination({boston, la})}
        unpicked_destinations = choose_from_dests - picked_destinations
        assert strat.pick(choose_from_dests) == unpicked_destinations

    @staticmethod
    def test_hold_10_play_more_than_10_cards(la_island_map: Map, nyc_to_boston: Connection):
        strat = Hold10Strategy()
        with mock.patch('Trains.Common.player_game_state.PlayerGameState') as pgs:
            pgs.get_all_obtainable_connections_for_player.return_value = la_island_map.get_connections()
            pgs.get_num_cards.return_value = 11

            assert strat.play(pgs) == ConnectionRequest(nyc_to_boston)

    @staticmethod
    def test_hold_10_play_10_cards(la_island_map: Map, nyc_to_boston: Connection):
        strat = Hold10Strategy()
        with mock.patch('Trains.Common.player_game_state.PlayerGameState') as pgs:
            pgs.get_all_obtainable_connections_for_player.return_value = la_island_map.get_connections()
            pgs.get_num_cards.return_value = 10

            assert strat.play(pgs) == CardRequest()

    @staticmethod
    def test_hold_10_play_less_than_10_cards(la_island_map: Map, nyc_to_boston: Connection):
        strat = Hold10Strategy()
        with mock.patch('Trains.Common.player_game_state.PlayerGameState') as pgs:
            pgs.get_all_obtainable_connections_for_player.return_value = la_island_map.get_connections()
            pgs.get_num_cards.return_value = 9

            assert strat.play(pgs) == CardRequest()

    @staticmethod
    def test_hold_10_play_more_than_10_cards_no_conns(la_island_map: Map, nyc_to_boston: Connection):
        strat = Hold10Strategy()
        with mock.patch('Trains.Common.player_game_state.PlayerGameState') as pgs:
            pgs.get_all_obtainable_connections_for_player.return_value = {}
            pgs.get_num_cards.return_value = 100

            assert strat.play(pgs) == CardRequest()


class TestBuyNow:
    @staticmethod
    def test_buy_now_pick(choose_from_dests: Set[Destination], boston: City, nyc: City, la: City, dc: City):
        strat = BuyNowStrategy()
        picked_destinations = {Destination({nyc, dc}), Destination({nyc, la})}
        unpicked_destinations = choose_from_dests - picked_destinations
        assert strat.pick(choose_from_dests) == unpicked_destinations

    @staticmethod
    def test_buy_now_no_conns():
        strat = BuyNowStrategy()
        with mock.patch('Trains.Common.player_game_state.PlayerGameState') as pgs:
            pgs.get_all_obtainable_connections_for_player.return_value = {}

            assert strat.play(pgs) == CardRequest()

    @staticmethod
    def test_buy_now_conns(la_island_map: Map, nyc_to_boston: Connection):
        strat = BuyNowStrategy()
        with mock.patch('Trains.Common.player_game_state.PlayerGameState') as pgs:
            pgs.get_all_obtainable_connections_for_player.return_value = la_island_map.get_connections()

            assert strat.play(pgs) == ConnectionRequest(nyc_to_boston)
