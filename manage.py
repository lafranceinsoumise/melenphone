#!/usr/bin/env python
import os
import sys

true_values = ['true', 't', 'yes', 'y']

if __name__ == "__main__":

    debug = os.environ.get('DEBUG')
    no_envdir = os.environ.get('NO_ENVDIR')

    # we load envdir only in debug mode and if no_envdir is not set to true
    load_envdir = (
        (debug is None or debug.lower() in true_values)
        and (no_envdir is None or no_envdir not in true_values)
    )

    if load_envdir:
        import envdir
        envdir.read()

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "melenchonPB.settings")
    try:
        from django.core.management import execute_from_command_line
    except ImportError:
        # The above import may fail for some other reason. Ensure that the
        # issue is really that Django is missing to avoid masking other
        # exceptions on Python 2.
        try:
            import django
        except ImportError:
            raise ImportError(
                "Couldn't import Django. Are you sure it's installed and "
                "available on your PYTHONPATH environment variable? Did you "
                "forget to activate a virtual environment?"
            )
        raise
    execute_from_command_line(sys.argv)
