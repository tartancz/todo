import factory
from datetime import datetime
from dateutil.relativedelta import relativedelta
from factory.django import DjangoModelFactory
from todo.models import ToDo, Comment
from user.tests.factories import UserFactory


class ToDoFactory(DjangoModelFactory):
    class Meta:
        model = ToDo

    title = factory.sequence(lambda a: f"title_test_{a}")
    description = factory.sequence(lambda a: f"description_test_{a}")
    created_by = factory.SubFactory(UserFactory)
    public = factory.Faker("pyint", min_value=0, max_value=1)
    dead_line = datetime.now() + relativedelta(years=1)


class CommentFactory(DjangoModelFactory):
    class Meta:
        model = Comment

    text = factory.sequence(lambda a: f"title_text_{a}")
    created_by = factory.SubFactory(UserFactory)
    created_in = factory.SubFactory(ToDoFactory)
