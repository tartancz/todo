from django.conf import settings
from django.core import management
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = "Helpful command to load all fixtures"

    def handle(self, *args, **options):
        if not settings.DEBUG:
            raise CommandError("Command not meant for production")

        management.call_command("loaddata", "fixtures/genders")
        management.call_command("loaddata", "fixtures/users")
        management.call_command("loaddata", "fixtures/profiles")
        management.call_command("loaddata", "fixtures/todos")
        management.call_command("loaddata", "fixtures/tokens")
        management.call_command("loaddata", "fixtures/comments")
