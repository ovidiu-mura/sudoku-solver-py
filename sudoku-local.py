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

def hist(values):
    h = [0] * 9
    for v in values:
        h[v - 1] += 1
    return h

def defect_degree(values):
    nd = 0
    h = hist(values)
    for n in h:
        nd += max(n - 1, 0)
    return nd

def defect_count(values):
    h = hist(values)
    for n in h:
        if n != 1:
            return 1
    return 0

class Sudoku(Puzzle):

    def __init__(self, filename):
        super(Sudoku, self).__init__(filename)
        self.bestv = None

    def restart(self):
        for cell in self.free:
            if cell in self.puzzle:
                del self.puzzle[cell]
        start_vs = [self.puzzle[cell] for cell in self.puzzle]
        h = hist(start_vs)
        missing = []
        for v in range(9):
            missing += [v + 1] * (9 - h[v])
        random.shuffle(missing)
        for cell in self.free:
            self.puzzle[cell] = missing.pop()

    def swap(self, cell1, cell2):
        self.puzzle[cell1], self.puzzle[cell2] = \
            self.puzzle[cell2], self.puzzle[cell1]

    def violations(self, defect):
        nd = 0
        for c in range(9):
            values = [self.puzzle[(r, c)] for r in range(9)]
            nd += defect(values)
        for r in range(9):
            values = [self.puzzle[(r, c)] for c in range(9)]
            nd += defect(values)
        for rbox in range(3):
            for cbox in range(3):
                values = []
                for r in range(rbox * 3, (rbox + 1) * 3):
                    for c in range(cbox * 3, (cbox + 1) * 3):
                        values.append(self.puzzle[(r, c)])
                nd += defect(values)
        return nd

    def local_move(self, defect):
        nv0 = self.violations(defect)
        if nv0 == 0:
            return True
        print("violations:", nv0)
        if self.bestv == None or nv0 < self.bestv:
            self.bestv = nv0
            self.best = copy.deepcopy(self)
        nvs = []
        for cell1 in self.free:
            for cell2 in self.free:
                if cell2 < cell1:
                    continue
                self.swap(cell1, cell2)
                nv = self.violations(defect)
                nvs.append((nv, (cell1, cell2)))
                self.swap(cell1, cell2)
        nvs.sort()
        bestv, _ = nvs[0]
        if random.random() <= p_noise:
            _, move = random.choice(nvs)
            cell1, cell2 = move
            self.swap(cell1, cell2)
            return False
        best_moves = [move for v, move in nvs if v == bestv]
        cell1, cell2 = random.choice(best_moves)
        self.swap(cell1, cell2)
        return False

    def search(self):
        for _ in range(5):
            print("restart")
            self.restart()
            for _ in range(500):
                if self.local_move(defect_degree):
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
