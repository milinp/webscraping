#!/usr/bin/python
import os
import MySQLdb
import sys
import scraper
from django.core.management.base import BaseCommand, CommandError
from django.core.management.base import make_option
#for multipart mailing
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from os.path import dirname, join
 
import boto.ses

#for screenshots
import re
import sys  
import time
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtWebKit import *
from boto.s3.connection import S3Connection
from boto.s3.key import Key
import boto
from django.utils.timezone import utc
import datetime
from scraper.models import Visited, URLToVisit, DummyVisited, IndexedTable, WatchListDB, ModifiedWatchListDB


class Command(BaseCommand):
  def handle(self, *args, **options):
    main(args)

class Screenshot(QWebView):
    def __init__(self):
        self.app = QApplication(sys.argv)
        QWebView.__init__(self)
        self._loaded = False
        self.loadFinished.connect(self._loadFinished)

    def capture(self, url, output_file):
        self.load(QUrl(url))
        self.wait_load()
        # set to webpage size
        frame = self.page().mainFrame()
        self.page().setViewportSize(frame.contentsSize())
        # render image
        image = QImage(self.page().viewportSize(), QImage.Format_ARGB32)
        painter = QPainter(image)
        frame.render(painter)
        painter.end()
        print 'saving', output_file
        image.save(output_file)

    def wait_load(self, delay=0):
        # process app events until page loaded
        while not self._loaded:
            self.app.processEvents()
            time.sleep(delay)
        self._loaded = False

    def _loadFinished(self, result):
        self._loaded = True


def sendMail(filePath, fileName):
  msg = MIMEMultipart()
  msg['Subject'] = 'Dow Jones Cyber Security Risk Notification'
  msg['From'] = 'astroprasad@gmail.com'
  msg['To'] = 'pranavkumar.patel@dowjones.com'
   
  # what a recipient sees if they don't use an email reader
  msg.preamble = 'Multipart message.\n'
   
  # the message body
  part = MIMEText('Please find the attachment that includes details of the data found on Pastebin.com')
  msg.attach(part)
  part = MIMEApplication(open(filePath, 'rb').read())
  part.add_header('Content-Disposition', 'attachment', filename=fileName)
  msg.attach(part)
   
  # connect to SES
  try:
    connection =  boto.ses.connect_to_region('us-east-1',aws_access_key_id='AKIAJDT4XSQEYXW5WE2Q', aws_secret_access_key='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')

   
  # and send the message
    result = connection.send_raw_email(msg.as_string()
    , source=msg['From']
    , destinations=[msg['To']])
    print result
  except Exception as ex:
    print "Exception in user code: " + str(ex)

def takeScreenShots(url, urlname):

  
  #urlname = matches[0] + '.png'
  s = Screenshot()
  s.capture(url, urlname)

  # s.capture('http://pastebin.com', 'pastebin1.png')
  # s.capture('http://pastebin.com/GGfXmcNa', 'pastebin2.png')
  # s.capture('http://pastebin .com/NSbZquFk', 'pastebin3.png')
  # s.capture('http://pastebin.com/4gpMEax3', 'pastebin4.png')
  # s.capture('http://pastebin.com/htiwBie8', 'pastebin5.png')
  # s.capture('http://pastebin.com/archive', 'pastebin6.png')

def checkWatchListDB(aWatchWord):
    # for remainingUrl in urlArray:
  if not ModifiedWatchListDB.objects.filter(matchedWord = aWatchWord).exists():
    return "00:00:00"
  else:
    dummydata = ModifiedWatchListDB.objects.get(matchedWord = aWatchWord)
    #print "checking database time"
    #print dummydata.modifiedTime.strftime('%Y-%m-%d %H:%M:%S')
    return dummydata.modifiedTime.strftime('%Y-%m-%d %H:%M:%S')

    '''
    datetime.datetime.now().strftime("%A, %d. %B %Y %I:%M%p")
'Saturday, 15. December 2012 11:19AM'
'''


#ef upDateWatchListDb(aWatchWord):
 


def insertIntoWatchList(aWatchWord):
  #print datetime.datetime.now()
  modifiedTime = datetime.datetime.utcnow().replace(tzinfo = utc)
  #print modifiedTime 
  if ModifiedWatchListDB.objects.filter(matchedWord = aWatchWord).exists():
    dummydata = ModifiedWatchListDB.objects.get(matchedWord = aWatchWord)
    #print dummydata
    dummydata.modifiedTime = modifiedTime
    dummydata.save()
    print "updating into the databse\n"
  else:
    print "inserting into the databse\n"
    ModifiedWatchListDB(matchedWord = aWatchWord, modifiedTime = modifiedTime).save()


