<h2>How to start admin(scraper) side or client-facing side:</h2>
So after you've forked the repo, cd into the directory of either the admin/client django project folder
<p><code>cd /directory/of/djangoproject</code></p>
The manage.py file acts as a wrapper around the django-admin.py file. The manage.py file can be utilized to host your application locally by running this command on the terminal:
<p><code>python manage.py runserver</code></p>
or for short if you have the permissions:
<p><code>./manage.py runserver</code></p>
runserver by default runs on port 8000, so you can specify the IP and port by giving it another argument. For example:
<p>runs application on port 127.0.0.1:1337:</p> <p><code>./manage.py runserver 1337</code></p>
<p>runs application on all IPs your machine can support instead of only the loopback interface:</p> <p><code>./manage.py runserver 0.0.0.0:8888</code></p>
For more information on managepy / django-admin.py the django website provides excellent documentation. https://docs.djangoproject.com/en/1.5/ref/django-admin/
<p>Once your development server is running, access the IP through the browser.</p>

<h2>Admin Interface</h2>
![Alt text](/assets/admin.png "Optional title")
![Alt text](/assets/admin-2.png "Optional title")

<h2>Client Interface</h2>
![Alt text](/assets/client.png "Optional title")
![Alt text](/assets/client-2.png "Optional title")
