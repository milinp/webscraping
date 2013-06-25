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
	start_time = time.time()
	initiate()
	while len(urls) > 0:
		# if len(visited) > 1000:
		# 	break
		try:
			soup = openURL(url[0])
		except Exception as ex:
			print "Exception in user code: " + str(ex)
			print "URL: " + urls[0]
		urls.pop(0)
		addLinks(soup)
		print "Number of visited pages: " + str(len(urls))
	print "Length of storage: " + str(len(storage))
	print time.time() - start_time, "seconds"

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


if __name__ == "__main__":
	main()

	#this is an edit