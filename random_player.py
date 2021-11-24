from random import shuffle

from Sapir.base_player import BasePlayer


class RandomPlayer(BasePlayer):
    def play(self, taki):
        shuffled_strategies = taki.strategies.copy()
        shuffle(shuffled_strategies)
        for try_play in taki.strategies:
            card = try_play(self)
            if card:
                taki.put_card_in_stock(card, self)
                return True

        return False

    def change_color_of_top_card_in_stock(self, taki):
        self.get_common_color()
