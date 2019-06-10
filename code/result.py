import logging
import os
import numpy as np
from scipy.linalg import orthogonal_procrustes
from scipy.spatial import procrustes
from scipy.spatial.distance import directed_hausdorff, euclidean, cityblock, chebyshev
import matplotlib as mpl
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt


# custom modules
import constants

# number of lines to skip in the .tertiary file
TERTIARY_HEADER_LINES = 2


class result():

    LOGGER = None

    FASTA_PATH = None
    TERTIARY_PATH = None

    TARGET = None
    is_target = False

    NAME = None
    SEQUENCE = None
    BACKBONE_MATRIX = None
    FITNESS = None

    def __init__(self, path_to_fasta, path_to_tertiary, target = None):
        
        # set up logger for this module
        self.LOGGER = logging.getLogger('fitness'); self.LOGGER.setLevel(logging.DEBUG)

        # define target structure
        self.TARGET = target
        if target is None:
            self.is_target = True

        self.FASTA_PATH = path_to_fasta; self.TERTIARY_PATH = path_to_tertiary
        for path in [path_to_fasta, path_to_tertiary]:
            if os.path.isfile(path) is False:
                raise FileNotFoundError("The file "+path+" was not found.")

        self._readData()
        self._preprocessData()
        if self.is_target is False:
            self._alignAndDetermineFitness()
            self.generatePlot()


    def _readData(self):
        fasta_file = open(self.FASTA_PATH, 'r')
        self.NAME = fasta_file.readline()[1:]
        self.SEQUENCE  = "".join([line.strip() for line in fasta_file.readlines()])
        fasta_file.close()

        tertiary_file = open(self.TERTIARY_PATH, 'r')
        for _ in range(TERTIARY_HEADER_LINES): tertiary_file.readline()
        data = np.array(" ".join([line.strip() for line in tertiary_file.readlines()]).split(" "))
        tertiary_file.close()

        data = data.astype(np.float)
        self.BACKBONE_MATRIX = np.reshape(data, (-1,3,3))

        if self.BACKBONE_MATRIX.shape[0] != len(self.SEQUENCE):
            raise RuntimeError("Sequence and backbone matrix do not have the same length: "+str(self.BACKBONE_MATRIX.shape[0])+" vs. "+str(len(self.SEQUENCE))+".")


    def _preprocessData(self):
        coordinates = np.reshape(self.BACKBONE_MATRIX, (-1,3))
        coordinates -= coordinates.mean(axis = 0)
        self.BACKBONE_MATRIX = np.reshape(coordinates, (-1,3,3))


    def _alignAndDetermineFitness(self):

        sample_coordinates = np.reshape(self.BACKBONE_MATRIX, (-1,3))
        target_coordinates = np.reshape(self.TARGET.BACKBONE_MATRIX, (-1,3))

        if len(sample_coordinates) > len(target_coordinates):
            target_coordinates = target_coordinates.append(np.zeros((len(sample_coordinates)-len(target_coordinates),3)))
        elif len(sample_coordinates) < len(target_coordinates):
            sample_coordinates = sample_coordinates.append(np.zeros((len(target_coordinates)-len(sample_coordinates),3)))

        R, _ = orthogonal_procrustes(sample_coordinates, target_coordinates)
        sample_coordinates = R.dot(sample_coordinates.T).T
        self.BACKBONE_MATRIX = np.reshape(sample_coordinates, (-1,3,3))
        
        if constants.DISTANCE_MEASURE is "directed_hausdorff":
            self.FITNESS, _, _ = directed_hausdorff(sample_coordinates, target_coordinates)
        elif constants.DISTANCE_MEASURE is "euclidean":
            self.FITNESS = sum([euclidean(a, b) for a, b in zip(sample_coordinates, target_coordinates)])
        elif constants.DISTANCE_MEASURE is "cityblock":
            self.FITNESS = sum([cityblock(a, b) for a, b in zip(sample_coordinates, target_coordinates)])
        elif constants.DISTANCE_MEASURE is "chebyshev":
            self.FITNESS = sum([chebyshev(a, b) for a, b in zip(sample_coordinates, target_coordinates)])
        else:
            raise RuntimeError("Specified distance measure \""+constants.DISTANCE_MEASURE+"\" is unknown.")

    
    def generatePlot(self):
        sample_coordinates = np.reshape(self.BACKBONE_MATRIX, (-1,3))
        target_coordinates = np.reshape(self.TARGET.BACKBONE_MATRIX, (-1,3))
        print(sample_coordinates)
        print(sample_coordinates[:,0])

        fig = plt.figure()
        ax = fig.gca(projection='3d')
        ax.plot(sample_coordinates[:,0], sample_coordinates[:,1], sample_coordinates[:,2], label='parametric curve')
        ax.plot(target_coordinates[:,0], target_coordinates[:,1], target_coordinates[:,2], label='parametric curve')
        plt.show()