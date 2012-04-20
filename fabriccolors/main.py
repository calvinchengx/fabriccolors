"""
This module contains fabriccolor's `main` method plus related subroutines.
"""

import fnmatch
import os
import sys


def find_fabsettings():
    """
    Look for fabsettings.py, which will contain all information about
    target servers and distros on each server.    i
    """
    matches = []
    for root, dirnames, filenames in os.walk(os.getcwd()):
        for filename in fnmatch.filter(filenames, 'fabsettings.py'):
            matches.append(os.path.join(root, filename))
    number_of_matches = len(matches)
    if number_of_matches == 1:
        path_to_fabsettings = matches[0]
        load_fabsettings(path_to_fabsettings)
        return True

    return False


def load_fabsettings(path_to_fabsettings):
    directory, fabsettings = os.path.split(path_to_fabsettings)
    if directory not in sys.path:
        sys.path.insert(0, directory)


def main():
    """
    Main command-line execution loop.

    Usage
    fabc

    """
    if find_fabsettings():
        import fabsettings
        project_sites = fabsettings.PROJECT_SITES.keys()
        print "You have specified the follow server targets:"
        print project_sites
        # or organized according to distros
        # TODO: we can now do things to the target server
        # e.g. `fabc server_setup:root,dev` should fire off all the server setup
        #      scripts using root user, at the 'dev' server
        #      `fabc server_setup:vagrant` should fire off all the server setup
        #      scripts using the vagrant user, at the 'vagrant' vm
        # and all these scripts are stored in fabfile.py
    else:
        print "fabric colors is a wrapper around python fabric."
        print "Begin using fabric colors by defining your servers in fabsettings.py"
        print "using the included fabsettings.py.sample as an example"
