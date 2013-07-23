import os
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, render_to_response
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.core.management import call_command # used to call script
from apscheduler.scheduler import Scheduler # used to schedule
import time, logging # used to schedule

from scraper.models import Document
from scraper.forms import DocumentForm

sched = Scheduler(standalone = True)
location = ""

def home(request):
	if 'run_scraper' in request.POST:
		logging.basicConfig()
		global sched
		sched = Scheduler(standalone = True)
		args = ['http://pastebin.com/archive', '1', '180']
		call_command('masterScrape', *args)	
	
		def scrape_sched():
			call_command('masterScrape', *args)
		sched.add_interval_job(scrape_sched, seconds = 180, max_instances = 1000)
		sched.start()
		return render(request, 'scraper/scraper.html')


	if 'stop_scraper' in request.POST:
		args = ['stop']
		call_command('masterScrape', *args)
		sched.shutdown(wait = False)

		return render(request, 'scraper/scraper.html')

	return render(request, 'scraper/scraper.html')

def results(request):
	if 'run_scraper' in request.POST:
		logging.basicConfig()
		global sched
		sched = Scheduler(standalone = True)
		args = ['http://pastebin.com/archive', '1', '180']
		call_command('masterScrape', *args)	
	
		def scrape_sched():
			call_command('masterScrape', *args)
		sched.add_interval_job(scrape_sched, seconds = 180, max_instances = 1000)
		sched.start()
		return render(request, 'scraper/index.html')


	if 'stop_scraper' in request.POST:
		args = ['stop']
		call_command('masterScrape', *args)
		sched.shutdown(wait = False)

		return render(request, 'scraper/index.html')

def stop(request):
	if 'stop_scraper' in request.POST:
		args = ['stop']
		call_command('masterScrape', *args)
		sched.shutdown(wait = False)

		return render(request, 'scraper/index.html')

def watchlist(request):
#Handle file upload
	global location
	if 'import' in request.POST:
		form = DocumentForm(request.POST, request.FILES)
		if form.is_valid():
			newdoc = Document(docfile = request.FILES['docfile'])
			newdoc.save()
			location = newdoc.path()
			# Redirect to the document list after POST
			return HttpResponseRedirect(reverse('scraper.views.watchlist'))
	else:
		form = DocumentForm() # An empty, unbound form

	if 'match' in request.POST:
		call_command('readfile', location)

		sched = Scheduler(standalone = True)
		def match_sched():
			call_command('readfile', location)
		sched.add_interval_job(match_sched, seconds = 20, max_instances = 1000)
		sched.start()
		

	# Load documents for the list page
	documents = Document.objects.all()

	# Redner list page with the documents and the form
	return render_to_response(
		'scraper/watchlist.html',
		{'documents': documents, 'form' : form},
		context_instance = RequestContext(request)
	)
# def list(request):
# 	#Handle file upload
# 	if request.method == "POST":
# 		form = DocumentForm(request.POST, request.FILES)
# 		if form.is_valid():
# 			newdoc = Document(docfile = request.FILES['docfile'])
# 			newdoc.save()

# 			# Redirect to the document list after POST
# 			return HttpResponseRedirect(reverse('scraper.vigews.watchlist'))
# 	else:
# 		form = DocumentForm() # An empty, unbound form

# 	# Load documents for the list page
# 	documents = Document.objects.all()

# 	# Redner list page with the documents and the form
# 	return render_to_response(
# 		'scraper/watchlist.html',
# 		{'documents': documents, 'form' : form},
# 		context_instance = RequestContext(request)
# 	)