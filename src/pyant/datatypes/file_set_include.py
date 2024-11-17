import os
import sys

from pyant.task import Task
from pyant.datatypes import build_exception

class FileSetInclude(Task):
    """Include task (inner task)"""

    #-----------------------------        
    def __init__(self, xml_element, parent):
        Task.__init__(self, xml_element, parent, attr={"name":""} )
    
    #-----------------------------        
    def validate(self):
        if not self._name:
            raise BuildException(self, "name attribute required but undefined")
    
    #-----------------------------        
    def execute(self):
        if hasattr(self._parent, "add_include"):
            self._parent.add_include(self._name)
        else:
            raise BuildException(self, "parent Task doesn't have required method")
        # [Place your code here]
