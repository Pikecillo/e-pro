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

class Matrix:

    def __init__(self, rows, cols, initial = 0):
        self.rows = rows
        self.cols = cols
        
        # Initialize matrix
        self.set_all(initial)

    # Retuns a string representation of the matrix
    def __str__(self):
        return str(self.matrix)

    # Addition of two matrixes
    def __add__(self, other):
        add = Matrix(self.rows, self.cols)
        add.matrix = [[self.matrix[i][j] + other.matrix[i][j]
                       for j in xrange(self.cols)]
                      for i in xrange(self.rows)]

        return add

    # Multiplication by a scalar
    def __mul__(self, scalar):
        mul = Matrix(self.rows, self.cols)
        mul.matrix = [[scalar * self.matrix[i][j]
                       for j in xrange(self.cols)]
                      for i in xrange(self.rows)]

        return mul

    # Set all elements of a matrix to value
    def set_all(self, value):
        self.matrix = [[value for j in xrange(self.cols)]
                       for i in xrange(self.rows)]

    # Sets element at (i, j) to value
    def set(self, i, j, value):
        self.matrix[i][j] = value

    # Returns element at (i, j)
    def at(self, i, j):
        return self.matrix[i][j]

    # Returns the sum of elements in row i
    def sum_row(self, i):
        return sum(self.matrix[i])

    # Returns the sum of elements in row j
    def sum_col(self, j):
        s = 0
        return sum([self.matrix[i][j] for i in xrange(self.rows)])

    # Returns an array with the sum of all rows
    def marginal_row(self):
        return [self.sum_row(i) for i in xrange(self.rows)]

    # Returns an array with the sum of all columns
    def marginal_col(self):
        return [self.sum_col(j) for j in xrange(self.cols)]
