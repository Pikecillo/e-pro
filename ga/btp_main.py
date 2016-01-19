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

from settings import *
from btp_population import BTPPopulation
from gen_algorithm import GenAlgorithm

def run_experiment(source, destination, parameter, seed):
    
    # Seed Mersenne twister
    random.seed(seed)

    population = BTPPopulation(parameter['population_size'],
                               source, destination,
                               parameter['init_kind'],
                               parameter['cost_kind'])

    GA = GenAlgorithm(population,
                      parameter['mutation_rate'],
                      parameter['crossover_rate'],
                      parameter['elitism'],
                      parameter['tournament_size'],
                      parameter['num_parents'],
                      parameter['mutation_kind'],
                      parameter['boundary_mutation'],
                      parameter['trace_file'],
                      parameter['stats_file'])
    GA.evolve(parameter['num_generations'])

def run_benchmarks():

    # First Transportation Problem
    source = (5, 5, 20, 15, 15)
    destination = (8, 8, 5, 5, 8, 20, 6)

    # Linear cost function
    parameter['cost_kind'] = 'linear'
    parameter['trace_file'] = 'trace_p1_linear.txt'
    parameter['stats_file'] = 'stats_p1_linear.txt'
    run_experiment(source, destination, parameter, seed)

    # Quadratic cost function
    parameter['cost_kind'] = 'quadratic'
    parameter['trace_file'] = 'trace_p1_quadratic.txt'
    parameter['stats_file'] = 'stats_p1_quadratic.txt'
    run_experiment(source, destination, parameter, seed)

    # General 1 cost function
    parameter['cost_kind'] = 'general1'
    parameter['trace_file'] = 'trace_p1_general1.txt'
    parameter['stats_file'] = 'stats_p1_general1.txt'
    run_experiment(source, destination, parameter, seed)

    # General 2 cost function
    parameter['cost_kind'] = 'general2'
    parameter['trace_file'] = 'trace_p1_general2.txt'
    parameter['stats_file'] = 'stats_p1_general2.txt'
    run_experiment(source, destination, parameter, seed)

    # Second Transportation Problem
    source = (14, 14, 14, 14, 14)
    destination = (10, 10, 10, 10, 10, 10, 10)

    # Linear cost function
    parameter['cost_kind'] = 'linear'
    parameter['trace_file'] = 'trace_p2_linear.txt'
    parameter['stats_file'] = 'stats_p2_linear.txt'
    run_experiment(source, destination, parameter, seed)

    # Quadratic cost function
    parameter['cost_kind'] = 'quadratic'
    parameter['trace_file'] = 'trace_p2_quadratic.txt'
    parameter['stats_file'] = 'stats_p2_quadratic.txt'
    run_experiment(source, destination, parameter, seed)

    # General 1 cost function
    parameter['cost_kind'] = 'general1'
    parameter['trace_file'] = 'trace_p2_general1.txt'
    parameter['stats_file'] = 'stats_p2_general1.txt'
    run_experiment(source, destination, parameter, seed)

    # General 2 cost function
    parameter['cost_kind'] = 'general2'
    parameter['trace_file'] = 'trace_p2_general2.txt'
    parameter['stats_file'] = 'stats_p2_general2.txt'
    run_experiment(source, destination, parameter, seed)

def run_mutation_experiment():

    parameter['evolution_kind'] = 'elitist'
    parameter['mutation_kind'] = 'fixed'

    # First Transportation Problem
    source = (5, 5, 20, 15, 15)
    destination = (8, 8, 5, 5, 8, 20, 6)

    # Boundary
    parameter['boundary_mutation'] = True
    parameter['trace_file'] = 'trace_fixed_b_linear.txt'
    parameter['stats_file'] = 'stats_fixed_b_linear.txt'
    run_experiment(source, destination, parameter, seed)

    # Non boundary
    parameter['boundary_mutation'] = False
    parameter['trace_file'] = 'trace_fixed_nb_linear.txt'
    parameter['stats_file'] = 'stats_fixed_nb_linear.txt'
    run_experiment(source, destination, parameter, seed)

def run_parent_experiment():

    parameter['num_parents'] = 2
    parameter['trace_file'] = 'trace_2par_linear.txt'
    parameter['stats_file'] = 'stats_2par_linear.txt'
    run_experiment(source, destination, parameter, seed)

    parameter['num_parents'] = 4
    parameter['trace_file'] = 'trace_4par_linear.txt'
    parameter['stats_file'] = 'stats_4par_linear.txt'
    run_experiment(source, destination, parameter, seed)

    parameter['num_parents'] = 5
    parameter['trace_file'] = 'trace_5par_linear.txt'
    parameter['stats_file'] = 'stats_5par_linear.txt'
    run_experiment(source, destination, parameter, seed)

def run_population_experiment():

    parameter['population_size'] = 50
    parameter['trace_file'] = 'trace_50pop_linear.txt'
    parameter['stats_file'] = 'stats_50pop_linear.txt'
    run_experiment(source, destination, parameter, seed)

    parameter['population_size'] = 150
    parameter['trace_file'] = 'trace_150pop_linear.txt'
    parameter['stats_file'] = 'stats_150pop_linear.txt'
    run_experiment(source, destination, parameter, seed)

    parameter['population_size'] = 200
    parameter['trace_file'] = 'trace_200pop_linear.txt'
    parameter['stats_file'] = 'stats_200pop_linear.txt'
    run_experiment(source, destination, parameter, seed)

def run_tournament_size_experiment():

    parameter['tournament_size'] = 5
    parameter['trace_file'] = 'trace_5tour_linear.txt'
    parameter['stats_file'] = 'stats_5tour_linear.txt'
    run_experiment(source, destination, parameter, seed)

    parameter['tournament_size'] = 10
    parameter['trace_file'] = 'trace_10tour_linear.txt'
    parameter['stats_file'] = 'stats_10tour_linear.txt'
    run_experiment(source, destination, parameter, seed)

    parameter['population_size'] = 25
    parameter['trace_file'] = 'trace_25tour_linear.txt'
    parameter['stats_file'] = 'stats_25tour_linear.txt'
    run_experiment(source, destination, parameter, seed)

if __name__ == '__main__':

    run_experiment(source, destination, parameter, seed)
    #run_benchmarks()
    #run_mutation_experiment()
    #run_parent_experiment()
    #run_tournament_size_experiment()
    #run_population_experiment()
