import urllib2
import urlparse
import sys
import traceback
import pdb
import unicodedata
import cookielib
import time
import threading
import re
from bs4 import BeautifulSoup
from django.core.management.base import BaseCommand, CommandError
from django.core.management.base import make_option
from scraper.models import Visited, URLToVisit

url = ""
wait = 0
url_key = "fafa"
jar = cookielib.FileCookieJar("cookies")

urls = []
visited = {url : "1"}
threads = []
urlArray = []
#dummy = "http://pastebin.com/ucDWguUf"

class Command(BaseCommand):
	def handle(self, *args, **options):
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
	global url
	url = args[0]
	urls.append(url)
	global url_key
	url_key = urlparse.urlsplit(urls[0]).netloc
	wait = float(args[1])
	try:
		soup = openURL(urls[0])
		urlArray = addLinks(soup)
		i = 0
		#print "length of URL array - %d" % (len(urlArray))
		for urlForScrape in urlArray:
			threadName = "Thread number %d" % (i)
			thread = myThread(1, threadName, 1, urlForScrape)
			thread.start()
			thread.join()
			# threads.append(thread)
	except Exception as ex:
		print "Exception in user code: " + str(ex)
		print "URL: " + urls[0]  
   	# for t in threads:
   	# 	t.join()

	#storage = scrape(soup)

	#print storage
	#print time.time() - start_time, "seconds"

def startScrapper(urlForScrape):
	#print "URL for Scraping = %s \n\n" % (urlForScrape)
	start_time = time.time()
	urlSoup = ""
	# if not Visited.objects.filter(url = urlForScrape).exists():
	urlSoup = openURL(urlForScrape)
	urlArray.append(addLinks(urlSoup))
	parsedText = scrape(urlSoup)
	Visited(url = urlForScrape, urlData = parsedText).save()

def scrape(soup):
	if soup.findAll(text = True):
		holder = []
		for s in soup.findAll(text = True):
			if "".join(s.encode("ascii", "ignore").split()):
				holder.append("".join(s.encode("ascii", "ignore").split()))
		return "".join(holder)

def openURL(aURL):
	time.sleep(wait)
	opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(jar))
	htmltext = BeautifulSoup(opener.open(aURL))
	return htmltext

def addLinks(soup):
	time.sleep(wait)
	for tag in soup.findAll("a", href = True):
		 	tag['href'] = urlparse.urljoin(url, tag['href'])
		 	tag['href'].encode("utf-8")
		 	#check to make sure crawler stays within page domain
		 	#also make sure crawler does not put an already visited page into the queue
		 	if tag['href'].find(url_key) != -1 and not visited.has_key(tag['href'].encode("utf-8")):
		 		urls.append(tag['href'].encode("utf-8"))
		 		visited[tag['href'].encode("utf-8")] = "1"
	return urls	 
