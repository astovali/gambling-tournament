import random
from itertools import combinations

class Card:
    def __init__(self, suit, value):
        self.suit = suit
        self.value = value

    def __str__(self):
        if self.value < 11:
            return f"{self.value} of {self.suit}"
        else:
            name = {11: "Jack",
                    12: "Queen",
                    13: "King",
                    14: "Ace",}[self.value]
            return f"{name} of {self.suit}"
        
    def __repr__(self):
        return str(self)
        
    def __lt__(self, other):
        return self.value < other.value

class Deck:
    values = list(range(2, 15))
    suits = "♠♥♣♦"
    def __init__(self):
        self.deck = []
        for value in Deck.values:
            for suit in Deck.suits:
                self.deck.append(Card(suit, value))
        self.shuffle()

    def shuffle(self):
        random.shuffle(self.deck)
        self.unshuffled = len(self.deck)

    def draw(self, num = 0):
        if num == 0:
            if self.unshuffled <= 0:
                self.shuffle()
            self.unshuffled -= 1
            return self.deck.pop(0)
        out = []
        for _ in range(num):
            if self.unshuffled <= 0:
                self.shuffle()
            self.unshuffled -= 1
            out.append(self.deck.pop(0))
        return out
    
    def add(self, card):
        self.deck.append(card)

