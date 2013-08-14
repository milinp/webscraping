<h2>Setting Up</h2>
<p>So after you've forked the repo it's time to make sure you have the proper environment before you can run our application.</p>
<p>The version of python used in the project is 2.7.5</p>
<p>Make sure you have pip installed: https://pypi.python.org/pypi/pip</p>
<p>Or if you live on the edge, you can easy_install it:</p>
<p><code>easy_install pip</code></p> 
<p>However, it is not recommended that you install pip using easy_install due to pip not using SSL for downloading packages from PyPI, and thus leaving users more vulnerable to security threats. </p>
<p>So now that you have pip, you can easily download all the required modules using our requirements.txt:</p>
<p><code>pip install -r requirements.txt</code></p>
<p>Note: you might want to set up a virtual environment, using <a href="http://www.virtualenv.org/en/latest/">virtualenv</a></p> 

<h2>How to start admin(scraper) side or client-facing side:</h2>
<p>So after everything is set up, cd into the directory of either the admin/client django project folder</p>
<p><code>cd /directory/of/djangoproject</code></p>
<p>The manage.py file acts as a wrapper around the django-admin.py file. The manage.py file can be utilized to host your application locally by running this command on the terminal:</p>
<p><code>python manage.py runserver</code></p>
<p>or for short if you have the permissions:</p>
<p><code>./manage.py runserver</code></p>
<p>runserver by default runs on port 8000, so you can specify the IP and port by giving it another argument. For example:</p>
<p>runs application on port 127.0.0.1:1337:</p> <p><code>./manage.py runserver 1337</code></p>
<p>runs application on all IPs your machine can support instead of only the loopback interface:</p> <p><code>./manage.py runserver 0.0.0.0:8888</code></p>
<p>For more information on managepy / django-admin.py the django website provides excellent documentation. https://docs.djangoproject.com/en/1.5/ref/django-admin/</p>
<p>Once your development server is running, access the IP through the browser.</p>

<h2>Admin Interface</h2>
![Alt text](/assets/admin.png "Optional title")
![Alt text](/assets/admin-2.png "Optional title")

<h2>Client Interface</h2>
![Alt text](/assets/client.png "Optional title")
![Alt text](/assets/client-2.png "Optional title")
