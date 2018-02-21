#!/usr/bin/python3
# Copyright (c) 2018 Bart Massey
# [This program is licensed under the "MIT License"]
# Please see the file LICENSE in the source
# distribution of this software for license terms.


# Permutations via "backtracking".
# Derived from Skiena, Algorithm Design Handbook (2nd ed),
# pp. 231-

import sys

from backtrack import State, backtrack

class Sudoku(State):

    def __init__(self, puzzle):
        self.puzzle = puzzle
        cells = {(i, j) for i in range(9) for j in range(9)}
        self.free = cells - set(puzzle.keys())
        self.ntries = 0

    def is_legal(self, cell, v):
        assert cell not in self.puzzle 
        row, col = cell
        for c in range(9):
            if (row, c) in self.puzzle and self.puzzle[(row, c)] == v:
                return False
        for r in range(9):
            if (r, col) in self.puzzle and self.puzzle[(r, col)] == v:
                return False
        rbox = row // 3
        cbox = col // 3
        for r in range(rbox * 3, (rbox + 1) * 3):
            for c in range(cbox * 3, (cbox + 1) * 3):
                if (r, c) in self.puzzle and self.puzzle[(r, c)] == v:
                    return False
        return True

    def legal_values(self, cell):
        candidates = []
        for v in range(1, 10):
            if self.is_legal(cell, v):
                candidates.append(v)
        return candidates

    def max_constrained(self):
        best_cell = None
        best_values = None
        for cell in self.free:
            vs = self.legal_values(cell)
            if best_values == None or len(vs) < len(best_values):
                best_cell = cell
                best_values = vs
        assert best_cell != None
        return (best_cell, best_values)

    def construct_candidates(self, a):
        next_cell, next_values = self.max_constrained()
        return ((next_cell, v) for v in next_values)

    def make_move(self, a):
        cell, v = a[-1]
        self.puzzle[cell] = v
        self.free.remove(cell)
        # self.print()
        # print()

    def unmake_move(self, a):
        cell, v = a[-1]
        del self.puzzle[cell]
        self.free.add(cell)

    def is_a_solution(self, a):
        self.ntries += 1
        return len(self.free) == 0

    def print(self):
        if self.ntries > 0:
            print("ntries:", self.ntries)
        for r in range(9):
            s = ""
            for c in range(9):
                if (r, c) in self.puzzle:
                    s += str(self.puzzle[(r, c)])
                else:
                    s += '.'
            print(''.join(s))

    def process_solution(self, a):
        self.print()
        self.finished = True

def read_sudoku(filename):
    puzzle = dict()
    row = 0
    with open(filename, "r") as f:
        for line in f:
            for col in range(len(line) - 1):
                if line[col] != '.':
                    puzzle[(row, col)] = int(line[col])
            row += 1
    return Sudoku(puzzle)

sudoku = read_sudoku(sys.argv[1])
sudoku.print()
print()
backtrack(sudoku, [])
