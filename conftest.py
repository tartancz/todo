from distutils.dir_util import copy_tree

import pytest
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User as User
from django.core import management
from pytest_factoryboy import register

from todo.tests.factories import ToDoFactory, CommentFactory
from user.tests.factories import (
    ProfileFactory,
    GenderFactory,
    UserFactory,
)

register(ToDoFactory)
register(CommentFactory)
register(ProfileFactory)
register(GenderFactory)
register(UserFactory)


@pytest.fixture
def api_client():
    from rest_framework.test import APIClient

    return APIClient()


@pytest.fixture
def api_request_factory():
    from rest_framework.test import APIRequestFactory

    return APIRequestFactory()


@pytest.fixture(autouse=True)
def set_media_to_testing(settings, tmp_path):
    path_to_temp_media = tmp_path / "media"
    path_to_temp_media.mkdir()
    copy_tree(str(settings.BASE_DIR / "fixtures" / "media"), str(path_to_temp_media))
    settings.MEDIA_ROOT = path_to_temp_media
    settings.MEDIA_URL = "/media/"


@pytest.fixture
def load_big_fixtures():
    management.call_command("loaddata", "fixtures/big_fixtures/genders")
    management.call_command("loaddata", "fixtures/big_fixtures/users")
    management.call_command("loaddata", "fixtures/big_fixtures/profiles")
    management.call_command("loaddata", "fixtures/big_fixtures/todos")
    management.call_command("loaddata", "fixtures/big_fixtures/comments")
    management.call_command("loaddata", "fixtures/big_fixtures/tokens")


@pytest.fixture
def load_fixtures():
    management.call_command("loaddata", "fixtures/genders")
    management.call_command("loaddata", "fixtures/users")
    management.call_command("loaddata", "fixtures/profiles")
    management.call_command("loaddata", "fixtures/todos")
    management.call_command("loaddata", "fixtures/comments")
    management.call_command("loaddata", "fixtures/tokens")


@pytest.fixture
def user(load_fixtures) -> User:
    UserModel = get_user_model()
    return UserModel.objects.get(id=1)


@pytest.fixture
def user2(load_fixtures) -> User:
    UserModel = get_user_model()
    return UserModel.objects.get(id=2)
