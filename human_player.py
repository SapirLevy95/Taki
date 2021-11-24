from Sapir.base_player import BasePlayer
from Sapir.enum import Color


class HumanPlayer(BasePlayer):
    def play(self, taki):
        while True:
            try:
                print(f'You have {len(self.players_cards)} cards.which card number would you like to use? '
                      f'(from left to right). If you dont have a fitting card at all, press 0')
                card_num = int(input())
                if (1 <= card_num <= len(self.players_cards)):
                    picked_card = self.players_cards[card_num - 1]
                    print(picked_card)
                    taki.try_play_card(picked_card, self)
                    break
                elif card_num == 0:
                    break
                else:
                    card_num = input("The card number  is not valid  \n")
                    break
            except ValueError:
                print(f"Enter only a number between 1-{len(self.players_cards)}")

    def change_color_of_top_card_in_stock(self, taki):
        colors_for_creating_pack = {1: Color.RED.name, 2: Color.BLUE.name, 3: Color.YELLOW.name, 4: Color.GREEN.name}
        while True:
            try:
                print(f'''1.for changing the packs color to red press 1
        2.for changing the packs color to red press 2
        3.for changing the packs color to red press 3''')
                num_choice = int(input())
                if 5 > num_choice > 0:
                    new_color = colors_for_creating_pack.get(num_choice)
                    taki.top_card_in_stocl.color = new_color
                else:
                    print("The card number is not valid  \n")
            except ValueError:
                print(f"Enter a number between 1-3")
