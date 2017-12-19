import httplib
import inspect
import threading
import time
import os
import shutil
import utils
import logger
import socket

log = logger.get_log(inspect.getfile(inspect.currentframe()))
rout = open(utils.resolv, 'w', 1) 
cout = open(utils.tmp_censored, 'w', 1)
cin  = open(utils.censored, 'w', 1) if os.path.exists(utils.censored) else None
lout= open(utils.conlog, 'w', 1)
unrout = open(utils.unresolv, 'w', 1)
#globalize Node objective variables.

class Node(threading.Thread):
    HTTP_PORT = 80
    HTTPS_PORT = 443
    GET = 'GET' #the only gurantee http(s) method
    CONNECT = 'CONNECT'
    def __init__(self, ip, host, port=None, path=None, lock=None, resolv=None, inst=None):
        threading.Thread.__init__(self)
        self.ip = ip
        self.port = Node.HTTP_PORT if port==None else int(port)
        self.host = host.split('\n')[0]
        self.path = '/' if path==None else path
        self.routable = True #guideline(1)
        self.con = None
        self.res = None
        self.method = Node.GET if self.port==Node.HTTP_PORT else Node.CONNECT
        self.lock = lock
        self.resolv = False if resolv==None else resolv
        self.inst = False if inst==None else inst
        
    def connect(self):
        self.con = httplib.HTTPConnection(self.host) if self.port==Node.HTTP_PORT else httplib.HTTPSConnection(self.host)

    def request(self):
        try:
            self.con.request(self.method, self.path, None, utils.headers)
            self.res = self.con.getresponse()
            if not self.res==None:
                self.log()
            if not self.res==None and self.method==Node.CONNECT and self.port==Node.HTTPS_PORT and self.res.status>=300:
                #fallback to GET, (TODO) the best you can do is to emulate http(s) connection with controlled ttl, and timeout
                self.method = Node.GET
                self.close()
                self.connect()
                self.request()
            else:
                self.routable = self.res.status<300
        except socket.gaierror, sock:
            log.info('******can\'t resolv!: %s', sock)
            unrout.write(self.ip+utils.SEP+self.host+'\n')
            return False
        except httplib.BadStatusLine, e:
            log.info('BadStatusLine: %s\n%s %s:%d:%s \n%d:%s\n%s', e, self.method, self.host, self.port, self.path, self.res.status if not self.res==None else -1, self.res.reason if not self.res==None else None, self.res.getheaders() if not self.res==None else None)
        except Exception, e:
            self.routable = False
            log.info('Exception: %s\n%s %s:%d:%s \n%d:%s\n%s', e, self.method, self.host, self.port, self.path, self.res.status if not self.res==None else -1, self.res.reason if not self.res==None else None, self.res.getheaders() if not self.res==None else None)
        return True

    def write(self):
        log.info('writing %s to disk', self.host)
        censored = self.ip+':'+str(self.port)+utils.SEP+self.host+utils.SEP+self.path
        if self.resolv: #resolv redirection, use files instead.
            resolv = censored+'\n'
            utils.dwrite(resolv, rout, self.lock)
        if not self.inst and not self.routable: #censored
            censorship_type = utils.get_censorship_type(self, cin)
            censored = utils.stamp()+utils.SEP+censored+utils.SEP+str(censorship_type)+'\n'
            utils.dwrite(censored, cout, self.lock)
        elif self.inst: #check instant resolv redirection
            for rec in old_censored:
                if rec.split(utils.SEP)[2]==self.host:
                    censored += rec
                    break
            if self.routable:
                censored += ','+str(True)
            censored+='\n'
            utils.dwrite(censored, cout, self.lock)

    def close(self):
        self.con.close()
        self.res = None

    def resolve_redirection(self):
        log.info('resolving host %s:%s%s' % (self.host, str(self.port), self.path))
        self.connect()
        if not self.request():
            return False
        if (not self.res==None) and self.res.status<400 and self.res.status>=300:
            location = self.res.getheader('location').split('://')
            if len(location)==1: #location:relative path
                self.path = location[0]
            else: #location:full path
                host = location[1].split('/', 1)
                self.host = host[0]
                self.path = ''
                if len(host)>1:
                    self.path += '/'
                    self.path += host[1]
                self.port = Node.HTTP_PORT if location[0].split('http')[1]=='' else Node.HTTPS_PORT
            self.close()
            self.resolve_redirection()
            return True
        elif self.res==None or self.res.status>=400:
            self.port = Node.HTTPS_PORT
        self.close()
        return True
    
    def log(self):
        #TODO(fix)  maintain order
        msg = utils.separate([self.ip, str(self.port), self.host, self.path, str(utils.headers), '\n', str(self.res.status), self.res.reason, str(self.res.getheaders()), '\n'], logger.sep)
        utils.dwrite(msg, lout, self.lock)
        
    def run(self):
        if self.resolv or self.inst: #TODO self.inst attribute is redundant
            log.info('***resolving started 4 %s**', self.host)
            if not self.resolve_redirection():
                self.close()
                return
        log.info('**validation started 4 %s**', self.host)
        self.connect()
        if self.request():
            self.write()
        self.close()
        log.info('**validation finished 4 %s**', self.host)

old_censored = []
class NodeIO:

    def __init__(self, fin):
        global rout
        global cout
        global cin
        self.nodes = []
        self.lock = threading.Lock()
        self.fin = fin #string name
        #todo append, and keep index pointer

    def run(self): 
        hin = open(self.fin, 'r')
        record = hin.readline()
        values = []
        ip = None
        port = None
        host = None
        path = None
        resolv = False
        inst = False
        line = 1
        time1 = time.time()
        time2 = 0
        timespan = 0
        NL = 100
        while not record=='':
            if line%NL==0 and line>0:
                delc = 0
                for i,node in enumerate(self.nodes):
                    node.join()
                    del self.nodes[i-delc]
                    delc+=1
                time2 = time.time()
                diff = time2-time1
                timespan += diff
                time1 = time2
                log.info(' %f hours: tiempo promedio igual %f min, timespan', timespan/3600, timespan/(10*60))
                
            values = record.split('\n')[0].split(utils.SEP)
            if self.fin==utils.censored:
                ip, port = values[1].split(':')
                host = values[2]
                path = values[3]
                resolv = True
                inst = True
                ctype = int(values[4])
                if ctype|utils.CENSORED==ctype or ctype|utils.NEWLY_CENSORED==ctype:
                    continue
            elif self.fin==utils.resolv:
                ip, port = values[0].split(':')
                host = values[1]
                path = values[2]
                inst = bool(values[3]) if values>3 else False
            elif self.fin==utils.alexa:
                ip = values[0]
                host = values[1]
                resolv = True
            else:
                log.warn("irregular input file")
            node = Node(ip, host, port, path, self.lock, resolv, inst)
            node.start() #todo it has to be pruned after it's done.
            self.nodes.append(node)
            old_censored.append(record)
            line+=1
            record = hin.readline()
        hin.close() #generalize
        for node in self.nodes:
            node.join()

    def close(self):
        shutil.copyfile(utils.tmp_censored, utils.censored)
        cin.close()
        cout.close()
        rout.close()
        lout.close()
        unrout.close()
