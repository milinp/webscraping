from django.conf.urls import patterns, url
from scraper import views

urlpatterns = patterns('',
	url(r'^$', views.scraper, name='scraper'),

	)