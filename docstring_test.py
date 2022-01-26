import doctest
import os
import importlib.util


def import_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    foo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(foo)
    return foo


if __name__ == "__main__":
    BASE_PATH = os.path.dirname(os.path.abspath(__file__))
    # parentdir = os.path.dirname(BASE_PATH)
    mod_path1 = os.path.join(BASE_PATH, "tracknaliser/tracks.py")
    doctest.testmod(import_module('', mod_path1), verbose=True)
    mod_path2 = os.path.join(BASE_PATH, "tracknaliser/utils.py")
    doctest.testmod(import_module('', mod_path2), verbose=True)
