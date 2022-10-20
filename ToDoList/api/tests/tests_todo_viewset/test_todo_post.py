import pytest
from rest_framework.reverse import reverse
from django.db.models import Q
from django.contrib.auth.models import User
from todo.models import ToDo


@pytest.mark.django_db
def test_post_list_todo_not_authenticated(api_client, user):
    data = {
        "title": "test",
        "description": "test_des",
    }
    response = api_client.post(reverse("todo-list"), data=data)
    assert response.status_code == 401
    assert response.data["detail"] == "Authentication credentials were not provided."


@pytest.mark.django_db
def test_post_list_todo_authenticated(api_client, user):
    data = {
        "title": "test_title",
        "description": "test_des",
    }
    api_client.force_login(user)
    response = api_client.post(reverse("todo-list"), data=data)
    todo = ToDo.objects.get(title="test_title")
    assert response.status_code == 201
    assert response.data["title"] == "test_title"
    assert todo.title == "test_title"
    assert todo.created_by == user
    assert todo.public == False


@pytest.mark.django_db
def test_post_action_comment_todo_not_authenticated_public(api_client, user):
    data = {"text": "test_text"}
    response = api_client.post(reverse("todo-comment", args=[98]))
    assert response.status_code == 401
    assert response.data["detail"] == "Authentication credentials were not provided."


@pytest.mark.django_db
def test_post_action_comment_todo_authenticated_public(api_client, user):
    data = {"text": "test_text"}
    api_client.force_login(user)
    response = api_client.post(reverse("todo-comment", args=[98]), data=data)
    assert response.status_code == 200


@pytest.mark.django_db
def test_post_action_comment_todo_authenticated_private_not_owner(api_client, user):
    data = {"text": "test_text"}
    api_client.force_login(user)
    response = api_client.post(reverse("todo-comment", args=[8]), data=data)
    assert response.status_code == 404


@pytest.mark.django_db
def test_post_action_comment_todo_authenticated_public_not_owner(api_client, user):
    data = {"text": "test_text"}
    api_client.force_login(user)
    response = api_client.post(reverse("todo-comment", args=[44]), data=data)
    assert response.status_code == 200


@pytest.mark.django_db
def test_post_action_comment_todo_bad_request(api_client, user):
    data = {"text_bad": "test_text"}
    api_client.force_login(user)
    response = api_client.post(reverse("todo-comment", args=[98]), data=data)
    assert response.status_code == 400
