from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model


class Command(BaseCommand):
    def handle(self, *args, **options):
        user = get_user_model()
        if not user.objects.filter(email='admin@example.com').exists():
            user.objects.create_superuser(
                email='admin@example.com',
                password='adminpass'
            )
            self.stdout.write(self.style.SUCCESS(
                'Successfully created new superuser'
            ))
        else:
            self.stdout.write(self.style.WARNING(
                'Superuser already exists'
            ))
