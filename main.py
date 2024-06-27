from dealer import Dealer
from player import Player, User
from virus_bot import VirusBot
from astovali_bot import AstovaliBot, AllInBot
from itertools import combinations

bots = [Player, AstovaliBot, AllInBot, VirusBot]
matchups = []
for r in range(2, len(bots)+1):
    matchups.extend(combinations(bots, r=r))

for matchup in matchups:
    dealer = Dealer(matchup, 1000)
    for _ in range(100):
        dealer.game(log=False)
    print(dealer.players)