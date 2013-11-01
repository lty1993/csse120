import datetime
from tkinter import INSERT, END

class Logger(object):
    """
    The logger class (FRONT) that logs all history events.
    Contributor: Xiangqing Zhang
    """
    def __init__(self):
        super().__init__()
        self.logger_list = {
            "ConsoleLogger": ConsoleLogger(),
            "GuiLogger": GuiLogger()
        }
    def add(self, message, method_name, level="DEBUG", logger=None):
        """
        Method that calls the logger to log events.
        @Parameter message: A STR which is the content of the event to log.
        @Parameter method_name: The name of the method where the event happens.
        @Parameter level: Should be "DEBUG", "WARNING", "SEVERE", "INFO" and "SUCCESS".
        @Parameter logger: Optional. By default, all loggers will be called to log the event.

        E.g.1 self._log("Lost connection.", "disconnect", "DEBUG")
        E.g.2 self._log("This will only be shown on the console.",
                        "test_function", logger="ConsoleLogger")
        Contributor: Xiangqing Zhang
        """
        # DONE: Move this method into a Logger class.
        if isinstance(message, str):
            if logger:
                if isinstance(logger, list):
                    for each_logger_name in self.logger_list:
                        if each_logger_name in logger:
                            self.logger_list[each_logger_name].log(message, method_name, level)
                else:
                    if logger in self.logger_list:
                        self.logger_list[logger].log(message, method_name, level)
                    else:
                        self.add("Cannot find the specific logger '%s'."%logger, "logger", "SEVERE", "ConsoleLogger")
            else:
                # print(self.logger_list)
                for each_logger_name in self.logger_list:
                    self.logger_list[each_logger_name].log(message, method_name, level)
        else:
            self.add("Error while adding the log. Debug level must be str type.", "add", "SEVERE")
    def add_ignore(self, logger_name, ignore_level):
        """
        Sets specific logger(s) to ignore specific level(s) of events.
        @Parameter logger_name: Can be a STR or a LIST of STRs.
        @Parameter ignore_level: Can be a STR or a LIST of STRs.
        Contributor: Xiangqing Zhang
        """
        if isinstance(logger_name, str): logger_name = [logger_name]
        if isinstance(ignore_level, str): ignore_level = [ignore_level]
        for each_logger_name in logger_name:
            if not each_logger_name in self.logger_list:
                self.add("Cannot find the specific logger '%s'."%logger_name, "logger", "SEVERE", "ConsoleLogger")
            else:
                for each_ignore in ignore_level:
                    self._add_ignore(each_logger_name, each_ignore)
    def _add_ignore(self, logger_name, ignore_level):
        self.logger_list[logger_name].ignore_level_list[ignore_level] = True
    def cancel_ignore(self, logger_name, ignore_level):
        """
        Sets specific logger(s) to log specific level(s) of events.
        @Parameter logger_name: Can be a STR or a LIST of STRs.
        @Parameter ignore_level: Can be a STR or a LIST of STRs.

        Notice: By default, the logger logs all events.
                Call this function is effective ONLY after calling self.add_ignore()!
        Contributor: Xiangqing Zhang
        """
        if isinstance(logger_name, str): logger_name = [logger_name]
        if isinstance(ignore_level, str): ignore_level = [ignore_level]
        for each_logger_name in logger_name:
            if not each_logger_name in self.logger_list:
                self.add("Cannot find the specific logger '%s'."%logger_name, "logger", "SEVERE", "ConsoleLogger")
            else:
                for each_ignore in ignore_level:
                    self._cancel_ignore(each_logger_name, ignore_level)
    def _cancel_ignore(self, logger_name, ignore_level):
        self.logger_list[logger_name].ignore_level_list[ignore_level] = False

class LoggerType(object):
    """
    General interface of a logger. (BACK END)
    Contributor: Xiangqing Zhang
    """
    def __init__(self):
        super().__init__()
        self.ignore_level_list = {}
    def log(self, message, method_name, level="DEBUG"):
        """
        Method that calls the logger to log events.
        @Parameter message: A STR which is the content of the event to log.
        @Parameter method_name: The name of the method where the event happens.
        @Parameter level: Should be "DEBUG", "WARNING", "SEVERE", "INFO" and "SUCCESS".

        Notice: This can be (and should be) ovrrided.

        E.g.1 self._log("Lost connection.", "disconnect", "DEBUG")
        E.g.2 self._log("This will only be shown on the console.", "test_function")
        Contributor: Xiangqing Zhang
        """
        raise NotImplementedError

class ConsoleLogger(LoggerType):
    """
    The logger that prints the event on the console.
    """
    def __init__(self):
        super().__init__()
    def log(self, message, method_name, level="DEBUG"):
        if not level in self.ignore_level_list:
            print(datetime.datetime.now().strftime("%H:%M:%S"), "[%s] <%s> %s"%(method_name, level, message))

class GuiLogger(LoggerType):
    """
    The logger that shows the event in the GUI.
    """
    def __init__(self):
        super().__init__()
        self.gui = None
    def log(self, message, method_name, level="DEBUG"):
        print(self.gui)
        if self.gui:
            if not level in self.ignore_level_list:
                self.gui.log_text.insert(INSERT, datetime.datetime.now().strftime("%H:%M:%S") + " [%s] <%s> %s\r\n"%(method_name, level, message))

# Please ONLY use the robotLogger!
robotLogger = Logger()

def main():
    logger = Logger()
    logger.add_ignore("ConsoleLogger", "DEBUG")
    logger.add("test", "aaa", "DEBUG")
    logger.add("test", "aaa", "DEBUG", "NotExistLogger")

if __name__ == '__main__':
    main()