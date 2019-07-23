import torch
import time
from openprotein_utils import encode_primary_string, get_structure_from_angles, write_to_pdb

input_sequence = ["EENTEEKIGDDKINATYMWISKDKKYLTIEFQYYSTHSEDKKHFLNLVINNKDNTDDEYINLEFRHNSERDSPDHLG"]


model_path = "../data/openprotein.model"
model = torch.load(model_path)
input_encoded = list(torch.LongTensor(encode_primary_string(aa)) for aa in input_sequence)

predicted_dihedral_angles, predicted_backbone_atoms, batch_sizes = model(input_encoded)

write_to_pdb(get_structure_from_angles(input_encoded[0], predicted_dihedral_angles[:,0]), "../data/target_"+time.strftime("%Y%m%d_%H%M%S")+".pdb")
print("Wrote prediction to ../data/target_*.pdb")