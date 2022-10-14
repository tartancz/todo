from django.conf import settings
from django.core import management
from django.core.management.base import BaseCommand, CommandError

import faker
from datetime import datetime
from todo.models import ToDo, Comment
from todo.tests.factories import ToDoFactory, CommentFactory
from user.models import Profile, User, Gender
from user.tests.factories import UserFactory, ProfileFactory, GenderFactory
from rest_framework.authtoken.models import Token
import random


class Command(BaseCommand):
    help = "Helpful command to load all fixtures"

    def handle(self, *args, **options):
        if not settings.DEBUG:
            raise CommandError("Command not meant for production")

        f = faker.Faker()
        #
        for x in range(10):
            GenderFactory()

        genders = Gender.objects.all()
        for x in range(50):
            ProfileFactory(
                gender=genders.order_by("?").first(),
                profile_pic="profile_pics/default_profile.jpg",
            )

        users = User.objects.all()
        for x in users:
            Token.objects.create(user=x)

        for x in range(100):
            ToDoFactory(
                created_by=users.order_by("?").first(),
                dead_line=f.date_time_between(
                    datetime(2010, 1, 1), datetime(2030, 1, 1)
                ),
                completed=random.randint(0, 1),
            )

        todos = ToDo.objects.all()
        for x in todos:
            x.created_on = f.date_time_between(datetime(2000, 1, 1), x.dead_line)
            x.save()
        #
        todos = ToDo.objects.all()
        users = User.objects.all()
        for x in range(1000):
            todo = todos.order_by("?").first()
            user = users.order_by("?").first()
            CommentFactory(
                created_by=user,
                created_on=f.date_between_dates(todo.created_on, datetime(2040, 1, 1)),
                created_in=todo,
            )
