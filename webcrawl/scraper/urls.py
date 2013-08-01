from django.conf.urls import patterns, url
from scraper import views

urlpatterns = patterns('',
	url(r'^$', views.home, name='home'),
	url(r'^watchlist/$', views.watchlist, name='watchlist'),
)