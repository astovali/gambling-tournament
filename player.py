class Player:
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
        return max([x["bet"] for x in data["others"]] + [data["self"]["bet"]])
    
    def debrief(self, data):
        # called at end of a game
        # data contains the same as in self.move but you also have
        # access to the "hand" attribute of each element in "others"
        pass

class User:
    def __init__(self):
        print("Bet at least the previous bet's amount")
        print("Bet no more than your balance")
        print("Bet 'F' to fold")
        self.money = 0
        self.folded = False
        self.allIn = False

    def move(self, data):
        self.money = data["self"]["money"]
        match_amount = max([x["bet"] for x in data["others"]] + [data["self"]["bet"]])
        print(f'Your balance: ${self.money}')
        print(f'Current bet is ${match_amount}')
        print(f'Your hand is {data["self"]["hand"]}')
        print(f'Pool is {data["pool"]}')
        if self.folded:
            print("You've folded")
            return 'F'
        if self.allIn:
            print("You've gone all in")
            return self.money
        bet = ''
        while not bet.isdigit() and bet != 'F':
            bet = input("Bet: $")
        if bet == 'F' or int(bet) < match_amount:
            self.folded = True
            return bet
        if int(bet) >= self.money:
            self.allIn = True
        return int(bet)
    
    def debrief(self, data):
        print("Other players hands were: ")
        for player in data["others"]:
            print(player["hand"], end='')
            if player["folded"]:
                print(" (folded),", end='')
            else:
                print(f' bet ${player["bet"]},', end='')
            print(f' balance: ${player["money"]}')
        gain = data["self"]["money"] - self.money
        self.money = data["self"]["money"]
        self.folded = False
        self.allIn = False
        if gain > 0:
            print(f"You won and gained ${gain}")
        elif gain < 0:
            print(f"You lost ${gain}")
        else:
            print(f"You didn't lose or gain any money")