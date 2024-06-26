from dealer import Dealer
from player import Player, User
from astovali_bot import AstovaliBot

dealer = Dealer([User, AstovaliBot, Player], 1000)
while True:
    dealer.game(log=False)