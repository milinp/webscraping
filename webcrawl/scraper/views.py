# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, render_to_response
from django.core.management import call_command

def scraper(request):
	return render(request, 'scraper/index.html')

def results(request):
	call_command('scrape2')

