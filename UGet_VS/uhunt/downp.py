import httplib, re

http1 = httplib.HTTPConnection("uva.onlinejudge.org")
fprob = open("problem.txt", "r")
sp = fprob.read()
fprob.close()
pat = re.compile(r"""\[(\d+),(\d+),"([^"]+)",[^,]+,[^,]+,[^,]+,[^,]+,[^,]+,[^,]+,[^,]+,[^,]+,[^,]+,[^,]+,[^,]+,[^,]+,[^,]+,[^,]+,[^,]+,[^,]+\]""")
allmat = pat.findall(sp)
for mat in allmat :
	np = int(mat[1])
	sp = mat[2]
	cf = True
	sf = "prob/%d - %s.html" % (np, sp)
	try :
		fw = open(sf, "w")
	except :
		cf = False
		print "could not create file : " + sf
	if cf :
		url = "/external/" + str(int(np / 100)) + "/" + str(np) + ".html"
		print "down [%d - %s] fron %s .." %(np, sp, url)
		fail = 1
		while fail == 1 :
			fail = 0
			try :
				http1.request("GET", url, headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain", "Referer": "http://hvs.me/proxy/index.php"})
				response = http1.getresponse()
				print "  ok."
			except :
				fail = 1
				print "  retry."
		data = response.read()
		newd = data
		imgpat = re.compile(r"""(<IMG[^>]+SRC[/s]*=[/s]*"([^"]*)"[^>]*>)""", re.I)
		allimg = imgpat.findall(data)
		for img in allimg :
			so = img[0]
			sn = so.replace(img[1], "http://uva.onlinejudge.org/external/" + str(int(np / 100)) + "/" + img[1])
			newd = newd.replace(so, sn)
		fw.write(newd)
		fw.close()

