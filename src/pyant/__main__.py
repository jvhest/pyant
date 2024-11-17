#! /usr/bin/python
# -*- coding: utf-8 -*-

import sys
import os
import getopt

from .project import Project
from .datatypes.build_exception import BuildException

# Project includes
DEFAULT_BUILD = "build.xml"


class Pyant:
    """Usage: pyant.py [options] [target]
    The options are as follows:
        --help, -h          Print this help
        -f <file>, --buildfile <file>    use given buildfile
        --version, -v           print the version information and exit
        -l <file>, --logfile <file> use given file for log
    """

    def __init__(self):
        self._basedir = ""
        self._build_file = DEFAULT_BUILD
        self._target = None

        try:
            opts, args = getopt.getopt(sys.argv[1:], 'f:l:h',
                 ['basedir=', 'buildfile=', 'help'])

        except (getopt.error, msg):
            sys.stderr.write(f"Options error: {str(msg)}\n")
            print(__doc__)
            sys.exit(2)

        for o, a in opts:
            if o == "--basedir":
                self._basedir = a
            elif o == "--buildfile" or o == "-f":
                self._build_file = a
            elif o == "--help" or o == "h":
                self.print_usage()
                sys.exit(0)

        if len(args) > 0:
            self._target = args[0]

    def print_usage(self):
        print(self.__class__.__doc__)

    def run(self):
        """Executes build file parsing and runs target specified
        """
        if not self._basedir:
            self._basedir = os.getcwd()

        sys.path.append(self._basedir)
        self._build_file = os.path.join(self._basedir, self._build_file)

        if os.path.isfile(self._build_file):
            try:
                project = Project(self._build_file)
                project.perform(self._target)

            except BuildException as exc:
                print(exc)
                sys.exit(1)

        else:
            print(f"geen geldige buildfile opgegeven: {self._build_file}")


def main():
    p = Pyant()
    p.run()

if __name__ == "__main__":
    main()
