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
import dateutil.parser as dparser
from django.core.management.base import BaseCommand, CommandError
from django.core.management.base import make_option
from scraper.models import DummyVisited

jar = cookielib.FileCookieJar("cookies")

class Command(BaseCommand):
	def handle(self, *args, **options):
		main()

def main():
	print "before basket"
	basket = DummyVisited.objects.all()
	print "after basket"
	i = 0
	while 1 == 1:
		try:
			print i
			soup = openURL(basket[i].url)
			dateObject = scrape_date(soup)
			print dateObject
			urlToFetch = basket[i].url
			actualRow = DummyVisited.objects.get(url = urlToFetch)
			actualRow.modifiedTime = dateObject
			print actualRow.modifiedTime
			actualRow.save()
			print DummyVisited.objects.get(url= urlToFetch).modifiedTime
		except Exception as ex:
			print "Exception: " + str(ex)
		i = i + 1
		time.sleep(.5)
		
def openURL(aURL):
	opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(jar))
	htmltext = BeautifulSoup(opener.open(aURL))
	return htmltext

# returns date of pastebin post as a datetime object
def scrape_date(soup):
	# check to see if div exists. It should because it's specific to pastebin.
	if soup.findAll("div", attrs = {"class" : "paste_box_info"}):
		# filter out the title attribute which holds the date
		for s in soup.findAll("span", title = True, style = True, text = True):
			dateString = s['title']

		# parses the pastebin time of post. pastebin time is default CDT (Central Date Time)
		pastebinTime = dparser.parse(dateString)
		pastebinHour = dparser.parse(dateString).hour

		# this get's the difference between the CDT and our timezone
		# should account for daylight savings time
		CDTHour = datetime.now(timezone("utc")).hour - 5 # CDT = UTC - 5
		difference = datetime.now().hour - CDTHour

		# if pastebinHour+difference == 24:
		# 	fixedHour = 0
		# else:
		# 	fixedHour = pastebinHour+difference

		#return the adjusted time to enable a uniform storing of time
		# TMZAdjusted = pastebinTime.replace(hour = pastebinHour)
		return pastebinTime
	else:
		return datetime(1993, 5, 21, 0, 0, 0, 0, None)

# strftime('%Y-%m-%d %H:%M:%S %Z')