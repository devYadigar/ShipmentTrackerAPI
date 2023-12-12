"""
Command to wait for the database to be available.
"""
import time

from MySQLdb import OperationalError as MySQLError
from django.db.utils import OperationalError
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    def handle(self, *args, **options):
        self.stdout.write('Waiting for database...')

        while True:
            try:
                self.check(databases=['default'])
                break
            except(MySQLError, OperationalError):
                self.stdout.write('Database unavailable, waiting 1 second...')
                time.sleep(1)

        self.stdout.write(self.style.SUCCESS('Database available!'))
