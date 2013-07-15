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
  msg['Subject'] = 'Data Dumped found'
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



def main(args):

  print "\t\t\t scheduling matching patterns start  \n\n\n"
  #s3.get_bucket('media.yourdomain.com').get_key('examples/first_file.csv')
    #conn = S3Connection 
  conn = boto.connect_s3('AKIAJDT4XSQEYXW5WE2Q', 'dHXOjTTxe9e9RrRna2nzvAa+qO5pd1FR0cDpWN39')
  bucket = conn.get_bucket('client1.bucket')
  k = Key(bucket)
  k.key = 'Fortune500ListCompanies1'
#k.set_contents_from_filename('pastebin1.png')  
  k.get_contents_to_filename((dirname(__file__) + '\\Fortune500ListCompanies1.txt'))
  print dirname(__file__) + '\\Fortune500ListCompanies1.txt'
  watchListFile = dirname(__file__) + '\\Fortune500ListCompanies1.txt'
  print "saasdasdaasfsdfsdfsfafasdfasdfasdfsdffasf \n\n"
  print watchListFile
  with open(watchListFile) as f:
      watchlist = f.readlines()
      #print watchlist
      print "\n\n\nChecking with the database......"

  db = MySQLdb.connect(host="interns-web.cwlx8eld8gjz.us-east-1.rds.amazonaws.com",user="interns",passwd="Dowjones1",db="url_info" )

  cursor = db.cursor()

  for match in watchlist:
    try:
      matchingword = match.rstrip()
      sql = "SELECT * FROM scraper_dummyvisited WHERE urlData LIKE '%%%s%%'"  % (matchingword)
      #print sql
      keyword = match
      cursor.execute(sql)
      i = 0
      results = cursor.fetchall()
      for row in results:
        i = i + 1
        urlname = '%s-%d.png' % (matchingword , i)
        #print row

        matches=re.findall(r'\'(.+?)\'',str(row))
       # print "this is the url  %s" % matches[0]
        #takeScreenShots(matches[0], urlname)
        directoryName = os.path.dirname(os.path.abspath(scraper.__file__)) + '\media\Matches\%s' % (matchingword) +'.txt'

        #print directoryName
        f = open(os.path.dirname(os.path.abspath(scraper.__file__)) + '\media\Matches\%s' % (matchingword) +'.txt', 'w')
        f.write(str(row) + "\n")
       
      if results: 
        fileName = matchingword + '.txt'
        filePathName =  os.path.dirname(os.path.abspath(scraper.__file__)) + '\media\Matches\%s' % (matchingword) +'.txt' 
        print "Size of the file\n\n"
        tempFileSize = os.path.getsize(filePathName)
        fileSize = float(tempFileSize)
        if fileSize < 20000:
          sendMail(filePathName,fileName)
    except Exception as ex:
      print "Exception in user code: " + str(ex)   
  f.close()
  db.close()