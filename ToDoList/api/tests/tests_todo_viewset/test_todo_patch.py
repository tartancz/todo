import pytest
from rest_framework.reverse import reverse
from django.db.models import Q
from django.contrib.auth.models import User
from todo.models import ToDo


@pytest.mark.django_db
def test_patch_action_done_profile_not_authenricated_private(api_client, user):
    response = api_client.patch(reverse("todo-done", args=[39]))
    assert response.status_code == 404


@pytest.mark.django_db
def test_patch_action_done_profile_not_owner_private(api_client, user):
    api_client.force_login(user)
    response = api_client.patch(reverse("todo-done", args=[39]))
    assert response.status_code == 404


@pytest.mark.django_db
def test_patch_action_done_profile_owner(api_client, user):
    api_client.force_login(user)
    response = api_client.patch(reverse("todo-done", args=[5]))
    assert ToDo.objects.get(pk=5).completed == True
    assert response.status_code == 200


@pytest.mark.django_db
def test_patch_action_done_profile_not_owner_public(api_client, user):
    api_client.force_login(user)
    response = api_client.patch(reverse("todo-done", args=[15]))
    assert response.status_code == 403
