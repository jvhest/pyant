#!/usr/bin/env python
# Author Ivan V. Begtin (C) 2002
# See license file in docs directory

import sys, os
from pyant.handlers import *

class Properties:

    #-----------------------------        
    def __init__(self, project):
        self._project = project
        self._properties = {}
        self._prophandlers = {}
        self.add_property_handler(FileHandler(self))
        self.add_property_handler(HttpHandler(self))
        self.add_property_handler(FtpHandler(self))
        if os.name == "nt":
            self.add_property_handler(RegkeyHandler(self))

    #-----------------------------        
    def __setitem__(self, name, value):
        handler = self._prophandlers.get(value.split(':')[0])
        if handler:
            self._properties[name] = handler.handle(value)
        else:
            self._properties[name] = value

    #-----------------------------        
    def __getitem__(self, name):
        if name is None:
            return None
        return self._properties[name]

    #-----------------------------        
    def add_properties(self, propdict):
        for key in propdict.keys():
            self._properties[key] = propdict[key]

    #-----------------------------        
    def get_properties(self):
        return self._properties

    #-----------------------------        
    def add_property_handler(self, handler):
        self._prophandlers[handler.get_prefix()] = handler

    #-----------------------------        
    def get_property_handlers(self):
        return self._prophandlers

    #-----------------------------        
    def replace_properties(self, value):

        fragments = []
        proprefs = []
        prev = 0
        pos = value.find( "$", prev)