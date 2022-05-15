import unittest
import model

class Buchholz_test(unittest.TestCase):
    def test_get_score(self):

        self.assertEqual(True, False)  # add assertion here

class Sudoku_test(unittest.TestCase):
    def test_solve_sudoku(self):
        grid = [[6,1,2,3,4,5],
                [1,6,3,4,5,2],
                [2,3,6,5,1,4],
                [3,4,5,6,2,1],
                [4,5,1,2,6,3],
                [5,2,4,1,3,6]]

        grid1 = [[6,1,2,3,4,5],
                [1,6,3,4,5,2],
                [2,3,6,0,0,0],
                [3,4,0,6,0,0],
                [4,5,0,0,6,0],
                [5,2,0,0,0,6]]

        if (model.Round.Suduko(grid1, 0, 0)):
            model.Round.puzzle(grid1)

        self.assertEqual(grid,grid1)

        
        
if __name__ == '__main__':
    unittest.main()
