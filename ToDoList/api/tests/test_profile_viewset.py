import pytest
from rest_framework.reverse import reverse
from django.db.models import Q
from django.contrib.auth.models import User


@pytest.mark.django_db
def test_get_profile_not_authenticated(api_client, user):
    response = api_client.get(reverse("profile-detail", args=[user.profile.id]))
    data = response.data

    assert data['name'] == user.profile.name
    assert user.profile.profile_pic.url in data['profile_pic']
    assert data['gender'] == user.profile.gender.gender_name
    assert len(data['todo']['results']) == user.todos.filter(public=True).count()
    assert user.username not in data
    assert response.status_code == 200


@pytest.mark.django_db
def test_get_profile_auth(api_client, user):
    api_client.force_login(user)
    response = api_client.get(reverse("profile-detail", args=[user.profile.id]))
    data = response.data
    assert data['name'] == user.profile.name
    assert user.profile.profile_pic.url in data['profile_pic']
    assert data['gender'] == user.profile.gender.gender_name
    assert len(data['todo']['results']) == user.todos.filter((Q(public=True) | Q(created_by=user))).count()
    assert user.username not in data
    assert response.status_code == 200


@pytest.mark.django_db
def test_get_profile_auth_not_owner(api_client, user):
    api_client.force_login(user)
    response = api_client.get(reverse("profile-detail", args=[2]))
    data = response.data
    user2 = User.objects.get(pk=2)
    assert data['name'] == user2.profile.name
    assert user2.profile.profile_pic.url in data['profile_pic']
    assert data['gender'] == user2.profile.gender.gender_name
    assert len(data['todo']['results']) == user2.todos.filter(public=True).count()
    assert user.username not in data
    assert response.status_code == 200


# @pytest.mark.django_db
# def test_patch_method_not_authenticated(api_client, user):
#     data = {'name': 'rename_test'}
#     response = api_client.patch(reverse("profile-detail", args=[user.profile.id]), data=data)
#     user.refresh_from_db()
#     assert response.status_code == 401
#     assert user.profile.name != data['name']


# @pytest.mark.django_db
# def test_patch_method_auth(api_client, user):
#     api_client.force_login(user)
#     data = {'name': 'rename_test'}
#     response = api_client.patch(reverse("profile-detail", args=[user.profile.id]), data=data)
#     user.refresh_from_db()
#     assert response.data['name'] == data['name']
#     assert response.status_code == 200
#     assert user.profile.name == data['name']


# @pytest.mark.django_db
# def test_patch_method_auth_not_owner(api_client, user):
#     api_client.force_login(user)
#     data = {'name': 'rename_test'}
#     response = api_client.patch(reverse("profile-detail", args=[2]), data=data)
#     assert response.status_code == 403

# @pytest.mark.django_db
# def test_delete_method_not_authenticated(api_client, user):
#     response = api_client.delete(reverse("profile-detail", args=[user.profile.id]))
#     assert response.status_code == 405
#     assert 'u cant delete account this way' == response.data['detail']

# @pytest.mark.django_db
# def test_delete_method_not_authenticated(api_client, user):
#     response = api_client.delete(reverse("profile-detail", args=[user.profile.id]))
#     assert response.status_code == 405
#     assert 'u cant delete account this way' == response.data['detail']

# @pytest.mark.django_db
# def test_delete_method_auth_not_owner(api_client, user):
#     response = api_client.delete(reverse("profile-detail", args=[2]))
#     assert response.status_code == 405
#     assert 'u cant delete account this way' == response.data['detail']

# @pytest.mark.django_db
# def test_delete_method_auth_not_owner(api_client, user):
#     response = api_client.delete(reverse("profile-detail", args=[2]))
#     assert response.status_code == 405
#     assert 'u cant delete account this way' == response.data['detail']
#
#
# @pytest.mark.django_db
# def test_delete_method(api_client, user):
#     api_client.force_login(user)
#     response = api_client.delete(reverse("profile-detail", args=[user.profile.id]))
#     assert response.status_code == 405
#     assert 'u cant delete account this way' == response.data['detail']


@pytest.mark.django_db
def test_delete_profile_thought_logged_not_authenticated(api_client, user):
    response = api_client.delete(reverse("profile-logged"))
    assert response.status_code == 401
    assert 'Authentication credentials were not provided.' == response.data['detail']


@pytest.mark.django_db
def test_delete_profile_thought_logged(api_client, user):
    api_client.force_login(user)
    response = api_client.delete(reverse("profile-logged"))
    assert response.status_code == 200
    assert 'account test0 was deleted' == response.data['info']
    assert User.objects.filter(pk=user.pk).count() == 0


@pytest.mark.django_db
def test_get_profile_thought_logged(api_client, user):
    api_client.force_login(user)
    response = api_client.get(reverse("profile-logged"))
    data = response.data
    assert data['name'] == user.profile.name
    assert user.profile.profile_pic.url in data['profile_pic']
    assert data['gender'] == user.profile.gender.gender_name
    assert len(data['todo']['results']) == user.todos.filter((Q(public=True) | Q(created_by=user))).count()
    assert user.username not in data
    assert response.status_code == 200


@pytest.mark.django_db
def test_generate_token_not_authenticated(api_client, user):
    response = api_client.get(reverse('profile-generate-token'))
    assert response.status_code == 401
    assert 'Authentication credentials were not provided.' == response.data['detail']


@pytest.mark.django_db
def test_generate_token_token_already_exist(api_client, user):
    api_client.force_login(user)
    response = api_client.get(reverse('profile-generate-token'))
    assert response.status_code == 200
    assert user.auth_token.key == response.data['token']


@pytest.mark.django_db
def test_generate_token_token(api_client, user2):
    api_client.force_login(user2)
    response = api_client.get(reverse('profile-generate-token'))
    assert response.status_code == 200
    assert user2.auth_token.key == response.data['token']


@pytest.mark.django_db
def test_create_method_not_authenticated(api_client, user):
    response = api_client.post(reverse("profile-detail", args=[user.profile.id]))
    assert response.status_code == 405
    assert 'Method "POST" not allowed.' == response.data['detail']


@pytest.mark.django_db
def test_create_method_auth_not_owner(api_client, user):
    response = api_client.post(reverse("profile-detail", args=[2]))
    assert response.status_code == 405
    assert 'Method "POST" not allowed.' == response.data['detail']