class Dealer:
    def __init__(self, player_classes, starting_money):
        self.deck = Deck()
        self.players = [{"class": player_class(), 
                         "hand": [], 
                         "bet": 0, 
                         "money": starting_money,
                         "folded": False} for player_class in player_classes]
        self.pool = []
        self.allIn = -1

    def get_move(self, player, log=False):
        non_folded = [x["bet"] for x in self.players if not x["folded"]]
        if len(non_folded) == 1:
            return "end"
        bet = player["class"].move({
            "self": {
                "hand": player["hand"],
                "bet": player["bet"],
                "money": player["money"]
            },
            "others": [{"bet": x["bet"],
                        "money": x["money"],
                        "folded": x["folded"],
                        "name": x["class"].__class__.__name__} 
                        for x in self.players
                        if x["class"] is not player["class"]],
            "pool": self.pool
        })

        if (type(bet) == int):
            if self.allIn != -1 and bet >= self.allIn:
                player["bet"] = self.allIn
                if log:
                    print(f'{player["class"].__class__.__name__} matched all in on ${self.allIn}')
            elif bet >= max(non_folded) and bet <= player["money"]:
                player["bet"] = bet
                if log:
                    if bet == max(non_folded):
                        print(f'{player["class"].__class__.__name__} matched ${bet}')
                    else:
                        print(f'{player["class"].__class__.__name__} raised to ${bet}')
            elif max(non_folded) > player["money"] and bet >= player["money"]:
                self.allIn = player["money"]
                for x in self.players:
                    x["bet"] = min(self.allIn, x["bet"])
                if log:
                    print(f'{player["class"].__class__.__name__} went all in on ${self.allIn}')
            else:
                player["folded"] = True
                if log:
                    print(f'{player["class"].__class__.__name__} folded')
        else:
            player["folded"] = True
            if log:
                print(f'{player["class"].__class__.__name__} folded')
        return
    
    @staticmethod
    def evaluate_hand(hand):
        ranking_values = {
            "high": 0,
            "pair": 1,
            "twopair": 2,
            "triplet": 3,
            "srt": 4,
            "flush": 5,
            "house": 6,
            "quad": 7,
            "srtfsh": 8
        }

        # high card
        value = max([card.value for card in hand])
        ranking = ranking_values["high"]
        
        # find four of a kind
        for quad in combinations(hand, r=4):
            if all(map(lambda x: x.value==quad[0].value, quad)):
                ranking = ranking_values["quad"]
                value = quad[0].value
        
        # find triplets
        if ranking < ranking_values["quad"]:
            for i, j, k in combinations(hand, r=3):
                if i.value == j.value and i.value == k.value:
                    ranking = ranking_values["triplet"]
                    value = i.value
        
        # find pairs
            for i, j in combinations(hand, r=2):
                if i.value == j.value:
                    if (ranking == ranking_values["triplet"]
                    and i.value != value):
                        ranking = ranking_values["house"]
                    elif (ranking == ranking_values["pair"]
                    and i.value != value):
                        ranking = ranking_values["twopair"]
                        value = max(value, i.value)
                    elif ranking == ranking_values["high"]:
                        ranking = ranking_values["pair"]
                        value = i.value

        # find straight and flush
        for five in combinations(hand, r=5):
            flush = all(map(lambda x: x.suit == five[0].suit, five))
            five = list(five)
            if 2 in [x.value for x in five]:
                five = [Card(x.suit, ((x.value-1)%13)+1) for x in five]
            five.sort()
            straight = all(map(lambda i: five[i].value+1 == five[i+1].value, range(4)))
            if flush and straight:
                ranking = ranking_values["srtfsh"]
                value = five[4].value
            elif flush:
                if ranking < ranking_values["flush"]:
                    ranking = ranking_values["flush"]
                    value = five[4].value
            elif straight:
                if ranking < ranking_values["srt"]:
                    ranking = ranking_values["srt"]
                    value = five[4].value

        return value + (14*ranking)
        
    def cleanup(self, log=False):
        reward = 0
        highest = 0
        winners = 0
        for player in self.players:
            player["money"] -= player["bet"]
            reward += player["bet"]
        for player in self.players:
            if player["folded"]:
                continue
            highest = max(highest, self.evaluate_hand(player["hand"] + self.pool))
        for player in self.players:
            if player["folded"]:
                continue
            if highest == self.evaluate_hand(player["hand"] + self.pool):
                winners += 1
        for player in self.players:
            if player["folded"]:
                continue
            if highest == self.evaluate_hand(player["hand"] + self.pool):
                if log:
                    print(f'{player["class"].__class__.__name__} won {reward//winners} (bet ${player["bet"]})')
                player["money"] += reward//winners
        for player in self.players:
            player["class"].cleanup({
                "self": {
                    "hand": player["hand"],
                    "bet": player["bet"],
                    "money": player["money"]
                },
                "others": [{"bet": x["bet"],
                            "money": x["money"],
                            "folded": x["folded"],
                            "name": x["class"].__class__.__name__,
                            "hand": x["hand"]} 
                            for x in self.players
                            if x["class"] is not player["class"]],
                "pool": self.pool
            })
        for player in self.players:
            while len(player["hand"]):
                self.deck.add(player["hand"].pop(0))
            player["bet"] = 0
            if player["money"] == 0:
                player["folded"] = True
            else:
                player["folded"] = False
        while len(self.pool):
            self.deck.add(self.pool.pop(0))
        self.allIn = -1

    def game(self, log=False):
        non_folded = [x["bet"] for x in self.players if not x["folded"]]
        if len(non_folded) == 1:
            if log:
                print("Only 1 has money")
            return "end"
        
        # first betting round
        for player in self.players:
            player["hand"].extend(self.deck.draw(2))
            if log:
                print(f'{player["class"].__class__.__name__} drew {player["hand"][0]}, {player["hand"][1]}')
            if self.get_move(player, log=log) == "end":
                self.cleanup(log=log)
                return
    
        # the flop
        self.pool.extend(self.deck.draw(3))
        if log:
            print(f'Flop was {", ".join(map(str, self.pool))}')
        for player in self.players:
            if player["folded"]:
                continue
            if self.get_move(player, log=log) == "end":
                self.cleanup(log=log)
                return
        
        # 2 subsequent betting rounds
        for i in range(2):
            self.pool.append(self.deck.draw())
            if log:
                if i == 0:
                    print(f"Turn was {self.pool[3]}")
                if i == 1:
                    print(f"River was {self.pool[4]}")
            for player in self.players:
                if player["folded"]:
                    continue
                if self.get_move(player, log=log) == "end":
                    self.cleanup(log=log)
                    return
        
        # make everyone match (no raises allowed)
        for player in self.players:
            if player["folded"]:
                continue
            non_folded = [x["bet"] for x in self.players if not x["folded"]]
            if len(non_folded) == 1:
                self.cleanup(log=log)
                return
            bet = player["class"].move({
                "self": {
                    "hand": player["hand"],
                    "bet": player["bet"],
                    "money": player["money"]
                },
                "others": [{"bet": x["bet"],
                            "money": x["money"],
                            "folded": x["folded"],
                            "name": x["class"].__class__.__name__} 
                            for x in self.players
                            if x["class"] is not player["class"]],
                "pool": self.pool
            })

            if (type(bet) == int):
                if self.allIn != -1 and bet >= self.allIn:
                    player["bet"] = self.allIn
                    if log:
                        print(f'{player["class"].__class__.__name__} matched all in on ${self.allIn}')
                elif bet >= max(non_folded) and bet <= player["money"]:
                    player["bet"] = min(max(non_folded), bet)
                    if log:
                        print(f'{player["class"].__class__.__name__} matched ${bet}')
                elif max(non_folded) > player["money"] and bet >= player["money"]:
                    self.allIn = player["money"]
                    for x in self.players:
                        x["bet"] = min(self.allIn, x["bet"])
                    if log:
                        print(f'{player["class"].__class__.__name__} went all in on ${self.allIn}')
                else:
                    player["folded"] = True
                    if log:
                        print(f'{player["class"].__class__.__name__} folded')
            else:
                player["folded"] = True
                if log:
                    print(f'{player["class"].__class__.__name__} folded')
                
        self.cleanup(log=log)