from dealer import Dealer
from player import Player
from astovali_bot import AstovaliBot

dealer = Dealer([Player, AstovaliBot])
for _ in range(10000):
    dealer.game(log=False)

for player in dealer.players:
    print(f'{player["class"].__class__.__name__}: ${player["money"]}')