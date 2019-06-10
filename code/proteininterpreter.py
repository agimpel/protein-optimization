import logging
import numpy as np
import Bio.PDB
from scipy.spatial.distance import directed_hausdorff, euclidean, cityblock, chebyshev


# custom modules
import constants



class proteinInterpreter():

    LOGGER = None

    TARGET = None
    is_target = False

    STRUCTURE = None
    BACKBONE_MATRIX = None

    NAME = None
    SEQUENCE = None

    ALIGNMENT_RMS = None
    HAUSDORFF = None
    EUCLIDEAN = None
    CITYBLOCK = None
    CHEBYSHEV = None


    def __init__(self, structure, target = None):
        
        # set up logger for this module
        self.LOGGER = logging.getLogger('fitness'); self.LOGGER.setLevel(logging.DEBUG)

        self.STRUCTURE = structure
        self.NAME = structure.id
        self.SEQUENCE = "".join([constants.AA_DICT[residue.resname] for residue in structure.get_residues()]))
        self._setBackboneMatrix()

        # define target structure
        self.TARGET = target
        if target is None:
            self.is_target = True

        if self.is_target is False:
            self._alignToTarget()
            self._determineFitness()


    def _alignToTarget(self):
        target_atoms = self.BACKBONE_MATRIX
        sample_atoms = self.TARGET.BACKBONE_MATRIX

        # align these paired atom lists
        super_imposer = Bio.PDB.Superimposer()
        super_imposer.set_atoms(target_atoms, sample_atoms)
        super_imposer.apply(self.STRUCTURE.get_atoms())
        self.ALIGNMENT_RMS = super_imposer.rms

        self.LOGGER.info("RMS(model %s, model %s) = %0.2f" % (self.TARGET.STRUCTURE.id, self.STRUCTURE.id, super_imposer.rms))


    def _determineFitness(self):
        sample_coordinates = np.array([atom.get_coord() for atom in self.BACKBONE_MATRIX])
        target_coordinates = np.array([atom.get_coord() for atom in self.TARGET.BACKBONE_MATRIX])

        self.HAUSDORFF, _, _ = directed_hausdorff(sample_coordinates, target_coordinates)
        self.EUCLIDEAN = sum([euclidean(a, b) for a, b in zip(sample_coordinates, target_coordinates)])
        self.CITYBLOCK = sum([cityblock(a, b) for a, b in zip(sample_coordinates, target_coordinates)])
        self.CHEBYSHEV = sum([chebyshev(a, b) for a, b in zip(sample_coordinates, target_coordinates)])


    @property
    def fitness(self): 
        if constants.DISTANCE_MEASURE is "directed_hausdorff":
            return self.HAUSDORFF
        elif constants.DISTANCE_MEASURE is "euclidean":
            return self.EUCLIDEAN
        elif constants.DISTANCE_MEASURE is "cityblock":
            return self.CITYBLOCK
        elif constants.DISTANCE_MEASURE is "chebyshev":
            return self.CHEBYSHEV
        elif constants.DISTANCE_MEASURE is "rms":
            return self.ALIGNMENT_RMS
        else:
            self.LOGGER.warning("unknown fitness measure \"%s\" specified, using RMS instead." % constants.DISTANCE_MEASURE)
            return self.ALIGNMENT_RMS


    def _setBackboneMatrix(self):
        atoms = []
        for residue in self.STRUCTURE.get_residues():
            for res_type in ['C', 'CA', 'N']:
                atoms.append(residue[res_type])
        self.BACKBONE_MATRIX = atoms