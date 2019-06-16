import logging

# custom modules
import constants



class generation():

    LOGGER = None

    GENOTYPES = None
    ID = None

    def __init__(self, genotypes, id = 1):
        
        # set up logger for this module
        self.LOGGER = logging.getLogger('generation'); self.LOGGER.setLevel(logging.DEBUG)

        if type(genotypes) is not list:
            genotypes = [genotypes]
        self.GENOTYPES = genotypes
        self.ID = id


    def __iter__(self):
       for genotype in self.GENOTYPES:
           yield genotype
