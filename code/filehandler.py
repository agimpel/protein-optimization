import os
import stat
import shutil
import logging
import pymol
from openprotein_utils import write_to_pdb
import Bio.PDB
from proteininterpreter import proteinInterpreter
from fitnessfunction import TARGET_RESULT
from numba import jit

# custom modules
import constants


# set up logger for this module
LOGGER = logging.getLogger('filehandler'); LOGGER.setLevel(logging.INFO)


def prepareOptimisation():
    shutil.copyfile(constants.PDB_TARGET_PATH, constants.RUN_ARCHIVE_DIR+"target.pdb")
    write_to_pdb(TARGET_RESULT.STRUCTURE, constants.RUN_ARCHIVE_DIR+"target_aligned.pdb")


@jit
def saveGeneration(generation):
    generation_id = generation.ID
    generation_dir = constants.RUN_ARCHIVE_DIR+"Generation_"+str(generation_id).zfill(5)+"/"
    os.mkdir(generation_dir)
    for genotype in generation:
        _saveGenotype(generation_id, generation_dir, genotype)


@jit
def _saveGenotype(generation_id, generation_dir, genotype):
    genotype_id = genotype.ID
    gentoype_dir = generation_dir+"Genotype_"+str(genotype_id).zfill(3)+"/"
    os.mkdir(gentoype_dir)
    pdb_path = _generatePDB(genotype, gentoype_dir, generation_id, genotype_id)
    datafile_path = _generateData(genotype, gentoype_dir, generation_id, genotype_id)
    _generatePlot(genotype, pdb_path, datafile_path, gentoype_dir, generation_id, genotype_id)


@jit
def _saveBestGenotype(generation_id, generation_dir, genotype):
    genotype_id = genotype.ID
    pdb_path = _generatePDB(genotype, generation_dir, generation_id, genotype_id)
    datafile_path = _generateData(genotype, generation_dir, generation_id, genotype_id)
    _generatePlot(genotype, pdb_path, datafile_path, generation_dir, generation_id, genotype_id)


def saveBestGenotypeFromGeneration(generation):
    generation_id = generation.ID
    generation_dir = constants.RUN_ARCHIVE_DIR+"Generation_"+str(generation_id).zfill(5)+"/"
    os.mkdir(generation_dir)
    genotype_fitness = [genotype.FITNESS for genotype in generation]
    best_genotype = generation.GENOTYPES[sorted(range(len(genotype_fitness)), key=lambda i: genotype_fitness[i], reverse=True)[0]]
    _saveBestGenotype(generation_id, generation_dir, best_genotype)


@jit
def _generatePDB(genotype, gentoype_dir, generation_id, genotype_id):
    pdb_path = gentoype_dir+constants.RUN_NAME+"_"+str(generation_id).zfill(5)+"_"+str(genotype_id).zfill(3)+".pdb"
    write_to_pdb(genotype._result.STRUCTURE, pdb_path)
    return pdb_path


def _generateData(genotype, gentoype_dir, generation_id, genotype_id):
    datafile_path = gentoype_dir+constants.RUN_NAME+"_"+str(generation_id).zfill(5)+"_"+str(genotype_id).zfill(3)+".data"
    with open(datafile_path, "w+") as datafile:
        datafile.write("run_name="+str(constants.RUN_NAME)+"\n")
        datafile.write("generation_id="+str(generation_id)+"\n")
        datafile.write("genotype_id="+str(genotype_id)+"\n")
        datafile.write("sequence="+str(genotype._result.SEQUENCE)+"\n")
        datafile.write("target_sequence="+str(genotype._result.TARGET.SEQUENCE)+"\n")
        datafile.write("fitness="+str(genotype.FITNESS)+"\n")
        datafile.write("fitness_hausdorff="+str(genotype._result.HAUSDORFF)+"\n")
        datafile.write("fitness_euclidean="+str(genotype._result.EUCLIDEAN)+"\n")
        datafile.write("fitness_cityblock="+str(genotype._result.CITYBLOCK)+"\n")
        datafile.write("fitness_chebyshev="+str(genotype._result.CHEBYSHEV)+"\n")
        datafile.close()
    return datafile_path


def _generatePlot(genotype, pdb_path, datafile_path, gentoype_dir, generation_id, genotype_id):
    pass
    # pymol.pymol_argv = ['pymol','-qc']
    # pymol.finish_launching()

    # sname = "Test"
    # sname2 = "test2"
    # pymol.cmd.load(path, sname)
    # pymol.cmd.load(path2, sname)
    # pymol.cmd.disable("all")
    # pymol.cmd.enable(sname)
    # pymol.cmd.enable(sname2)
    # pymol.cmd.png("my_image.png")

    # # Get out!
    # pymol.cmd.quit()
