import numpy as np
from string import lowercase as letts
from time import time

class WordBrainSolver:

    def __init__(self):
        self.init_board = np.array([])
        self.board_int = np.array([])

        self.init_movetree = dict()

        self.side_length = 0

        self.word_ls = []
        self.word_lengths = []
        self.answer = []

        self.solved = False


    def load_word_ls(self, wl):
        with open(wl, 'r') as fid:
            self.word_ls = {w.replace('\n', '') for w in fid.readlines()}


    def choose_word_ls(self, ion = False, path = 'wordbrain_words.txt'):
        if ion:
            while 1:
                print "1:  wordbrain_words.txt\n"
                print "2:  words.txt\n\n"
                try:
                    ans = int(raw_input("Please choose word list (1 or 2): "))
                    wl = 'wordbrain_words.txt' if ans == 1 else 'words.txt'
                    break
                except:
                    raw_input("Incorrect input please try again.")
                    print '\n'*25
            self.load_word_ls(wl)
        else:
            self.load_word_ls(path)


    def is_board_made(self):
        if self.init_board.size != 0:
            return True
        else:
            raise ValueError("The board is not defined. Use the 'make_board' method.")
            

    def num2let(self, n, board):
        self.is_board_made()

        return board[n / board.shape[0],
                     n % board.shape[0]]


    def make_board(self):
        while 1:
            try:
                self.side_length = int(raw_input("\n\nSize of board (n x n), n = "))
                break
            except ValueError:
                print '\nInput must be an integer.\n\n'

        letters = []
        ind = 0
        while ind != self.side_length:
            letters += [raw_input("\nLetters in Row %s: " %(str(ind + 1)))]
            if len(letters[ind]) != self.side_length:
                letters.pop(ind)
                print "\n\nWrong Number of Letters in Row %s.\n\n" %(str(ind + 1))
            else:
                ind += 1

        self.init_board = np.array([list(str(s)) for s in letters])
        self.board_int = np.arange(self.init_board.size).reshape(self.init_board.shape)

        print '\n' * 2
        self.init_movetree = self.make_move_tree(self.init_board)
        return


    def get_word_lengths(self):
        while 1:
            try:
                self.word_lengths = map(int,
                                    raw_input("Input word lengths separated by commas: ").replace(' ','').split(','))
                if sum(self.word_lengths) != sum([1 for i in self.init_board.flatten() if i != ' ']):
                    print "\n\nNumber of letters doesn't match the size of the board."
                    raise ValueError
                return
            except ValueError:
                print '\nIncorrect input, please try again.\n\n'
            else:
                return


    def make_move_tree(self, board):
        self.is_board_made()
        moves = np.array([[i,j] for i in [1,0,-1] for j in [1,0,-1] if i or j])
        d = {}
        for r in xrange(len(self.board_int)):
            for c in xrange(len(self.board_int)):
                ar = np.array([r,c])
                ls = []
                if board[r, c] != ' ':
                    for m in (moves + ar):
                        try:
                            if -1 not in m:
                                num = self.board_int[m[0], m[1]]
                                if num != self.board_int[r, c] and board[m[0], m[1]] != ' ':
                                    ls.append(num)
                        except:
                            continue

                d[self.board_int[r,c]] = ls

        return d


    def search4word(self, start, length, movetree, board):
        tree = {i: iter(movetree[i]) for i in movetree}
        word = self.num2let(start, board)
        search_ls = {w for w in self.word_ls if w.startswith(word) and len(w) == length}
        parent = start
        done = False
        mapper = [start]
        sol = dict()
        while not done:
            try:
                child = tree[parent].next()

                if child in mapper:
                    continue

                mapper.append(child)
                word += self.num2let(child, board)

            except:
                tree[parent] = iter(movetree[parent])
                word = word[:-1]
                mapper.pop(-1)
                if parent == start:
                    done = True
                else:
                    parent = mapper[-1]
                continue

            test = {w for w in search_ls if w.startswith(word)}
            if test:
                parent = child
            else:
                word = word[:-1]
                mapper.pop(-1)
                continue


            if len(word) == length:
                if word in test:
                    if word in sol:
                        sol[word] = [i for i in sol[word]] + [[i for i in mapper]]
                    else:
                        sol[word] = [[i for i in mapper]]
                    

                word = word[:-1]
                mapper.pop(-1)
                parent = mapper[-1]


        return sol


    def find_words(self, length, board):
        ans = dict()
        movetree = self.make_move_tree(board)
        for spot in movetree:
            solut = self.search4word(spot, length, movetree, board)
            for w in solut:
                if w not in ans.keys():
                    ans[w] = [i for i in solut[w]]
                else:
                    ans[w] = ans[w] + [i for i in solut[w]]

        return ans


    def update_board(self, nums, board):
        for c in xrange(len(board)):
            for r in xrange(len(board)):
                if self.board_int[r, c] in nums:
                    board[:r+1, c] = [' '] + list(board[:r, c])

        return board


    def solution(self, bd, j):
        word_dict = self.find_words(self.word_lengths[j], bd)
        if not word_dict:
            return
        else:
            for w in word_dict:
                self.answer.append(w)
                for v in word_dict[w]:
                    b = self.update_board(v, bd.copy())
                    if not (' ' == b).all():
                        self.solution(b, j+1)
                    else:
                        self.solved = True
                        return
                    if self.solved:
                        return
                else:
                    self.answer.pop()


#######################################################################################################


def main():
    w = WordBrainSolver()
    w.choose_word_ls()
    w.make_board()
    w.get_word_lengths()
    start = time()
    w.solution(w.init_board, 0)
    tot = time() - start
    if len(w.answer) == 0:
        print("\n\nNo solution could be found.")
    else:
        with open('wb_solver_times.txt', 'a') as fid:
            fid.write(', '.join([str(i) for i in w.word_lengths]) + ' ')
            
            fid.write(str(tot) + '\n')

            print "\n"*20 + "Solution:\n"
            for word in w.answer:
                print word.rjust(25)
            
            print '\nTotal solution time: %s sec' %(str(round(tot, 2)))
    print '\n'*13
    if 'y' in raw_input("Solve the next puzzle? (y / n):  ").lower():
        print '\n'*30
        main()


if __name__ == '__main__':
    main()