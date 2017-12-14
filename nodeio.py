import httplib
import inspect
import threading
import logger
import time
import utils
import input

log = logger.Log(inspect.getfile(inspect.currentframe())).log

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
            self.con.request(self.method, self.path)
            self.res = self.con.getresponse()
            if not (self.res == None) and self.method==Node.CONNECT and self.port==Node.HTTPS_PORT and self.res.status>=300:
                #fallback to GET, (TODO) the best you can do is to emulate http(s) connection with controlled ttl, and timeout
                self.method = Node.GET
                self.close()
                self.connect()
                self.request()
            else:
                self.routable = self.res.status<300
        except httplib.BadStatusLine:
            pass
        except:
            self.routable = False
        return self.routable

    def resolve_redirection(self):
        log.info('resolving host %s:%s' % (self.host, str(self.port)))
        self.connect()
        self.request()
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
            return
        elif self.res==None or self.res.status>=400:
            self.port = Node.HTTPS_PORT
        self.close()

    def valid(self):
        self.connect()
        self.request()
        self.close()
        return self.routable

    def run(self):
        if self.resolv or self.inst: #TODO self.inst attribute is redundant
            self.resolve_redirection()
        self.valid()

    def close(self):
        self.con.close()
        self.res = None

class NodeIO:

    def __init__(self, fin):
        self.nodes = []
        self.records = []
        self.lock = threading.Lock()
        self.fin = fin #string name
        if self.fin==input.alexa:
            self.rout = open(input.resolv, 'w', 1)
        self.cout = open(input.censored, 'w', 1)
        #todo append, and keep index pointer

    def load(self):
        log.info('loading')
        file = open(self.fin, 'r')
        record = file.readline()
        values = []
        ip = None
        port = None
        host = None
        path = None
        resolv = False
        inst = False
        line = 1
        while not record=='':
            if line>1 and line%1000==0:
                log.info('node %d record:%s', line, record)
            values = record.split('\n')[0].split(utils.SEP)
            if self.fin==input.censored:
                ip, port = values[1].split(':')
                host = values[2]
                path = values[3]
                resolv = True
                inst = True
                ctype = int(values[4])
                if ctype|utils.CENSORED==ctype or ctype|utils.NEWLY_CENSORED==ctype:
                    continue
            elif self.fin==input.resolv:
                ip, port = values[0].split(':')
                host = values[1]
                path = values[2]
                inst = bool(values[3]) if values>3 else False
            elif self.fin==input.alexa:
                ip = values[0]
                host = values[1]
                resolv = True
            else:
                log.warn("irregular input file")
            self.nodes.append(Node(ip, host, port, path, self.lock, resolv, inst))
            if self.fin==input.censored:
                self.records.append(record)
            line+=1
            record = file.readline()
        file.close()

    def run(self, joining=True):
        log.info('running')
        time1 = time.time()
        time2 = 0
        timespan = 0
        mils = 0
        MIL = 1000
        for i,node in enumerate(self.nodes):
            if i%MIL==0 and i >0:
                time2 = time.time()
                diff = tinme2-time1
                timespan += diff
                time1 = time2
                mils += 1
                log.info(' %f hours: tiempo promedio por mil igual %f min, timespan', timespan/3600, timespan/(mils*60))
            node.run()
            node.start()
            log.info('loading node per host %s', node.host)
        if joining:
            censored = ''
            resolv = ''
            for node in self.nodes:
                node.join()
                log.info('writing node %s', node.host)
                censored = node.ip+':'+str(node.port)+utils.SEP+node.host+utils.SEP+node.path
                if node.resolv: #resolv redirection, use files instead.
                    resolv = censored+'\n'
                    utils.dwrite(resolv, self.rout, self.lock)
                if not node.inst and not node.routable: #censored
                    censorship_type = utils.get_censorship_type(node)
                    censored = utils.stamp()+utils.SEP+censored+str(censorship_type)+'\n'
                    utils.dwrite(censored, self.cout, self.lock)
                elif node.inst: #check instant resolv redirection
                    for rec in self.records:
                        if rec.split(utils.SEP)[2]==node.host:
                            censored += rec
                            break
                    if node.routable:
                        censored += ','+str(True)
                    censored+='\n'
                    utils.dwrite(censored, self.cout, self.lock)
        self.cout.close()
        if self.rout:
            self.rout.close()
