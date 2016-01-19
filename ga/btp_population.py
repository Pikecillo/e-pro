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

import heapq
import math
import random

from btp_chromosome import BTPChromosome

class BTPPopulation:

    def __init__(self, size, source, destination,
                 init_kind='simple', cost='linear'):
        self.size = size
        self.population = []
        self.source = source
        self.destination = destination
        self.init_kind = init_kind
        self.cost = cost

        # Create initial population
        self.genesis()
    
    # Create initial population
    def genesis(self):
        
        for i in xrange(self.size):
            chromosome = BTPChromosome(self.source, self.destination,
                                       self.init_kind, self.cost)
            individual = (chromosome.fitness(), chromosome)

            # The container is a min priority queue
            heapq.heappush(self.population, individual)

    # Adds a list of individuals to the population
    def add_individuals(self, offsprings):

        self.population += offsprings
        # Maintain heap condition
        heapq.heapify(self.population)

    # K-tournament selection
    def tournament(self, size, rep = 1):
        champions = []

        for i in xrange(rep):
            tournament = []
            
            # Randomly pick competing individuals
            for i in xrange(size):
                contestant = self.population[random.randrange(self.size)]
                heapq.heappush(tournament, contestant)

            champions.append(heapq.heappop(tournament))

        return champions
       
    # Individual with best fitness within population
    def best_fitted(self):
        return self.population[0]

    # Average fitness across population
    def avg_fitness(self):
        total = sum([individual[0] for individual in self.population])

        return total / len(self.population)

    # Meassure of the variability of the population
    def variability(self):
        avg = self.avg_fitness()

        var = sum([(individual[0] - avg) ** 2
                   for individual in self.population])

        return var / (len(self.population) - 1)

    # Keeps the fittest individuals and discards the rest
    # This is meant to be used when the new generation has been merged
    # with the new one and the size of the population has to be kept
    # fixed
    def keep_fittest(self):

        self.container = heapq.nsmallest(self.size, self.population)
        heapq.heapify(self.population)
