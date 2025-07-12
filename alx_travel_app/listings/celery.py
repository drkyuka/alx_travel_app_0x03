"""
Celery configuration for the listings app.
This module sets up Celery to work with Django, allowing for asynchronous task processing.
It includes the necessary imports and configuration settings to integrate Celery with Django's settings.
"""

from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from django.conf import settings

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "alx_travel_app.settings")

app = Celery("listings")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.conf.broker_connection_retry_on_startup = True
app.autodiscover_tasks()
