from Sapir.base_player import BasePlayer


class SmartPlayer(BasePlayer):
    def play(self, taki):
        for try_play in taki.strategies:
            card = try_play(self)
            if card:
                taki.put_card_in_stock(card, self)
                return True

        return False

    def change_color_of_top_card_in_stock(self, taki):
        self.get_common_color()
