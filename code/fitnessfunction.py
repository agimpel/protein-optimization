import logging
import torch

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

def evaluate_sequence(sequences):
    if type(sequences) is not list:
        sequences = [sequences]
    sequences_encoded = [torch.LongTensor(encode_primary_string(sequence)) for sequence in sequences]
    predicted_dihedral_angles, _, _ = PREDICTION_MODEL(sequences_encoded)
    predicted_structures = [get_structure_from_angles(sequences_encoded[i], predicted_dihedral_angles[:,i]) for i in range(len(sequences_encoded))]
    return [proteinInterpreter(structure, target=TARGET_RESULT) for structure in predicted_structures]


def evaluate_generation(generation):
    genotypes = generation.GENOTYPES
    sequences = [genotype.GENOTYPE for genotype in genotypes]
    results = evaluate_sequence(sequences)

    for genotype, result in zip(genotypes, results):
        genotype.RESULT = result