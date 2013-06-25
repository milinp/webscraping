import threading
import time
import urllib2
import urlparse
import sys
import traceback
import pdb
import unicodedata
import cookielib
from bs4 import BeautifulSoup

url = sys.argv[1]
url_key = urlparse.urlsplit(url).netloc
jar = cookielib.FileCookieJar("cookies")

urls = [url]
visited = [url]
storage = []
delay = 1

threads = []


class myThread (threading.Thread):
    def __init__(self, threadID, name, counter):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter
    def run(self):
        print "Starting " + self.name
        #print_time(self.name, self.counter, 5)
        spawnThreadForScrapping(urls[0])
       # print "Exiting " + self.name





def print_time():
   count = 0
   while count < 5:
      time.sleep(delay)
      count += 1
      print "%s" % ( time.ctime(time.time()) )
      
def main():
	if len(sys.argv) != 2:
		print "Input must be two arguments\nExiting..."
		sys.exit()
	elif sys.argv[1].find("://") == -1:
		print "Input should be include scheme/protocol!\nExiting..."
		sys.exit()
	soup = openURL(url[0])
        addLinks(soup)
        for tag in soup.findAll("textarea", attrs = {"id" : "paste_code"}):
                storage.append(tag.text.strip(" ").encode("ascii","ignore"))
                                       
	print storage
	print "Length of storage: " + str(len(storage))
          
	nb_threads = len(urls)
        i = 0;
        while len(urls) > 0:
          i = i + 1
          threadName = "Thread number %d" % (i)
          thread = myThread(1, threadName, 1)
          thread.start()
          urls.pop(0)
          threads.append(thread)    
        for t in threads:
          t.join()
  #print "Exiting Main Thread"
        
def  spawnThreadForScrapping(url):
        soup = openURL(url)
        for tag in soup.findAll("textarea", attrs = {"id" : "paste_code"}):
                storage.append(tag.text.strip(" ").encode("ascii","ignore"))
                print "Number of visited pages: " + str(len(visited))
                addLinks(soup)
                if len(visited) > 500:
                        break
        return
                
##        while len(urls) > 0:
##                soup = openURL(url[0])
##                for tag in soup.findAll("textarea", attrs = {"id" : "paste_code"}):
##                        storage.append(tag.text.strip(" ").encode("ascii","ignore"))
##                urls.pop(0)
##                print "Number of visited pages: " + str(len(visited))
##                addLinks(soup)
##                if len(visited) > 500:
##                        break


def openURL(url):
	try:
		opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(jar))
		htmltext = BeautifulSoup(opener.open(urls[0]))
	except Exception as ex:
		print "Exception in user code: " + str(ex)
		print "URL: " + urls[0]
		#traceback.print_exc(file=sys.stdout) #prints entire trace
	return htmltext

def addLinks(soup):
	for tag in soup.findAll("a", href = True):
		 	tag['href'] = urlparse.urljoin(url, tag['href'])
		 	tag['href'].encode("utf-8")
		 	#print tag['href'].encode("utf-8")
		 	if tag['href'].find(url_key) != -1 and tag['href'] not in visited:
		 		urls.append(tag['href'].encode("utf-8"))
		 		visited.append(tag['href'].encode("utf-8"))

def whatisthis(s):
    if isinstance(s, str):
        print "ordinary string"
    elif isinstance(s, unicode):
        print "unicode string"
    else:
        print "not a string"

if __name__ == "__main__":
	main()
