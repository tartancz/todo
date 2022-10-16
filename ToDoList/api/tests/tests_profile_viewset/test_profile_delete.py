import pytest
from rest_framework.reverse import reverse
from django.db.models import Q
from django.contrib.auth.models import User
from todo.models import ToDo



@pytest.mark.django_db
def test_delete_detail_profile_not_authenticated(api_client, user):
    response = api_client.delete(reverse("profile-detail", args=[user.profile.id]))
    assert response.status_code == 405
    assert 'Method "DELETE" not allowed.' == response.data['detail']


@pytest.mark.django_db
def test_delete_detail_profile_authenticated(api_client, user):
    api_client.force_login(user)
    response = api_client.delete(reverse("profile-detail", args=[user.profile.id]))
    assert response.status_code == 405
    assert 'Method "DELETE" not allowed.' == response.data['detail']



@pytest.mark.django_db
def test_delete_detail_profile_not_owner(api_client, user):
    response = api_client.delete(reverse("profile-detail", args=[2]))
    assert response.status_code == 405
    assert 'Method "DELETE" not allowed.' == response.data['detail']


@pytest.mark.django_db
def test_delete_list_action_logged_profile_not_authenticated(api_client, user):
    response = api_client.delete(reverse("profile-logged"))
    data = response.data
    assert data['detail'] == 'Authentication credentials were not provided.'
    assert response.status_code == 401



@pytest.mark.django_db
def test_delete_list_action_logged_profile_authenticated(api_client, user):
    api_client.force_login(user)
    response = api_client.delete(reverse("profile-logged"))
    data = response.data
    assert data['info'] == f'account {user.username} was deleted'
    assert User.objects.filter(pk=user.id).count() == 0
    assert ToDo.objects.filter(created_by=user.id).count() == 0
    assert response.status_code == 200
