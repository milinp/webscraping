# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, render_to_response


def upload_file(request):
	if request.method == 'POST':
		form = UploadFileForm(request.POST, request.FILES)
		if form.is_valid():
			handle_uploaded_file(request.FILES['file'])
			return HttpResponse("Banana")
	else:
		form = UploadFileForm()
		return render_to_response('index.html', {'form' : form})

def scraper(request):
	return render(request, 'scraper/index.html')
