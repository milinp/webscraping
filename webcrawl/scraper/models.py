import os, re 
import scraper
from django.db import models
from django.db.models.base import ModelBase
# Create your models here.

class Visited(models.Model):
	url = models.CharField(primary_key = True, max_length = 255)
	urlData = models.TextField()
	urlInfo = models.TextField()
	modifiedTime = models.DateTimeField(auto_now = True)
	def __unicode__(self):
		return "URL: %s" % self.url

class URLToVisit(models.Model):
	url = models.CharField(primary_key = True, max_length = 255)
	def __unicode__(self):
		return "URL: %s" % self.url

class DummyVisited(models.Model):
	url = models.CharField(primary_key = True, max_length = 255)
	urlData = models.TextField()
	urlInfo = models.TextField()
	modifiedTime = models.DateTimeField(auto_now = False)
	def __unicode__(self):
		return "URL: %s" % self.url

class Document(models.Model):
	docfile = models.FileField(upload_to='Watchlists')
	def __unicode__(self):
		return self.docfile.name
	# Used to get the path of specific watchlist to pass on to the readfile.py matching process
	def path(self):
		m = re.search('<Document: (.*?)>', str(self.path))
		return os.path.dirname(os.path.abspath(scraper.__file__)) + "/media/" + str(m.group(1)) # MEDIA_ROOT + watchlist/name


class IndexedTable(models.Model):
	url = models.CharField(primary_key = True, max_length = 255)
	urlData = models.TextField()
	urlInfo = models.TextField()
	modifiedTime = models.DateTimeField(auto_now = True)
	def __unicode__(self):
		return "URL: %s" % self.url

class ModifiedWatchListDB(models.Model):
	matchedWord = models.TextField()
	modifiedTime = models.DateTimeField()

		
#creates model for table scraper_pastiedatabase

class PastieEntries(models.Model):
	url = models.CharField(primary_key = True, max_length = 255)
	urlData = models.TextField()
	modifiedTime = models.DateTimeField(auto_now = False)
	def __unicode__(self):
		return "URL: %s" % self.url


class PastieWatchListDB(models.Model):
	matchedWord = models.TextField()
	modifiedTime = models.DateTimeField()		

