#!/usr/bin/python3
# Copyright (c) 2018 Bart Massey
# [This program is licensed under the "MIT License"]
# Please see the file LICENSE in the source
# distribution of this software for license terms.


# Sudoku puzzle IO support.

def read_puzzle(filename):
    puzzle = dict()
    row = 0
    with open(filename, "r") as f:
        for line in f:
            for col in range(len(line) - 1):
                if line[col] != '.':
                    puzzle[(row, col)] = int(line[col])
            row += 1
    return puzzle

def print_puzzle(puzzle):
    for r in range(9):
        s = ""
        for c in range(9):
            if (r, c) in puzzle:
                s += str(puzzle[(r, c)])
            else:
                s += '.'
        print(''.join(s))
