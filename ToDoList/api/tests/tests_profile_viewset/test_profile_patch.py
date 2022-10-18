import pytest
from rest_framework.reverse import reverse
from django.db.models import Q
from django.contrib.auth.models import User
from user.models import Gender





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
    data = {'name': 'rename_test',
            'gender': 5
            }
    response = api_client.patch(reverse("profile-logged"), data=data)
    user.refresh_from_db()
    assert response.status_code == 200
    assert user.profile.name == data['name']
    assert user.profile.gender == Gender.objects.get(pk=data['gender'])


@pytest.mark.django_db
def test_patch_list_action_logged_profile_authenticated_bad_request(api_client, user, rf):
    api_client.force_login(user)
    over_150_char='aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa'
    data = {'name':over_150_char}
    response = api_client.patch(reverse("profile-logged"), data=data)
    assert response.status_code == 400