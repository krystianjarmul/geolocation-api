from __future__ import absolute_import, unicode_literals
import os

from celery import Celery

from .tasks import BackupTask, LoadDumpTask

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")

app = Celery("core")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.tasks.register(BackupTask())
app.tasks.register(LoadDumpTask())
