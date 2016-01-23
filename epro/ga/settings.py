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

#
# Configuration file for the parameters of the balanced transportation
# problem genetic algorithm
#

# Mersenne twister seed
seed = 2010

# Balanced transportation problem capacities
# for sources and destinations
source = (5, 5, 20, 15, 15)
destination = (8, 8, 5, 5, 8, 20, 6)

# GA parameters
parameter = {}
parameter['population_size'] = 100
parameter['num_generations'] = 500
parameter['init_kind'] = 'simple' # complex | simple
parameter['mutation_rate'] = 0.9
parameter['crossover_rate'] = 0.1
parameter['elitism'] = 0.01
parameter['tournament_size'] = 20
parameter['num_parents'] = 3
parameter['mutation_kind'] = 'submatrix' # submatrix | fixed
parameter['boundary_mutation'] = False
parameter['evolution_kind'] = 'elitist' # elitist | free
parameter['cost_kind'] = 'general2' # linear | quadratic | general1 | general2 
parameter['trace_file'] = 'trace.txt'
parameter['stats_file'] = 'stats.txt'
