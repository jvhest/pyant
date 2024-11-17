import time

from .utils import utils as utils
from .xmlcomponent import XmlComponent
from .datatypes.build_exception import BuildException


# Rules definition for Target, starting from 1,
# just don't like to start from zero...

RULE_IF = 1
RULE_UNLESS = 2
RULE_IFTIME = 3


def isValueTrue(value):
    if value.lower() == "false":
        return False
    if value == "0":
        return False
    if value == "":
        return False
    return True


class Target(XmlComponent):
    """Class with PyAnt Target
    """

    def __init__(self, xml_element, parent):
        XmlComponent.__init__(self, xml_element, parent,
                              attr={
                                  "name": "",
                                  "if": "",
                                  "iftime": "",
                                  "unless": "",
                                  "depends": ""
                              },
                              children=["*"]
                              )

        # target name
        if not self._name:
            raise BuildException(self, "Target has not (name) attribute")

        # setup rules
        self._rules = []
        if self._if:
            self._rules.append((RULE_IF, self._if))
        if self._unless:
            self._rules.append((RULE_UNLESS, self._unless))
        if self._iftime:
            self._rules.append((RULE_IFTIME, self._iftime))

        # build depends-list
        parts = self._depends.split(',')
        self._depends = []
        for part in parts:
            if part:
                self._depends.append(part.strip())

        self._performed = False

    def check_rules(self):
        keep_on = True
        for rule in self._rules:
            if rule[0] == RULE_IF:
                if not isValueTrue(self._project.get_property(rule[1])):
                    self.log(0, "   --- failed if rule: %s" % (rule[1]))
                    keep_on = False
                    break
            elif rule[0] == RULE_UNLESS:
                if isValueTrue(self._project.get_property(rule[1])):
                    self.log(0, "   --- failed unless rule: %s" % (rule[1]))
                    keep_on = False
                    break
            elif rule[0] == RULE_IFTIME:
                if not utils.its_time(rule[1]):
                    self.log(0, "   --- failed iftime rule: %s" % (rule[1]))
                    keep_on = False
                    break
        return keep_on

    def get_dependencies(self):
        """Called by Project"""
        return self._depends

    def get_log_prefix(self):
        return "[" + self._tagname + " - " + self._name + "] "

    def perform(self, indent):
        if not self._performed:
            self.log(indent, "--- start running target `%s`: %s" % (self._name, time.ctime()))
            for tag, task in self._children:
                try:
                    task.perform(indent+1)
                except Exception as exc:
                    from traceback import format_exception
                    frmt = format_exception(exc)
                    for line in frmt:
                        self.log(0, str(line.strip()))
                    raise BuildException(self, str(exc))

            self.log(indent, "--- end end target `%s`: %s" % (self._name, time.ctime()))
            self._performed = True
