import os
import stat
import shutil
import logging


# custom modules
import constants


# set up logger for this module
LOGGER = logging.getLogger('filehandler'); LOGGER.setLevel(logging.INFO)



def clearWorkspace():
    _clear_dir(constants.WORKSPACE_DIR)

def clearRgnInput():
    _clear_dir(constants.RGN_INPUT_DIR)

def clearRgnOutput():
    _clear_dir(constants.RGN_OUTPUT_DIR)

def copyFileToRgnInput(paths):
    if type(paths) is not list:
        paths = [paths]
    return [shutil.copy(path, constants.RGN_INPUT_DIR) for path in paths]

def copyFileFromRgnOutput(paths, targets):
    if type(paths) is not list:
        paths = [paths]
    if type(targets) is not list:
        targets = [targets]
    if len(paths) != len(targets): LOGGER.warning("Number of sources and targets do not match, using first target instead."); targets = [targets[0]]

    if len(targets) == 1:
        return [shutil.copy(path, targets[0]) for path in paths]
    else:
        return [shutil.copy(paths[i], targets[i]) for i in range(len(paths))]

def copyFileToWorkspace(paths, subdir = None):
    if type(paths) is not list:
        paths = [paths]
    target_dir = constants.WORKSPACE_DIR
    if subdir is not None:
        target_dir += str(subdir)+"/"
    return [shutil.copy(path, target_dir) for path in paths]

def copyDirToWorkspace(paths, subdir = None):
    if type(paths) is not list:
        paths = [paths]
    target_dir = constants.WORKSPACE_DIR
    if subdir is not None:
        target_dir += str(subdir)+"/"
    return [shutil.copytree(path, target_dir) for path in paths]

def copyFileToArchive(paths, subdir = None):
    if type(paths) is not list:
        paths = [paths]
    target_dir = constants.ARCHIVE_DIR
    if subdir is not None:
        target_dir += str(subdir)+"/"
    return [shutil.copy(path, target_dir) for path in paths]

def copyDirToArchive(paths, subdir = None):
    if type(paths) is not list:
        paths = [paths]
    target_dir = constants.ARCHIVE_DIR
    if subdir is not None:
        target_dir += str(subdir)+"/"
    return [shutil.copytree(path, target_dir) for path in paths]


# http://stackoverflow.com/questions/1889597/deleting-directory-in-python
def _remove_readonly(fn, path_, excinfo):
    # Handle read-only files and directories
    if fn is os.rmdir:
        os.chmod(path_, stat.S_IWRITE)
        os.rmdir(path_)
    elif fn is os.remove:
        os.lchmod(path_, stat.S_IWRITE)
        os.remove(path_)

def _force_remove_file_or_symlink(path_):
    try:
        os.remove(path_)
    except OSError:
        os.lchmod(path_, stat.S_IWRITE)
        os.remove(path_)

def _is_regular_dir(path_):
    try:
        mode = os.lstat(path_).st_mode
    except os.error:
        mode = 0
    return stat.S_ISDIR(mode)

def _clear_dir(path_):
    if _is_regular_dir(path_):
        # Given path is a directory, clear its content
        for name in os.listdir(path_):
            fullpath = os.path.join(path_, name)
            if _is_regular_dir(fullpath):
                shutil.rmtree(fullpath, onerror=_remove_readonly)
            else:
                _force_remove_file_or_symlink(fullpath)
    else:
        # Given path is a file or a symlink.
        # Raise an exception here to avoid accidentally clearing the content
        # of a symbolic linked directory.
        raise OSError("Cannot call clear_dir() on a symbolic link")