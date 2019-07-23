import logging
import signal
import sys
import time
import Bio.PDB
import random
from numba import jit

# custom modules
import constants
import filehandler
import fitnessfunction
from proteininterpreter import proteinInterpreter
from generation import generation
from genotype import genotype
from genetic_algorithm import GA


logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s\t%(levelname)s\t[%(name)s: %(funcName)s]\t%(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    handlers=[logging.FileHandler(constants.RUN_ARCHIVE_DIR + "log"), 
                    logging.StreamHandler()])

# setting of global minimum logging level
logging.disable(logging.NOTSET)

# set up logger for this module
LOGGER = logging.getLogger('main'); LOGGER.setLevel(logging.DEBUG)

GENETIC_ALGORITHM = GA()
MAX_GENERATIONS = 9999999
POPULATION_SIZE = 24
GENOTYPE_LENGTH = 5

@jit
def main(initial_population):
    population = initial_population
    best_result = 0

    for g in range(MAX_GENERATIONS):

        fitnessfunction.evaluate_generation(population)

        result = list()
        for phenotype in population:
            result.append(phenotype.FITNESS)
        best_fitness = max(result)
        if best_fitness > best_result:
            best_result = best_fitness
            filehandler.saveBestGenotypeFromGeneration(population)
        LOGGER.info("Generation "+str(g)+": fitness: "+str(best_fitness))
        
        population = GENETIC_ALGORITHM.generateNewPopulation(population)


def initialisePopulation():
    genotypes = [genotype("".join(random.choices(constants.GENE_LIST, k=GENOTYPE_LENGTH)), i) for i in range(POPULATION_SIZE)]
    # genotypes[0] = genotype("GIAAAACMSICSLYQLENPCN", 0)
    return generation(genotypes, 0)



# MAIN EXECUTION
# INFO:     run script as main, attach signal handling
# ARGS:     /
# RETURNS:  /
if __name__ == "__main__":

    filehandler.prepareOptimisation()
    initial_population = initialisePopulation()
    
    main(initial_population)
    # while True:
    #     fitnessfunction.evaluate_generation(initial_population)
    #     print(initial_population.GENOTYPES[0].FITNESS)
    #     time.sleep(1)