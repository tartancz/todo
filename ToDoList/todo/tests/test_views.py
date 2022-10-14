import pytest
import pytest_django.asserts
from django.contrib.auth.models import AnonymousUser
from django.urls import reverse
from django.db.models import Q
from todo.views import IndexView
from todo.models import ToDo, Comment
from todo.tests.factories import CommentFactory, ToDoFactory
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User


@pytest.mark.django_db
def test_index_view_queryset(rf, load_fixtures):
    request = rf.get(reverse("todo:index"))
    request.user = AnonymousUser()
    view = IndexView()
    view.request = request
    qs = view.get_queryset()
    pytest_django.asserts.assertQuerysetEqual(ToDo.objects.filter(public=True), qs)


@pytest.mark.django_db
def test_index_view_logged_in_queryset(rf, user):
    request = rf.get(reverse("todo:index"))
    request.user = user
    view = IndexView()
    view.request = request
    qs = view.get_queryset()
    pytest_django.asserts.assertQuerysetEqual(
        ToDo.objects.filter(Q(created_by=user) | Q(public=True)), qs
    )


def test_login_required(client):
    response = client.get(reverse("todo:create-view"))
    assert response.status_code == 302
    assert reverse("login") in response.url


@pytest.mark.django_db
def test_create_todo_view(client, user):
    data = {
        "title": "test_title",
        "description": "test_description",
    }
    client.force_login(user)
    response = client.post(reverse("todo:create-view"), data=data)
    pytest_django.asserts.assertRedirects(response, reverse("todo:index"))
    todo = ToDo.objects.get(title="test_title")
    assert todo.title == data["title"]
    assert todo.created_by == user


@pytest.mark.django_db
def test_delete_todo_view(client, user):
    todo = ToDoFactory(created_by=user)
    response = client.get(reverse("todo:todo-done", args=[todo.id]))
    assert not todo.completed
    assert response.status_code == 403
    client.force_login(user)
    response_auth = client.get(reverse("todo:todo-done", args=[todo.id]))
    todo.refresh_from_db()
    assert todo.completed
    assert response_auth.status_code == 302


@pytest.mark.django_db
def test_detail_todo_get_obj_privilage(client, user2):
    #public:False
    response = client.get(reverse('todo:detail-view', args=[88]))
    assert response.status_code == 404
    #public:True
    response = client.get(reverse('todo:detail-view', args=[98]))
    assert response.context['obj'] == get_object_or_404(ToDo, (Q(pk=98) & Q(public=True)))
    assert response.status_code == 200
    #public:False and owner
    client.force_login(user2)
    response = client.get(reverse('todo:detail-view', args=[88]))
    assert response.context['obj'] == get_object_or_404(ToDo, (Q(created_by=user2) | Q(public=True)) & Q(pk=88))
    assert response.status_code == 200


@pytest.mark.django_db
def test_detail_todo_auth_owner(client, user2):
    client.force_login(user2)
    #owner and public is false
    response = client.get(reverse('todo:detail-view', args=[88]))
    assert response.status_code == 200
    #not owner and public is false
    response = client.get(reverse('todo:detail-view', args=[92]))
    assert response.status_code == 404
    #owner and public is true
    response = client.get(reverse('todo:detail-view', args=[46]))
    assert response.status_code == 200
    #not owner and public is true
    response = client.get(reverse('todo:detail-view', args=[51]))
    assert response.status_code == 200

@pytest.mark.django_db
def test_detail_todo_post_comment(client, user):
    #creating comment without being auth
    context = {
        'text':'testing_unit'
    }
    response = client.post(reverse('todo:detail-view', args=[98]), data=context)
    assert response.status_code == 302
    assert 'login' in response.url
    assert Comment.objects.filter(text='testing_unit').filter(created_in=98).count() == 0
    #creating comment with being auth
    client.force_login(user)
    response = client.post(reverse('todo:detail-view', args=[98]), data=context)
    assert response.status_code == 302
    assert Comment.objects.filter(text='testing_unit').filter(created_in=98).count() == 1
    #creating comment with being auth and public is private
    response = client.post(reverse('todo:detail-view', args=[92]), data=context)
    assert response.status_code == 404
