from dealer import Dealer, Card
from math import ceil
import random as rd

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
        pre = int(rd.randint(0,10))
        if len(data["pool"]) == 0:
            if data["self"]["hand"][0].value == data["self"]["hand"][1].value:
                if data["self"]["hand"][0].value == 14 and data["self"]["hand"][1].value == 14:
                    bet = match_value*5
                else:
                    bet = match_value*2
            elif data["self"]["hand"][0].value != data["self"]["hand"][1].value:
                if data["self"]["hand"][0].value == 14 or data["self"]["hand"][1].value == 14:
                    if pre <= 3:
                        bet = match_value*2.25
                    elif pre > 3:
                        bet = match_value*1.75
                elif data["self"]["hand"][0].value > 10 and data["self"]["hand"][1].value > 10:
                    if pre <= 3:
                        bet = match_value*1.75
                    elif pre > 3:
                        bet = match_value*1.25
        else:
            hand = data["self"]["hand"] + data["pool"]
            value = Dealer.evaluate_hand(hand)
            evaluate_value = max([card.value for card in hand])
            ranking = (value - evaluate_value)/14
            unpre = int(rd.randint(0,10))
            if ranking == 8:  
                bet = data["self"]["money"]
            elif ranking == 7:
                if unpre <= 3:
                    bet = match_value*8
                elif unpre > 3:
                    bet = match_value*7.5
            elif ranking == 0:
                bet = match_value
            elif ranking == 1 or ranking == 2:
                unpred = int(rd.randint(0,1000))
                bet = match_value
            elif ranking == 6:
                if unpre <= 3:
                    bet = match_value*5.25
                elif unpre > 3:
                    bet = match_value*4.75
            elif ranking == 5 or ranking == 4:
                if unpre <= 3:
                    bet = match_value*2.75
                elif unpre > 3:
                    bet = match_value*2.25
            elif ranking == 3:
                if unpre <= 3:
                    bet = match_value*1.75
                elif unpre > 3:
                    bet = match_value*1.25
        if bet < match_value:
            return min(match_value, data["self"]["money"])
        elif data["self"]["money"] < bet:
            return data["self"]["money"]
        if data["self"]["money"] < match_value:
            return 'F'
        return min(ceil(bet), data["self"]["money"])
    
    def debrief(self, data):
        pass