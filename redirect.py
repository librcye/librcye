import sys
import logger
import inspect
import nodeio
import input
import utils

log = logger.Log(inspect.getfile(inspect.currentframe())).log

def resolve_redirection(node):
    log.info('resolving host %s:%s' % (node.host, str(node.port)))
    node.connect()
    node.request()
    if (not node.res==None) and node.res.status<400 and node.res.status>=300: 
        location = node.res.getheader('location').split('://')
        host = location[1].split('/', 1)
        node.host = host[0]
        node.path = '/' if host[1]==None else '/'+host[1]
        node.port = nodeio.Node.HTTP_PORT if location[0].split('http')[1]=='' else nodeio.Node.HTTPS_PORT
        node.close()
        resolve_redirection(node)
    elif node.res==None or node.res.status>=400:
        node.port = nodeio.Node.HTTPS_PORT
    node.close()
    return node

if len(sys.argv)>1 and sys.argv[1] == '-inst':
    fin = open(input.censored, 'r')
    record = fin.readline().split('\n')[0].split(utils.SEP)
    while len(record)==2:
        node = nodeio.Node(nodeio.Node.HTTP_PORT, record[1])
        node = resolve_redirection(node)
        if node.routable:
            utils.update_instant_redirection(node)
        record = fin.readline().split('\n')[0].split(utils.SEP)
    fin.close()
else:
    fin = open(input.alexa_test, 'r')
    fout = open(input.alexa_test_res, 'w')
    record = fin.readline().split('\n')[0].split(utils.SEP)
    node = None
    while len(record)>=2:
        node = nodeio.Node(nodeio.Node.HTTP_PORT, record[1])
        node = resolve_redirection(node)
        fout.write(str(node.port)+utils.SEP+node.host+utils.SEP+node.path+'\n')
        record = fin.readline().split(utils.SEP)
    fin.close()
    fout.close()
