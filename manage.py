#!/usr/bin/env python
import os
import sys

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "anole.settings")
    
    if 'devserver' in sys.argv or 'runserver' in sys.argv:
        os.environ.setdefault("ENVIRONMENT", "development")
        
    elif 'prodserver' in sys.argv or 'runuwsgi' in sys.argv:
        os.environ.setdefault("UWSGI_MODULE", "anole.wsgi")
        os.environ.setdefault("ENVIRONMENT", "production")
        
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)
