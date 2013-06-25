from django.db import models
from django.db.models.base import ModelBase
# Create your models here.

class Website(models.Model):
	url = models.CharField(max_length = 2100)
	urlData = models.TextField()
	modifiedTime = models.DateTimeField(auto_now = True)
	def __unicode__(self):
		return "URL: %s" % self.url