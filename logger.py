import logging
import sys
import utils
import threading

FORMAT = "%(asctime)-15s %(message)s"
formatter = logging.Formatter(FORMAT)
logging.basicConfig(level=logging.INFO)
STDOUT_HANDLER = logging.StreamHandler(sys.stdout)
STDOUT_HANDLER.setFormatter(formatter)
FILE_HANDLER = logging.FileHandler(utils.DATA_DIR+'/librcye.log')
FILE_HANDLER.setFormatter(formatter)
sep = '||'

def get_log(cname):
    log = logging.getLogger(cname)
    #self.log.addHandler(STDOUT_HANDLER)
    log.addHandler(FILE_HANDLER)
    return log
