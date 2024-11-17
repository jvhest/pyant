import sys
import os
import time

from xml.etree.ElementTree import ElementTree

from typing import Dict

from pyant.properties import Properties
from pyant.datatypes.build_exception import BuildException
from pyant.handlers.build_logger import BuildLogger
from pyant.handlers.exec_logger import ExecLogger
from pyant.target import Target
import pyant.utils.utils as utils


class Project:
    """Class with PyAnt project
    """

    def __init__(self, xml_file):
        self._project = self

        # execution logger
        self._execlog = ExecLogger()

        # buildlog
        self._buildlog = BuildLogger()
        self._buildlog.add_log(sys.stdout)

        # build task-mapping
        import pyant.taskdefs as tasks
        self._task_definitions = {}
        self._task_definitions.update(tasks._task_defs_)

        # parse xml-file
        tree = ElementTree(file=xml_file)
        root = tree.getroot()

        # properties:
        self._properties = Properties(self)

        self._properties["pyant.file"] = xml_file

        self._properties["project.date.year"] = time.strftime("%Y")
        self._properties["project.date.month"] = time.strftime("%b")
        self._properties["project.date.day"] = time.strftime("%d")
        self._properties["project.date.weekday"] = time.strftime("%A")
        self._properties["project.date.hour"] = time.strftime("%H")
        self._properties["project.date.minutes"] = time.strftime("%M")
        self._properties["project.date.seconds"] = time.strftime("%S")

        # Patch from Janos BEKESI
        self._properties["project.DSTAMP"] = time.strftime("%Y%m%d")
        self._properties["project.TSTAMP"] = time.strftime("%H:%M")
        self._properties["project.TODAY"] = utils.today()

        # convenience formatted timestring (JB)
        self._properties["project.TSTAMPF"] = time.strftime("%d.%m.%Y %H:%M:%S")

        self._properties["sys.version"] = sys.version
        self._properties["sys.platform"] = sys.platform
        self._properties["sys.byteorder"] = sys.byteorder
        if sys.platform == "win32":
            self._properties["sys.winver"] = sys.winver

        # project attributes:
        self.allowed_attr = ['name', 'basedir', 'buildlog', 'default', 'description']

        # pyant.project
        self._name = self.resolve_property(root.get("name", ""))
        if self._name:
            self._properties["pyant.project"] = self._name
        else:
            raise BuildException(self, "Project has not (name) attribute")

        # pyant.basedir
        self._basedir = root.get("basedir", "")
        if (not self._basedir) or (self._basedir == "."):
            self._basedir = os.getcwd() + "/"
        if os.path.isdir(self._basedir):
            self._properties["pyant.basedir"] = self._basedir
        else:
            raise BuildException(self, "Basedir not a valid directory path: %s" % (self._basedir))

        # buildlog
        log = self.resolve_property(root.get("buildlog", ""))
        if log:
            self._buildlog.add_log(log)

        self.log(0, "-"*70)
        self.log(0, "--- start of build: %s" % (time.ctime()))
        self.log(0, "--- buildfile     : %s" % (xml_file))
        self.log(0, "-"*70)

        # handle child-elements:
        self._target = {}
        for child in root:
            tag = child.tag.lower()
            if tag == "target":
                target = Target(child, self)
                self._target[target._name] = target
            elif tag in ["property", "logging"]:   # - allowed project-tasks
                # handle project-tasks: like: taskdef, property
                if tag in self._task_definitions:
                    task = self._task_definitions[tag](child, self)
                    task.init()
                    task.perform(1)
                else:
                    raise BuildException(self, "task '%s' not defined" % (child.tag))

        # diverse attributes
        self._description = self.resolve_property(root.get("description", ""))
        self._default = self.resolve_property(root.get("default", "main"))

    def resolve_property(self, value):
        return self._properties.replace_properties(value)

    def log(self, indent, msg):
        self._buildlog.write_log(indent, msg)

    def get_log_prefix(self):
        return "[project - " + self._name + "] "

    def execute(self, target):

        deps = target.get_dependencies()
        for dep in deps:
            dep_target = self._target.get(dep)
            if dep_target:
                self.execute(dep_target)
            else:
                raise BuildException(self, "Build target `%s` not defined" % (dep_target._name))
        target.perform(1)

    def perform(self, target_name=None):
        try:
            self.log(0, "--- start running build: %s" % (time.ctime()))
            if not target_name:
                target_name = self._default

            target = self._target.get(target_name)
            if target:
                if target.check_rules():
                    self.execute(target)
                else:
                    self.log(0, "--- target passed by target rule")
            else:
                raise BuildException(self, "Build target `%s` not defined" % (target_name))

            self.log(0, "--- end running build: %s" % (time.ctime()))
            self._buildlog.close()
            self._execlog.close()

        except BuildException as ex:
            self.log(0, "--- error running build: %s" % (time.ctime()))
            raise ex
