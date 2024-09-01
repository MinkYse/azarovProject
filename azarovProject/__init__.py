# your_project_name/__init__.py

from __future__ import absolute_import, unicode_literals

# Это для того, чтобы Celery запускался при старте Django
from .celery import app as celery_app

__all__ = ('celery_app',)