def scanDatabaseForMatchList(watchListFile, aFileName):
  print "inside Scan database"
  listOfFiles = []
  
  print watchListFile
  with open(watchListFile) as f:
      watchlist = f.readlines()
      print "saasdasdaasfsdfsdfsfafasdfasdfasdfsdffasf \n\n"
      print watchlist
      print "\n\n\nChecking with the database......"

  db = MySQLdb.connect(host="interns-web.cwlx8eld8gjz.us-east-1.rds.amazonaws.com",user="interns",passwd="Dowjones1",db="url_info" )

  cursor = db.cursor()

  for match in watchlist:
    try:
      i = 0
      f = open(os.path.dirname(os.path.abspath(scraper.__file__)) + '\media\Matches\%s_%d' % (aFileName, i) +'.txt', 'w')
      f.close()
      time = str(checkWatchListDB(match))
      #print time
      #print datetime.datetime.now()
      newModifiedTime = datetime.datetime.utcnow().replace(tzinfo = utc).strftime('%Y-%m-%d %H:%M:%S')
      #print newModifiedTime 
      #Select * From scraper_dummyvisited where modifiedTime Between '2013-07-16' AND '2013-07-17';
      matchingword = match.rstrip()
      #sql = "SELECT * FROM scraper_dummyvisited WHERE urlData LIKE '%%%s%%';"  % (matchingword)
      sql = "SELECT * FROM scraper_dummyvisited WHERE urlData LIKE '%%%s%%' AND modifiedTime Between '%s' AND '%s';"  % (matchingword, time, newModifiedTime  )

      print sql
      keyword = matchingword
      cursor.execute(sql)
      
      results = cursor.fetchall()
      for row in results:
        print "\n\n\n"
        print row
        print "\n\n\n"

        print "inside for loop"
       
        fileName = "%s_%d.txt" %(aFileName, i)
        filePathName =  os.path.dirname(os.path.abspath(scraper.__file__)) + '\media\Matches\%s_%d' % (aFileName, i) +'.txt' 
        print filePathName
        urlname = '%s-%d.png' % (matchingword , i)
        #print row

        matches=re.findall(r'\'(.+?)\'',str(row))
       # print "this is the url  %s" % matches[0]
        #takeScreenShots(matches[0], urlname)
        directoryName = os.path.dirname(os.path.abspath(scraper.__file__)) + '\media\Matches\%s' % (aFileName) +'.txt'

        #print directoryName
              #print results
        tempFileSize = os.path.getsize(filePathName)  
        fileSize = float(tempFileSize)
        print "Size of the file"
        print fileSize 
        if fileSize < 20000000:
          f = open(filePathName, 'a')
          #print "inside the if condition"
          #print fileSize
          f.write("\n\n\n-------------------------------------------------------------------------------------------------------------------\n\n")
          f.write("KEYWORD: " + matchingword + "\n\n\n") 
          print ("Data Dump URL:  " + str(row[1]) + "\n\n\n")
          f.write("Data Dump URL:  " + str(row[0]) + "\n\n\n")
          f.write("Content:  \n\n")
          f.write(str(row[1]) + "\n\n")
          f.write("-------------------------------------------------------------------------------------------------------------------------\n")
          f.close()
        else:
          listOfFiles.add(fileName);
          i = i + 1
      #print results
      insertIntoWatchList(match)
        
        
        

      print "Printing the list of files \n\n\n\n"
      print listOfFiles;
      print fileName
      print filePathName
      sendMail(filePathName,fileName)    
    except Exception as ex:
      print "Exception in user code: " + str(ex)   
  f.close()
  db.close()



def main(args):

  print "\t\t\t scheduling matching patterns start  \n\n\n"
  #s3.get_bucket('media.yourdomain.com').get_key('examples/first_file.csv')
    #conn = S3Connection 
  conn = boto.connect_s3('AKIAJDT4XSQEYXW5WE2Q', 'dHXOjTTxe9e9RrRna2nzvAa+qO5pd1FR0cDpWN39')
  bucket = conn.get_bucket('client1.bucket')
  for key in bucket.list():
    filename = key.name.encode('utf-8')
    print "File name is : "
    print filename
    key.get_contents_to_filename((dirname(__file__) +'\\'+ filename))
    watchListFile =  dirname(__file__) +'\\'+filename
    print "Printing watchlist"
    #print watchListFile
    if filename == "Fortune500List":
        scanDatabaseForMatchList(watchListFile,filename)  
'''
  k = Key(bucket)
  k.key = 'Fortune500ListCompanies1'
#k.set_contents_from_filename('pastebin1.png')  
  k.get_contents_to_filename((dirname(__file__) + '\\Fortune500ListCompanies1.txt'))
  print dirname(__file__) + '\\Fortune500ListCompanies1.txt'
  watchListFile = dirname(__file__) + '\\Fortune500ListCompanies1.txt'
'''
