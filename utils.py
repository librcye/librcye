import input
import time

SEP = ','

def stamp():
    return time.ctime(None)

#TODO  generalize instant,remove_censored, and diff below
def add_instant_redirection(node):
    lines = ''
    fin = open(input.instant_redirection, 'rw')
    line = fin.readline()
    while len(line):
        if not line.split('\n')[0]==node.host:
            lines+=line
        line = fin.readline()
    lines+=node.host+'\n'
    fin.write(lines)
    
def remove_censored(node):
    lines = ''
    fin = open(input.censored, 'rw')
    line = fin.readline()
    while len(line):
        if not line.split(SEP)[1].split('\n')[0]==node.host:
            lines+=line
        line = fin.readline()
    fin.write(lines)

def update_instant_redirection(node, index):
    add_instant_redirection(node)
    remove_censored(node)

def readiff(fin, index):
    nodes = []
    line = fin.readline()
    while len(line) and len(line.split(SEP))==index+1:
        nodes.append([line, -1])
        line = fin.readline()
    return nodes

'''
left, right old, new of the same format, seperated by character \,
index is for the comparsion indeces
'''
def diff_records(left, right , index):
    lnodes = readiff(left, index)
    rnodes = readiff(right, index)
    for i, l in enumerate(lnodes):
        for j, r in enumerate(rnodes):
            #you can do better by pushing un mapped diffy to end, and holding index for start of unmapped region.
            if l[0].split(SEP, index)[index]==r[0].split(SEP, index)[index]:
                l[1] = j
                r[1] = i
    return [lnodes, rnodes]
