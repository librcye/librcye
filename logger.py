import logging
import sys
import input

FORMAT = "%(asctime)-15s %(message)s"
formatter = logging.Formatter(FORMAT)
logging.basicConfig(level=logging.INFO)
STDOUT_HANDLER = logging.StreamHandler(sys.stdout)
STDOUT_HANDLER.setFormatter(formatter)
FILE_HANDLER = logging.FileHandler(input.DATA_DIR+'/librcye.log')
FILE_HANDLER.setFormatter(formatter)

class Log:
    def __init__(self, cname):
        self.log = logging.getLogger(cname)
        self.log.addHandler(STDOUT_HANDLER)
        self.log.addHandler(FILE_HANDLER)
