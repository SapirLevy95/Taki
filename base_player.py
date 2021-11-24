from abc import ABC, abstractmethod
from Sapir.enum import CardType


class BasePlayer(ABC):
    def __init__(self, name, players_cards, age):
        self.players_cards = players_cards
        self.name = name
        self.age = age

    def print_player(self):
        players_cards = [f'{card}' for card in self.players_cards]
        print(f'name : {self.name}, age: {self.age}, players type: {self.__class__.__name__}')
        print(f'cards : {players_cards}')

    def return_players_cards_status(self):
        return [f'{card}' for card in self.players_cards]

    @abstractmethod
    def play(self, taki):
        pass

    @abstractmethod
    def change_color_of_top_card_in_stock(self, taki):
        pass

    def get_common_color(self):
        # colors = [card.color for card in self.players_cards if card.color]
        # return mode(colors) if colors else Color.RED.name

        dict_of_colors_and_their_counters = {"red": 0, "blue": 0, "yellow": 0, "green": 0}
        for card in self.players_cards:
            if card.card_kind != CardType.CHANGES_COLOR and card.card_kind != CardType.STOP and card.card_kind != CardType.CHANGES_DIRACTION:
                dict_of_colors_and_their_counters[card.color] += 1
        inverse = [(value, key) for key, value in dict_of_colors_and_their_counters.items()]
        common_color = max(inverse)[1]
        return common_color
