from django.conf.urls import patterns, url
from scraper import views

urlpatterns = patterns('',
	url(r'^$', views.home, name='home'),
	url(r'^results/$', views.results, name = 'results'),
	url(r'^stop/$', views.stop, name = 'stop'),
	url(r'^watchlist/$', views.watchlist, name='watchlist'),
	# url(r'^list/$', views.list, name='list'),
)