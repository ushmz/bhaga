import logging
from logging import getLogger, StreamHandler, Formatter, FileHandler

# class LoggingFilter():
    # def __init__(self, level):
    #    self.__level = level
    
    # def filter(self, record):
    #     return record.levelno <= self.__level

class LogHandler:

    def __init__(self, label):
        if label == 'init':
            sep = '########################'
            self.logger = getLogger(__name__)
            self.logger.setLevel(logging.INFO)

            logFormat = logging.Formatter(sep+'\n%(asctime)s\n\t%(levelname)s - %(message)s\n')

            self.setLogHandler(logging.ERROR, './error.log', logFormat)
            self.setLogHandler(logging.WARNING, './warning.log', logFormat)
            self.setLogHandler(logging.INFO, './info.log', logFormat)
        elif label != None:
            self.addLogHandler()
    
    def setLogHandler(self, level, filename, logFormat):
        handler = logging.FileHandler(filename)
        handler.setLevel(level)
        handler.setFormatter(logFormat)
        self.logger.addHandler(handler)
    
    def addLogHandler(self):
        sep = '########################'
        logFormat = logging.Formatter(sep+'\n%(asctime)s\nFile:'+'label'+'.py\n\t%(levelname)s - %(message)s\n')
        handler = logging.FileHandler('./error.log')
        handler.setLevel(logging.ERROR)
        handler.setFormatter(logFormat)
        self.logger.addHandler(handler)

    def logInfo(self, text):
        self.logger.info(text)

    def logWarning(self, text):
        self.logger.warn(text)

    def logException(self, text):
        self.logger.exception(text)
