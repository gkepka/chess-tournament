from model.Match import Match

# Solves sudoku

M = 6


def puzzle(a):
    for i in range(M):
        for j in range(M):
            print(a[i][j], end=" ")
        print()


def solve(grid, row, col, num):
    for x in range(6):
        if grid[row][x] == num:
            return False

    for x in range(6):
        if grid[x][col] == num:
            return False

    return True


def Suduko(grid, row, col):
    if (row == M - 1 and col == M):
        return True
    if col == M:
        row += 1
        col = 0
    if grid[row][col] > 0:
        return Suduko(grid, row, col + 1)
    for num in range(1, M + 1, 1):

        if solve(grid, row, col, num):

            grid[row][col] = num
            if Suduko(grid, row, col + 1):
                return True
        grid[row][col] = 0
    return False

class Round:

    def __init__(self, tournament, round_no, round_id=None):
        self.__round_no = round_no
        self.matches = self.generate_matches()
        self.tournament = tournament
        self.round_id = round_id

    # Generates matches for the next round`

    def generate_matches(self):
        RoundGames = []
        n = self.tournament.maxRounds
        if n % 2 == 0:
            n = n + 1
        Games = [[0 for _ in range(n)] for _ in range(n)]
        for i in range(n):
            for j in range(n):
                if i == j:
                    Games[i][j] = n
        if (Suduko(Games, 0, 0)):
            puzzle(Games)
        else:
            print("Solution does not exist:(")
        if self.tournament.maxRounds % 2 == 1:
            for i in range(n):
                for (j) in range(n):
                    if i > j:
                        if Games[i][j] == self.__round_no:
                            if self.__round_no % 2 == 0:
                                Match1 = Match(self.tournament, self, self.tournament.params_list[i],
                                               self.tournament.params_list[j], None, None)
                                RoundGames.append(Match1)
                            else:
                                Match1 = Match(self.tournament, self, self.tournament.params_list[j],
                                               self.tournament.params_list[i], None, None)
                                RoundGames.append(Match1)
        else:
            for i in range(n):
                for (j) in range(n):
                    if i > j:
                        if Games[i][j] == self.__round_no:
                            if i != n - 1 and j != n - 1:
                                if self.__round_no % 2 == 0:
                                    Match1 = Match(self.tournament, self, self.tournament.params_list[i],
                                                   self.tournament.params_list[j], None, None)
                                    RoundGames.append(Match1)
                                else:
                                    Match1 = Match(self.tournament, self, self.tournament.params_list[j],
                                                   self.tournament.params_list[i], None, None)
                                    RoundGames.append(Match1)
        return RoundGames

    def get_round_no(self):
        return self.__round_no


if __name__ == '__main__':
    '''0 means the cells where no value is assigned'''
    grid = [[6, 1, 2, 3, 4, 5],
            [1, 6, 3, 4, 5, 2],
            [2, 3, 6, 0, 0, 0],
            [3, 4, 0, 6, 0, 0],
            [4, 5, 0, 0, 6, 0],
            [5, 2, 0, 0, 0, 6]]

    if (Suduko(grid, 0, 0)):
        puzzle(grid)
    else:
        print("Solution does not exist")