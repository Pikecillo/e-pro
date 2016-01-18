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

class GPOperator:

    # Crossover operator. If bloat is false the size of the offspring
    # will never be larger than that of their parents
    @staticmethod
    def crossover(parent1, parent2, bloat=False):
        # Clone both parents
        offspring1 = copy.deepcopy(parent1)
        offspring2 = copy.deepcopy(parent2)
        
        # Randomly pick first subtree
        subtree1 = offspring1.randomNode()

        # Bloat control. If bloat is allowed any node from the
        # second parent can be chosen
        if bloat:
            subtree2 = offspring2.randomNode()
        else:
            max_depth = offspring2.max_height - subtree1.getHeight()
            max_height = offspring1.max_height - subtree1.getDepth()
            subtree2 = offspring2.randomNode(max_depth, max_height)

        # Clone one of the subtrees
        clone = copy.copy(subtree2)
        # Update children references
        for child in clone.children:
            child.parent = clone

        # This'll do the swapping
        offspring1.substituteNode(subtree1, clone)
        offspring2.substituteNode(subtree2, subtree1)

        if offspring1.getHeight() > offspring1.max_height or\
                offspring2.getHeight() > offspring2.max_height:
            print "Crossover bloat"

        return (offspring1, offspring2)

    # Mutator operator. If bloat is false the size of the offspring
    # will never be larger than that of their parents
    @staticmethod
    def mutation(parent, bloat=False):
        # Clone parent
        offspring = copy.deepcopy(parent)
        # Pick random subtree
        subtree_root = offspring.randomNode()

        # Bloat control. If bloat allowed the new subtree can be
        # one level higher than old subtree
        if bloat:
            max_height = subtree_root.getHeight() + 1
        else:
            max_height = offspring.max_height - subtree_root.getDepth()

        # Substitute for a random subtree
        offspring.substituteNode(subtree_root,
                                 offspring.randomInit(max_height).root)
            
        if offspring.getHeight() > offspring.max_height:
            print "Mutation bloat"

        return offspring
