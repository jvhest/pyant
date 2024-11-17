# -*- coding: utf-8 -*-


class Properties:

    def __init__(self, project):
        self._project = project
        self._properties = {}

    def __setitem__(self, name, value):
        self._properties[name] = value

    def __getitem__(self, name):
        if name is None:
            return None
        return self._properties[name]

    def add_properties(self, propdict):
        for key in propdict.keys():
            self._properties[key] = propdict[key]

    def get_properties(self):
        return self._properties

    def replace_properties(self, value):

        fragments = []
        proprefs = []
        prev = 0
        pos = value.find("$", prev)
        while pos >= 0:
            if pos > 0:
                fragments.append(value[prev:pos])
            if pos == len(value) - 1:
                fragments.append("$")
                prev = pos + 1
            elif value[pos+1] != '{':
                fragments.append(value[pos+1: pos+2])
                prev = pos + 2
            else:
                endPos = value.find("}", pos)
                if endPos < 0:
                    raise
                propertyName = value[pos+2: endPos]
                fragments.append(None)
                proprefs.append(propertyName)
                prev = endPos + 1
            pos = value.find("$", prev)

        if prev < len(value):
            fragments.append(value[prev:])

        result = ""
        for frag in fragments:
            if frag is None:
                pName = proprefs.pop(0)
                if pName in self._properties:
                    frag = self._properties[pName]
                else:
                    frag = ""
                    self.log(0, "property niet gedefinieerd: %s" % pName)
            result = result + frag

        return result

