#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
from onlineCAL.config import email_username, email_password


def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'onlineCAL.settings')
    try:
        assert ' ' not in (email_username, email_password)
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    except AssertionError as err:
        raise Exception(
            "Email username and password empty! " +
            "See onlineCAL/config.py for more info"
        ) from err
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
