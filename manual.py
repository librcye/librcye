import httplib
import sys

if sys.argv[4]==str(80) or sys.argv[4]==str(0):
    con = httplib.HTTPConnection(sys.argv[1])
    con.request(sys.argv[2], sys.argv[3])
    res = con.getresponse()
    print ('%s:%s' % (res.status, res.reason))
    print res.getheaders()
    if len(sys.argv)>5:
        print res.read()
    con.close()
if sys.argv[4] == str(443) or sys.argv[4]==str(0):
    con = httplib.HTTPSConnection(sys.argv[1])
    con.request(sys.argv[2], sys.argv[3])
    res = con.getresponse()
    print ('%s:%s' % (res.status, res.reason))
    print res.getheaders()
    if len(sys.argv)>5:
        print res.read()
    con.close()

