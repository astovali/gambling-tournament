from dealer import Dealer, Card
from math import ceil

class VirusBot:
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
    