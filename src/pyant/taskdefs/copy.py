import os
import shutil

from pyant.task import Task
from pyant.datatypes import build_exception, file_set
import pyant.utils.utils

class Copy(Task):
    """Copies files and directories"""

    #-----------------------------        
    def __init__(self, xml_element, parent):
        Task.__init__(self, xml_element, parent, 
                attr = { "tofile"   : "",
                         "todir"    : "",
                         "file"     : "",
                         "modifier" : ""
                       },
                children = ["fileset", "filelist"]
                )

    #-----------------------------        
    def modify_fname(self, fname):
        if self._modifier:
            if self._modifier =="date":
                return datename(fname, uur_min=False)
            elif self._modifier =="datetime":
                return datename(fname, uur_min=True)
        else:
            return fname                            
    
    #-----------------------------        
    def validate(self): 
        ## - todir OR tofile:
        if (not self._todir) and (not self._tofile):
            raise BuildException(self, "todir OR tofile required")

        ## - todir:
        if self._todir:            
            if not os.path.isdir(self._todir):
                raise BuildException(self, "todir not a valid directory path: %s"%(self._todir))

        ## - tofile:
        if self._tofile:            
            head, tail = os.path.split(self._tofile)
            if not os.path.isdir(head):
                raise BuildException(self, "tofile not valid directory part: %s"%(self._tofile))
            
        ## - file:
        if self._file:
            ## - must be absolute path, and must exist
            if not os.path.isfile(self._file):
                raise BuildException(self, "file %s not a existing file"%(self._file))
            elif not os.path.isabs(self._file):
                raise BuildException(self, "file %s not absolute path"%(self._file))
                
        ## - modifier
        if self._modifier:
            if self._modifier not in ["date","datetime"]:
                raise BuildException(self, "%s not a valid modifier"%(self._modifier))

    #-----------------------------        
    def execute(self):

        if self._todir:
            ## - copy single file todir
            if self._file:
                head, tail = os.path.split(fname)
                tail = self.modify_fname(tail)
                self._project.log(0, "copy: %s -> %s"%(fname, os.path.join(self._todir, tail)))
                shutil.copy(fname, os.path.join(self._todir, tail))
                
            ## - copy fileset(s) todir (if any)             
            fnames = []
            filesets = self.get_children("fileset") 
            for fset in filesets:
                fset.scan()
                fnames += fset.get_filenames()
    
            filelists = self.get_children("filelist") 
            for flist in filelists:
                fnames += flist.get_filenames()
                
            for fname in fnames:
                head, tail = os.path.split(fname)
                filename = self.modify_fname(tail)
                self._project.log(0,"copy: %s -> %s"%(fname, os.path.join(self._todir, filename)))
                shutil.copy(fname, os.path.join(self._todir, filename))

        ## - copy single file tofile
        elif self._file and self._tofile: 
            filename = self.modify_fname(self._tofile)
            self._project.log(0,"copy: %s -> %s"%(self._file, filename))
            shutil.copy(self._file, filename)
