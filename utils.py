import input
import time
import os

CENSORED=0b1
UNCENSORED=0b10
NEWLY_CENSORED=0b100

#classification
UNDEFINED=0b1000
NEWS=0b10000
ACTIVISM=0b100000
LAW=0b1000000
HUMANE_RIGHTS=0b10000000
RELIGION=0b1000000000
SEXUALITY=0b100000000000
PORNOGRAPHY=0b10000000000000
SEP = ','

def stamp():
    return time.ctime(None)

def get_censorship_type(node):
    if os.path.exists(input.censored):
        fin = open(input.censored)
        record = fin.readline().split(',')
        while len(record)>1:
            if record[2]==node.host:
                ctype = int(record[4])
                if ctype|CENSORED==ctype or ctype|NEWLY_CENSORED==ctype:
                    if node.routable:
                        return UNCENSORED
                    else:
                        return CENSORED
            record = fin.readline().split(',')
        return NEWLY_CENSORED

def pwrite(msg, path, mode, lock=None, close=False):
    write(msg, lock, None, close, path, mode)
def dwrite(msg, fout, lock=None, close=False):
    write(msg, lock, fout, close)
def write(msg, lock=None, fout=None, close=False, path=None, mode=None):
    if fout==None:
        fout = open(path, mode)
    if not lock==None:
        lock.acquire()
    fout.write(msg)
    if not lock==None:
        lock.release()
    if close:
        fout.close()
        
