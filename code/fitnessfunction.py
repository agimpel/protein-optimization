import logging
import torch
from numba import jit

# custom modules
import constants
import filehandler
from openprotein_utils import encode_primary_string, get_structure_from_angles, write_to_pdb
import Bio.PDB

import warnings
warnings.simplefilter("ignore")

from proteininterpreter import proteinInterpreter

# set up logger for this module
LOGGER = logging.getLogger('fitness'); LOGGER.setLevel(logging.DEBUG)

TARGET_RESULT = proteinInterpreter(Bio.PDB.PDBParser().get_structure("TARGET", constants.PDB_TARGET_PATH))
PREDICTION_MODEL = torch.load(constants.ML_MODEL_PATH)

SEQUENCE_PREFIX = "EENTEEKIGDDKINATYMWISKDKKYLTIEFQYYST"
SEQUENCE_SUFFIX = "KHFLNLVINNKDNTDDEYINLEFRHNSERDSPDHLG"

def evaluate_sequence(sequence):
    sequence = [SEQUENCE_PREFIX + sequence + SEQUENCE_SUFFIX]
    sequence_encoded = list(torch.LongTensor(encode_primary_string(aa)) for aa in sequence)
    predicted_dihedral_angles, _, _ = PREDICTION_MODEL(sequence_encoded)
    return proteinInterpreter(get_structure_from_angles(sequence_encoded[0], predicted_dihedral_angles[:,0]), target=TARGET_RESULT)


@jit
def evaluate_generation(generation):
    genotypes = generation.GENOTYPES
    sequences = [genotype.GENOTYPE for genotype in genotypes]
    results = [evaluate_sequence(sequence) for sequence in sequences]

    for genotype, result in zip(genotypes, results):
        genotype.RESULT = result