import os

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User


class Command(BaseCommand):
    help = "Create admin user"

    def handle(self, *args, **kwargs):
        username = os.environ.get("ADMIN_USERNAME")
        password = os.environ.get("ADMIN_PASSWORD")

        if not username or not password:
            self.stdout.write(
                self.style.ERROR(
                    "ADMIN_USERNAME or ADMIN_PASSWORD is not configured."
                )
            )
            return

        if not User.objects.filter(username=username).exists():
            User.objects.create_superuser(
                username=username,
                password=password
            )
            self.stdout.write(
                self.style.SUCCESS("Admin created successfully")
            )
        else:
            self.stdout.write("Admin already exists")