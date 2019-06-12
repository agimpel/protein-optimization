import logging

# custom modules
import constants



class genotype():

    LOGGER = None

    GENOTYPE = None
    FITNESS = None

    def __init__(self, genotype):
        
        # set up logger for this module
        self.LOGGER = logging.getLogger('genotype'); self.LOGGER.setLevel(logging.DEBUG)

        self.GENOTYPE = genotype

    @property
    def RESULT(self):
        return self._result

    @RESULT.setter
    def RESULT(self, RESULT): 
        self._result = RESULT
        self.FITNESS = RESULT.FITNESS
