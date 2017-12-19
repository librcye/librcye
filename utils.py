import time
import os
import sys

DATA_DIR = os.curdir+'/data'
conlog = DATA_DIR+'/con.log'
alexa = DATA_DIR+'/zgrab'
resolv = DATA_DIR+'/resolv'
unresolv = DATA_DIR+'/unresolved'
censored = DATA_DIR+'/'
tmp_censored = censored+'censored'
censored += sys.argv[3] if len(sys.argv)>2 and sys.argv[2]=='-o' else 'censored'
headers = {
    'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'User-Agent':'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:57.0) Gecko/20100101 Firefox/57.0',
    'Accept-Encoding':'gzip, deflate'
    
}


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

def get_censorship_type(node, fin):
    if not node==None:
        return CENSORED
    record = fin.readline().split(',')
    while len(record)>2:
        if record[2]==node.host and len(record)>4:
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

def separate(values, sep):
    strv = ''
    l = len(values)
    for i,val in enumerate(values):
        strv+= val+sep if i<l-1 else val
    return strv
    
