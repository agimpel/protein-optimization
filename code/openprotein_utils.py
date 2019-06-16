# This file is part of the OpenProtein project.
#
# @author Jeppe Hallgren
#
# For license information, please see the LICENSE file in the root directory.

import torch
import PeptideBuilder
import Bio.PDB
import math
import openprotein_pnerf as pnerf
from numba import jit

AA_ID_DICT = {'A': 1, 'C': 2, 'D': 3, 'E': 4, 'F': 5, 'G': 6, 'H': 7, 'I': 8, 'K': 9,
              'L': 10, 'M': 11, 'N': 12, 'P': 13, 'Q': 14, 'R': 15, 'S': 16, 'T': 17,
              'V': 18, 'W': 19,'Y': 20}

@jit
def calculate_dihedral_angles_over_minibatch(atomic_coords_padded, batch_sizes, use_gpu):
    angles = []
    atomic_coords = atomic_coords_padded.transpose(0,1)
    for idx, _ in enumerate(batch_sizes):
        angles.append(calculate_dihedral_angles(atomic_coords[idx][:batch_sizes[idx]], use_gpu))
    return torch.nn.utils.rnn.pad_packed_sequence(
            torch.nn.utils.rnn.pack_sequence(angles))

def protein_id_to_str(protein_id_list):
    _aa_dict_inverse = {v: k for k, v in AA_ID_DICT.items()}
    aa_list = []
    for a in protein_id_list:
        aa_symbol = _aa_dict_inverse[int(a)]
        aa_list.append(aa_symbol)
    return aa_list

def get_structure_from_angles(aa_list_encoded, angles):
    aa_list = protein_id_to_str(aa_list_encoded)
    omega_list = angles[1:,0]
    phi_list = angles[1:,1]
    psi_list = angles[:-1,2]
    assert len(aa_list) == len(phi_list)+1 == len(psi_list)+1 == len(omega_list)+1
    structure = PeptideBuilder.make_structure(aa_list,
                                              list(map(lambda x: math.degrees(x), phi_list)),
                                              list(map(lambda x: math.degrees(x), psi_list)),
                                              list(map(lambda x: math.degrees(x), omega_list)))
    return structure

@jit
def write_to_pdb(structure, path):
    out = Bio.PDB.PDBIO()
    out.set_structure(structure)
    out.save(path)


def get_backbone_positions_from_angular_prediction(angular_emissions, batch_sizes, use_gpu):
    # angular_emissions -1 x minibatch size x 3 (omega, phi, psi)
    points = pnerf.dihedral_to_point(angular_emissions, use_gpu)
    coordinates = pnerf.point_to_coordinate(points, use_gpu) / 100 # devide by 100 to angstrom unit
    return coordinates.transpose(0,1).contiguous().view(len(batch_sizes),-1,9).transpose(0,1), batch_sizes

@jit
def encode_primary_string(primary):
    return list([AA_ID_DICT[aa] for aa in primary])