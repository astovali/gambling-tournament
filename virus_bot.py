from dealer import Dealer, Card
from math import ceil

class VirusBot:
    best_hand = [
        Card('♠', 14),
        Card('♠', 13),
        Card('♠', 12),
        Card('♠', 11),
        Card('♠', 10)
    ]
    '''
    high:0
    pair:1
    twopair:2
    triplet:3
    straight:4
    flush:5
    house:6
    quad:7
    straight flush:8
    '''
    def __init__(self):
        pass

    def move(self, data):
        match_value = max([x["bet"] for x in data["others"]] + [data["self"]["bet"]])
        bet = match_value
        if len(data["pool"]) == 0:
            if data["self"]["hand"][0].value == data["self"]["hand"][1].value:
                if data["self"]["hand"][0].value == 14 and data["self"]["hand"][1].value == 14:
                    bet = match_value*5
                else:
                    bet = match_value*2
            elif data["self"]["hand"][0].value != data["self"]["hand"][1].value:
                if data["self"]["hand"][0].value == 14 or data["self"]["hand"][1].value == 14:
                    bet = match_value*2
                elif data["self"]["hand"][0].value > 10 and data["self"]["hand"][1].value > 10:
                    bet = match_value*1.5
        else:
            hand = data["self"]["hand"] + data["pool"]
            value = Dealer.evaluate_hand(hand)
            evaluate_value = max([card.value for card in hand])
            ranking = (value - evaluate_value)/14
            if ranking == 8:
                bet = data["self"]["money"]
            elif ranking == 7:
                bet = match_value*10
            elif ranking == 0:
                bet = match_value*10
            elif ranking == 1 or ranking == 2:
                bet = match_value
            elif ranking == 6:
                bet = match_value*5
            elif ranking == 5 or ranking == 4:
                bet = match_value*2.5
            elif ranking == 3:
                bet = match_value*1.5
        if bet < match_value:
            return min(match_value, data["self"]["money"])
        if data["self"]["money"] < bet:
            return data["self"]["money"]
        if data["self"]["money"] < match_value:
            return 'F'
        return min(ceil(bet), data["self"]["money"])
    
    def cleanup(self, data):
        pass
    
    '''
    def __init__(self):
        # Called once at the beginning of tournament
        pass

    def move(self, data):
        # called each betting round
        # data layout:
        # "self": {"hand": [...Card], "bet": int, "money": int}
        # "others": [...{"bet": int, "money": int, "folded": False, "name": "Player"}]
        # "pool": [...Card]
        # You should store or find any other data you want...
        # ...such as turn num, previous bet changes
        # return what you want to set your bet to (or F to fold)
        currentbet = max([x["bet"] for x in data["others"]] + [data["self"]["bet"]])
        maxbet = int(currentbet * 2) 
        hand = data["self"]["hand"] + data["pool"]
        value = Dealer.evaluate_hand(hand)
        if data["self"]["money"] > currentbet:
            if value == 0:
                if maxbet < data["self"]["money"]:
                    return int(maxbet)
                else:
                    return int(data["self"]["money"])
            elif value == 8:
                return int(data["self"]["money"])
            else:
                return max([x["bet"] for x in data["others"]] + [data["self"]["bet"]])
        else:
            return 'F'
    
    def cleanup(self, data):
        # called at end of a game
        # data contains the same as in self.move but you also have
        # access to the "hand" attribute of each element in "others"
        pass
    '''