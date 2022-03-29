class Round:

    def __init__(self, tournament, round_no):
        self.__round_no = round_no
        self.matches = self.generate_matches(tournament)

    def generate_matches(self, tournament):
        return []
        # TODO
