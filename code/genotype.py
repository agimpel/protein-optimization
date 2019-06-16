import logging

# custom modules
import constants



class genotype():

    LOGGER = None

    GENOTYPE = None
    ID = None
    FITNESS = None

    def __init__(self, genotype, id):
        
        # set up logger for this module
        self.LOGGER = logging.getLogger('genotype'); self.LOGGER.setLevel(logging.DEBUG)

        self.GENOTYPE = genotype
        self.ID = id

    @property
    def RESULT(self):
        return self._result

    @RESULT.setter
    def RESULT(self, RESULT): 
        self._result = RESULT
        self.FITNESS = 1/(RESULT.FITNESS+1)
