.. django-numerics documentation master file, created by
   sphinx-quickstart on Sun Apr 19 14:51:06 2015.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to django-numerics's documentation!
===========================================

Give your app a mobile dashboard.

django-numerics is a numerics dashboard endpoint provider for django.

Note
----

This project is still under development give a month or so to get stable.

Install django-numerics
-----------------------
django-numerics can be installed using pip.

.. code-block:: bash

   $ pip install django-numerics

Or source code can be downloaded from github.


Integration
-----------
To use django-numerics in a project first add it to INSTALLED_APPS in your django settings file.

.. code-block:: python

   INSTALLED_APPS = (
       'django.contrib.admin',
       'django.contrib.auth',
       ...
       # add djangonumerics to installed apps
       'djangonumerics',
   )

Go to main urls file and add django-numerics endpoints to url patterns

.. code-block:: python

   urlpatterns = patterns(
       '',
       url(r'', include(core.urls)),
       url(r'^admin/', include(admin.site.urls)),
       url(r'^accounts/', include(accounts.urls)),
       ## add django-numerics to urls.py
       url(r'^numerics/', include(djangonumerics.urls)),
   )

Than you can register some endpoints for your dashboard. For instance following code adds number of current users as an endpoint.

.. code-block:: python

    from djangonumerics import NumberResponse
    def total_users(user):
        """Return total number of users."""
        user_count = User.objects.filter(is_active=True).count()
        return NumberResponse(user_count, 'Total number of users')

    # register endpoint to django-numerics
    register('total-users', total_users, NumberResponse)

In this case, registered endpoint does not have user specific info. User specific info could be provided by using user argument of endpoint function.

After endpoint registration, open http://localhost:8000/numerics to see list of endpoints for current user. If there is no logged in user you will get a 404. This behivour can be changed by providing a new permission function to register function.


Run tests
---------
 To run tests, first make sure that django is installed on current environment. Than run following command

 .. code-block:: bash

   $ python setup.py test

Build documentation
-------------------

.. code-block:: bash

   $ pip install -r doc_requirements.txt
   $ python setup.py build_sphinx
