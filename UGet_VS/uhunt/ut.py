import os, sys, httplib, re, time, codecs, csv

ShowAll = False	# True if show all user, otherwise only ours
UseProxy = True	# True if can not access uhunt directly
ACDetail = True # True if want time & rank for ac submission

# host config
if UseProxy :
	uhunt_host = 'uhunt.felix-halim.net'
	url_u2i = '/api/uname2uid/'
	url_poll = '/api/poll/'
	url_usp = '/api/subs-pids/'
	url_usi = '/api/subs-user/'
else :
	uhunt_host = 'uhunt.felix-halim.net'
	url_u2i = '/api/poll/uname2uid/'
	url_poll = '/api/poll/'
	url_usp = '/api/subs-pids/'
	url_usi = '/api/subs/'

# status table, with color header (only work in linux?)
status = {	0 : ['Unknown', 'UN', '\033[1;35m'],
			10 : ['Submission error', 'SE', '\033[1;35m'],
			15 : ['Can\'t be judged', 'CJ', '\033[1;35m'],
			20 : ['In queue', 'QU', '\033[1;37m'],
			30 : ['Compile error', 'CE', '\033[1;33m'],
			35 : ['Restricted function', 'RF', '\033[1;35m'],
			40 : ['Runtime error', 'RE', '\033[1;36m'],
			45 : ['Output limit', 'OL', '\033[1;35m'],
			50 : ['Time limit', 'TL', '\033[1;34m'],
			60 : ['Memory limit', 'ML', '\033[1;34m'],
			70 : ['Wrong answer', 'WA', '\033[1;31m'],
			80 : ['PresentationE', 'PE', '\033[0;33m'],
			90 : ['Accepted', 'AC', '\033[1;32m']
		}

LIGHT_GRAY = '\033[0;37m'
ENDC = '\033[0m'

# read problem, using regular expression
prob = dict()
probr = dict()
fprob = open('problem.txt', 'r')
sp = fprob.read().replace("\\\"", "@fuck@")
fprob.close()
pat = re.compile(r"""\[(\d+),(\d+),"([^"]+)",[^,]+,[^,]+,[^,]+,[^,]+,[^,]+,[^,]+,[^,]+,[^,]+,[^,]+,[^,]+,[^,]+,[^,]+,[^,]+,[^,]+,[^,]+,[^,]+,[^,]+,[^,]+\]""")
allmat = pat.findall(sp)
for mat in allmat :
	d = {int(mat[0]) : [int(mat[1]), mat[2].replace("@fuck@", '"')]}
	prob.update(d)
	d = {int(mat[1]) : int(mat[0])}
	probr.update(d)
#	print('%6d %6d %s' %(int(mat[0]), prob[int(mat[0])][0], prob[int(mat[0])][1]))

def loaduser(fil) :
	allusr = ''
	users = dict()
	usersr = dict()
	fusr = codecs.open(fil, 'r', 'gb2312')
	sn = int(fusr.readline())
	for i in range(1, sn + 1) :
		uid = int(fusr.readline())
		uname = fusr.readline().replace('\n', '').strip()
		d = {uid : uname}
		users.update(d)
		d = {uname : uid}
		usersr.update(d)
		if i == 1 :
			allusr = str(uid)
		else :
			allusr += ',' + str(uid)
		#print('%6d %s' %(uid, users[uid]))
	fusr.close()
	return users, usersr, allusr

# extract user submission data
def extract_user_submit(uname, data, lst) :
	# extract data from the response js array
	pat = re.compile(r"""\[([F\-]?\d+),([\-]?\d+),([\-]?\d+),([\-]?\d+),([\-]?\d+),([\-]?\d+),([\-]?\d+)\]""")
	allmat = pat.findall(data)
	for mat in allmat :
		ns = int(mat[2])
		#print(mat)
		#print(mat[2])
		if ns != 0 : # show status except verdict 0 (in queue infact)
			lst.insert(0, [ns, int(mat[4]), uname, int(mat[3]), int(mat[6]), 0, int(mat[1])])

# extract submission data
def extract_submit(data, lst) :
	pat = re.compile(r"""{"name":"[^}]*","uname":"([^}]*)","subs":\[([^}]*)\]}""")
	allmat = pat.findall(data)
	for mat in allmat :
		if mat[1] != '' :
			extract_user_submit(mat[0], mat[1], lst)

