import urllib2
import urlparse
import sys
import traceback
import pdb
import unicodedata
import cookielib
import time
from bs4 import BeautifulSoup

url = sys.argv[1]
url_key = urlparse.urlsplit(url).netloc
jar = cookielib.FileCookieJar("cookies")

urls = [url]
visited = {url : "1"}
storage = []

def main():
	
	initiate()
	try:
		soup = openURL(url[0])
		startScrapper(soup);
	except Exception as ex:
		print "Exception in user code: " + str(ex)
		print "URL: " + urls[0]

	#storage = scrape(soup)

	#print storage
	#print time.time() - start_time, "seconds"

def startScrapper(soup):
	start_time = time.time()	
	urlArray = addLinks(soup) 
	print "printing the URL Array \n"
	print urlArray
	i = 0
	print "length of URL array - %d" % (len(urlArray))
	while i < len(urlArray):
		urlSoup = openURL(urlArray[i])
		#storage = scrape(soup)
		print '\n\n'
		#print storage
		i = i + 1
		print i
	

	print time.time() - start_time, "seconds"

def scrape(soup):
	if soup.findAll(text = True):
		holder = []
		for s in soup.findAll(text = True):
			if "".join(s.encode('utf-8').split()):
				holder.append("".join(s.encode("ascii", "ignore").split()))
		return "".join(holder)

def initiate():
	if len(sys.argv) != 2:
		print "Input must be two arguments\nExiting..."
		sys.exit()
	elif sys.argv[1].find("://") == -1:
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

if __name__ == "__main__":
	main()

	#this is an edit