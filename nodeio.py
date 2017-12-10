import httplib
import inspect
import logger
import utils
import input

log = logger.Log(inspect.getfile(inspect.currentframe())).log

class Node:
    HTTP_PORT = 80
    HTTPS_PORT = 443
    GET = 'GET' #the only gurantee http(s) method
    CONNECT = 'CONNECT'
    def __init__(self, port, host, path=None):
        self.port = int(port)
        self.host = host.split('\n')[0]
        self.path = '/' if path==None else path
        self.routable = True #guideline(1)
        self.con = None
        self.res = None
        self.method = Node.GET if self.port==Node.HTTP_PORT else Node.CONNECT
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
    
    def valid(self):
        self.connect()
        self.request()
        self.close()
        return self.routable
    
    def close(self):
        self.con.close()
        self.res = None

class NodeIO:
    
    def __init__(self):
        self.nodes = []
        self.line = 1
        
    #from censys.io alexa1min
    def load_alexa1mil(self):
        file = open(input.alexa_test_res, 'r')
        while True:
            record = file.readline()
            if record=='' or record=='\n':
                break
            values = record.split('\n')[0].split(',')
            self.nodes.append(Node(values[0], values[1], values[2]))
        file.close()

    def write_node(self, node):
        if not node.routable:
            out = open(input.tmp_censored, "a")
            out.write(str(self.line)+','+utils.stamp()+','+node.host+'\n')
            out.close()
        self.line+=1
