import factory
from django.contrib.auth.models import User
from factory.django import DjangoModelFactory
from django.contrib.auth.hashers import make_password

from user.models import Profile, Gender


class UserFactory(DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Sequence(lambda n: f"test{n}")
    email = factory.Sequence(lambda n: f"test{n}@testing.com")
    password = factory.Faker("password")


class GenderFactory(DjangoModelFactory):
    class Meta:
        model = Gender

    gender_name = factory.Faker("name")


class ProfileFactory(DjangoModelFactory):
    class Meta:
        model = Profile

    name = factory.Faker("name")
    user = factory.SubFactory(UserFactory)
    gender = factory.SubFactory(GenderFactory)
    profile_pic = factory.django.ImageField(color="blue", width=400, height=400)
    delete_number = factory.Faker("pyint", min_value=1000, max_value=9999)
