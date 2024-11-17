import time

from pyant.xmlcomponent import XmlComponent
from pyant.datatypes.build_exception import BuildException


class Task(XmlComponent):
    """Abstract Task"""

    def __init__(self, xml_element, parent, attr={}, children=[]):
        XmlComponent.__init__(self, xml_element, parent, attr, children)
        self._run_innertasks = True

    def validate(self):
        pass

    def init(self):
        """called after construction of class"""
        pass

    def get_log_prefix(self):
        msg = '<' + self._tagname
        for key in self.allowed_attr:
            if self.__dict__[key]:
                msg += ' %s="%s"' % (key[1:], str(self.__dict__[key]))
        msg += ' >\n'
        return msg

    def execute(self):
        # need override
        raise BuildException(self, "undefined task executed")

    def perform(self, indent):
        """Performs the Task"""
        # resolve used properties
        for key in self.allowed_attr:
            self.__dict__[key] = self._project.resolve_property(self.__dict__[key])

        # check/update the attributes of this task
        self.validate()

        try:
            self.log(indent, "--- start running task `%s`: %s" % (self._tagname, time.ctime()))
            # innertask/datatypes
            if self._run_innertasks:
                for tag, task in self._children:
                    task.perform(indent+1)

            # this task (override)
            self.execute()
            self.log(indent, "--- end running task `%s`: %s" % (self._tagname, time.ctime()))

        except BuildException as exc:
            self.log(indent, "--- end running task `%s`: %s" % (self._tagname, time.ctime()))
            raise exc
