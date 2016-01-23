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

import copy
import random

class CDF:
    def __init__(self, histogram):
        mass = float(sum(histogram))
        self.pdf = [v / mass for v in histogram]
        p = 0.0
        self.cdf = []
        for v in self.pdf:
            self.cdf.append(p + v)
            p += v

    def rand(self):
        rand_num = random.random()
        bin = 0

        for p in self.cdf:
            if rand_num < p:
                return bin
            bin += 1

        return bin

class RandomSet:
    def __init__(self, elements, histogram):
        self.elements = elements
        self.cdf = CDF(histogram)
    
    def rand(self):
        return self.elements[self.cdf.rand()]

class GeneticOperatorSet:
    def __init__(self, operator_list, histogram):
        self.random_set = RandomSet(operator_list, histogram)

    def select(self):
        return self.random_set.rand()

class AbstractGeneticOperator:

    def __init__(self, arity):
        self.arity = arity

    def apply(self, *programs):
        pass

"""
Reproduction genetic operator
"""
class GeneticReproduction(AbstractGeneticOperator):
    def __init__(self):
        AbstractGeneticOperator.__init__(self, 1)

    def apply(self, *programs):
        return (copy.deepcopy(programs[0]),)

"""
Crossover genetic operator
"""
class GeneticCrossover(AbstractGeneticOperator):
    """
    If bloat is false the size of the offspring will never be larger
    than that of their parents
    """
    def __init__(self, bloat=False):
        AbstractGeneticOperator.__init__(self, 2)
        self.bloat = bloat

    """
    Apply the crossover operator
    """
    def apply(self, *programs):
        # Clone both parents
        offspring1 = copy.deepcopy(programs[0])
        offspring2 = copy.deepcopy(programs[1])

        # Randomly pick first subtree
        subtree1 = offspring1.randomNode()

        # Bloat control. If bloat is allowed any node from the
        # second parent can be chosen
        if self.bloat:
            subtree2 = offspring2.randomNode()
        else:
            max_depth = offspring2.max_height - subtree1.height()
            max_height = offspring1.max_height - subtree1.depth()
            subtree2 = offspring2.randomNode(max_depth, max_height)

        # Clone one of the subtrees
        clone = copy.copy(subtree2)
        # Update children references
        for child in clone.children:
            child.parent = clone

        # This'll do the swapping
        offspring1.substituteNode(subtree1, clone)
        offspring2.substituteNode(subtree2, subtree1)

        if offspring1.height() > offspring1.max_height or\
                offspring2.height() > offspring2.max_height:
            print "Crossover bloat"

        return (offspring1, offspring2)

"""
Mutation genetic operator
"""
class GeneticMutation(AbstractGeneticOperator):

    def __init__(self, bloat=False):
        AbstractGeneticOperator.__init__(self, 1)
        self.bloat = bloat
 
    """
    If bloat is false the size of the offspring will never be larger
    than that of their parents
    """
    def apply(self, *programs):
        # Clone parent
        offspring = copy.deepcopy(programs[0])
        # Pick random subtree
        subtree_root = offspring.randomNode()

        # Bloat control. If bloat allowed the new subtree can be
        # one level higher than old subtree
        if self.bloat:
            max_height = subtree_root.height() + 1
        else:
            max_height = offspring.max_height - subtree_root.depth()

        # Substitute for a random subtree
        offspring.substituteNode(subtree_root,
                                 offspring.randomInit(max_height).root)
            
        if offspring.height() > offspring.max_height:
            print "Mutation bloat"

        return (offspring,)
