from dealer import Dealer, Card
from math import ceil
from statistics import mean
from itertools import combinations

class AstovaliBot:
    best_hand = [
        Card('♠', 14),
        Card('♠', 13),
        Card('♠', 12),
        Card('♠', 11),
        Card('♠', 10)
    ]
    
    def __init__(self):
        pass

    def cleanse_bet(self, bet, money, match):
        if bet == 'F':
            return bet
        return max(match, min(ceil(bet), money-1))

    def move(self, data):
        match_value = max([x["bet"] for x in data["others"]] + [data["self"]["bet"]])

        bet = match_value

        if len(data["pool"]) == 0:
            hand = data["self"]["hand"]
            value = hand[0].value + hand[1].value
            if hand[0].suit == hand[1].suit:
                value += 5

            if hand[0].value == hand[1].value:
                bet = data["self"]["money"] * 0.2 * (value/(14+14+5))
            else:
                if value < 17:
                    return 'F'
                bet = data["self"]["money"] * 0.05 * (value/(14+14+5))
        else:
            hand = data["self"]["hand"]
            pool = data["pool"]

            straightness = 0
            flushness = 0
            fives = (sorted(five) for five in (combinations(hand+pool, r=5)) 
                     if any([y in hand for y in five]))
            for five in fives:
                straight_temp = 0
                flush_temp = 0
                for i in range(4):
                    if five[i].value+1 == five[i+1].value:
                        straight_temp += 1
                    if five[i].suit == five[i+1].suit:
                        flush_temp += 1
                straightness = max(straightness, straight_temp)
                flushness = max(flushness, flush_temp)
                if straightness == 4 and flushness == 4: # straight flush
                    if len(pool) == 5: # all in
                        return data["self"]["money"]
                    bet = match_value * 5
                    return self.cleanse_bet(bet, data["self"]["money"], match_value)

            quads = (quad for quad in (combinations(hand+pool, r=4)) 
                     if any([y in hand for y in quad]))
            for quad in quads:
                if all(i == j for i, j in combinations(quad, r=2)): # four of a kind
                    bet = match_value * 4
                    return self.cleanse_bet(bet, data["self"]["money"], match_value)

            trio_value = -1

            trios = (trio for trio in (combinations(hand+pool, r=3)) 
                     if any([y in hand for y in trio]))
            for trio in trios:
                if all(i == j for i, j in combinations(trio, r=2)):
                    trio_value = trio[0].value
            
            pairs = (pair for pair in (combinations(hand+pool, r=2)) 
                     if any([y in hand for y in pair]))
            pair_num = 0
            for pair in pairs:
                if all(i == j for i, j in combinations(pair, r=2)):
                    if trio_value != -1 and pair[0].value != trio_value: # full house
                        bet = match_value * 3.5
                        return self.cleanse_bet(bet, data["self"]["money"], match_value)
                    pair_num += 1

            if flushness == 4: # flush
                bet = match_value * 3
                return self.cleanse_bet(bet, data["self"]["money"], match_value)
            
            if straightness == 4: # straight
                bet = match_value * 2.5
                return self.cleanse_bet(bet, data["self"]["money"], match_value)
            
            if trio_value != -1: # trio
                bet = match_value * 2
                return self.cleanse_bet(bet, data["self"]["money"], match_value)
            
            if pair_num == 2: # two pair
                bet = match_value * 1.5
                return self.cleanse_bet(bet, data["self"]["money"], match_value)
            
            if pair_num == 1: # one pair
                bet = match_value * 1.2
                return self.cleanse_bet(bet, data["self"]["money"], match_value)
            
            if flushness-len(pool) > 0 or straightness-len(pool) > 0:
                bet = match_value * (1 + 1/len(pool))

        return self.cleanse_bet(bet, data["self"]["money"], match_value)
    
    def debrief(self, data):
        pass

class AllInBot:
    def __init__(self):
        pass

    def move(self, data):
        match_value = max([x["bet"] for x in data["others"]])
        if match_value == 0: # no one has bet
            return min(data["self"]["money"], 5) # bet $5
        return data["self"]["money"] # GO ALL IN !!!!

    def debrief(self, data):
        pass