librcye (libre cyber)->(librecyber)->(librecy)->(librcye)

GOAL
  censorship watchdog, and solutions, with eye on increasing censorship in Middle-East region, blocking any dissent, secure communication, and VOIP, as tyranny increases, with censorship on evading tools, and solutions, we hope to provide awareness, guidance, and solutions to each problem.

LANGUAGE
 nost ?
 node------------destination service, or ip:port
 non-http [node]-tcp node with no binding at 80, or 443
 http [node]-----tcp node binding at 80, or 443
 validtion-------censorship test
 censored--------node is censored if guidelines (2), or (3) are valid.
 nodes-database--human-readable http nodes database. see below

GUIDELINES
  1- each node makred censored only after validation.
  2- ISPs apply DPI(Deep Packet Inspection).
  3- DNSs are censored.

INPUT/OUTPUT
  in---nodes database
  out--censored nodes database

DESIGN
'''
INSTANT_FORMAT: host
CENSORED_FORMAT: stamp,host

'''

NODES DATABASE
  nodes Database: records
  |records\nstamp
  records: PORT\tHOST\n
  | record\nrecord
  stamp: (string returned by ctime(2)
  
  PORT--80/443
  HOST--two-labeled hostname lable1.hostname.tld 
--------------------------------------------------------
FACTS
  - some servers (top ranked) resonse to not supported by status code 3xx  instad of 4xx
POSSIBLE CENSORSHIP TECHINQUES:
  - DPI
    - the most used.
  - DNS filtering
    - naive.
  - url paths[links]
    - economically expensive.
TODO
  - imp test
  - emulate protocols
  - does all severs respond with higher labels?
  - some site could have instance redirection, emulate redirection of sensored sites.
  - types of redirection 302, torproject.com redirect to www.torproject.com
  - classify sites, services, research, ML, manually
  - implement  parallel connection
  - usetimeout, the right amount?
  - distributed scan
  - implement censys API
  - TODO does all 3xx has location header
  - work beyond alexa1mil
QUESTIONS
  - some requests succeed in first time, and fails afterwards, like https://www.torproject.org, letancy increases per time as more connections are made.
  - are any services other than http are censored?which?
  - how http is censored?
  - does DNS offer any kind of statistics for top used?
  - statistics and backward compatability of ipv6
  - are censys records apre unique?
  - DPI in egypt drops connection(443) during handshake,
    and thus make any http method to fail, does that same method allover?
    it could be smart and drop packets based on ip history, to confuse the watchdog.
  - todo in nodeio.py
  - some hosts doesn't support HEAD, GET it the only gurantee responsive method, verify it was the case with roletaryk.info
  - badstatusline (not known status code) is it censored? is marked as not censored.
    - is badstatusline censored?