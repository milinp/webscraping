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
from scraper.models import Visited, URLToVisit, DummyVisited, IndexedTable, WatchListDB, ModifiedWatchListDB, PastebinEntries


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

def main(args):
  print "\t\t\t scheduling matching patterns start  \n\n\n"
  #s3.get_bucket('media.yourdomain.com').get_key('examples/first_file.csv')
    #conn = S3Connection 
  conn = boto.connect_s3('AKIAIJZ56E33VC2GBG3Q', 'xfSWxuK9uGAsRwtwdJgIPBhiye0Z3ka5oRqRa8FD')
  bucket = conn.get_bucket('client1.bucket')
  for key in bucket.list():
    filename = key.name.encode('utf-8')
    print "File name is : "
    print filename
    key.get_contents_to_filename((dirname(__file__) +'\\'+ filename))
    watchListFile =  dirname(__file__) +'\\'+filename
    print "Printing watchlist"
    scanDatabaseForMatchList(watchListFile,filename)  

def sendMail(filePath, fileName,matchingword,latestUrl,latestUrlData):
  msg = MIMEMultipart()
  msg['Subject'] = 'Dow Jones Cyber Security Risk Notification'
  msg['From'] = 'astroprasad@gmail.com'
  addresses = ['pranav16@gmail.com','pranavkumar.patel@dowjones.com','astroprasad@gmail.com']

  # what a recipient sees if they don't use an email reader
  msg.preamble = 'Multipart message.\n'
  part = MIMEText('**** Notification of keyword match ****\n\n This email serves as notification of possible security breach or potential targeting for a future incident.' 
    'The named data dump site is commonly used to share stolen data or information related to security breaches. Data related to your organization has been detected on this site.\n\n\n'
     'KEYWORD: %s' % matchingword + '\n\nData Dump URL:  %s' % latestUrl + '\n\nContent\n %s' % latestUrlData + '\n\n')
  msg.attach(part)
  part = MIMEApplication(open(filePath, 'rb').read())
  part.add_header('Content-Disposition', 'attachment', filename=fileName)
  msg.attach(part)
   
  # connect to SES
  try:
    connection =  boto.ses.connect_to_region('us-east-1',aws_access_key_id='AKIAIJZ56E33VC2GBG3Q', aws_secret_access_key='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')
   
  # and send the message
    result = connection.send_raw_email(msg.as_string()
    , source=msg['From']
    , destinations=addresses)
    print result
  except Exception as ex:
    print "Exception in user code: " + str(ex)

def takeScreenShots(url, urlname):  
  s = Screenshot()
  s.capture(url, urlname)

def checkWatchListDB(aWatchWord):
  if not ModifiedWatchListDB.objects.filter(matchedWord = aWatchWord).exists():
    return "00:00:00"
  else:
    dummydata = ModifiedWatchListDB.objects.get(matchedWord = aWatchWord)  
    return dummydata.modifiedTime.strftime('%Y-%m-%d %H:%M:%S')
 
def insertIntoWatchList(aWatchWord):
  modifiedTime = datetime.datetime.utcnow().replace(tzinfo = utc)
  if ModifiedWatchListDB.objects.filter(matchedWord = aWatchWord).exists():
    dummydata = ModifiedWatchListDB.objects.get(matchedWord = aWatchWord)
    dummydata.modifiedTime = modifiedTime
    dummydata.save()
  else:
    ModifiedWatchListDB(matchedWord = aWatchWord, modifiedTime = modifiedTime).save()


def scanDatabaseForMatchList(watchListFile, aFileName):
  print "inside Scan database"
  listOfFiles = []
  with open(watchListFile) as f:
      watchlist = f.readlines()
  db = MySQLdb.connect(host="interns-web.cwlx8eld8gjz.us-east-1.rds.amazonaws.com",user="interns",passwd="Dowjones1",db="url_info" )
  cursor = db.cursor()
  fileSize = 0
  filePathName = ''
  i = 0
  f = open(os.path.dirname(os.path.abspath(scraper.__file__)) + '\media\Matches\%s_%d' % (aFileName, i) +'.txt', 'w')
  for match in watchlist:
    try:
      time = str(checkWatchListDB(match))
      newModifiedTime = datetime.datetime.utcnow().replace(tzinfo = utc).strftime('%Y-%m-%d %H:%M:%S')
      matchingword = match.rstrip()
      #sql = "SELECT * FROM scraper_dummyvisited WHERE urlData LIKE '%%%s%%';"  % (matchingword)
      sql = "SELECT * FROM scraper_dummyvisited WHERE urlData LIKE '%%%s%%' AND modifiedTime Between '%s' AND '%s';"  % (matchingword, time, newModifiedTime  )
      #sql = "SELECT * from scraper_dummyvisited where urlData LIKE '%%%s%%' order by modifiedTime desc LIMIT 1;" % (matchingword)
      print sql
      keyword = matchingword
      cursor.execute(sql)
      
      results = cursor.fetchall()
      for row in results:
        fileName = "%s_%d.txt" %(aFileName, i)
        filePathName =  os.path.dirname(os.path.abspath(scraper.__file__)) + '\media\Matches\%s_%d' % (aFileName, i) +'.txt' 
        urlname = '%s-%d.png' % (matchingword , i)
        matches=re.findall(r'\'(.+?)\'',str(row))
        # print "this is the url  %s" % matches[0]
        #takeScreenShots(matches[0], urlname)
        directoryName = os.path.dirname(os.path.abspath(scraper.__file__)) + '\media\Matches\%s' % (aFileName) +'.txt'
        tempFileSize = os.path.getsize(filePathName)  
        fileSize = float(tempFileSize)
        if fileSize < 20000000:
          f = open(filePathName, 'a')
          f.write("\n\n\n-------------------------------------------------------------------------------------------------------\n\n")
          f.write("KEYWORD: " + matchingword + "\n\n\n") 
          f.write("Data Dump URL:  " + str(row[0]) + "\n\n\n")
          f.write("Content:  \n\n")
          f.write(str(row[1]) + "\n\n")
          f.write("-------------------------------------------------------------------------------------------------------\n")
          f.close()
          notificationWatchword = matchingword
          insertIntoWatchList(match)
        else:
          listOfFiles.add(fileName);
          i = i + 1
        latestUrl = results[-1][0]
        latestUrlData = results[-1][1]
      print "Printing the list of files \n\n\n\n"
      print listOfFiles;
    except Exception as ex:
      print "Exception in user code: " + str(ex)
  if not filePathName == '':
    sendMail(filePathName,fileName,notificationWatchword,latestUrl,latestUrlData)
  f.close()
  db.close()