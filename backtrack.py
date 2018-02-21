#!/usr/bin/python3
# Copyright (c) 2018 Bart Massey
# [This program is licensed under the "MIT License"]
# Please see the file LICENSE in the source
# distribution of this software for license terms.

# Backtracking code with examples.
# Derived from Skiena, Algorithm Design Handbook (2nd ed),
# pp. 231-

from abc import ABC, abstractmethod

# State for search, containing methods for
# search operations and maybe some auxiliary data.

class State(ABC):
    finished = False

    def __init__(self):
        assert False

    @abstractmethod
    def is_a_solution(self, a):
        pass

    @abstractmethod
    def construct_candidates(self, a):
        pass

    @abstractmethod
    def process_solution(self, a):
        pass

    def make_move(self, a):
        pass

    def unmake_move(self, a):
        pass

# Backtracking search. Given a model for the search and a
# partial solution in a, try to extend a to total solutions.
def backtrack(model, a):
    if model.is_a_solution(a):
        model.process_solution(a)
        return
    for c in model.construct_candidates(a):
        a.append(c)
        model.make_move(a)
        backtrack(model, a)
        model.unmake_move(a)
        a.pop()
        if model.finished:
            return
