#!/usr/bin/env python
"""
Django's command-line utility for administrative tasks.

This script is used to execute management commands for the CRM project.
You can pass commands like 'runserver', 'migrate', or 'createsuperuser'.
For more details, see: https://docs.djangoproject.com/en/stable/ref/django-admin/
"""

import os
import sys
import logging

logger = logging.getLogger(__name__)


def main():
    """Run administrative tasks."""
    # Set the default settings module
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'CRM.settings')

    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        logger.critical("Failed to import Django. Ensure it is installed and available.")
        raise ImportError(
            "Couldn't import Django. Ensure it's installed and "
            "available on your PYTHONPATH environment variable. Did you "
            "forget to activate a virtual environment?"
        ) from exc

    try:
        # Execute the management command
        execute_from_command_line(sys.argv)
    except Exception as e:
        logger.error(f"An error occurred while executing a management command: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
