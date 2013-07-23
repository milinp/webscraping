import httplib2
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
import os, signal, subprocess
from bs4 import BeautifulSoup, SoupStrainer
from datetime import datetime
from django.utils.timezone import utc
import dateutil.parser as dparser 
import pytz
from pytz import timezone
from django.core.management.base import BaseCommand, CommandError
from django.core.management.base import make_option
from scraper.models import DummyVisited, PastebinEntries
import pytz



url = ""
wait = 0
url_key = "fafa"
jar = cookielib.FileCookieJar("cookies")
urls = []
visited = {url : "1"}
isStop = False
urlArray = []
start_time = 0
#dummy = "http://pastebin.com/ucDWguUf"

class Command(BaseCommand):
	def handle(self, *args, **options):
		startTimer()
		if(args[0] == 'stop'):
			stopScraping()
		else:
			main(args)

class myThread (threading.Thread):
    def __init__(self, threadID, name, counter, urlForScrape):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter
        self.urlForScrape = urlForScrape
    def run(self):
        startScrapper(self.urlForScrape)

def main(args):
	global isStop
	isStop = False
	global urlArray
	global url
	url = args[0]
	urls.append(url)
	global url_key
	url_key = urlparse.urlsplit(urls[0]).netloc
	wait = float(args[1])
	try:
		urlArray = []
		soup = openURL("http://pastebin.com/archive")
		addLinks(soup)
		i = 0
		print "\n\n\n---------------------------------------Restarting----------------------------------------------------------------------------\n\n"
		print "Length of urlArray = %d\n\n\n" % (len(urlArray))
		print urlArray
		for urlForScrape in urlArray:
			status = getStatus()
			print getTime()
			if status or getTime() > float(args[2]) - 2:
				print("We killed it")
			else: 
				i = i + 1
				threadName = "Thread number %d" % (i)
				thread = myThread(1, threadName, i, urlForScrape)
				time.sleep(wait)
				thread.start()
				thread.join()
				urlArray.pop(0)

			if len(urlArray) == 1:
				print "\n\n\n"
				print urlArray
				print "\n\n\n"
				addLinks(soup)
		
	except Exception as ex:
		print "Exception in user code: " + str(ex)
		print "URL: " + urls[0]  

def getStatus()	:
	return isStop

def startScrapper(urlForScrape):
	start_time = time.time()
	urlSoup = ""
	if not DummyVisited.objects.filter(url = urlForScrape).exists():
		print "new entry = %s\n\n" % (urlForScrape)
		urlSoup = openURL(urlForScrape)
		parsedText = scrape(urlSoup)
		modifiedTime = scrape_date(urlSoup)
		#modifiedTime = datetime.utcnow().replace(tzinfo = utc).strftime('%Y-%m-%d %H:%M:%S')
		#print "modifiedTime Time"
		#print parsedText
		DummyVisited(url = urlForScrape, urlData = parsedText, modifiedTime = modifiedTime).save()
		
	else:
		print "Repeated entry  = %s" % (urlForScrape)

def scrape(soup):
	textBody = ""
	# check to see if div exists. It should because it's specific to pastebin.
	if soup.findAll("textarea", attrs = {"id" : "paste_code"}):
		for s in soup.find("textarea", attrs = {"id" : "paste_code"}):
			textBody = s.encode("ascii","ignore")
		return textBody
	else: 
		return "This is not the text you are looking for."

# returns date of pastebin post as a datetime object
def scrape_date(soup):
	# check to see if div exists. It should because it's specific to pastebin.
	if soup.findAll("div", attrs = {"class" : "paste_box_info"}):
		# filter out the title attribute which holds the date
		for s in soup.findAll("span", title = True, style = True, text = True):
			dateString = s['title']

		# parses the pastebin time of post. pastebin time is default CDT (Central Date Time)
		pastebinTime = dparser.parse(dateString)
		return pastebinTime
	else:
		return datetime(1993, 5, 21, 0, 0, 0, 0, None)


def openURL(aURL):
	#time.sleep(wait)
	opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(jar))
	htmltext = BeautifulSoup(opener.open(aURL))
	return htmltext

def addLinks(soup):
	maintable = soup.find("table", attrs = {"class" : "maintable"})
	if maintable:
		for a in maintable.findAll("a"):
			if "archive" not in a['href']:
		 		a['href'] = urlparse.urljoin("http://pastebin.com/", a['href'])
				urlArray.append(a['href'])
	'''
	for tag in soup.findAll("a", href = True):
		 	tag['href'] = urlparse.urljoin(url, tag['href'])
		 	tag['href'].encode("utf-8")
		 	#check to make sure crawler stays within page domain
		 	#also make sure crawler does not put an already visited page into the queue
		 	# if tag['href'].find(url_key) != -1 and not visited.has_key(tag['href'].encode("utf-8")):
		 	# 	urlArray.append(tag['href'].encode("utf-8"))
		 	# 	visited[tag['href'].encode("utf-8")] = "1"
		 	if tag['href'].find(url_key) != -1:
		 		urlArray.append(tag['href'].encode("utf-8"))
		 		#visited[tag['href'].encode("utf-8")] = "1"
	return urls	 
	'''


	

def stopScraping():
	global isStop
	global urlArray
	print "STOP STOP STOP !!!"
	print len(urlArray)
	#urlArray = []
	isStop = True


def startTimer():
	global start_time
	start_time = time.time()

def getTime():
	return time.time() - start_time
