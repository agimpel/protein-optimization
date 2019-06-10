import logging
import signal
import sys
import time
import Bio.PDB

# custom modules
import constants
import filehandler
import fitnessfunction
from proteininterpreter import proteinInterpreter

class Main():

    # __init__
    # INFO:     Sets up logging and threads of this program.
    # ARGS:     -
    # RETURNS:  -
    def __init__(self):

        # set-up of general logging
        logging.basicConfig(level=logging.INFO,
                            format='%(asctime)s\t%(levelname)s\t[%(name)s: %(funcName)s]\t%(message)s',
                            datefmt='%Y-%m-%d %H:%M:%S',
                            handlers=[logging.FileHandler(constants.RUN_ARCHIVE_DIR + "log"), logging.StreamHandler()])

        # setting of global minimum logging level
        logging.disable(logging.NOTSET)

        # start services
        logging.info('starting threads')


        # set-up for logging of work. Level options: DEBUG, INFO, WARNING, ERROR, CRITICAL
        self.loglevel = logging.INFO
        self.logtitle = 'main'
        self.logger = logging.getLogger(self.logtitle)
        self.logger.setLevel(self.loglevel)

    def stop(self):
        self.logger.info("Stopping main thread")
        sys.exit()



# MAIN EXECUTION
# INFO:     run script as main, attach signal handling
# ARGS:     /
# RETURNS:  /
if __name__ == "__main__":

    # start main thread
    main = Main()

    test1 = Bio.PDB.PDBParser().get_structure("1", constants.OUTPUT_DIR+"1.pdb")
    test2 = Bio.PDB.PDBParser().get_structure("2", constants.OUTPUT_DIR+"2.pdb")
    target = proteinInterpreter(test1)
    sample = proteinInterpreter(test2, target=target)
    sample._generatePlot(constants.OUTPUT_DIR+"2.pdb", constants.OUTPUT_DIR+"1.pdb")
    # fitnessfunction.evaluate()


    # attach SIGTERM handling
    signal.signal(signal.SIGTERM, main.stop())