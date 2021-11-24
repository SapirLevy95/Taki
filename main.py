from Sapir.taki import Taki

taki = Taki()
print(f'WELCOME PLAYERS!, lets play.\n')
for player in taki.players:
    print(f'{player.name} with {len(player.players_cards)} cards: {player.return_players_cards_status()}')
print(f'The card on the table is {taki.stock[0]}')
taki.start_game()
