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
import sys
import random

import settings

import gp.core
import gp.protected
import gp.tree
import gp.util

# This is the fitness function to be used to drive
# evolution. It is the average of the sum of squared prediction
# errors. The average is taken to make proper posterior
# comparisons between training and testing errors, since
# both data sets can have different sizes
def fitness_function(tree, data_set):
    tree_code = tree.getCompiledCode()
    sse = 0

    safe_function = gp.protected.GPFunction

    locals = {'add': safe_function.add,
              'sub': safe_function.sub,
              'mul': safe_function.mul,
              'div': safe_function.div,
              'pow': safe_function.pow,
              'sqrt': safe_function.sqrt,
              'log': safe_function.log,
              'log10': safe_function.log10,
              'sin': safe_function.sin,
              'cos': safe_function.cos,
              'tan': safe_function.tan,
              'exp': safe_function.exp,
              'min': safe_function.min,
              'max': safe_function.max}

    for item in data_set.data:
        locals['x'] = item[0]
        locals['y'] = item[1]
        locals['z'] = item[2]
        
        # Training error is predicted - ground truth
        training_error = eval(tree_code, {}, locals) - item[3]

        try:
            sse += (training_error ** 2)
        except Exception:
            return float('inf')

    return sse

def usage():
    print "Usage: regression.py training_set testing_set seed"

if __name__ == '__main__':
    if(len(sys.argv) != 4):
        usage()
        sys.exit(1)

    training_set = gp.util.CSVDataSet(sys.argv[1])
    test_set = gp.util.CSVDataSet(sys.argv[2])

    random.seed(int(sys.argv[3])) # 23 very good

    terminal_set = ['x', 'y', 'z']
    internal_set = [('add', 2), ('sub', 2), ('mul', 2), ('div', 2),
                    ('pow', 2), ('sqrt',1), ('abs', 1), ('log', 1),
                    ('log10', 1), ('sin', 1), ('cos', 1), ('tan', 1),
                    ('max', 2), ('min', 2)]
    parameters = gp.tree.GPTreeInitParameters(terminal_set,
                                              internal_set, 0.05)

    print "Creating population..................."
    population = gp.core.GPPopulation(size=settings.POPULATION_SIZE,
                                      tree_parameters=parameters,
                                      max_depth=settings.MAX_HEIGHT,
                                      init_depth=settings.INITIAL_DEPTH)
    evaluator = gp.core.GPEvaluator(fitness_function, training_set, test_set)

    print "Evolving.............................."
    best = gp.core.evolution(population, evaluator,
                             settings.GENERATIONS)

    tr_size = len(training_set.data)
    te_size = len(test_set.data)

    print "+++Best individual+++"
    print "\tTraining error: " + str(evaluator.evaluate(best) / tr_size)
    print "\tTesting error: " + str(evaluator.testingError(best) / te_size)
    print "\tLearnt function: " + best.getExpression()
