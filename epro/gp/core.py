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

import epro.gp.tree
import epro.gp.operator
import epro.gp.protected

# Default parameter values
MAX_DEPTH = 30
INIT_DEPTH = 3
P_GROW = 1.0
POPULATION_SIZE=500
CROSSOVER_RATE=0.95

class GPPopulation:
    def __init__(self, size, tree_parameters,
                 max_depth=MAX_DEPTH,
                 init_depth=INIT_DEPTH,
                 p_grow=P_GROW):
        self.individuals = []
        self.tree_parameters = tree_parameters
        self.halfAndHalfInit(size, max_depth, init_depth, p_grow)

    def halfAndHalfInit(self, size, max_depth,
                        init_depth=INIT_DEPTH,
                        p_grow=P_GROW):

        # About half of the trees are initialized using the full method
        # The other half are grown and have about 100p_grow% of the
        # nodes of a full tree
        for i in range(size):
            grow = 1.0 if random.random() < 0.5 else p_grow
            tree = epro.gp.tree.Tree(self.tree_parameters, max_depth,
                                     init_depth, grow)
            self.individuals += [tree]

class GPSettings:
    def __init__(self, eval_func, population_size=POPULATION_SIZE,
                 mutation_rate=0.05, crossover_rate=0.95,
                 max_generations=200):
        self.eval_func = eval_func
        self.population_size = population_size
        self.reproduction_rate = 1 - mutation_rate - crossover_rate
        self.mutation_rate = mutation_rate
        self.crossover_rate = crossover_rate
        self.max_generations = max_generations

class GPEvaluator:
    
    def __init__(self, func, training_args, testing_args):
        self.func = func
        self.training_args = training_args
        self.testing_args = testing_args

    def evaluate(self, individual):
        individual.fitness = self.func(individual, self.training_args)
        return individual.fitness

    def testingError(self, individual):
        return self.func(individual, self.testing_args)

    def evaluatePopulation(self, population):

        for individual in population.individuals:
            self.evaluate(individual)

    def rank(self, population):
        self.evaluatePopulation(population)
        population.individuals.sort(key = lambda x: x.fitness)

    # K tournament with greedy overselection
    def select(self, population):
        rule_of_thumb = {1000: 0.32,
                         2000: 0.16,
                         4000: 0.08,
                         8000: 0.04};

        individuals = population.individuals
        boundary = int(0.32 * len(individuals))

        # 80% of time pick from top best and the rest
        # from the bottom
        if random.random() < 0.8:
            individuals = individuals[:boundary]
        else:
            individuals = individuals[boundary:]

        return self.kTournament(individuals, 2)

    def kTournament(self, individuals, k):
        return max([random.choice(individuals) for i in range(k)])

def evolution(population, genetic_operator_set, evaluator,
              generations, verbose=True):
    # A generational model is used for survival selection
    # This list keeps the best individual observed in each generation
    best_record = []
    
    for i in range(generations):
        new_generation = []

        evaluator.rank(population)

        if verbose:
            print "Generation " + str(i)
            best = population.individuals[0]
            best_record += [best]
            print "Training error: " + str(best.fitness)
            print "Testing error: " + str(evaluator.testingError(best))
            print "Function: " + str(best)
            print "Depth: " + str(best.root.height())
            print "--------------------------------------"

        while(len(new_generation) < len(population.individuals)):
            # Select genetic operator, as well as program(s) to apply
            # the operator, operate, and add to new generation
            genetic_operator = genetic_operator_set.select()
            selected_programs = [evaluator.select(population)
                                 for i in range(genetic_operator.arity)]
            new_generation += list(genetic_operator.apply(*selected_programs))

        # New generation
        population.individuals = new_generation
    
    best_record.sort(key = lambda x: evaluator.evaluate(x))

    return best_record[0]
