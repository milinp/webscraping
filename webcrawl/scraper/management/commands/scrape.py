
import urllib2, urlparse, sys, traceback, pdb, unicodedata, cookielib, time, threading
from bs4 import BeautifulSoup
from django.core.management.base import BaseCommand, CommandError
from django.core.management.base import make_option
from scraper.models import Website

url = sys.argv[2]
wait = float(sys.argv[3])
url_key = urlparse.urlsplit(url).netloc
jar = cookielib.FileCookieJar("cookies")

urls = [url]
visited = {url : "1"}
storage = []
threads = []
urlArray = []
dummy = "http://news.google.com/news/section?pz=1&cf=all&ned=us&hl=en&q=Wimbledon&topicsid=FRONTPAGE&ict=tnv6"

class Command(BaseCommand):
	def handle(self, *args, **options):
		self.stdout.write('Successfully opened scrape.py')
		main()

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

def main():
	
	initiate()
	try:
		soup = openURL(urls[0])
		urlArray = addLinks(soup)
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
	#print time.time() - start_time, "seconds"

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

def main():
	start_time = time.time()
	initiate()
	try:
		soup = openURL(url[0])
	except Exception as ex:
		print "Exception in user code: " + str(ex)
		print "URL: " + urls[0]

	storage = scrape(soup)

	print storage
	print time.time() - start_time, "seconds"

#returns a string containing all text in html
def scrape(soup):
	if soup.findAll(text = True):
		holder = []
		for s in soup.findAll(text = True):
			if "".join(s.encode('utf-8').split()):
				holder.append("".join(s.encode("ascii", "ignore").split()))
		return "".join(holder)

def initiate():
	if len(sys.argv) != 3:
		print "Input must be two arguments\nCurrently %d\nExiting..." % len(sys.argv)
		sys.exit()
	elif sys.argv[2].find("://") == -1:
		print "Input should be include scheme/protocol!\nExiting..."
		sys.exit()

def openURL(url):
	opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(jar))
	htmltext = BeautifulSoup(opener.open(urls[0]))
	#traceback.print_exc(file=sys.stdout) #prints entire stack trace
	return htmltext

def addLinks(soup):
	for tag in soup.findAll("a", href = True):
		 	tag['href'] = urlparse.urljoin(url, tag['href'])
		 	tag['href'].encode("utf-8")

		 	#check to make sure crawler stays within page domain
		 	#also make sure crawler does not put an already visited page into the queue
		 	if tag['href'].find(url_key) != -1 and not visited.has_key(tag['href'].encode("utf-8")):
		 		urls.append(tag['href'].encode("utf-8"))
		 		visited[tag['href'].encode("utf-8")] = "1"
	return urls	 
