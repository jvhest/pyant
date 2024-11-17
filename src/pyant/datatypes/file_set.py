import os
import sys
import glob

from pyant.task import Task
from pyant.datatypes import build_exception, file_set_include, file_set_exclude

"""
example:

<fileset dir="${server.src}" >
  <include name="**/*.java"/>
  <exclude name="**/*Test*"/>
</fileset>

<fileset file="${server.src}/file.txt" >
"""

class FileSet(Task):
    """Creating set of the files"""

    #-----------------------------
    def __init__(self, xml_element, parent):
        Task.__init__(self, xml_element, parent,
                attr = {
                    "file"      : "",
                    "dir"       : "",
                    "recursive" : "",
                    },
                children=["exclude-set", "include-set" ]
                )

        self.__includes     = []
        self.__excludes     = []
        self.__filenames    = []
        self.__directories  = []

    #-----------------------------
    def add_include(self, incl):
        """Adds include pattern to fileset"""
        self.__includes.append(incl)

    #-----------------------------
    def add_exclude(self, excl):
        """Adds exclude pattern to fileset"""
        self.__excludes.append(excl)

    #-----------------------------
    def get_filenames(self):
        """Returns filenames"""
        return self.__filenames

    #-----------------------------
    def scan_included(self, dir, incl):
        if not dir in self.__directories:
            self.__directories.append(dir)
        absname = os.path.join(dir, incl)
        files = glob.glob(absname)
        for fname in files:
            if os.path.isdir(fname):
                if self._recursive =="true":
                    self.scan_included(fname, incl)

            elif not fname in self.__filenames:
                self.__filenames.append(fname)

    #-----------------------------
    def scan_excluded(self, dir, excl):
        absname = os.path.join(dir, excl)
        files = glob.glob(absname)
        for fname in files:
            if os.path.isdir(fname):
                if self._recursive =="true":
                    self.scan_excluded(fname, excl)
            elif fname in self.__filenames:
                self.__filenames.remove(fname)

    #-----------------------------
    def scan(self):
        """Starts scanning"""
        for incl in self.__includes:
            self.scan_included(self._dir, incl)

        for excl in self.__excludes:
            self.scan_excluded(self._dir, excl)

    #-----------------------------
    def validate(self):
        ## - file or dir required
        if not self._dir and not self._file:
            raise BuildException(self, "dir or file attribute required")
        ## - not both
        elif self._dir and self._file:
            raise BuildException(self, "dir OR file attribute required, not both")
        ## - dir:
        elif self._dir:
            if self._dir == ".":
                self._dir = os.getcwd()
            else:
                if not os.path.isdir(self._dir):
                    raise BuildException(self, "dir not a valid directory path: %s"%(self._dir))
        ## - file:
        elif self._file:
            ## - must be absolute path, and must exist
            if not os.path.isfile(self._file):
                raise BuildException(self, "file %s not a existing file"%(self._file))
            elif not os.path.isabs(self._file):
                raise BuildException(self, "file %s not absolute path"%(self._file))

    #-----------------------------
    def execute(self):
        if self._file:
            ## - setup for scanning
            self._dir, file = os.path.split(self._file)
            self.__includes = []
            self.add_include(file)

        ## - if no include attribute used then include all files
        if self.__includes == []:
            self.__includes.append("*")

        ## - fill __filenames and __directories
        self.scan()

        ## - testing
        for f in self.get_filenames():
            self._project.log(0,"- fileset: %s"%(f))

