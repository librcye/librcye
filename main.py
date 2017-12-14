import sys
import nodeio
import input

fin = input.resolv
if len(sys.argv)>1:
    if sys.argv[1]=='-resolv':
        fin = input.alexa
    elif sys.argv[1]=='-inst':
        fin = input.censored
io = nodeio.NodeIO(fin)
io.load()
io.run()
