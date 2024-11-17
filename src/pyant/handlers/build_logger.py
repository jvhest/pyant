class BuildLogger:

    def __init__(self):
        self._loggers = []
        self._indent = "  "

    def add_log(self, logfile):
        if type(logfile) == type(''):
            self._loggers.append(open(logfile, "w+"))
        else:
            self._loggers.append(logfile)

    def write_log(self, indent, msg):
        for log in self._loggers:
            log.write(self._indent * indent + msg + "\n")

    def close(self):
        for log in self._loggers:
            log.close()
