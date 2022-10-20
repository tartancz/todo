import pytest
from rest_framework.reverse import reverse
from django.db.models import Q
from django.contrib.auth.models import User
from todo.models import ToDo


# test_method_list/detail_ACTION_NAMEOFACTION_model_auth_extrainfo


@pytest.mark.django_db
def test_get_list_todo_not_authenticated(api_client, user):
    response = api_client.get(reverse("todo-list"))
    data = response.data
    assert response.status_code == 200
    assert data["count"] == ToDo.objects.filter(public=True).count()


@pytest.mark.django_db
def test_get_list_todo_authenticated(api_client, user2):
    api_client.force_login(user2)
    response = api_client.get(reverse("todo-list"))
    data = response.data
    assert response.status_code == 200
    assert (
        data["count"]
        == ToDo.objects.filter(Q(public=True) | Q(created_by=user2)).count()
    )


@pytest.mark.django_db
def test_get_detail_todo_not_authenticated(api_client, user):
    response = api_client.get(reverse("todo-detail", args=[98]))
    data = response.data
    todo = ToDo.objects.get(pk=98)
    assert response.status_code == 200
    assert data["title"] == todo.title
    assert data["comments"]["count"] == todo.comments_in.count()


@pytest.mark.django_db
def test_get_detail_todo_authenticated(api_client, user):
    api_client.force_login(user)
    response = api_client.get(reverse("todo-detail", args=[98]))
    data = response.data
    todo = ToDo.objects.get(pk=98)
    assert response.status_code == 200
    assert data["title"] == todo.title
    assert data["comments"]["count"] == todo.comments_in.count()


@pytest.mark.django_db
def test_get_detail_todo_authenticated_not_owner_private(api_client, user):
    api_client.force_login(user)
    response = api_client.get(reverse("todo-detail", args=[8]))
    assert response.status_code == 404
