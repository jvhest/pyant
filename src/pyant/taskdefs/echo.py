
import sys
import os

from pyant.task import Task
from pyant.datatypes.build_exception import *


class Echo(Task):
    """Echo message"""

    def __init__(self, xml_element, parent):
        Task.__init__(self, xml_element, parent, 
                attr = { "file"     : "",
                         "stdout"   : "false",
                         "message"  : "",
                         "append"   : "false"
                       })
    
    def execute(self):
        if self._message:
            msg = self._message
        else:
            msg = self.get_cdata()
            if msg == None:
                raise BuildException(self, "message attribute or text as CDATA required but undefined")

        if self._stdout:
            print(f"{str(msg)}")

        elif self._file:
            if self._append == "true":
                f = open(self._file, "ab")
                f.write(str(msg)+"\n")
                f.close()
            else:
                f = open(self._file, "wb")
                f.write(str(msg)+"\n")
                f.close()       
        else:
            self._project.log(0,str(msg))
