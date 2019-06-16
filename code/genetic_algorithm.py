import logging
import numpy as np
from numba import jit

# custom modules
import constants
from generation import generation
from genotype import genotype
import random


class GA():

    LOGGER = None

    # Settings
    ELITISM = 2

    CROSSOVER = True
    RANDOM_CROSSOVER_CUT = True
    CROSSOVER_CUT_POSITION = None

    MUTATION = True
    MUTATION_RATE = 0.05
    FORCE_MUTATION = 1

    POPULATION_SIZE = None
    GENOTYPE_LENGTH = None


    def __init__(self, settings = None):
        
        # set up logger for this module
        self.LOGGER = logging.getLogger('generation'); self.LOGGER.setLevel(logging.DEBUG)

        if settings is not None:
            pass


    @jit
    def generateNewPopulation(self, old_generation):
        self.POPULATION_SIZE = len(old_generation.GENOTYPES)
        self.GENOTYPE_LENGTH = len(old_generation.GENOTYPES[0].GENOTYPE)

        new_generation = list()
        new_generation_id = old_generation.ID+1

        if self.ELITISM is not 0:
            self._addElitism(new_generation, old_generation)

        if self.CROSSOVER is True:
            self._addCrossover(new_generation, old_generation)
        else:
            new_generation[self.ELITISM:] = [genotype.GENOTYPE for genotype in old_generation] 

        if self.MUTATION is True:
            self._addMutation(new_generation)

        print(new_generation)

        new_genotypes = [genotype(new_generation[i], i) for i in range(len(new_generation))]
        return generation(new_genotypes, new_generation_id)


    def _addElitism(self, new_generation, old_generation):
        fitness = [genotype.FITNESS for genotype in old_generation]
        for index in sorted(range(len(fitness)), key=lambda i: fitness[i], reverse=True)[:self.ELITISM]:
            new_generation.append(old_generation.GENOTYPES[index].GENOTYPE)
        for index in sorted(sorted(range(len(fitness)), key=lambda i: fitness[i])[:self.ELITISM], reverse=True):
            del old_generation.GENOTYPES[index]
        
    def _addCrossover(self, new_generation, old_generation):
        fitnesses = [genotype.FITNESS for genotype in old_generation]
        total_sum = sum(fitnesses)
        delta = np.array([[sum(fitnesses[0:n]), sum(fitnesses[0:n+1])] for n in range(len(fitnesses))])
        while len(new_generation) < self.POPULATION_SIZE:
            random_p1 = random.uniform(0, total_sum)
            p1 = np.where((delta[:,0] <= random_p1) & (delta[:,1] >= random_p1))[0][0]
            total_sum_new = total_sum - fitnesses[p1]
            delta_new = delta.copy()
            delta_new[p1+1:] = delta_new[p1+1:]-fitnesses[p1]
            delta_new[p1] = np.zeros(2)
            random_p2 = random.uniform(0, total_sum_new)
            p2 = np.where((delta_new[:,0] <= random_p2) & (delta_new[:,1] >= random_p2))[0][0]

            new_genotypes = self._crossoverFromParents(old_generation.GENOTYPES[p1].GENOTYPE, old_generation.GENOTYPES[p2].GENOTYPE)
            for genotype in new_genotypes:
                if True or genotype not in new_generation:
                    new_generation.extend([genotype])
        del new_generation[self.POPULATION_SIZE:]

    @jit
    def _crossoverFromParents(self, genotype1, genotype2):
        if self.RANDOM_CROSSOVER_CUT:
            cut = random.randint(1, self.GENOTYPE_LENGTH-1)
        else:
            cut = self.CROSSOVER_CUT_POSITION
        return genotype1[:cut]+genotype2[cut:], genotype2[:cut]+genotype1[cut:]

    @jit
    def _addMutation(self, new_generation):
        for genotype in range(self.ELITISM, self.POPULATION_SIZE):
            mutation_counter = 0
            for gene in range(self.GENOTYPE_LENGTH):
                if random.random() < self.MUTATION_RATE:
                    mutation_counter += 1
                    new_generation[genotype] = new_generation[genotype][:gene]+random.choice(constants.GENE_LIST)+new_generation[genotype][gene+1:]
            while self.FORCE_MUTATION is not False and mutation_counter < self.FORCE_MUTATION:
                mutation_counter += 1
                position = random.randrange(self.GENOTYPE_LENGTH)
                new_generation[genotype] = new_generation[genotype][:position]+random.choice(constants.GENE_LIST)+new_generation[genotype][position+1:]