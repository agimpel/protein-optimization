import logging
import signal
import sys
import time

# custom modules
import constants
import filehandler
import fitnessfunction
import rgncaller
from result import result





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
    # paths = []
    # for i in range(2):
    #     paths.append(constants.WORKSPACE_DIR+str(i+1))
    # rgncaller.evaluate(paths)
    target = result(constants.WORKSPACE_DIR+"1", constants.WORKSPACE_DIR+"1.tertiary")
    result(constants.WORKSPACE_DIR+"2", constants.WORKSPACE_DIR+"2.tertiary", target=target)


    # attach SIGTERM handling
    signal.signal(signal.SIGTERM, main.stop())