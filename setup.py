"""setup for django-numerics."""

import logging
import sys

from setuptools import find_packages
from setuptools import setup

logging.basicConfig()

VERSION = '0.1.2'
DESCRIPTION = 'numerics dashboard endpoint provider for django.'


def runtests():
    """Run django tests."""
    import django
    from django.conf import settings
    settings.configure(
        DATABASES={
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': ':memory:',
            },
        },
        INSTALLED_APPS=(
            'django.contrib.contenttypes',
            'django.contrib.auth',
            'djangonumerics',
        ),
        MIDDLEWARE_CLASSES=(
            'django.contrib.sessions.middleware.SessionMiddleware',
            'django.contrib.auth.middleware.AuthenticationMiddleware',
            'django.contrib.messages.middleware.MessageMiddleware',
        ),
        ROOT_URLCONF='djangonumerics.urls',
    )

    if hasattr(django, 'setup'):
        # django >= 1.7
        django.setup()
    # This need to be imported after the settings has been configured
    try:
        from django.test.runner import DiscoverRunner
    except ImportError:
        # Django < 1.8
        from django.test.simple import DjangoTestSuiteRunner as DiscoverRunner

    test_runner = DiscoverRunner(verbosity=1, interactive=False)
    failures = test_runner.run_tests([])
    sys.exit(failures)


setup(
    name='django-numerics',
    version=VERSION,
    description=DESCRIPTION,
    url='https://github.com/huseyinyilmaz/django-numerics',
    author='Huseyin Yilmaz',
    author_email='yilmazhuseyin@gmail.com',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    test_suite='setup.runtests',
    tests_require=[
        'Django>=1.6.0',
        'cryptography>=0.8.0'
    ],
)
