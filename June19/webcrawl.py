import urllib2
import urlparse
import sys
import traceback
import pdb
import unicodedata
import cookielib
import sqlite3 as lite
import sys

from bs4 import BeautifulSoup

def whatisthis(s):
    if isinstance(s, str):
        print "ordinary string"
    elif isinstance(s, unicode):
        print "unicode string"
    else:
        print "not a string"

'''
This is for the command line args
'''

def setUpDatabaseConnection( databaseName ):

    try:
        con = lite.connect(databaseName)

        cur = con.cursor()  

        cur.executescript("""
            DROP TABLE IF EXISTS URLs;
            CREATE TABLE Urls(URL TEXT, DATA TEXT);""")
        con.commit()
    except lite.Error, e:
        
        if con:
            con.rollback()
            
        print "Error %s:" % e.args[0]
        sys.exit(1)






def InsertURLsIntoDatabase( url ):

    #print url

    con = lite.connect('URL.db')

    with con:    
        
        cur = con.cursor()   
        cur.execute("INSERT INTO Urls VALUES ('%s', '%s')" % (url, 'Data'))
       
        cur.execute("SELECT * FROM Urls")

        rows = cur.fetchall()

        for row in rows:
            print row

        
setUpDatabaseConnection('URL.db');
# if len(sys.argv) != 2:
# 	print "Input must be two arguments\nExiting..."
# 	sys.exit()
# elif sys.argv[1].find("http://") == -1:
# 	sys.argv[1] = "http://" + sys.argv[1]

url = "http://yahoo.com"
url_key = urlparse.urlsplit(url).netloc
jar = cookielib.FileCookieJar("cookies")
urls = [url]
visited = [url]
storage = []

while len(urls) > 0:
        try:
                opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(jar))
                htmltext = BeautifulSoup(opener.open(urls[0]))
        except Exception as ex:
                print "Exception in user code: " + str(ex)
               # print "URL: " + urls[0]
                #traceback.print_exc(file=sys.stdout) #prints entire trace

        urls.pop(0)
        
        #print "Number of visited pages: " + str(len(visited))        
        for tag in htmltext.findAll("a", href = True):
                tag['href'] = urlparse.urljoin(url, tag['href'])
                url = tag['href'].encode("utf-8")
               # print url + '\n'
                if tag['href'].find(url_key) != -1 and tag['href'] not in visited:
                        InsertURLsIntoDatabase(url);
                        urls.append(tag['href'].encode("utf-8"))
                        visited.append(tag['href'].encode("utf-8"))



#print visited
