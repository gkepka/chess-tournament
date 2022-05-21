class Match:

    # Result from white player perspective

    def __init__(self, tournament, round, player_white, player_black, result, match_id = None):
        self.tournament = tournament
        self.round = round
        self.player_white = player_white
        self.player_black = player_black
        self.result = result
        self.match_id = match_id

    def get_result(self):
        return self.result

    def set_result(self, result):
        self.result = result
