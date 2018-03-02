#!/usr/bin/python3
# Copyright (c) 2018 Bart Massey
# [This program is licensed under the "MIT License"]
# Please see the file LICENSE in the source
# distribution of this software for license terms.


# Sudoku puzzle board class with caching.

class Cache(object):
    def __init__(self, puzzle, cells):
        self.puzzle = puzzle
        self.cells = cells
        self.free = self.puzzle.free & cells
        self.avail = set(range(1, 10))
        self.hist = [0] * 9
        for cell in self.cells:
            if cell in self.puzzle.puzzle:
                v = self.puzzle.puzzle[cell]
                self.avail.remove(v)
                self.hist[v - 1] += 1

    def add(self, cell, v):
        assert cell in self.free
        if v in self.avail:
            self.avail.remove(v)
        self.free.remove(cell)
        self.hist[v - 1] += 1

    def remove(self, cell):
        assert cell in self.cells
        assert cell not in self.free
        v = self.puzzle.puzzle[cell]
        self.free.add(cell)
        self.hist[v - 1] -= 1
        if self.hist[v - 1] == 0:
            self.avail.add(v)

    def defect_degree(self):
        nd = 0
        for n in self.hist:
            nd += max(n - 1, 0)
        return nd

    def defect_exists(self):
        for n in self.hist:
            if n > 1:
                return 1
        return 0

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
        self.init_cache()

    def init_cache(self):
        self.cols = dict()
        for c in range(9):
            cells = {(r, c) for r in range(9)}
            self.cols[c] = Cache(self, cells)
        self.rows = dict()
        for r in range(9):
            cells = {(r, c) for c in range(9)}
            self.rows[r] = Cache(self, cells)
        self.boxes = dict()
        for rbox in range(3):
            for cbox in range(3):
                cells = set()
                for r in range(rbox * 3, (rbox + 1) * 3):
                    for c in range(cbox * 3, (cbox + 1) * 3):
                        cells.add((r, c))
                self.boxes[(rbox, cbox)] = Cache(self, cells)

    def remove(self, cell):
        assert cell in self.puzzle
        assert cell not in self.free
        self.free.add(cell)
        r, c = cell
        self.cols[c].remove(cell)
        self.rows[r].remove(cell)
        self.boxes[(r // 3, c // 3)].remove(cell)
        v = self.puzzle[cell]
        del self.puzzle[cell]
        return v

    def add(self, cell, v):
        assert cell not in self.puzzle
        assert cell in self.free
        r, c = cell
        self.cols[c].add(cell, v)
        self.rows[r].add(cell, v)
        self.boxes[(r // 3, c // 3)].add(cell, v)
        self.puzzle[cell] = v
        self.free.remove(cell)

    def swap(self, cell1, cell2):
        assert cell1 != cell2
        v1 = self.remove(cell1)
        v2 = self.remove(cell2)
        self.add(cell1, v2)
        self.add(cell2, v1)

    def defect_degree(self):
        nd = 0
        for c in range(9):
            nd += self.cols[c].defect_degree()
        for r in range(9):
            nd += self.rows[r].defect_degree()
        for r in range(3):
            for c in range(3):
                nd += self.boxes[(r, c)].defect_degree()
        return nd

    def cell_defect_degree(self, cell):
        r, c = cell
        nd = 0
        nd += self.cols[c].defect_degree()
        nd += self.rows[r].defect_degree()
        nd += self.boxes[(r // 3, c // 3)].defect_degree()
        return nd

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
