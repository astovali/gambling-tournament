from dealer import Dealer, Card

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

    def move(self, data):
        match_value = max([x["bet"] for x in data["others"]] + [data["self"]["bet"]])
        bet = match_value

        if len(data["pool"]) == 0:
            value = data["self"]["hand"][0].value + data["self"]["hand"][1].value
            if data["self"]["hand"][0].value == data["self"]["hand"][1].value:
                value = value + 28
            best_value = 14*4 # two aces
            bet = (((value**2)/(best_value**2)) * data["self"]["money"])/10
        else:
            hand = data["self"]["hand"] + data["pool"]
            value = Dealer.evaluate_hand(hand)
            best_value = Dealer.evaluate_hand(AstovaliBot.best_hand[0:len(hand)])
            bet = ((value**2)/(best_value**2)) * data["self"]["money"]

        if bet < match_value and match_value*0.8 < bet:
            return min(match_value, data["self"]["money"])

        return min(int(bet), data["self"]["money"])
    
    def cleanup(self, data):
        pass