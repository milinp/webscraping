import urllib2
import urlparse
import cookielib
import time
import threading
import re
import os
import pytz
import dateutil.parser as dparser 
from bs4 import BeautifulSoup
from bs4 import SoupStrainer
from datetime import datetime
from pytz import timezone
from django.utils.timezone import utc
from django.core.management.base import BaseCommand
from django.core.management.base import CommandError
from django.core.management.base import make_option
from scraper.models import DummyVisited, PastieEntries

url = ""
wait = 0
url_key = ""
jar = cookielib.FileCookieJar("cookies")
isStop = False
urlArray = []
start_time = 0

class Command(BaseCommand):
	def handle(self, *args, **options):
		startTimer()
		if(args[0] == 'stop'):
			stopScraping()
		else:
			scraper(args)

class myThread (threading.Thread):
    def __init__(self, threadID, name, counter, urlForScrape, url_key):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter
        self.urlForScrape = urlForScrape
        self.url_key = url_key
    def run(self):
    	if self.url_key == "pastebin.com":
        	startScraperPastebin(self.urlForScrape)
        if self.url_key == "pastie.org":
        	startScraperPastie(self.urlForScrape)

def scraper(args):
	global urlArray
	global url
	global isStop
	global url_key
	isStop = False
	i = 0
	url = args[0]
	url_key = urlparse.urlsplit(url).netloc
	wait = float(args[1])
	try:
		urlArray = []		
		soup = openURL(url)
		if url_key == "pastie.org":
			addLinksPastie(soup)
			#getHistoricalDataPastie(soup)
			for i in range(0,8):
			 	soup = openURL(getPastieNextPage(soup))
			 	addLinksPastie(soup)
		if url_key == "pastebin.com":
			addLinksPastebin(soup)
		print "\n\n\n---------------------------------------Restarting----------------------------------------------------------------------------\n\n"
		print "Length of urlArray = %d\n\n\n" % (len(urlArray))
		file1 = open("urlArray.txt", "w");
		for url1 in urlArray:
  			file1.write("%s\n" % url1)	
		for urlForScrape in urlArray:
			status = getStatus()
			#print getTime()
			if status or getTime() > float(args[2]) - 2:
				#print("We killed it")
				print ""
			else: 
				i = i + 1
				threadName = "Thread number %d" % (i)
				thread = myThread(1, threadName, i, urlForScrape, url_key)
				time.sleep(wait)
				thread.start()
				thread.join()
				#urlArray.pop(0)
	except Exception as ex:
		print "Exception in user code: " + str(ex)

# invoked a thread to begin scraping a Pastebin page for information (specifically its date and contents)
# stores into database
def startScraperPastebin(urlForScrape):
	start_time = time.time()
	urlSoup = ""
	if not DummyVisited.objects.filter(url = urlForScrape).exists():
		print "new entry = %s\n\n" % (urlForScrape)
		urlSoup = openURL(urlForScrape)
		parsedText = scrapePastebin(urlSoup)
		modifiedTime = scrapeDatePastebin(urlSoup)
		DummyVisited(url = urlForScrape, urlData = parsedText, modifiedTime = modifiedTime).save()
	else:
		print "Repeated entry = %s\n" % (urlForScrape)

# invoked a thread to begin scraping a Pastie page for information (specifically its date and contents)
# stores into database
def startScraperPastie(urlForScrape):
	start_time = time.time()
	urlSoup = ""
	if not PastieEntries.objects.filter(url = urlForScrape).exists():
		print "new entry = %s\n\n" % (urlForScrape)
		urlSoup = openURL(urlForScrape)
		parsedText = scrapePastie(urlSoup)
		modifiedTime = scrapeDatePastie(urlSoup)
		if parsedText:
			PastieEntries(url = urlForScrape, urlData = parsedText, modifiedTime = modifiedTime).save()
	else:
		print "Repeated entry  = %s\n" % (urlForScrape)

# syntaxy stuff to open the url with Cookies enabled
# takes in url (ex: http://bananaman.com)
# returns a BeautifulSoup object
def openURL(url):
	#time.sleep(wait)
	opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(jar))
	htmltext = BeautifulSoup(opener.open(url))
	return htmltext

# extract payload from Pastie site
# returns a string
def scrapePastie(soup):
	textBody = ""
	if soup.find("pre", attrs={"class" : "textmate-source"}):
		s = soup.find("pre", attrs={"class" : "textmate-source"})
		for f in s.findAll(text= True):
			textBody += f.encode("ascii", "ignore")
		return textBody

