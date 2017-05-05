import unittest
import time
import numpy as np
import wordbrain_solver as WBS

EASY_LEVEL = 'Lion-13'

EASY_BOARD = np.array([
    list('nnlaa'),
    list('onant'),
    list('nntpe'),
    list('gnapi'),
    list('siecg')
    ])

EASY_WORD_LENGTHS = [
    5, 6, 4,
    3, 7
    ]

EASY_ANSWERS = [
    'petal', 'cannon', 'sign', 
    'pig', 'antenna'
    ]





HARD_LEVEL = 'Unicorn-20'

HARD_BOARD = np.array([
    list('trssehca'), 
    list('hmoemree'),
    list('islsiepp'),
    list('nalpilpc'),
    list('koensile'),
    list('stiesssc'), 
    list('qhetmtia'), 
    list('uesantfw')
    ])

HARD_WORD_LENGTHS = [
    4, 4, 8,
    3, 5, 5,
    7, 6, 7,
    5, 5, 5
    ]

HARD_ANSWERS = [
    'face', 'moss', 'question', 
    'hen', 'smell', 'steak',
    'panties', 'pepper', 'missile',
    'scale', 'witch', 'shirt'
    ]

class Test_test1(unittest.TestCase):
    def test_easy(self):
        self.setup(EASY_BOARD, EASY_WORD_LENGTHS)

    def test_hard(self):
        self.setup(HARD_BOARD, HARD_WORD_LENGTHS)

    def setup(self, board, word_lengths):
        w = WBS.WordBrainSolver()
        w.choose_word_ls()

        w.init_board = board
        w.board_int = np.arange(w.init_board.size).reshape(w.init_board.shape)

        w.init_movetree = w.make_move_tree(w.init_board)
        w.word_lengths = word_lengths

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
