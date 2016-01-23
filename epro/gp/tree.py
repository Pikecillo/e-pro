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

import random
import string

"""
Tree node
"""
class TreeNode:
    def __init__(self):
        self.children = []
        self.parent = self

    """
    Returns height of tree for which this node is root
    """
    def height(self):
        if(not self.children):
            return 0
        
        # If node is internal its height is the maximum height
        # among its subtrees plus one
        return max([subtree.height()
                    for subtree in self.children]) + 1

    """
    Returns the depth of this node
    """
    def depth(self):
        depth = 0
        node = self

        while(not node.parent is node):
            node = node.parent
            depth = depth + 1

        return depth
    
    """
    Pre-order traversal for the tree for which this node is root
    """
    def preTraversal(self):
        order = [self]

        for child in self.children:
            order += child.preTraversal()

        return order

"""
Function node
"""
class FunctionNode(TreeNode):
    def __init__(self, function, children):
        TreeNode.__init__(self)
        self.function = function
        self.setChildren(children)

    """
    String representation of the internal node is a python expression
    ready to be evaluated
    """
    def __str__(self):
        function_name = self.function[0]
        arguments = [str(child) for child in self.children]

        return (function_name + "(%s)") % string.join(arguments, ",")

    """
    Set children of this node
    """
    def setChildren(self, children):
        self.children = children

        # Keep a reference to parent
        for child in self.children:
            child.parent = self

"""
Terminal node
"""
class TerminalNode(TreeNode):
    def __init__(self, value):
        TreeNode.__init__(self)
        self.value = value

    """
    The terminal node value should be a string already
    """
    def __str__(self):
        return self.value

    def evaluate(self):
        return self.value

class TreeInitParameters:
    def __init__(self, terminal_set, internal_set,
                 p_rand = 0.0, rand_bounds = (-1.0, 1.0)):
        self.terminal_set = terminal_set # List of terminal symbols
        self.internal_set = internal_set # List of functions
        self.p_rand = p_rand             # Prob of node to be random number
        self.rand_bounds = rand_bounds   # Bounds for those random numbers

"""
Syntactic tree
"""
class Tree:
    def __init__(self, parameters, max_height=30, init_depth=-1, p_full=0.0):
        self.root = None
        self.parameters = parameters
        self.fitness = None
        self.max_height = max_height

        # The default parameter creates an empty tree
        if init_depth >= 0:
            self.root = self.randomInit(init_depth, p_full).root

    def __str__(self):
        return str(self.root)

    """
    Compiling the expression before evaluation over the data set
    for efficiency
    """
    def getCompiledCode(self):
        try:
            return compile(str(self), '<string>', 'eval')
        except MemoryError:
            print "Warning: bloated tree. Depth %d" % self.height()
            return str(float('inf'))

    """
    Returns depth of the tree
    """
    def height(self):
        return self.root.height()

    """
    Returns a random tree with a maximum depth. It uses the same
    set of internal and terminal symbols of this tree.
    The initialization method is controlled through the p_full
    parameter. If it is one then a complete trees will always
    be created. Other values may allow non-complete trees. Trees
    will never exceed the maximum height
    """
    def randomInit(self, max_height, p_full=1.0):
        tree = Tree(self.parameters)

        # This function os meant to be called from outside the
        # class to generate random trees with the same properties
        # as this tree. This is for avoiding generating larger trees
        max_height = min(max_height, self.max_height)

        # Node is at maximum height so it has to be terminal
        if max_height == 0:
            terminal_set = self.parameters.terminal_set
            
            # Random numbers are allowed as terminals with a certain
            # probability
            if random.random() < self.parameters.p_rand:
                terminal = random.uniform(*self.parameters.rand_bounds)
            else:
                # Randomly pick the terminal symbol
                terminal = random.choice(terminal_set)
            
            tree.root = TerminalNode(str(terminal))
        else:
            # Randomly pick the function
            function = random.choice(self.parameters.internal_set)
            arity = function[1]
            # Pick the depth of subtrees according to initialization
            # method
            next_heights = [max_height - 1 if random.random() < p_full else 0
                           for i in range(arity)]
            # Create children
            children = [self.randomInit(next_heights[i], p_full).root
                        for i in range(len(next_heights))]

            tree.root = FunctionNode(function, children)

        return tree

    """
    Picks a random node (uniformly) which is root of a subtree
    with depth not larger than max_depth or height larger
    than max_height
    """
    def randomNode(self, max_depth=30, max_height=30):
        # Get list of nodes with labeled heights
        nodes = self.root.preTraversal()
        # Pick nodes complying with depth restriction
        valid_nodes = [node for node in nodes
                       if (node.depth() <= max_depth and \
                               node.height() <= max_height)]

        try:
            return random.choice(valid_nodes)
        except IndexError:
            print max_depth
            print len(nodes)
            print len(valid_nodes)

    # Substitute a node within the tree
    def substituteNode(self, old_node, new_node):
        # If the node is the root
        if old_node.parent is self.root:
            self.root = new_node
            new_node.parent = new_node
        else:
            siblings = old_node.parent.children
            siblings[siblings.index(old_node)] = new_node
            new_node.parent = old_node.parent
