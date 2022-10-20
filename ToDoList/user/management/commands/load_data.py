from django.conf import settings
from django.core import management
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = "Helpful command to load all fixtures"

    def handle(self, *args, **options):
        management.call_command("loaddata", "user/management/data.json")
