import os
import time
import inspect
import logger
import nodeio
import input
import utils

def classify():
    if not os.path.exists(input.censored):
        file = open(input.censored, 'w')
        file.close()
    ofile = open(input.censored, 'r')
    nfile = open(input.tmp_censored, 'r')
    diff = utils.diff_records(ofile, nfile, 2)
    ofile.close()
    nfile.close()
    #post newly censored
    newly = open(input.newly_censored, 'w') 
    for diffy in diff[1]:
        if diffy[1] == -1:
            newly.write(diffy[0])
    newly.close()
    #post uncensored
    uncensored = open(input.uncensored, 'w')
    for diffy in diff[0]:
        if diffy[1] == -1:
            uncensored.write(diffy[0])
    uncensored.close()
    os.rename(input.tmp_censored, input.censored)

log = logger.Log(inspect.getfile(inspect.currentframe())).log
io = nodeio.NodeIO()
io.load_alexa1mil()
time1 = time.time()
time2 = 0
timespan = 0
mils = 0
MIL = 1000
for i, node in enumerate(io.nodes):
    if i%MIL==0 and i >0:
        time2 = time.time()
        diff = time2-time1
        timespan += diff
        time1 = time2
        mils += 1
        log.info(' %f hours: tiempo promedio por mil igual %f min, timespan', timespan/3600, timespan/(mils*60))
    node.valid()
    io.write_node(node)
classify()
