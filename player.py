class Player:
    def __init__(self):
        # Called once at the beginning of tournament
        pass

    def move(self, data):
        # called each betting round
        # data layout:
        # "self": {"hand": [...Card], "bet": int, "money": int}
        # "others": [...{"bet": int, "money": int, "folded": False}]
        # "pool": [...Card]
        # You should store or find any other data you want...
        # ...such as turn num, previous bet changes
        # return what you want to set your bet to (or F to fold)
        return data["self"]["bet"] + 1
    
    def cleanup(self, data):
        # called at end of a game
        # data contains the same as in self.move but you also have
        # access to the "hand" attribute of each element in "others"
        pass