# show all users' submission on some pid
def get_submit_pid(pid, usr, lst) :
	http1 = httplib.HTTPConnection(uhunt_host)
	fail = False
	try :
		http1.request('GET', url_usp + allusr + '/' + str(pid) + '/0' , headers = {'Content-type': 'application/x-www-form-urlencoded', 'Accept': 'text/plain', 'Referer': 'http://hvs.me/proxy/index.php'})
		response = http1.getresponse()
	except :
		fail = True
	if fail :
		print('network error.')
		return False
	else :
		data = response.read()
		extract_submit(data, lst)
		return True

def uname2uid(uname) :
	uid = usersr.get(uname, 0)
	if uid :
		return uid
	http1 = httplib.HTTPConnection(uhunt_host)
	fail = False
	try :
		http1.request('GET', url_u2i + uname, headers = {'Content-type': 'application/x-www-form-urlencoded', 'Accept': 'text/plain', 'Referer': 'http://hvs.me/proxy/index.php'})
		response = http1.getresponse()
		uid = int(response.read())
	except :
		fail = True
	if fail :
		print('network error.')
		return 0
	else :
		return uid

# get all submission of one user
def get_submit_uid(uid, lst, force) :
	fil = './cache/uvasub_' + str(uid) + '.dat'
	if force or not os.path.isfile(fil) :
		http1 = httplib.HTTPConnection(uhunt_host)
		fail = False
		try :
			http1.request('GET', url_usi + str(uid), headers = {'Content-type': 'application/x-www-form-urlencoded', 'Accept': 'text/plain', 'Referer': 'http://hvs.me/proxy/index.php'})
			response = http1.getresponse()
			data = response.read()
		except :
			fail = True
		if fail :
			print('network error.')
			return False
		else :
			# update cache
			f = open(fil, 'w')
			f.write(data)
			f.close()
	else :
		# read from cache file
		f = open(fil, 'r')
		data = f.read()
		f.close()
	pat = re.compile(r"""{"name":"[^}]*","uname":"([^}]*)","subs":\[([^}]*)\]}""")
	allmat = pat.findall(data)
	for mat in allmat :
		if mat[1] != '' :
			extract_user_submit(mat[0], mat[1], lst)
	return True

def display_submit_list(lst) :
	for item in lst :
		if item[5] != 1 :
			ns = int(item[0])
			if ns != 0 : # show status except verdict 0 (in queue infact)
				sout = '%s%s %-18s %s%s' %(status[ns][2], time.strftime('%m-%d %H:%M:%S', time.localtime(int(item[1]))), item[2], status[ns][1], ENDC)
				if ns == 90 :
					sout += ' %d ms, rank %d' %(item[3], item[4])
				print(sout)

def display_user_submit_list(lst) :
	for item in lst :
		if item[5] != 1 :
			ns = int(item[0])
			if ns != 0 : # show status except verdict 0 (in queue infact)
				sout = '%s%s %s %s%s' %(status[ns][2], time.strftime('%m-%d %H:%M:%S', time.localtime(int(item[1]))), status[ns][1], prob.get(item[6], 'unknown'), ENDC)
				if ns == 90 :
					sout += ' %d ms, rank %d' %(item[3], item[4])
				print(sout)

def cmp_by_name_rank(a, b) :
	if a[2] == b[2] :
		return cmp(a[4], b[4])
	return cmp(a[2], b[2])

def cmp_by_time(a, b) :
	return cmp(a[1], b[1])

def cmp_by_rank(a, b) :
	return cmp(a[4], b[4])

def cmp_by_validsub(a, b) :
	if a[0] == 90 and b[0] == 90 :
		return cmp(a[1], b[1])
	if a[0] == 90 :
		return 1
	return -1

