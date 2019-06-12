import logging

# custom modules
import constants



class generation():

    LOGGER = None

    GENOTYPES = None

    def __init__(self, genotypes):
        
        # set up logger for this module
        self.LOGGER = logging.getLogger('generation'); self.LOGGER.setLevel(logging.DEBUG)

        if type(genotypes) is not list:
            genotypes = [genotypes]
        self.GENOTYPES = genotypes


    def __iter__(self):
       for genotype in self.GENOTYPES:
           yield genotype
