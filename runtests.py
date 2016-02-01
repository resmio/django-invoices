#!/usr/bin/env python
import sys
import os

import django
from django.conf import settings


if not settings.configured:
    # Choose database for settings
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': ':memory:'
        }
    }

    test_db = os.environ.get('DB', 'sqlite')

    if test_db == 'mysql':
        DATABASES['default'].update({
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'invoices',
            'USER': 'root',
        })
    elif test_db == 'postgres':
        DATABASES['default'].update({
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'USER': 'postgres',
            'NAME': 'invoices',
            'OPTIONS': {
                'autocommit': True,
            }
        })

    settings.configure(
        DATABASES=DATABASES,
        INSTALLED_APPS=(
            'django.contrib.contenttypes',
            'django.contrib.auth',
            'invoices',
        ),
        SITE_ID=1,
        SECRET_KEY='this-is-just-for-tests-so-not-that-secret',
        ROOT_URLCONF='invoices.urls',
        MIDDLEWARE_CLASSES=('django.middleware.csrf.CsrfViewMiddleware', )
    )


from django.test.utils import get_runner  # noqa


def run_tests():
    if hasattr(django, 'setup'):
        django.setup()
    apps = sys.argv[1:] or ['invoices', ]
    test_runner = get_runner(settings)
    test_runner = test_runner(verbosity=1, interactive=True, failfast=False)
    failures = test_runner.run_tests(apps)
    sys.exit(failures)


if __name__ == '__main__':
    run_tests()
