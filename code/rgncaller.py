import os
import logging
import subprocess

# custom modules
import constants
import filehandler



# set up logger for this module
LOGGER = logging.getLogger('rgncaller'); LOGGER.setLevel(logging.DEBUG)



def evaluate(paths):
    if type(paths) is not list:
        paths = [paths]
    
    LOGGER.debug("Evaluating a total of "+str(len(paths))+" samples.")

    for operation in [_runJackhmmer, _runConvertToProteinnet, _runConvertToTfrecord]:
        processes = [operation(path) for path in paths]
        exit_codes = [process.wait() for process in processes]

        if any(exit_code is not 0 for exit_code in exit_codes):
            raise subprocess.CalledProcessError
    
    filehandler.clearRgnInput()
    filehandler.clearRgnOutput()
    filehandler.copyFileToRgnInput([path+".tfrecord" for path in paths])

    _runRGN()

    output_paths = [constants.RGN_OUTPUT_DIR+os.path.basename(path)+".tertiary" for path in paths]
    target_paths = [os.path.dirname(path) for path in paths]
    filehandler.copyFileFromRgnOutput(output_paths, target_paths)
    filehandler.clearRgnInput()
    filehandler.clearRgnOutput()


def _runJackhmmer(path):
    cmd = " ".join([constants.JH_EXEC_PATH, path, constants.JH_DATABASE_PATH])
    LOGGER.debug("Started running JackHmmer: \""+cmd+"\".")
    return subprocess.Popen(cmd, shell=True)

def _runConvertToProteinnet(path):
    cmd = " ".join(["python", constants.RGN_CONVERTPROTEIN_PATH, path])
    LOGGER.debug("Started running ProteinNet conversion: \""+cmd+"\".")
    return subprocess.Popen(cmd, shell=True)

def _runConvertToTfrecord(path):
    cmd = " ".join(["python", constants.RGN_CONVERTTFRECORD_PATH, path+".proteinnet", path+".tfrecord", "42"])
    LOGGER.debug("Started running TFRecord conversion: \""+cmd+"\".")
    return subprocess.Popen(cmd, shell=True)

def _runRGN():
    cmd = " ".join(["python", constants.RGN_EXEC_PATH, constants.RGN_CONFIG_PATH, "-d", constants.RGN_BASE_DIR, "-g 0 -p -e weighted_testing"])
    LOGGER.debug("Started running RGN: \""+cmd+"\".")
    subprocess.check_call(cmd, shell=True)
    LOGGER.debug("RGN finished.")