from __future__ import absolute_import, unicode_literals
import os
import sys

import celery
import psycopg2
from psycopg2 import extensions
from urllib.parse import urlparse
from django import db
from django.core.management import call_command

DUMP_FILE_PATH = "backup/dbdump.json"


def are_tables_empty() -> bool:
    with db.connection.cursor() as cursor:
        cursor.execute("SELECT count(*) FROM geolocation_geolocation;")
        geolocation_count = cursor.fetchone()[0]
        cursor.execute("SELECT count(*) FROM auth_user;")
        users_count = cursor.fetchone()[0]
        return not bool(geolocation_count + users_count)


class BackupTask(celery.Task):
    def __init__(self):
        self.name = "backup_task"

    def run(self):
        try:
            if not are_tables_empty():
                self.do_backup()
                return "Database backup created."
        except db.OperationalError:
            return "Database is temporary unavailable."

    @staticmethod
    def do_backup(dump_file_path=DUMP_FILE_PATH):
        with open(dump_file_path, "w") as f:
            sys.stdout = f
            call_command("dumpdata", exclude=["contenttypes", ])


class LoadDumpTask(celery.Task):
    def __init__(self):
        self.name = "load_dump_task"

    def run(self):
        try:
            if are_tables_empty() and os.path.isfile(DUMP_FILE_PATH):
                call_command("loaddata", DUMP_FILE_PATH)
        except (db.ProgrammingError, db.OperationalError):
            self.create_database("geodb")
            if os.path.isfile(DUMP_FILE_PATH):
                self.load_dump()
            return "Dump has been loaded."

    @staticmethod
    def load_dump():
        call_command("flush", interactive=False)
        call_command("migrate")
        call_command("loaddata", DUMP_FILE_PATH)

    @staticmethod
    def create_database(db_name):
        autocommit = extensions.ISOLATION_LEVEL_AUTOCOMMIT
        connection = None
        try:
            if os.getenv("DATABASE_URL"):
                database_url = os.getenv("DATABASE_URL")
                result = urlparse(database_url)
                username = result.username
                password = result.password
                hostname = result.hostname
                port = result.port
            else:
                username = os.getenv("POSTGRES_USER")
                password = os.getenv("POSTGRES_PASSWORD")
                hostname = os.getenv("POSTGRES_HOST")
                port = os.getenv("POSTGRES_PORT")
            connection = psycopg2.connect(
                user=username, password=password, host=hostname, port=port
            )
            connection.set_isolation_level(autocommit)
            with connection.cursor() as cursor:
                cursor.execute(f"CREATE DATABASE {db_name};")
        finally:
            if connection:
                connection.close()