def count_tree(r, i, lv, lst, pd, pinf, cd) :
	c = r.get(i)[1]
	for item in c :
		p = r.get(item)[0]
		if p['oj'] != 'nil' :
			cd[int(p['name'])] = pd[int(p['name'])];
	cd2 = dict(cd)
	for item in c :
		p = r.get(item)[0]
		if p['oj'] == 'nil' :
			ncd = dict(cd2)
			count_tree(r, item, lv + 1, lst, pd, pinf, ncd)
			for item in ncd :
				cd[item] = ncd[item]
	nd = 0
	nf = 0
	np = 0
	for item in cd :
		if cd[item] == 90 :
			nd = nd + 1
		elif cd[item] == -1 :
			np = np + 1
		else :
			nf = nf + 1
	pinf.update({i : [nd, nf, np]})

def draw_analyze_tree(r, i, lv, lst, pd, pinf, outf, detail) :
	for l in range(1, lv) :
		print('- -'),
		outf.write(l == lv + 1 and '- -' or '- - ')
	s = '%s [ %d = %d : %d : %d, %.2f%% ]' %(i != 0 and r.get(i)[0]['name'] or 'root', pinf[i][0] + pinf[i][1] + pinf[i][2], pinf[i][0], pinf[i][1], pinf[i][2], pinf[i][0] * 100 / (float)(pinf[i][0] + pinf[i][1] + pinf[i][2]))
	print(s)
	outf.write(s + '\n')
	c = r.get(i)[1]
	bd = False
	bf = False
	bp = False
	for item in c :
		p = r.get(item)[0]
		if p['oj'] != 'nil' :
			if pd[int(p['name'])] == 90 :
				bd = True
			elif pd[int(p['name'])] == -1 :
				bp = True
			else :
				bf = True
	if bd :
		for l in range(1, lv + 1) :
			if detail :
				print('   '),
			outf.write(l == lv + 1 and '   ' or '    ')
		if detail :
			print('accept :'),
		outf.write('accept :')
		for item in c :
			p = r.get(item)[0]
			if p['oj'] != 'nil' and pd[int(p['name'])] == 90:
				if detail :
					print(status[pd[int(p['name'])]][2] + p['name'] + ENDC),
				outf.write(' ' + p['name'])
		if detail :
			print('')
		outf.write('\n')
	if bf :
		for l in range(1, lv + 1) :
			if detail :
				print('   '),
			outf.write(l == lv + 1 and '   ' or '    ')
		if detail :
			print('failed :'),
		outf.write('failed :')
		for item in c :
			p = r.get(item)[0]
			if p['oj'] != 'nil' and pd[int(p['name'])] != 90 and pd[int(p['name'])] != -1 :
				if detail :
					print(status[pd[int(p['name'])]][2] + p['name'] + ENDC),
				outf.write(' ' + p['name'])
		if detail :
			print('')
		outf.write('\n')
	if bp :
		for l in range(1, lv + 1) :
			if detail :
				print('   '),
			outf.write(l == lv + 1 and '   ' or '    ')
		if detail :
			print('no sub :'),
		outf.write('no sub :')
		for item in c :
			p = r.get(item)[0]
			if p['oj'] != 'nil' and pd[int(p['name'])] == -1 :
				if detail :
					print(LIGHT_GRAY + p['name'] + ENDC),
				outf.write(' ' + p['name'])
		if detail :
			print('')
		outf.write('\n')
	for item in c :
		p = r.get(item)[0]
		if p['oj'] == 'nil' :
			draw_analyze_tree(r, item, lv + 1, lst, pd, pinf, outf, detail)

def load_analyze(fil) :
	f = open(fil, 'r')
	analst = dict()
	csvlst = csv.DictReader(f, delimiter = ',')
	for item in csvlst :
		pid = int(item['pid'])
		nid = int(item['id'])
		if analst.get(pid, None) == None :
			d = {pid : [None, list()]}
			analst.update(d)
		analst.get(pid)[1].insert(len(analst.get(pid)[1]), nid)
		if analst.get(nid, None) == None :
			d = {nid : [item, list()]}
			analst.update(d)
		else :
			analst.get(pid)[1] = item
	f.close()
	return analst

