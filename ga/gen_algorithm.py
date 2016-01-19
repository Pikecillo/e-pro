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

# Genetic algorithm class
class GenAlgorithm:

    def __init__(self, population, mutation_rate=0.9,
                 crossover_rate=0.1, elitism=0.05,
                 tournament_size=20, num_parents=2,
                 mutation_kind='submatrix', boundary_mutation=True,
                 trace_file='trace.txt', stats_file='stats.txt'):
        self.population = population

        self.mutation_rate = mutation_rate
        self.crossover_rate = crossover_rate
        self.elitism = elitism
        self.tournament_size = tournament_size
        self.num_parents = num_parents
        self.mutation_kind = mutation_kind
        self.boundary_mutation = boundary_mutation
        
        self.current_generation = 0
        self.num_gen_ops = 0

        self.trace_file = open(trace_file, 'w')
        self.stats_file = open(stats_file, 'w')

    # Evolve population for a number of generations.
    # The crossover and mutation rates, vary only during the
    # initial 80% of the generations
    def evolve(self, num_generations, kind='elitist'):
        range_mutation = 0.8
        range_crossover = 0.8
        delta_mutation = ((0.3 - self.mutation_rate) /
                           (range_mutation * num_generations))
        delta_crossover = ((1.0 - self.crossover_rate) /
                           (range_crossover * num_generations))

        for i in xrange(num_generations):
            self.current_generation = i
            
            self.store_stats()
            self.store_trace()

            if kind == 'elitist':
                self.elite_generation()
            else:
                self.free_generation()
            
            # Update mutation rate
            if self.mutation_rate + delta_mutation > 0.3:
                self.mutation_rate += delta_mutation
            else:
                self.mutation_rate = 0.3

            # Update crossover rate
            if self.crossover_rate + delta_crossover < 1.0:
                self.crossover_rate += delta_crossover
            else:
                self.crossover_rate = 1.0

            self.num_gen_ops = 0

        self.store_stats()
        self.store_trace()

    # One generation
    def elite_generation(self):

        new_generation = []
        increase = int(self.population.size * (1 - self.elitism))

        # Increase population
        for i in xrange(increase):
            # Select parents through k-tournaments
            parent_tuplist = self.population.tournament(self.tournament_size,
                                                        self.num_parents)
            parents = [pt[1] for pt in parent_tuplist]

            # Always crossover in elite generations
            offspring = parents[0].crossover(parents[1:])
            self.num_gen_ops += 1

            # Mutation
            if self.mutation_kind == 'submatrix':
                offspring.submatrix_mutation(self.mutation_rate)
                self.num_gen_ops += 1
            else:
                if(random.uniform(0.0, 1.0) < self.mutation_rate):
                    offspring.fixed_mutation(self.boundary_mutation)
                    self.num_gen_ops += 1

            individual = (offspring.fitness(), offspring)

            new_generation.append(individual)

        # Merge the new generation with the old generation
        self.population.add_individuals(new_generation)
        # Keep only the fitest individuals.
        self.population.keep_fittest()

    def free_generation(self):

        # Keep the best solution
        new_generation = [self.population.best_fitted()]
        
        for i in xrange(self.population.size - 1):
            
            # Select parents through k-tournaments
            parent_tuplist = self.population.tournament(self.tournament_size,
                                                        self.num_parents)
            parents = [pt[1] for pt in parent_tuplist]

            # If a crossover is due
            if(random.uniform(0.0, 1.0)< self.crossover_rate):
                offspring = parents[0].crossover(parents[1:])
                self.num_gen_ops += 1
            else:
                offspring = parents[0]

            # Mutation
            if self.mutation_kind == 'submatrix':
                offspring.submatrix_mutation(self.mutation_rate)
                self.num_gen_ops += 1
            else:
                if(random.uniform(0.0, 1.0) < self.mutation_rate):
                    offspring.fixed_mutation(self.boundary_mutation)
                    self.num_gen_ops += 1

            individual = (offspring.fitness(), offspring)

            new_generation.append(individual)

        # Merge the new generation with the old generation
        self.population.add_individuals(new_generation)
        # Keep only the fitest individuals.
        self.population.keep_fittest()

    def store_trace(self):
        best = self.population.best_fitted()

        self.trace_file.write("Generation " +  str(self.current_generation))
        self.trace_file.write(": cost function=" + str(self.population.cost))
        self.trace_file.write(" cost=" + str(best[0]) + "\n")
        self.trace_file.write(str(best[1]))
        self.trace_file.write("-" * 80 + "\n")
        

    def store_stats(self):
        line = str(self.current_generation) + " " + \
            str(self.population.best_fitted()[0]) + " " + \
            str(self.population.avg_fitness()) + " " + \
            str(self.population.variability()) + " " + \
            str(self.num_gen_ops) + " " + \
            str(self.mutation_rate) + " " + \
            str(self.crossover_rate)

        print line
        self.stats_file.write(line + "\n")
