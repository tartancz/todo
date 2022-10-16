import pytest
from rest_framework.reverse import reverse
from django.db.models import Q
from django.contrib.auth.models import User





@pytest.mark.django_db
def test_patch_detail_profile_not_authenticated(api_client, user):
    data = {'name': 'rename_test'}
    response = api_client.patch(reverse("profile-detail", args=[user.profile.id]), data=data)
    user.refresh_from_db()
    assert response.status_code == 405
    assert user.profile.name != data['name']


@pytest.mark.django_db
def test_patch_detail_profile_authenticated(api_client, user):
    api_client.force_login(user)
    data = {'name': 'rename_test'}
    response = api_client.patch(reverse("profile-detail", args=[user.profile.id]), data=data)
    user.refresh_from_db()
    assert response.status_code == 405
    assert user.profile.name != data['name']


@pytest.mark.django_db
def test_patch_list_action_logged_profile_not_authenticated(api_client, user):
    data = {'name': 'rename_test'}
    response = api_client.patch(reverse("profile-logged"), data=data)
    user.refresh_from_db()
    assert response.status_code == 401
    assert user.profile.name != data['name']


@pytest.mark.django_db
def test_patch_list_action_logged_profile_authenticated(api_client, user):
    api_client.force_login(user)
    data = {'name': 'rename_test'}
    response = api_client.patch(reverse("profile-logged"), data=data)
    user.refresh_from_db()
    assert response.status_code == 200
    assert user.profile.name == data['name']
