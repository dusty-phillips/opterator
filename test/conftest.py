# py.test plugin to ignore collection of unit tests in test files
# that use python 3 syntax that fails to compile under python 2.
# These test advanced features that aren't available in python 2.

import sys


def pytest_ignore_collect(path, config):
    if path.basename == 'test_function_annotations.py':
        if sys.version_info < (3, 3):
            return True
    return False
