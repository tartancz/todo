import pytest
from rest_framework.reverse import reverse
from django.db.models import Q
from django.contrib.auth.models import User
from todo.models import ToDo



@pytest.mark.django_db
def test_get_list_todo_not_authenticated(api_client, user):
    response = api_client.get(reverse("todo-list"))
    data = response.data

    assert response.status_code == 200
    assert data['count'] == ToDo.objects.filter(public=True).count()


@pytest.mark.django_db
def test_get_list_todo_authenticated(api_client, user2):
    api_client.force_login(user2)
    response = api_client.get(reverse("todo-list"))
    data = response.data

    assert response.status_code == 200
    assert data['count'] == ToDo.objects.filter(Q(public=True) | Q(created_by=user2)).count()


@pytest.mark.django_db
def test_post_list_todo_not_authenticated(api_client, user):
    data= {
        'title':'test',
        'description':'test_des',
    }
    response = api_client.post(reverse("todo-list"), data=data)
    assert response.status_code == 401
    assert response.data['detail'] == 'Authentication credentials were not provided.'

@pytest.mark.django_db
def test_post_list_todo_authenticated(api_client, user):
    data= {
        'title':'test_title',
        'description':'test_des',
    }
    api_client.force_login(user)
    response = api_client.post(reverse("todo-list"), data=data)
    todo = ToDo.objects.get(title='test_title')
    assert response.status_code == 201
    assert response.data['title'] == 'test_title'
    assert todo.title == 'test_title'
    assert todo.created_by == user
    assert todo.public == False


@pytest.mark.django_db
def test_get_detail_todo_not_authenticated(api_client, user):
    response = api_client.get(reverse("todo-detail", args=[98]))
    data = response.data
    todo = ToDo.objects.get(pk=98)

    assert response.status_code == 200
    assert data['title'] == todo.title
    assert data['comments']['count'] == todo.comments_in.count()


@pytest.mark.django_db
def test_get_detail_todo_authenticated(api_client, user):
    api_client.force_login(user)
    response = api_client.get(reverse("todo-detail", args=[98]))
    data = response.data
    todo = ToDo.objects.get(pk=98)

    assert response.status_code == 200
    assert data['title'] == todo.title
    assert data['comments']['count'] == todo.comments_in.count()

@pytest.mark.django_db
def test_get_detail_todo_authenticated_not_owner_private(api_client, user):
    api_client.force_login(user)
    response = api_client.get(reverse("todo-detail", args=[3]))

    assert response.status_code == 404

@pytest.mark.django_db
def test_delete_detail_todo_not_authenticated(api_client, user):
    response = api_client.delete(reverse("todo-detail", args=[98]))

    assert response.status_code == 401
    assert response.data['detail'] == 'Authentication credentials were not provided.'



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
    response = api_client.delete(reverse("todo-detail", args=[3]))

    assert response.status_code == 404
    assert ToDo.objects.filter(pk=3).count() == 1

##########

@pytest.mark.django_db
def test_post_comment_action_todo_not_authenticated_public(api_client, user):
    data = {
        'text':'test_text'
    }
    response = api_client.post(reverse('todo-comment', args=[98]))
    assert response.status_code == 401
    assert response.data['detail'] == 'Authentication credentials were not provided.'

@pytest.mark.django_db
def test_post_comment_action_todo_authenticated_public(api_client, user):
    data = {
        'text':'test_text'
    }
    api_client.force_login(user)
    response = api_client.post(reverse('todo-comment', args=[98]), data=data)
    assert response.status_code == 200

@pytest.mark.django_db
def test_post_comment_action_todo_authenticated_private_not_owner(api_client, user):
    data = {
        'text':'test_text'
    }
    api_client.force_login(user)
    response = api_client.post(reverse('todo-comment', args=[3]), data=data)
    assert response.status_code == 404

@pytest.mark.django_db
def test_post_comment_action_todo_authenticated_public_not_owner(api_client, user):
    data = {
        'text':'test_text'
    }
    api_client.force_login(user)
    response = api_client.post(reverse('todo-comment', args=[44]), data=data)
    assert response.status_code == 200

@pytest.mark.django_db
def test_post_comment_action_todo_bad_request(api_client, user):
    data = {
        'text_bad':'test_text'
    }
    api_client.force_login(user)
    response = api_client.post(reverse('todo-comment', args=[98]), data=data)
    assert response.status_code == 400