def analyze_user(analst, r, uid, fil, detail) :
	lst = list()
	if get_submit_uid(uid, lst, False) :
		pdone = dict()
		pinf = dict()
		cd = dict()
		for e in analst :
			d = {e: [0, 0, 0]}
			pinf.update(d)
		for pr in probr :
			d = {pr : -1}
			pdone.update(d)
		lst.sort(cmp_by_validsub)
		for pr in lst :
			#print("=============\n")
			#print(pr)
			#print(pr[6], pr[0])
			#print(prob.get(pr[6], -1))
			if prob.get(pr[6], -1) == -1:
				continue
			d = {prob.get(pr[6], -1)[0] : pr[0]}
			#print(d)
			pdone.update(d)
		outf = codecs.open(fil, 'w', 'gb2312')
		outf.write(('[%d] %s\n\n' %(uid, users.get(uid, 'unknown'))))
		count_tree(analst, r, 1, lst, pdone, pinf, cd)
		draw_analyze_tree(analst, r, 1, lst, pdone, pinf, outf, detail)
		outf.close()

# main ------------------------------

users = ''
usersr = ''
allusr = ''
analst = ''

users, usersr, allusr = loaduser('user.txt')
analst = load_analyze('uva.csv')

while True :
	cmd = sys.stdin.readline().replace('\n', '').strip()
	if re.match('sub[\s]+(\d+)[\s]*', cmd) or re.match('cmp[\s]+(\d+)[\s]*', cmd) :
		mat = re.findall('([\S]+)[\s]+(\d+)', cmd)
		cmd = mat[0][0]
		pid = probr.get(int(mat[0][1]), 0)
		if pid == 0 :
			print('problem not found.')
		else :
			lst = list()
			if get_submit_pid(pid, allusr, lst) :
				if cmd == 'cmp' :
					lst.sort(cmp_by_name_rank)
					for i in range (0, len(lst)) :
						if lst[i][0] != 90 :
							lst[i][5] = 1
						if i > 0 and lst[i][2] == lst[i - 1][2] and lst[i - 1][0] == 90 :
							lst[i][5] = 1
					lst.sort(cmp_by_rank)
				else :
					lst.sort(cmp_by_time)
				display_submit_list(lst)
				print('%d - %s' %(prob[pid][0], prob[pid][1]))
	elif re.match('us[\s]+(.*\S)', cmd) or re.match('ac[\s]+(.*\S)', cmd) :
		mat = re.findall('([\S]+)[\s]+(.*\S)', cmd)
		cmd = mat[0][0]
		usr = mat[0][1]
		uid = uname2uid(usr)
		if uid == -1 :
			print('no such user')
		elif uid > 0 :
			lst = list()
			if get_submit_uid(uid, lst, True) :
				lst.sort(cmp_by_time)
				display_user_submit_list(lst)
			print('[%d] %s' %(uid, usr))
	elif re.match('load[\s]+(\S.*)', cmd) :
		mat = re.findall('([\S]+)[\s]+([\S]+)', cmd)
		cmd = mat[0][0]
		fil = mat[0][1]
		analst = load_analyze(fil + '.csv')
	elif re.match('ana[\s]+(\d*)[\s]+(.*\S)', cmd) or re.match('ana[\s]+(\d*)', cmd) :
		if re.match('ana[\s]+(\d*)[\s]+(.*\S)', cmd) :
			mat = re.findall('(\S+)[\s]+(\d*)[\s]+(.*\S)', cmd)
			for item in analst :
				if analst.get(item)[0] != None and analst.get(item)[0]['name'] == mat[0][2] :
					r = item
					break
		else :
			mat = re.findall('(\S+)[\s]+(\d*)', cmd)
			r = 0
		usr = mat[0][1]
		fail = False
		try :
			uid = int(usr) # uname2uid(usr)
		except :
			fail = True
		if fail :
			print('uid should be integer')
		else :
			if uid == -1 :
				print('no such user')
			elif uid > 0 :
				print('[%d] %s' %(uid, users.get(uid, 'unknown')))
				analyze_user(analst, r, uid, 'output.txt', True)
	elif re.match('anaf[\s]+(.*\S)', cmd) :
		mat = re.findall('(\S+)[\s]+(.*\S)', cmd)
		fil = mat[0][1]
		us, ur, su = loaduser(fil)
		for u in us :
			print('[%d] %s' %(u, users.get(u, 'unknown')))
			lst = list()
			get_submit_uid(u, lst, True)
			analyze_user(analst, 0, u, 'ana_' + str(u) + '.txt', False)
		print('all done.')
	elif re.match('\s*cls\s*', cmd) :
		os.system("clear")
	else :
		print('command invalid.')

