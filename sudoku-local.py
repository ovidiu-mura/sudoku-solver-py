#!/usr/bin/python3
# Copyright (c) 2018 Bart Massey
# [This program is licensed under the "MIT License"]
# Please see the file LICENSE in the source
# distribution of this software for license terms.


# Permutations via "backtracking".
# Derived from Skiena, Algorithm Design Handbook (2nd ed),
# pp. 231-

import copy
import math
import random
import sys

from puzzle import Puzzle

class Sudoku(Puzzle):

    def __init__(self, filename, restarts, steps, pnoise):
        super(Sudoku, self).__init__(filename)
        self.init_free = set(self.free)
        self.bestv = None
        self.restarts = restarts
        self.steps = steps
        self.pnoise = pnoise

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
        if self.bestv == None or self.nviolations < self.bestv:
            print("bestv:", self.nviolations)
            self.bestv = self.nviolations
            self.best = copy.deepcopy(self)
        else:
            print("nv:", self.nviolations)
        if self.nviolations == 0:
            return True
        neighbors = []
        for cell1 in self.init_free:
            for cell2 in self.init_free:
                if cell2 <= cell1:
                    continue
                if self.puzzle[cell1] == self.puzzle[cell2]:
                    continue
                nv = self.nviolations
                nv -= self.cell_defect_degree(cell1)
                nv -= self.cell_defect_degree(cell2)
                self.swap(cell1, cell2)
                nv += self.cell_defect_degree(cell1)
                nv += self.cell_defect_degree(cell2)
                neighbors.append((nv, (cell1, cell2)))
                self.swap(cell1, cell2)
        neighbors.sort()
        bestnv, _ = neighbors[0]
        if bestnv > 0 and random.random() <= self.pnoise:
            weights = [1.0 / math.sqrt(dv) for dv, _ in neighbors]
            [(nv, move)] = random.choices(neighbors, weights=weights)
            cell1, cell2 = move
            nviolations = nv
        else:
            best_moves = [move for nv, move in neighbors if nv == bestnv]
            cell1, cell2 = random.choice(best_moves)
            nviolations = bestnv
        self.swap(cell1, cell2)
        self.nviolations = nviolations
        return False

    def search(self):
        for _ in range(self.restarts):
            print("restart")
            self.restart()
            for _ in range(self.steps):
                if self.local_move(self.defect_degree):
                    print("solution found")
                    print(self)
                    return
        assert self.bestv
        print("no solution found: violations =", self.bestv)
        print(self.best)

sudoku = Sudoku(sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), float(sys.argv[4]))
print(sudoku)
print()
sudoku.search()
