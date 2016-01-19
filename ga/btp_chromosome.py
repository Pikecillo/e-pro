#========================================================================
#
# Copyright (C) 2010. Mario Rincon-Nigro.
#
# This file is a part of E-Pro.
#
# E-Pro is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Flowie is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with E-Pro.  If not, see <http://www.gnu.org/licenses/>.
#
#========================================================================

import functools
import math
import random

from matrix import Matrix

class BTPConstraintViolationException(Exception):

    def __init__(self):
        self.msg = "BTP matrix does not comply with the " + \
            "provided constraints"

class BTPChromosome:
    
    # Cost functions
    function = {
        'linear':
            (lambda i, j, u: float(abs(i * j - 17) * u)),
        'quadratic':
            (lambda i, j, u: float(((i * i - j * j + 1) ** 2) * (u * u))),
        'general1':
            (lambda i, j, u: float(abs(i * j - 11) * math.sqrt(u))),
        'general2':
            (lambda i, j, u: float(abs(i * j - 17) * u + u ** 4)),
        }

    def __init__(self, source, destination, init=None, cost='linear'):
        self.source = source
        self.destination = destination
        self.cost = cost

        self.btp_matrix = Matrix(len(source), len(destination))

        # Initialize if requested
        if init:
            init_kind = {
                'simple': 0,
                'complex': 3
                }
            self.init([], init_kind[init])

    def __str__(self):
        str = (" " * 10)

        for i in xrange(len(self.destination)):
            str += "{0:10.2}".format(float(self.destination[i]))

        str += "\n"

        for i in xrange(self.btp_matrix.rows):
            str += "{0:10.2}".format(float(self.source[i]))
            for j in xrange(self.btp_matrix.cols):
                num = float(self.btp_matrix.matrix[i][j])
                str += "{0:10.2}".format(num)
            str += "\n"

        return str

    # Returns the fitness of this individual
    def fitness(self):
        
        mat = self.btp_matrix

        # Evaluate and accumulate results of the fitness function
        # across the matrix
        return sum([sum([BTPChromosome.function[self.cost](i, j, mat.at(i, j))
                         for j in xrange(mat.cols)])
                    for i in xrange(mat.rows)])
    
    # Check that the BTP matrix complies with the constraints
    def check_constraints(self):

        tolerance = 1E-6

        # Returns true if we can tolerate the error
        is_tolerable = lambda a, b: math.fabs(a - b) < tolerance
        # This sequence say for rows and cols if the
        # current solution is acceptable
        row_is_ok = map(is_tolerable,
                      self.btp_matrix.marginal_row(), self.source)
        col_is_ok = map(is_tolerable,
                      self.btp_matrix.marginal_col(), self.destination)

        and_op = lambda x, y: x and y

        return (functools.reduce(and_op, row_is_ok) and
                functools.reduce(and_op, col_is_ok))

    # For an element of the BTP matrix returns the maximum value
    # to which it can be set within constraints
    def delta(self, i, j):
        row = self.btp_matrix.marginal_row()
        col = self.btp_matrix.marginal_col()
        
        return min(self.source[i] - row[i],
                   self.destination[j] - col[j])

    # Initialization procedure: traverse the matrix in a random
    # order and assign, within constraints, a portion of the maximum
    # possible value. The portion depends on the value of the depth parameter
    def init(self, index_seq=[], depth=0):
        if index_seq:
            traversal = index_seq
        else:
            traversal = self.random_traversal()

        # Choose portion
        if depth:
            portion = random.uniform(0.0, 1.0)
        else:
            portion = 1.0

        # Assign always the maximum possible value
        for (i, j) in traversal:
            value = self.btp_matrix.at(i, j) + self.delta(i, j) * portion
            self.btp_matrix.set(i, j, value)

        if depth:
            self.init(traversal, depth - 1)
            return

        if not self.check_constraints():
            print sum(self.btp_matrix.marginal_row())
            print sum(self.btp_matrix.marginal_col())
            raise BTPConstraintViolationException()

    # Mutation operator. If parameter boundary is True an element
    # is changed to its maximum allowed value. Otherwise, it is changed
    # to a portion of its maximum allowed value
    def fixed_mutation(self, boundary=True):
        cell = (i, j) = self.random_element()

        # If boundary mutation set to maximum, otherwise set to a portion
        if boundary:
            portion = 1.0
            depth = 0
            traversal = self.random_traversal()
            traversal.remove(cell)
        else:
            portion = random.uniform(0.0, 1.0)
            depth = 3
            traversal = []
        
        self.btp_matrix.set_all(0)
        new_value = self.delta(i, j) * portion
        self.btp_matrix.set(i, j, new_value)

        # Rerun initialization with zero depth, ignoring that element
        self.init(traversal, 0)

    # This mutation operator selects a random submatrix and
    # reinitialize its values
    def submatrix_mutation(self, mutation_rate):

        selected_rows = [i for i in xrange(self.btp_matrix.rows)
                         if random.uniform(0.0, 1.0) < mutation_rate]
        selected_cols = [i for i in xrange(self.btp_matrix.cols)
                         if random.uniform(0.0, 1.0) < mutation_rate]

        # If no rows or columns were selected then return
        if not selected_rows or not selected_cols:
            return

        sources = [0 for i in selected_rows]
        destinations = [0 for i in selected_cols]

        # Calculate sources and destinations
        for i in xrange(len(selected_rows)):
            for j in xrange(len(selected_cols)):
                cell = (selected_rows[i], selected_cols[j])
                sources[i] += self.btp_matrix.at(*cell)
                destinations[j] += self.btp_matrix.at(*cell)

        small_chromosome = BTPChromosome(tuple(sources), tuple(destinations),
                                         'complex', self.cost)

        # Reset corresponding values
        for i in xrange(len(selected_rows)):
            for j in xrange(len(selected_cols)):
                args = (selected_rows[i], selected_cols[j],
                        small_chromosome.btp_matrix.at(i, j))
                self.btp_matrix.set(*args)
        
        if not self.check_constraints():
            raise BTPConstraintViolationException()

    # Crossover operator, the offspring is a convex combination of
    # the parents. It supports more than two parents
    def crossover(self, others):
        offspring = BTPChromosome(self.source, self.destination,
                                  False, self.cost)
        others.append(self)

        coeff = [random.uniform(0.3, 0.6) for i in others]
        total = sum(coeff)
        coeff = [c / total for c in coeff]

        mul = lambda a, b: a.btp_matrix * float(b)
        add = lambda a, b: a + b

        offspring.btp_matrix = functools.reduce(add, map(mul, others, coeff))

        if not offspring.check_constraints():
            raise BTPConstraintViolationException()

        return offspring

    # Picks a random element from the matrix
    def random_element(self):
        return (random.randrange(self.btp_matrix.rows),
                random.randrange(self.btp_matrix.cols))

    # Random sequence of indexes for visiting all elements of the matrix
    def random_traversal(self):
            
        traversal = []
        total_elements = self.btp_matrix.rows * self.btp_matrix.cols
        
        # Pick a random cell, if it hasn't been visited yet
        # then add it to the sequence
        while(total_elements):
            cell = self.random_element()
            
            if cell not in traversal:
                total_elements -= 1
                traversal.append(cell)
                
        return traversal

if __name__ == '__main__':
    c = BTPChromosome((14, 14, 14, 14, 14), (10, 10, 10, 10, 10, 10, 10),
                      'simple')

    print c
