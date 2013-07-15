import os, re
import upload
from django.db import models

# Create your models here.
class Document(models.Model):
	docfile = models.FileField(upload_to='Watchlists')
	def __unicode__(self):
		return self.docfile.name
	def path(self):
		m = re.search('<Document: (.*?)>', str(self.path))
		return os.path.dirname(os.path.abspath(upload.__file__))+ "/media/" + str(m.group(1))