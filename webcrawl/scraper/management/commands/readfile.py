#!/usr/bin/python
import os
import MySQLdb
import sys
import scraper
from django.core.management.base import BaseCommand, CommandError
from django.core.management.base import make_option

class Command(BaseCommand):
  def handle(self, *args, **options):
    main(args)


def main(args):
  with open(args[0]) as f:
      watchlist = f.readlines()
      #print watchlist
      print "\n\n\nChecking with the database......"

  db = MySQLdb.connect(host="interns-web.cwlx8eld8gjz.us-east-1.rds.amazonaws.com",user="interns",passwd="Dowjones1",db="url_info" )

  cursor = db.cursor()

  for match in watchlist:

    matchingword = match.rstrip()
    sql = "SELECT url FROM scraper_dummyvisited WHERE urlData LIKE '%%%s%%'"  % (matchingword)
    #print sql
    keyword = match
    cursor.execute(sql)
    results = cursor.fetchall()
    for row in results:
      f = open(os.path.dirname(os.path.abspath(scraper.__file__)) + '\media\Matches\%s' % (matchingword) +'.txt', 'a')
      f.write(str(row) + "\n")

  f.close()
  db.close()