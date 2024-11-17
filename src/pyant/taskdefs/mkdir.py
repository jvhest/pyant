from pyant.task import Task
from pyant.datatypes import build_exception

import os

class MkDir(Task):

    #-----------------------------        
    def __init__(self, xml_element, parent):
        Task.__init__(self, xml_element, parent, 
                attr={ "dir":"" })

    #-----------------------------        
    def execute(self):
        if self._dir:
            if not os.path.isdir(self._dir):        
                try:
                    os.makedirs(self._dir)
                except (OSError, err):
                    self.log(0, "warning-mkdir %s: %s" %(self._dir, str(err)))
            else:                    
                self.log(0, "mkdir: %s already exists" %(self._dir))
        else:
            raise BuildException(self, "dir attribute required")
