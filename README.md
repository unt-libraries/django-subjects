Django Subjects
===============

[![Build Status](https://travis-ci.com/unt-libraries/django-subjects.svg?branch=master)](https://travis-ci.com/unt-libraries/django-subjects)


About
-----

This Django web application allows for the creation and maintenance of a catalog of subjects.


Requirements
------------

* Python 2.7, 3.5 - 3.7
* Django 1.11


Installation
------------

To install this app into your own Django project,

1.  Install the app from the git repository:

        $ pip install git+https://github.com/unt-libraries/django-subjects.git

2.  Add to your INSTALLED_APPS in your Django project's settings:

        INSTALLED_APPS = [
            ...
            subjects
        ]

3.  Include subjects' URLs in your project's urls.py file:

        urlpatterns = [
            ...
            url(r'^admin/', admin.site.urls),
            url(r'^subjects/', include('subjects.urls')),
            url(r'^accounts/login/$', auth.views.login,
                {'template_name': 'subjects/login.html'}, name="login"),
            url(r'^accounts/logout/$', auth.views.logout,
                {'template_name': 'subjects/logout.html'}, name="logout"),
        ]

4.  Apply the migrations (from wherever your project's manage.py file is):

        $ manage.py migrate


Developing
----------

If you'd like to work on the code or take this app for a test run without setting up a separate Django project,
you can do so by following these instructions, which will run the app with the Django test server.

1.  Clone the git repository:

        $ git clone https://github.com/unt-libraries/django-subjects.git

2.  Navigate into the cloned repository:

        $ cd django-subjects

3.  Install the requirements (preferably in a virtual environment):

        $ pip install -r requirements.txt

4.  Navigate to the root of the project directory and run the migrations:

        $ ./manage.py migrate

5.  Create a superuser so you can log into the admin interface and add/remove/modify subjects:

        $ ./manage.py createsuperuser

    Follow the instructions to create the superuser with whatever username, email, and password you wish.

6.  Start the test server:

        $ ./manage.py runserver

    The test server can be viewed from a browser by navigating to the default location: `http://localhost:8000/subjects`

To stop the test server, hit Ctrl-C. You can always start it up again with the command in Step 4.


Testing
-------

To manually run the tests with your current version of Python (system or virtual environment):

1.  Follow steps 1-3 of Developing

2.  Run the tests:

        $ pytest

Alternatively, you can use tox to run the tests in specific environments, along with the flake8 style checker:

1.  Follow steps 1-2 of Developing

2.  Install tox on your system:

        $ sudo apt-get install tox

3.  Run the tox test suite:

        $ tox


License
-------

See LICENSE.txt.


Contributors
------------

* Brandon Fredericks
* [Mark Phillips](https://github.com/vphill)
* [Joey Liechty](https://github.com/yeahdef)
* [Lauren Ko](https://github.com/ldko)
* [Gio Gottardi](https://github.com/somexpert)
