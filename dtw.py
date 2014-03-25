# !/usr/bin/python
#
# Author: geolado | g3ol4d0
# Email : g3ol4d0[at]gmail.com
# Python 2.7

# To do : 1 - Making the Google Parser better and more efficient , Google Ajax obtains less results and ban easily
#		  2 - Working in the Proxies ( identify which was banned , etc )


import sys , argparse , socket , urllib , subprocess , urllib2 , json , random , time , os

def banner():
	screen = getTerminalSize()
	center_width = screen[1]

	banner_ascii =	[" _____ _________          __",
					 "|  __ \__   __\ \        / /",
					 "| |  | | | |   \ \  /\  / / ",
					 "| |  | | | |    \ \/  \/ /  ",
					 "| |__| | | |     \  /\  /   ",
					 "|_____/  |_|      \/  \/    ",
					 "                            ",
					 "Dork The World/0.1",
					 "by geolado | g3ol4d0"]
				 
	for line in banner_ascii :
		print line.center(center_width)				 

def getTerminalSize():

	line = os.popen('stty size', 'r').read().split()
	line = map(int , line)

	return line    

class Google_parser(object) :
	
	def __init__(self):

		self.google = "http://ajax.googleapis.com"
		self.agents = [
		'Mozilla/4.0 (compatible; GoogleToolbar 4.0.1019.5266-big; Windows XP 5.1; MSIE 6.0.2900.2180)',
		'Nokia3230/2.0 (5.0614.0) SymbianOS/7.0s Series60/2.1 Profile/MIDP-2.0 Configuration/CLDC-1.0',
		'Opera/10.61 (J2ME/MIDP; Opera Mini/5.1.21219/19.999; en-US; rv:1.9.3a5) WebKit/534.5 Presto/2.6.30',
		'SonyEricssonW995/R1EA Profile/MIDP-2.1 Configuration/CLDC-1.1 UNTRUSTED/1.0',
		'HTC-ST7377/1.59.502.3 (67150) Opera/9.50 (Windows NT 5.1; U; en) UP.Link/6.3.1.17.0',
		'FeedFetcher-Google; ( http://www.google.com/feedfetcher.html)',
		'DoCoMo/2.0 N905i(c100;TB;W24H16) (compatible; Googlebot-Mobile/2.1;  http://www.google.com/bot.html)',
		'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; de-at) AppleWebKit/533.21.1 (KHTML, like Gecko) Version/5.0.5 Safari/533.21.1',
		'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.57 Safari/537.36'
		]
		self.dork = urllib.quote_plus(args.dork)
		self.pages = args.pages
		self.type = args.type
		self.delay = args.delay
		self.proxy_on = args.proxy_on
		self.ip = urllib2.urlopen("http://myip.dnsdynamic.org/").read()
		self.proxy = []
		self.loop = 0
		self.google_list = []

		with open("dtw_proxy_list.txt") as f :
			self.proxy = f.readlines()

	def dorking(self) :
		
		while True :

			if self.loop > self.pages :
				break

			screen = getTerminalSize()
			screen_height = screen[0]
			screen_width = screen[1]
			center_width = screen[1]		

			if self.proxy_on :	
				try :
					proxy_in = {"http":"http://%s" % self.proxy[random.randint(0,len(self.proxy)-1)]}	
					proxy_support = urllib2.ProxyHandler(proxy_in)	
					opener = urllib2.build_opener(proxy_support)
					urllib2.install_opener(opener)
				except :
					print "[!] Proxy list invalid ( example : 192.168.0.1:80 , jumping line ) , or the proxy is down ."	

			self.google_post = self.google +'/ajax/services/search/web?v=2.0&rsz=8&q=%s&start=%s&userip=%s' %(self.dork,self.loop,self.ip)

			self.header = {'User-Agent' : self.agents[random.randint(0,len(self.agents)-1)]}

			try :
				self.req = urllib2.Request(self.google_post,None,self.header)
				self.google_response = urllib2.urlopen(self.req).read()
				self.google_json = json.loads(self.google_response)
			except :
				print "[!] Can't connect to Google !"

			if self.google_json['responseData'] == None :
				print "[!] Error : 403 ! Google is blocking our dorking .Try change the syntax of it , add an proxy or increase the delay"
				break

			for i in range(len(self.google_json['responseData']['results'])) :
				self.google_list.append(self.google_json['responseData']['results'][i]["url"])	

			self.loop += 1 

			time.sleep(self.delay)

		return self.google_list	

class dork_the_world(object):

	def __init__(self):

		self.lurl = []
		self.cmd = args.cmd
		self.type = args.type
		self.dork = args.dork
	
	def search(self):	

		print "[i] Beginning search on Google , may take awhile ..."
		print "[i] Dork : {dork}".format( dork = self.dork)

		self.urls = g.dorking()
	
		if self.type == "ip" :
			for url in self.urls :
				self.lurl.append(socket.gethostbyname(url.split("/",3)[2]))
		elif self.type == "path" :
			for url in self.urls :
				self.lurl.append("/"+url.split("/",3)[3])
		elif self.type == "url"	:
			for url in self.urls :
				self.lurl.append(url)	

		self.lurl = list(sorted(set(self.lurl)))		

		print"[i] Found {number} results".format(number = len(self.lurl))
		print"[i] List : "

		for url in self.lurl :
			print "\t"+url
	
	def cmdexec(self):

		screen = getTerminalSize()
		screen_width = screen[1]
		screen_height = screen[0]

		print "[i] Executing commands"

		for url in self.lurl :
			print "[i] #{i} $ {cmd}".format( i = self.lurl.index(url)+1 , cmd = self.cmd.replace("^URL^",url) )
			print "-"*screen_width
			subprocess.call(self.cmd.replace("^URL^",url) , shell=True)
			print "-"*screen_width

		print "[i] Finished !"
		
	

if __name__ == "__main__":

	banner()

	parser = argparse.ArgumentParser()
	parser.add_argument('-d' , '--dork' , type=str , help='The dork to search' , required=True)
	parser.add_argument('--cmd' , help='Command to execute with the URL/IP. Example : --dork="ping -c 5 ^URL^"' , required=True)
	parser.add_argument('-p' , '--pages' , type=int , default=5 , help='Number of pages to get from Google' )
	parser.add_argument('--delay' , type=int , default=1 , help='Delay time in secs ( Default = 1 s )' )
	parser.add_argument('--type' , action='store' , default="url" , help='Determinate the type of the URL output ( url , ip , path )')
	parser.add_argument('--proxy_on' , action  = 'store_true' , help= 'Turn on the proxy list ( dtw_proxy_list.txt )')

	args = parser.parse_args()
	d = dork_the_world()
	g = Google_parser()

	d.search()
	d.cmdexec()


