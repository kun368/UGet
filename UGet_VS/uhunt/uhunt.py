import httplib, re, time, codecs

ShowAll = False	# True if show all user, otherwise only ours
UseProxy = True	# True if can not access uhunt directly
ACDetail = True # True if want time & rank for ac submission

# host config
if UseProxy :
	uhunt_host = "hvs.me"
	url_poll = "/proxy/browse.php?b=0&f=norefer&u=http://uhunt.felix-halim.net/api/poll/"
else :
	uhunt_host = "uhunt.felix-halim.net"
	url_poll = "/api/poll/"

# status table, with color header (only work in linux?)
status = {	0 : ["Unknown", "UN", "\033[1;35m"],
			10 : ["Submission error", "SE", "\033[1;35m"],
			15 : ["Can't be judged", "CJ", "\033[1;35m"],
			20 : ["In queue", "QU", "\033[1;37m"],
			30 : ["Compile error", "CE", "\033[1;33m"],
			35 : ["Restricted function", "RF", "\033[1;35m"],
			40 : ["Runtime error", "RE", "\033[1;36m"],
			45 : ["Output limit", "OL", "\033[1;35m"],
			50 : ["Time limit", "TL", "\033[1;34m"],
			60 : ["Memory limit", "ML", "\033[1;34m"],
			70 : ["Wrong answer", "WA", "\033[1;31m"],
			80 : ["PresentationE", "PE", "\033[0;33m"],
			90 : ["Accepted", "AC", "\033[1;32m"]
		}

ENDC = "\033[0m"

# read problem, using regular expression
prob = dict()
fprob = open("problem.txt", "r")
sp = fprob.read().replace('\\"', '@fuck@')
fprob.close()
pat = re.compile(r"""\[(\d+),(\d+),"([^"]+)",[^,]+,[^,]+,[^,]+,[^,]+,[^,]+,[^,]+,[^,]+,[^,]+,[^,]+,[^,]+,[^,]+,[^,]+,[^,]+,[^,]+,[^,]+,[^,]+\]""")
allmat = pat.findall(sp)
for mat in allmat :
	d = {int(mat[0]) : [int(mat[1]), mat[2].replace("@fuck@", '"')]}
	prob.update(d)
#	print "%6d %6d %s" %(int(mat[0]), prob[int(mat[0])][0], prob[int(mat[0])][1])

users = dict()
fusr = codecs.open("user.txt", "r", "gb2312")
sn = int(fusr.readline())
for i in range(1, sn) :
	uid = int(fusr.readline())
	uname = fusr.readline().replace("\n", "")
	d = {uid : uname}
	users.update(d)
#	print "%6d %s" %(uid, users[uid])
fusr.close()

http1 = httplib.HTTPConnection(uhunt_host)
st = "0"
binit = True
print "game start."
# main loop
while True :
#	print st
	fail = 1
	while fail == 1 :
		fail = 0
		try :
			http1.request("GET", url_poll + st, headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain", "Referer": "http://hvs.me/proxy/index.php"})
			response = http1.getresponse()
		except :
			fail = 1
	data = response.read()
#	print response.status, response.reason, len(data), response.getheaders()
	# extract data from the response js array
	pat = re.compile(r"""{"id":([\-]?\d+),"type":"lastsubs","msg":{"sid":([\-]?\d+),"pid":([\-]?\d+),"ver":([\-]?\d+),"run":([\-]?\d+),"mem":([\-]?\d+),"uid":([\-]?\d+),"sbt":([\-]?\d+),"lan":([\-]?\d+),"name":"([^"]+)","uname":"([^"]+)","rank":([\-]?\d+)}}""")
	allmat = pat.findall(data)
	for mat in allmat :
		st = mat[0] # update event index, as stamp for next loop
		if ShowAll or users.get(int(mat[6]), "") != "": # show only our users
			ns = int(mat[3])
			if ns != 0 : # show status except verdict 0 (in queue infact)

				print "%s%s %-18s %s %6d %s%s" %(status[ns][2], time.strftime("%m-%d %H:%M:%S", time.localtime(int(mat[7]))), mat[10], status[ns][1], prob[int(mat[2])][0], prob[int(mat[2])][1], ENDC)
				if ACDetail and (ns == 90 or ns == 70) :
					print "                                  " + mat[4] + " ms, rank " + mat[11]
	binit = False

