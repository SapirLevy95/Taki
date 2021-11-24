from random import shuffle

from Sapir.card import Card
from Sapir.enum import Color, CardType
from Sapir.human_player import HumanPlayer
from Sapir.random_player import RandomPlayer
from Sapir.smart_player import SmartPlayer


class Taki:
    def __init__(self):
        self.used_stop_in_top_card_in_stock = False
        self.amount_of_active_plus_two_in_stock = 0

        self.pack = self.init_pack()
        self.stock = [self.pack.pop()]
        self.players = self.init_players()
        self.winners = []
        self.strategies = [self.try_play_regular_card,
                           self.try_play_stop_card,
                           self.try_play_change_diraction_card,
                           self.try_play_change_color_card,
                           self.try_play_plus_two_card]

    # short funcs for ctor
    def init_pack(self):
        pack = []
        colors_for_creating_pack = [Color.RED.name, Color.BLUE.name, Color.YELLOW.name, Color.GREEN.name]
        # We dont have 2 cards (we have only +2)
        pack = [Card.regular_card(color, num_card) for num_card in range(1, 11) for color in colors_for_creating_pack]
        pack += [Card.changes_color_card() for num_card in range(4)]
        pack += [Card.changes_direction_card(color) for num_card in range(4) for color in colors_for_creating_pack]
        pack += [Card.stop_card(color) for num in range(4) for color in colors_for_creating_pack]
        pack += [Card.plus_two_card(color) for num in range(4) for color in colors_for_creating_pack]
        # pack += [Card.plus_card(color) for num in range(4) for color in colors_for_creating_pack]
        shuffle(pack)
        return pack

    def init_players(self):
        count_players = self.get_players_count()
        players = []
        for player in range(count_players):
            players.append(self.get_new_player())
        players.sort(key=lambda player: player.age, reverse=False)
        return players

    def get_new_player(self):
        dict_players_types = {1: SmartPlayer, 2: RandomPlayer, 3: HumanPlayer}
        while True:
            try:
                name = str(input(f'Player please enter your name'))
                if (len(name) > 2) and name.isalpha():
                    break
                else:
                    raise TypeError
            except TypeError:
                print("Enter only letters please.")

        while True:
            try:
                print(f'Player please enter your age')
                age = int(input())
                break
            except ValueError:
                print(f"your age must have be a number")
        while True:
            try:
                print('Enter player type : 1 for a smart bot , 2 for a random bot or 3 for a human player')
                num_choice = int(input())
                if num_choice in dict_players_types.keys():
                    player_type = dict_players_types[num_choice]
                    player = player_type(name, self.pack[:3], age)
                    del self.pack[:3]
                    return player
                else:
                    print("The input is not valid, please enter a number between 1 to 3")
            except ValueError:
                print(f"Enter a number between 1 to 3")

    @property
    def top_card_in_stock(self):
        return self.stock[-1]

    def start_game(self):
        first_player = self.players[0]
        first_card_in_stock_is_changes_color = self.top_card_in_stock.card_type == CardType.CHANGES_COLOR and self.stock[0].color is None
        if first_card_in_stock_is_changes_color:
            first_player.change_color_of_top_card_in_stock(self)
        elif self.top_card_in_stock.card_type == CardType.PLUS_TWO:
            self.amount_of_active_plus_two_in_stock = 1

        while self.players:
            player = self.players[0]
            print()
            self.print_game_status()
            print()
            print("The current player is:")
            player.print_player()
            print(f'The current top card in stock is {self.top_card_in_stock}')

            is_turn_finished = False
            if len(self.players) == 1:
                self.add_winner(player)
            elif self.top_card_in_stock.card_type == CardType.STOP and not self.used_stop_in_top_card_in_stock:
                print(f'There is a stop sign in stock , {player.name} you missed your turn ')
                self.used_stop_in_top_card_in_stock = True
                is_turn_finished = True
                self.next_in_line(player)
            elif self.top_card_in_stock.card_type == CardType.PLUS_TWO and self.amount_of_active_plus_two_in_stock != 0:
                is_turn_finished = player.play(self)
                if not is_turn_finished:
                    if len(self.pack) >= 2 * self.amount_of_active_plus_two_in_stock:
                        player.players_cards += self.pack[:2 * self.amount_of_active_plus_two_in_stock]
                        del self.pack[:2 * self.amount_of_active_plus_two_in_stock]
                        self.amount_of_active_plus_two_in_stock = 0
                    else:
                        player.players_cards.append(self.pack[:])
                    is_turn_finished = True
            else:
                is_turn_finished = player.play(self)

            if is_turn_finished and not player.players_cards:
                self.add_winner(player)
            else:
                if self.pack:
                    print(f'{player.name} doesnt have a fitting card, so {player.name} is taking from stock {player.players_cards[-1]}.')
                    player.players_cards.append(self.pack.pop())
                else:
                    raise Exception('Pack is empty')
            self.next_in_line(player)

    def try_play_card(self, card, player):
        same_color = self.top_card_in_stock.color == card.color
        same_type = self.top_card_in_stock.card_type == card.card_type
        same_number = self.top_card_in_stock.number == card.number

        if card.card_type == CardType.PLUS_TWO and (same_type or same_color):
            self.amount_of_active_plus_two_in_stock += 1
            return True

        if self.amount_of_active_plus_two_in_stock > 0:
            return False

        if card.card_type == CardType.CHANGES_COLOR:
            player.change_color_of_top_card_in_stock(self)
            return True

        if card.card_type == CardType.REGULAR_CARD and (same_color or same_number):
            self.put_card_in_stock(card, player)
            return True

        if card.card_type == CardType.CHANGES_DIRECTION and (same_color or same_type):
            self.players.reverse()
            return True

        if card.card_type == CardType.STOP and (same_color or same_type):
            self.used_stop_in_top_card_in_stock = False
            return True

        return False

    ########################################################################################################################

    # Strategies
    def try_play_regular_card(self, player):
        for card in player.players_cards:
            if card.card_type == CardType.REGULAR_CARD and self.try_play_card(card, player):
                return card
        return None

    def try_play_change_color_card(self, player):
        for card in player.players_cards:
            if card.card_type == CardType.CHANGES_COLOR and self.try_play_card(card, player):
                return card
        return None

    def try_play_stop_card(self, player):
        for card in player.players_cards:
            if card.card_type == CardType.STOP and self.try_play_card(card, player):
                return card
        return None

    def try_play_change_diraction_card(self, player):
        for card in player.players_cards:
            if card.card_type == CardType.CHANGES_DIRECTION and self.try_play_card(card, player):
                return card
        return None

    def try_play_plus_two_card(self, player):
        for card in player.players_cards:
            if card.card_type == CardType.PLUS_TWO and self.try_play_card(card, player):
                return card
        return None

    ########################################################################################################################

    def put_card_in_stock(self, card, player):
        print(f"{player.name} have a fitting card {card}.")
        player.players_cards.remove(card)
        self.stock.append(card)

    def next_in_line(self, player):
        self.players.remove(player)
        self.players.append(player)

    def change_color_of_top_card_in_stock_to_common_color_in_players_deck(self, player):
        common_color = player.get_common_color()
        self.top_card_in_stock.color = common_color
        print(f'we have a changing color card on stock, i choose {common_color} \n')

    # ##prints
    def print_game_status(self):
        for player in self.players:
            print(f'{player.name} with {len(player.players_cards)} cards: {player.return_players_cards_status()}')
        print(f'Pack = {len(self.pack)}, table card is = {self.stock[-1]}\n')

    def print_pack(self):
        for card in self.pack:
            print(card)

    def add_winner(self, player):
        self.winners.append(player)
        self.players.remove(player)
        winner_num = len(self.winners)
        print(f'{player.name} you are on number {winner_num} place')

    def print_list_of_winners(self):
        [print(f"{player} you are in the {place} place") for place, player in enumerate(self.winners, start=1)]

    def print_pack(self):
        [print(card) for card in self.pack]
        print(len(self.pack))

    def print_stock(self):
        [print(card) for card in self.stock]

    def print_players(self):
        [player.print_player() for player in self.players]

    def get_players_count(self):
        while True:
            try:
                count_of_players = int(input("How many players are you? - enter between 2-4 players\n"))
                if not (2 <= int(count_of_players) <= 4):
                    count_of_players = input("you didn't enter an acceptable number, please enter again\n")
                else:
                    return count_of_players
            except ValueError:
                print("Enter only a number between 2-4 ")
