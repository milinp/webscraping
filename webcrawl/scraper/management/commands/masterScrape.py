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
from bs4 import BeautifulSoup
from datetime import datetime
import pytz
from pytz import timezone
from django.core.management.base import BaseCommand, CommandError
from django.core.management.base import make_option
from scraper.models import ScrapeCheck

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
        #print "/n %s /n"  % (self.name)
        startScrapper(self.urlForScrape)

def main(args):
	global isStop
	isStop = False
	global urlArray
	global url
	# URLToVisit.objects.all().delete()
	# unfinishedURLData = URLToVisit.objects.all()
	# if unfinishedURLData:
	# 	for unfinishedURL in unfinishedURLData:
	# 		urls.append(unfinishedURL.url)
	# 		URLToVisit.objects.all().delete()
	url = args[0]
	urls.append(url)
	global url_key
	url_key = urlparse.urlsplit(urls[0]).netloc
	wait = float(args[1])
	try:
		soup = openURL(urls[0])
		urlArray.extend(addLinks(soup))
		i = 0
		#print "length of URL array - %d" % (len(urlArray))
		for urlForScrape in urlArray:
			print ("\n\n\tinside the for loop \n\n\n")
			status = getStatus()
			#print status
			print getTime()
			if status or getTime() > float(args[2]) - 2:
				print("We killed it")
				#sys.exit(0)
				#break
				
				#threads.append(thread)
			#	print ("\n\n length of threads = %d" % (len(threads)))
			else: 
				i = i + 1
				threadName = "Thread number %d" % (i)
				print ("Thread name = %s" % (threadName))
				thread = myThread(1, threadName, i, urlForScrape)
				time.sleep(wait)
				thread.start()
				thread.join()
				urlArray.pop(0)
	except Exception as ex:
		print "Exception in user code: " + str(ex)
		print "URL: " + urls[0]  
   	# for t in threads:
   	# 	t.join()

	#storage = scrape(soup)

	#print storage
	#print time.time() - start_time, "seconds"
def getStatus()	:
	return isStop

def startScrapper(urlForScrape):
	#print "URL for Scraping = %s \n\n" % (urlForScrape)
	start_time = time.time()
	urlSoup = ""
	if not ScrapeCheck.objects.filter(url = urlForScrape).exists():
		print "new entry = %s\n\n" % (urlForScrape)
		urlSoup = openURL(urlForScrape)

		addLinks(urlSoup)
		parsedText = scrape(urlSoup)
		publishTime = scrape_date(urlSoup)
		ScrapeCheck(url = urlForScrape, urlData = parsedText, urlPublishedTime = str(publishTime)).save()
		
	else:
		print "Repeated entry  = %s" % (urlForScrape)

# returns content of pastebin page as a string
def scrape(soup):
	textBody = ""
	# check to see if div exists. It should because it's specific to pastebin.
	if soup.findAll("textarea", attrs = {"id" : "paste_code"}):
		for s in soup.find("textarea", attrs = {"id" : "paste_code"}):
			textBody = s
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

		fmt = "%A %dth of %B %Y %I:%M:%S %p CDT" # specific format of the title attribute string

		# grabs the pastebin time of post. pastebin time is default CDT (Central Date Time)
		pastebinTime = datetime.strptime(dateString, fmt)
		pastebinHour = datetime.strptime(dateString, fmt).hour

		# this get's the difference between the CDT and our timezone
		# should account for daylight savings time
		CDTHour = datetime.now(timezone("CST6CDT")).hour
		difference = datetime.now().hour - CDTHour

		#return the adjusted time to enable a uniform storing of time
		TMZAdjusted = pastebinTime.replace(hour = pastebinHour+difference)
		return TMZAdjusted
	else:
		return datetime(1993, 5, 21, 0, 0, 0)


def openURL(aURL):
	#time.sleep(wait)
	opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(jar))
	htmltext = BeautifulSoup(opener.open(aURL))
	return htmltext

def addLinks(soup):
	#time.sleep(wait)
	for tag in soup.findAll("a", href = True):
		 	tag['href'] = urlparse.urljoin(url, tag['href'])
		 	tag['href'].encode("utf-8")
		 	#check to make sure crawler stays within page domain
		 	#also make sure crawler does not put an already visited page into the queue
		 	if tag['href'].find(url_key) != -1 and not visited.has_key(tag['href'].encode("utf-8")):
		 		urlArray.append(tag['href'].encode("utf-8"))
		 		visited[tag['href'].encode("utf-8")] = "1"
	return urls	 

def stopScraping():
	global isStop
	global urlArray
	print "STOP STOP STOP !!!"
	print len(urlArray)
	#urlArray = []
	isStop = True
	# for remainingUrl in urlArray:
	# 	if not ScrapeCheck.objects.filter(url = remainingUrl).exists():
	# 		URLToVisit(url = remainingUrl).save()
	# 

def startTimer():
	global start_time
	start_time = time.time()

def getTime():
	return time.time() - start_time
