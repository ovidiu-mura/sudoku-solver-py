#!/usr/bin/python3
# Copyright (c) 2018 Bart Massey
# [This program is licensed under the "MIT License"]
# Please see the file LICENSE in the source
# distribution of this software for license terms.


# Permutations via "backtracking".
# Derived from Skiena, Algorithm Design Handbook (2nd ed),
# pp. 231-

import copy
import random
import sys

from puzzle import Puzzle

p_noise = 0.5

class Sudoku(Puzzle):

    def __init__(self, filename):
        super(Sudoku, self).__init__(filename)
        self.init_free = set(self.free)
        self.bestv = None

    def restart(self):
        for cell in self.init_free:
            if cell in self.puzzle:
                self.remove(cell)
        hist = [0] * 9
        for cell in self.puzzle:
            hist[self.puzzle[cell] - 1] += 1
        missing = []
        for v in range(len(hist)):
            missing += [v + 1] * (9 - hist[v])
        random.shuffle(missing)
        for cell in self.init_free:
            self.add(cell, missing.pop())
        self.nviolations = self.defect_degree()

    def local_move(self, defect):
        print("violations:", self.nviolations)
        if self.bestv == None or self.nviolations < self.bestv:
            self.bestv = self.nviolations
            self.best = copy.deepcopy(self)
        if self.nviolations == 0:
            return True
        nvs = []
        for cell1 in self.init_free:
            for cell2 in self.init_free:
                if cell2 <= cell1:
                    continue
                nv = self.nviolations
                nv -= self.cell_defect_degree(cell1)
                nv -= self.cell_defect_degree(cell2)
                self.swap(cell1, cell2)
                nv += self.cell_defect_degree(cell1)
                nv += self.cell_defect_degree(cell2)
                nvs.append((nv - self.nviolations, (cell1, cell2)))
                self.swap(cell1, cell2)
        nvs.sort()
        if random.random() <= p_noise:
            dv, move = random.choice(nvs)
            cell1, cell2 = move
            self.swap(cell1, cell2)
            self.nviolations += dv
            return False
        bestdv, _ = nvs[0]
        best_moves = [move for dv, move in nvs if dv == bestdv]
        cell1, cell2 = random.choice(best_moves)
        self.swap(cell1, cell2)
        self.nviolations += bestdv
        return False

    def search(self):
        for _ in range(5):
            print("restart")
            self.restart()
            for _ in range(500):
                if self.local_move(self.defect_degree):
                    print("solution found")
                    print(self)
                    return
        assert self.bestv
        print("no solution found: violations =", self.bestv)
        print(self.best)

sudoku = Sudoku(sys.argv[1])
print(sudoku)
print()
sudoku.search()
