import pytest
from rest_framework.reverse import reverse
from django.db.models import Q
from django.contrib.auth.models import User
from todo.models import ToDo


@pytest.mark.django_db
def test_delete_detail_todo_not_authenticated(api_client, user):
    response = api_client.delete(reverse("todo-detail", args=[98]))
    assert response.status_code == 401
    assert response.data["detail"] == "Authentication credentials were not provided."


@pytest.mark.django_db
def test_delete_detail_todo_authenticated(api_client, user):
    api_client.force_login(user)
    response = api_client.delete(reverse("todo-detail", args=[98]))

    assert response.status_code == 204
    assert ToDo.objects.filter(pk=98).count() == 0


@pytest.mark.django_db
def test_delete_detail_todo_authenticated_not_owner(api_client, user):
    api_client.force_login(user)
    response = api_client.delete(reverse("todo-detail", args=[44]))

    assert response.status_code == 403
    assert ToDo.objects.filter(pk=3).count() == 1


@pytest.mark.django_db
def test_delete_detail_todo_authenticated_private(api_client, user):
    api_client.force_login(user)
    response = api_client.delete(reverse("todo-detail", args=[8]))

    assert response.status_code == 404
    assert ToDo.objects.filter(pk=4).count() == 1
