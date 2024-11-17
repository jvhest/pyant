# -*- coding: utf-8 -*-
import os
import time


class ExecLogger:

    def __init__(self):
        self._log = None

    def set_log(self, logfile, mode):
        if mode == 'write':
            # rewrite file
            self._log = open(logfile, "w+")
        else:
            # append file
            if os.path.exists(logfile):
                self._log = open(logfile, "a+")
            else:
                self._log = open(logfile, "w+")

    def write(self, msg):
        if self._log:
            self._log.write(msg)

    def writeln(self, msg=''):
        if self._log:
            self._log.write(msg + "\n")

    def write_colomn(self, msg, width, align='left'):
        if self._log:
            if align == 'left':
                self._log.write("%%-%ds"%(5)%msg[:width])
            elif align == 'right':
                self._log.write("%%%ds"%(5)%msg[:width])

    def write_list(self, lst, width, col_count, align='left'):
        if self._log:
            col = 0
            for l in lst:
                if col == col_count:
                    self.writeln()
                    col = 0
                self.write_colomn(str(l), width, align)
                col += 1

            self.writeln()

    def write_dict(self, dic, width):
        if self._log:
            for k, v in dic:
                self.write_colomn(str(k), width)
                self.write(': ')
                self.write_colomn(str(v), width)
                self.writeln()

    def write_line(self, width, char='-'):
        if self._log:
            self.writeln(char * width)

    def write_tstamp(self):
        if self._log:
            self.write(time.strftime("%Y%m%d-%H%M"))

    def close(self):
        if self._log:
            self._log.close()
