from django.db import models
<<<<<<< HEAD
from django.db.models.base import ModelBase
# Create your models here.

class Website(models.Model):
	url = models.CharField(max_length = 2100)
	urlData = models.TextField()
	modifiedTime = models.DateTimeField(auto_now = True)
	def __unicode__(self):
		return "URL: %s" % self.url
=======

# Create your models here.

class Website(models.Model):
	http = models.CharField(max_length = 200)
	bodytext = models.TextField()
	def __unicode__(self):
		return self.http

class Queries(models.Model):
	user_id=models.CharField(max_length=200)
	query=models.CharField(max_length=200)
>>>>>>> 2e4fa8b70daf6a01bceaa93166b81401a3f7daf1
