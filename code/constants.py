import os
import time


RUN_NAME = "RUN_"+time.strftime("%Y%m%d_%H%M%S")

# available: directed_hausdorff, euclidean, cityblock, chebyshev, rms
DISTANCE_MEASURE = "euclidean"

AA_DICT = {'CYS': 'C', 'ASP': 'D', 'SER': 'S', 'GLN': 'Q', 'LYS': 'K',
           'ILE': 'I', 'PRO': 'P', 'THR': 'T', 'PHE': 'F', 'ASN': 'N', 
           'GLY': 'G', 'HIS': 'H', 'LEU': 'L', 'ARG': 'R', 'TRP': 'W', 
           'ALA': 'A', 'VAL':'V', 'GLU': 'E', 'TYR': 'Y', 'MET': 'M'}

# main directory path
PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# path to individual directories
DATA_DIR = os.path.join(PATH, "data/")
ARCHIVE_DIR = os.path.join(DATA_DIR, "archive/")
RUN_ARCHIVE_DIR = os.path.join(ARCHIVE_DIR, RUN_NAME + "/"); os.mkdir(RUN_ARCHIVE_DIR)
WORKSPACE_DIR = os.path.join(DATA_DIR, "workspace/")
OUTPUT_DIR = os.path.join(PATH, "output/")
DIRS = [DATA_DIR, ARCHIVE_DIR, RUN_ARCHIVE_DIR, WORKSPACE_DIR]


# path to individual files
PDB_TARGET_PATH = os.path.join(DATA_DIR, "target.pdb")
ML_MODEL_PATH = os.path.join(DATA_DIR, "openprotein.model")
FILES = [PDB_TARGET_PATH, ML_MODEL_PATH]

# check directories and files for their existence
for a_dir in DIRS:
    if os.path.isdir(a_dir) is False:
        raise FileNotFoundError("The directory "+a_dir+" was not found. Please set it up before running.")

for a_file in FILES:
    if os.path.isfile(a_file) is False:
        raise FileNotFoundError("The file "+a_file+" was not found. Please set it up before running.")