from dealer import Dealer
from player import Player

dealer = Dealer([Player, Player])
for _ in range(1):
    dealer.game(log=True)