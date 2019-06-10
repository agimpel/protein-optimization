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

def evaluate():
    input_sequences = ["GIAPPACMSICSLYQLENPCN"]
    model_path = "data/openprotein.model"

    model = torch.load(model_path)
    input_senquences_encoded = list(torch.LongTensor(encode_primary_string(aa)) for aa in input_sequences)

    predicted_dihedral_angles, predicted_backbone_atoms, batch_sizes = model(input_senquences_encoded)
    return proteinInterpreter(get_structure_from_angles(input_senquences_encoded[0], predicted_dihedral_angles[:,0]), target=TARGET_RESULT)

