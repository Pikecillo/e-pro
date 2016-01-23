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

import math

class GPFunction:

    @staticmethod
    def add(x, y):
        try:
            return float(x) + y
        except (ValueError, OverflowError):
            return 0.0

    @staticmethod
    def sub(x, y):
        try:
            return float(x) - y
        except (ValueError, OverflowError):
            return 0.0

    @staticmethod
    def mul(x, y):
        try:
            return float(x) * y
        except (ValueError, OverflowError):
            return 0.0

    @staticmethod
    def div(x, y):
        try:
            return float(x) / y
        except ZeroDivisionError:
            return 1.0

    @staticmethod
    def pow(x, y):
        try:
            return float(x) ** y
        except (ValueError, OverflowError, ZeroDivisionError):
            return 1.0
    
    @staticmethod
    def sqrt(x):
        try:
            return math.sqrt(math.fabs(x))
        except (ValueError, OverflowError):
            return 1.0

    @staticmethod
    def log(x):
        try:
            return math.log(math.fabs(x))
        except (ValueError, OverflowError):
            return 1.0

    @staticmethod
    def log10(x):
        try:
            return math.log10(math.fabs(x))
        except (ValueError, OverflowError):
            return 1.0

    @staticmethod
    def exp(x):
        try:
            return math.tan(x)
        except (ValueError, OverflowError):
            return 1.0

    @staticmethod
    def sin(x):
        try:
            return math.sin(x)
        except (ValueError, OverflowError):
            return 1.0

    @staticmethod
    def cos(x):
        try:
            return math.cos(x)
        except (ValueError, OverflowError):
            return 1.0
        
    @staticmethod
    def tan(x):
        try:
            return math.tan(x)
        except (ValueError, OverflowError):
            return 1.0

    @staticmethod
    def abs(x):
        try:
            return abs(x)
        except (ValueError, OverflowError):
            return 1.0

    @staticmethod
    def min(x, y):
        try:
            return min(x, y)
        except (ValueError, OverflowError):
            return 1.0

    @staticmethod
    def max(x, y):
        try:
            return max(x, y)
        except (ValueError, OverflowError):
            return 1.0
