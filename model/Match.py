class Match:

    def __init__(self, player_white, player_black):
        self.player_white = player_white
        self.player_black = player_black
        self.result = None

    #Result from white player perspective

    def __init__(self, player_white, player_black, result):
        self.player_white = player_white
        self.player_black = player_black
        self.result = result

    def get_result(self):
        return self.result


    def set_result(self, result):
        self.result = result

