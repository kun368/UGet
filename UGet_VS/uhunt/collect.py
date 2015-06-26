import sys, httplib, re, csv, time

url_start = "/index.php?option=com_onlinejudge&Itemid=8&category=93"
csv_filename = "aoapci.csv"
root_name = "AOAPC I: Beginning Algorithm Contests"
nall = 1

url_start = "/index.php?option=com_onlinejudge&Itemid=8&category=28"
csv_filename = "pc.csv"
root_name = "Programming Challenges"
nall = 360

url_start = "/index.php?option=com_onlinejudge&Itemid=8&category=293"
csv_filename = "rujua_liu.csv"
root_name = " Rujia Liu's Presents"
nall = 487

url_start = "/index.php?option=com_onlinejudge&Itemid=8&category=442"
csv_filename = "aoapci_tg.csv"
root_name = "AOAPC I: Beginning Algorithm Contests -- Training Guide"
nall = 566

stat = "ok"

#nall = 360

def sub_collect(url, lv, nid, pid) :
#	print url
	global nall
	global stat
	fail = True
	again = 5
	while fail :
		http1 = httplib.HTTPConnection("uva.onlinejudge.org")
		try :
			print("request data")
			http1.request("GET", url, headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain", "Referer": "http://hvs.me/proxy/index.php"})
			print("get response")
			response = http1.getresponse()
			print("read data")
			data = response.read()
		except :
			#fail = True
			http1.close()
			if again > 0 :
				print("try again %d." % again)
				again -= 1;
				time.sleep(10)
			else :
				print("network error.")
				stat = "error"
				return 0
			#print("try again.")
		else :
			fail = False
			print("ok.")
			#stat = "ok"
		#if fail :
		#	print("network error.")
		#	stat = "error"
		#	return 0
	#else :
	if fail == False :
		http1.close()
		print("analyz data.")
		allmat = patfile.findall(data)
		for mat in allmat :
			nall = nall + 1
			writer.writerow([nall, nid, int(mat[1]), 'uva'])
			for i in range(1, lv) :
				print('- -'),
			print("@ " + mat[1])
		allmat = patfolder.findall(data)
		for mat in allmat :
			nall = nall + 1
			writer.writerow([nall, nid, mat[1], 'nil'])
			for i in range(1, lv) :
				print('- -'),
			print(mat[1])
			sub_collect('/' + mat[0].replace('&amp;', '&'), lv + 1, nall, nid)

writer = csv.writer(file(csv_filename, 'wb'))
writer.writerow(['id', 'pid', 'name', 'oj'])

patfolder = re.compile(r"""<img[^>]*alt="FOLDER"[^>]*>[\s]*</td>[\s]*<td>[\s]*<a href="([^"]*)">([^<]*)</a>""", re.I)
patfile = re.compile(r"""<img[^>]*alt="FILE"[^>]*>[\s]*</td>[\s]*<td>[\s]*<a href="([^"]*)">(\d*)[^<]*</a>""", re.I)

writer.writerow([nall, 0, root_name, 'nil'])
sub_collect(url_start, 1, nall, 0)

if stat == "error":
	print("error, plz try again. -_-")
else:
	print("all data down! ^o^")
