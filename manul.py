import httplib
import sys

headers = {'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8', 'User-Agent':'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:57.0) Gecko/20100101 Firefox/57.0'}
con = httplib.HTTPConnection(sys.argv[1]) if int(sys.argv[4])==80 else httplib.HTTPSConnection(sys.argv[1])
con.request(sys.argv[3], sys.argv[2], None, headers)

res = con.getresponse()
print str(res.status)+':'+res.reason
print res.getheaders()
if len(sys.argv)>5:
    print res.read()
