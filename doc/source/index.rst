.. django-numerics documentation master file, created by
   sphinx-quickstart on Sun Apr 19 14:51:06 2015.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to django-numerics's documentation!
===========================================

Give your app a mobile dashboard.

django-numerics is a numerics dashboard endpoint provider for django.

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
    from djangonumerics import register
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

Usage
======

Registration
------------
In order to add a new widget to your numerics dashboard, first you need to register an endpoint on your application. registration of an endpoint is a very simple process. just call djangonumerics.api.register with andpoint information. Here is signiture of register function.

.. code-block:: python

   def register(name, func, response_type, args=None, kwargs=None,
                cache_timeout=0, permission_func=grant_access):
       ...

Here is the explanation of all arguments.

1) **name**: name of the endpoint. This will be used as an identifier for you endpoint. Make sure that it is unique. If you try to register multiple endpoints with the same name latter ones will be ignored.
2) **func, args, kwargs**: Those should be your endpoint function and its arguments. Your endpoint function will be called as following.

.. code-block:: python

   endpoint_response = func(user, *args, **kwargs)

So normally your endpoint function will be a normal function that takes a django user as an argument and returns a response objects that is instance of one of widget responses from djangonumerics.responses. But you can provide extra arguments from args and kwargs variables.

3) **response_type**: This is a response type of endpoint function. Every endpoint will be formated for certain widget. So response type of the endpoints should stay same at all times. This value should be one of the response classes in djangonumerics.responses module. Chose the response type for widget that you will use this endpoint with.
4) **cache_timeout**: Normally endpoint function will be called for every request. But you can cache the endpoint response for any period of time. By default caching is disabled.
5) **permission_func**: This function is used to decide if a user has permission for that endpoint. it takes a user and an internal endpoint namedtuple as an argument and return a boolean value. permission_func will be explained more in permission section.

Here is some example registration calls.

.. code-block:: python

   # caching number of users value for 60 seconds.
   register('total-users', total_users, NumberResponse, cache_timeout=60)
   # caching the return value for a day
   register('employee-of-the-month', calculate_eom, LabelResponse,
            cache_timeout=1*24*60*60)
   # using same endpoint for different backends
   register('invalid-paypal-transactions', invalid_transactions_endpoints,
            NumberResponse, kwargs={'backends': ['paypal']},)
   register('invalid-payu-transactions', invalid_transactions_endpoints,
            NumberResponse, kwargs={'backends': ['payu']},)

Widgets widgets
---------------
For now two widgets are supported. Since I did not bought the rest of the custom json widgets, I did not wrote the wrappers for them. If you have them, feel free to contrubite.
