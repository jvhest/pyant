
from .datatypes.build_exception import BuildException


class XmlComponent:
    """Abstract XML Component"""

    def __init__(self, xml_element, parent, attr={}, children=[]):
        self._parent = parent

        self._project = self._parent._project
        self._execlog = self._project._execlog
        self._properties = self._project._properties

        self.allowed_children = children

        self._cdata = xml_element.text      # - characterdata
        self._tagname = xml_element.tag       # - xml tagname

        # update attributes with actual xml-attributes or default value
        self.allowed_attr = []
        for key in attr.keys():
            self.__dict__["_"+key] = xml_element.get(key, attr[key])
            self.allowed_attr.append('_'+key)

        # check for illegal attibutes
        for key in xml_element.keys():
            if '_'+key not in self.allowed_attr:
                raise BuildException(self, "Attribute %s of [%s] not defined" % (key, str(self._tagname)))

        # handle child-elements:
        self._children = []
        for child in xml_element:
            tag = child.tag
            if (self.allowed_children == ["*"]) or (tag in self.allowed_children):   # - tag allowed??
                if tag in self._project._task_definitions:
                    task = self._project._task_definitions[tag](child, self)
                    task.init()
                    self._children.append((tag, task))
                else:
                    raise BuildException(self, "task '%s' not defined" % (child.tag))

    def get_children(self, tag):
        return [v for k, v in self._children if k == tag]

    def get_log_prefix(self):
        # override in target and abstract task
        pass

    def log(self, indent, msg):
        self._project.log(indent, msg)
