from django.db import models
from django.db.models.base import ModelBase
# Create your models here.

class Visited(models.Model):
	url = models.CharField(primary_key = True, max_length = 255)
	urlData = models.TextField()
	modifiedTime = models.DateTimeField(auto_now = True)
	def __unicode__(self):
		return "URL: %s" % self.url

class URLToVisit(models.Model):
	url = models.CharField(primary_key = True, max_length = 255)
	def __unicode__(self):
		return "URL: %s" % self.url