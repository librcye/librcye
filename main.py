import sys
import nodeio
import input

fin = input.resolv
if len(sys.argv)>1:
    if sys.argv[1]=='-resolv':
        fin = input.alexa
    elif sys.argv[1]=='-inst':
        fin = input.censored
    if len(sys.argv)>2 and sys.argv[2]=='-o':
        input.set_censored(sys.argv[3])

io = nodeio.NodeIO(fin)
io.load()
io.run()
