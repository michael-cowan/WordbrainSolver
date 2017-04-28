import unittest
import time
import numpy as np
import wordbrain_solver as WBS

class Test_test1(unittest.TestCase):
    def test_solver(self):
        w = WBS.WordBrainSolver()
        w.choose_word_ls()
        w.init_board = np.array([list('nnlaa'), list('onant'), list('nntpe'), list('gnapi'), list('siecg')])
        w.board_int = np.arange(w.init_board.size).reshape(w.init_board.shape)
        w.init_movetree = w.make_move_tree(w.init_board)
        w.word_lengths = [5, 6, 4, 3, 7]
        start = time.time()
        w.solution(w.init_board, 0)
        end = time.time()

        # If no words were returned assert failure
        self.failIfEqual(len(w.answer), 0)

        print("Completed in %f seconds." %(end - start))
        print("Solution:")
        for word in w.answer:
            print(word.rjust(25))

if __name__ == '__main__':
    unittest.main()
