import sys
import nodeio
import utils

fin = utils.resolv
if len(sys.argv)>1:
    if sys.argv[1]=='-resolv':
        fin = utils.alexa
    elif sys.argv[1]=='-inst':
        fin = utils.censored

io = nodeio.NodeIO(fin)
io.run()
