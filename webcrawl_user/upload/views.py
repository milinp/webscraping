# Create your views here.
from upload.models import Document
from upload.forms import DocumentForm
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from django.shortcuts import render, get_object_or_404, render_to_response
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import logout_then_login
from boto.s3.connection import S3Connection
from boto.s3.key import Key
import boto
import re
location = ""

@login_required
def home(request):
	global location
	if 'import' in request.POST:
		newdoc = Document(docfile = request.FILES['upload'])
		newdoc.save()
		location = newdoc.path()
		# Redirect to the document list after POST
		print "hiiiiiii"
		

		# creating S3 bucket connection
		conn = boto.connect_s3('AKIAJDT4XSQEYXW5WE2Q', 'dHXOjTTxe9e9RrRna2nzvAa+qO5pd1FR0cDpWN39')
		bucket = conn.create_bucket('client1.bucket')
		k = Key(bucket)

		filename = str(request.FILES['upload'])
		filenameKey = re.sub('\.txt$', '', filename)

		print filenameKey
		
		
		k.key = filenameKey 
		#k.set_contents_from_filename('pastebin1.png')	
		k.set_contents_from_filename(location)
		#print k.get_contents_to_filename("newFile.txt")
		return HttpResponseRedirect(reverse('upload.views.home'))
	else:
		form = DocumentForm() # An empty, unbound form

	# Load documents for the list page
	documents = Document.objects.all()

	# Redner list page with the documents and the form
	return render_to_response(
		'upload/parallax.html',
		{'documents': documents, 'form' : form},
		context_instance = RequestContext(request)
	)

def logout(request):
	return logout_then_login(request)

def parallax(request):
	return render(request, 'upload/parallax.html')