# extract payload from Pastebin site
# returns string
def scrapePastebin(soup):
	textBody = ""
	# check to see if div exists. It should because it's specific to pastebin.
	s = soup.find("textarea", attrs = {"id" : "paste_code"})
	textBody = s.text.encode("ascii", "ignore")
	return textBody

# extracts date of pastie post
# returns a datetime object (timezone = US/Eastern)
def scrapeDatePastie(soup):
	s = soup.findAll(title = True)
	if s:
		for time in s:
			dateString = time['title']
		pastieTime = dparser.parse(dateString,ignoretz= True)
		tz = pytz.timezone('GMT')	
		pastieTZ = tz.localize(pastieTime)
		pastieEST = pastieTZ.astimezone(pytz.timezone('US/Eastern'))
		pastieEST.strftime("%Y-%m-%d %H:%M:%S")
		return pastieEST
	else:
		return datetime(1993, 5, 21, 0, 0, 0, 0, None)

# extracts date of pastebin post
# returns a datetime object (timezone = US/Eastern)
def scrapeDatePastebin(soup):
	# check to see if div exists. It should because it's specific to pastebin.
	if soup.findAll("div", attrs = {"class" : "paste_box_info"}):
		# filter out the title attribute which holds the date
		for s in soup.findAll("span", title = True, style = True, text = True):
			dateString = s['title']
		# parses the pastebin time of post. pastebin time is default CDT (Central Date Time)
		pastebinTime = dparser.parse(dateString)
		tz = pytz.timezone('CST6CDT')
		pastebinTZ = tz.localize(pastebinTime)
		pastebinEST = pastebinTZ.astimezone(pytz.timezone('US/Eastern'))
		pastebinEST.strftime("%Y-%m-%d %H:%M:%S")
		return pastebinEST
	else:
		return datetime(1993, 5, 21, 0, 0, 0, 0, None)

# extracts all links on the archive/browse page of Pastie and stores into urlArray
def addLinksPastie(soup):
	s = soup.findAll("div", attrs={"class" : "pastePreview"})
	for section in s:
		linkTag = section.find("a")
		link = linkTag['href']
		urlArray.append(link)

# extracts all links on the archive/browse page of Pastebin and stores into urlArray
def addLinksPastebin(soup):
	maintable = soup.find("table", attrs = {"class" : "maintable"})
	if maintable:
		for a in maintable.findAll("a"):
			if "archive" not in a['href']:
		 		a['href'] = urlparse.urljoin("http://pastebin.com/", a['href'])
				urlArray.append(a['href'])

# extracts link to next page of Pastie archive (ex: http://pastie.org/pastes/y/2013/8/page/2)
# returns string
def getPastieNextPage(soup):
	if soup.find(text = "Next page").parent['href']:
		tag = soup.find(text = "Next page").parent['href']
		nextPage = urlparse.urljoin("http://pastie.org/", tag)
		return nextPage

# extracts all the historical data
def getHistoricalDataPastie(soup):
	if soup.findAll("div", attrs={"class" : "months"}):
		monthsURLSoup = soup.findAll("div", attrs={"class" : "months"})
		for eachMonth in monthsURLSoup:
			linkTag = eachMonth.find("a")
			print linkTag['href']
			link = urlparse.urljoin("http://pastie.org/", linkTag['href'])
			url1Array = getPastieNextPageRecursively(link)

def getPastieNextPageRecursively(nextURL):
	nextURLSoup = openURL(nextURL)
	if nextURLSoup.find(text = "Next page"):
		tag = nextURLSoup.find(text = "Next page").parent['href']
		nextPage = urlparse.urljoin("http://pastie.org/", tag)
		print "\n~~~~~~~~~ printing next Page ~~~~~~~~~~\n"
		print nextPage
		urlArray.append(nextURL)
		return getPastieNextPageRecursively(nextPage)
	else:
		return urlArray


# sets flags to stop scraping function
# invoked when Stop is pressed from Admin User Interface
def stopScraping():
	global isStop
	global urlArray
	print len(urlArray)
	#urlArray = []
	isStop = True

def startTimer():
	global start_time
	start_time = time.time()

def getTime():
	return time.time() - start_time

# check flag used for stopping
def getStatus()	:
	return isStop
