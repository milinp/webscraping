# Create your views here.
from upload.models import Document
from upload.forms import DocumentForm
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from django.shortcuts import render, get_object_or_404, render_to_response
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import logout_then_login

location = ""

@login_required
def home(request):
	global location
	if 'import' in request.POST:
		# form = DocumentForm(request.POST, request.FILES)
		# if form.is_valid():
		newdoc = Document(docfile = request.FILES['upload'])
		newdoc.save()
		location = newdoc.path()
		# Redirect to the document list after POST
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
