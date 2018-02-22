#!/usr/bin/python3
# Copyright (c) 2018 Bart Massey
# [This program is licensed under the "MIT License"]
# Please see the file LICENSE in the source
# distribution of this software for license terms.


# Sudoku puzzle board class with caching.

class Puzzle(object):
    def __init__(self, filename):
        self.puzzle = dict()
        row = 0
        with open(filename, "r") as f:
            for line in f:
                for col in range(len(line) - 1):
                    if line[col] != '.':
                        self.puzzle[(row, col)] = int(line[col])
                row += 1
        self.cells = {(i, j) for i in range(9) for j in range(9)}
        self.free = self.cells - set(self.puzzle.keys())

    def __str__(self):
        s = ""
        for r in range(9):
            for c in range(9):
                if (r, c) in self.puzzle:
                    s += str(self.puzzle[(r, c)])
                else:
                    s += '.'
            s += '\n'
        return s
