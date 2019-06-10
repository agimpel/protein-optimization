import os
import time


RUN_NAME = "RUN_"+time.strftime("%Y%m%d_%H%M%S")

# available: directed_hausdorff, euclidean, cityblock, chebyshev
DISTANCE_MEASURE = "directed_hausdorff"


# main directory path
PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# path to individual directories
RGN_DIR = os.path.join(PATH, "rgn/")
DATA_DIR = os.path.join(PATH, "data/")
ARCHIVE_DIR = os.path.join(DATA_DIR, "archive/")
RUN_ARCHIVE_DIR = os.path.join(ARCHIVE_DIR, RUN_NAME + "/"); os.mkdir(RUN_ARCHIVE_DIR)
WORKSPACE_DIR = os.path.join(DATA_DIR, "workspace/")
RGN_BASE_DIR = os.path.join(DATA_DIR, "RGN12/")
RGN_INPUT_DIR = os.path.join(DATA_DIR, "prediction_input/")
RGN_OUTPUT_DIR = os.path.join(DATA_DIR, "prediction_output/")
RGN_PROCESSING_DIR = os.path.join(RGN_DIR, "data_processing/")
RGN_MODEL_DIR = os.path.join(RGN_DIR, "model/")

DIRS = [RGN_DIR, DATA_DIR, ARCHIVE_DIR, RUN_ARCHIVE_DIR, WORKSPACE_DIR, RGN_BASE_DIR, RGN_INPUT_DIR, RGN_OUTPUT_DIR, RGN_PROCESSING_DIR, RGN_MODEL_DIR]


# path to individual files
RGN_CONFIG_PATH = os.path.join(DATA_DIR, "rgn_config")
JH_DATABASE_PATH = os.path.join(DATA_DIR, "database.fa")
RGN_EXEC_PATH = os.path.join(RGN_MODEL_DIR, "protling.py")
JH_EXEC_PATH = os.path.join(RGN_PROCESSING_DIR, "jackhmmer.sh")
RGN_CONVERTPROTEIN_PATH = os.path.join(RGN_PROCESSING_DIR, "convert_to_proteinnet.py")
RGN_CONVERTTFRECORD_PATH = os.path.join(RGN_PROCESSING_DIR, "convert_to_tfrecord.py")

FILES = [RGN_CONFIG_PATH, JH_DATABASE_PATH, RGN_EXEC_PATH, JH_EXEC_PATH, RGN_CONVERTPROTEIN_PATH, RGN_CONVERTTFRECORD_PATH]


# check directories and files for their existence
for a_dir in DIRS:
    if os.path.isdir(a_dir) is False:
        raise FileNotFoundError("The directory "+a_dir+" was not found. Please set it up before running.")

for a_file in FILES:
    if os.path.isfile(a_file) is False:
        raise FileNotFoundError("The file "+a_file+" was not found. Please set it up before running.")