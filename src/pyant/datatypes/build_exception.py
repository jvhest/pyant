# -*- coding: utf-8 -*-


class BuildException(Exception):

    def __init__(self, obj, msg):
        Exception.__init__(self)
        self._message = obj.get_log_prefix() + msg

    def get_message(self):
        """Returns message associated with this exception
        """
        return self._message

    def __str__(self):
        """Exception to string, for info only not for serialize
        """
        s = self._message
        return s
