import urllib2, urlparse, sys, traceback, pdb, unicodedata, cookielib, time, threading
from bs4 import BeautifulSoup
from django.core.management.base import BaseCommand, CommandError
from django.core.management.base import make_option
from scraper.models import Visited

url = ""
wait = 0
url_key = urlparse.urlsplit(url).netloc
jar = cookielib.FileCookieJar("cookies")

urls = []
visited = {url : "1"}
storage = []
threads = []
urlArray = []
dummy = "http://news.google.com/news/section?pz=1&cf=all&ned=us&hl=en&q=Wimbledon&topicsid=FRONTPAGE&ict=tnv6"


class Command(BaseCommand):

	def handle(self, *args, **options):
		self.stdout.write('Successfully openedfafafa scrape.py')
		main(args)

class myThread (threading.Thread):
    def __init__(self, threadID, name, counter, urlForScrape):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter
        self.urlForScrape = urlForScrape
    def run(self):
        #print "/n %s /n"  % (self.name)
        startScrapper(self.urlForScrape)

def main(args):
	print args

	initiate()
	url = args[0]
	urls.append(url)
	wait = float(args[1])
	start_time = time.time()
	try:
		soup = openURL(urls[0])
		addLinks(soup)
		i = 0
		print "length of URL array - %d" % (len(urlArray))
		for urlForScrape in urlArray:
			i = i + 1
			#if i == 2:
			#	break
   			threadName = "Thread number %d" % (i)
   			thread = myThread(1, threadName, 1, urlForScrape)
   			thread.start()
   			threads.append(thread)
   	except Exception as ex:
		print "Exception in user code: " + str(ex)
		print "URL: " + urls[0]  
   	for t in threads:
   		t.join()

	#storage = scrape(soup)

	#print storage
	print time.time() - start_time, "seconds"

def startScrapper(urlForScrape):
	time.sleep(wait)

	#print "printing the URL Array \n"
	#print urlArray
	print "URL for Scraping = %s \n\n" % (urlForScrape)
	start_time = time.time()
	urlSoup = ""
	urlSoup = openURL(urlForScrape)
	#print "printing URL soup %s"  % (urlSoup)
	parsedText = scrape(urlSoup)
	storage.append(parsedText)	
	print storage
	print '\n\n'
	print time.time() - start_time, "seconds"

# def scrape(soup):
# 	if soup.findAll(text = True):
# 		holder = []
# 		for s in soup.findAll(text = True):
# 			if "".join(s.encode('utf-8').split()):
# 				holder.append("".join(s.encode("ascii", "ignore").split()))
# 		return "".join(holder)

def scrape(soup):
	
	[s.extract() for s in soup('!DOCTYPE')]
	[s.extract() for s in soup('script')]
	[s.extract() for s in soup('form')]
	[s.extract() for s in soup('style')]
	[s.extract() for s in soup('head')]
	
	if soup.findAll(text = True):
		holder = []


		ingreds = soup.find('div', {'id': 'code_frame'})
		for s in ingreds.findAll('li'):
			holder.append(s.getText().encode('utf-8'))
		return "".join(holder)

    	#ingreds = [str(s.getText().strip( ))	 for s in ingreds.findAll('li')]
    	#return ingreds
		#<textarea id="paste_code"
		#<div class="paste_box_info">
		#<div class="paste_box_info">
		#(id=re.compile("para$"))
		#print soup.findAll('div', attrs={'id':'code_frame'})
		#print "this is another attempt \n"
		#print soup.findAll(text = True)
		#return soup.findAll('textarea', attrs={'id':'paste_code'})
		#return soup.findAll(text = True)

def initiate():
	print "the length of arguments are %d" % len(sys.argv)
	if len(sys.argv) < 3:
		print "Input must be two arguments\nExiting..."
		sys.exit()
	# elif sys.argv[2].find("://") == -1:
	# 	print sys.argv[2]
	# 	print "Input should be include scheme/protocol!\nExiting..."
	# 	sys.exit()

def openURL(url):
	opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(jar))
	htmltext = BeautifulSoup(opener.open(urls[0]))
	#traceback.print_exc(file=sys.stdout) #prints entire stack trace
	return htmltext

def addLinks(soup):
	banana = []
	for tag in soup.findAll("a", href = True):
		 	tag['href'] = urlparse.urljoin(url, tag['href'])
		 	tag['href'].encode("utf-8")

		 	#check to make sure crawler stays within page domain
		 	#also make sure crawler does not put an already visited page into the queue
		 	# if tag['href'].find(url_key) != -1 and not visited.has_key(tag['href'].encode("utf-8")):
		 	banana.append(tag['href'].encode("utf-8"))
	 		visited[tag['href'].encode("utf-8")] = "1"
	for peel in banana:
		Website(url = peel).save()
		

if __name__ == "__main__":
	main()

	#this is an edit