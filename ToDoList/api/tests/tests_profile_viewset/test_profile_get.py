import pytest
from rest_framework.reverse import reverse
from django.db.models import Q
from django.contrib.auth.models import User
from todo.models import ToDo



@pytest.mark.django_db
def test_get_list_profile_not_authenticated(api_client, user, rf):
    response = api_client.get(reverse("profile-list"))
    data = response.data
    assert data['count'] == User.objects.count()
    assert user.profile.profile_pic.url in data['results'][0]['profile_pic']
    assert data['results'][0]['name'] == user.profile.name
    assert data['results'][0]['gender'] == user.profile.gender.gender_name
    assert data['results'][0]['profile_api'] == reverse('profile-detail', args=[user.profile.id], request=rf.request())
    assert data['results'][0]['profile_web'] == reverse('profile', args=[user.profile.id], request=rf.request())
    assert user.username not in data
    assert response.status_code == 200


@pytest.mark.django_db
def test_get_list_profile_authenticated(api_client, user, rf):
    api_client.force_login(user)
    response = api_client.get(reverse("profile-list"))
    data = response.data
    assert data['count'] == User.objects.count()
    assert data['results'][0]['name'] == user.profile.name
    assert user.profile.profile_pic.url in data['results'][0]['profile_pic']
    assert data['results'][0]['gender'] == user.profile.gender.gender_name
    assert data['results'][0]['profile_api'] == reverse('profile-detail', args=[user.profile.id], request=rf.request())
    assert data['results'][0]['profile_web'] == reverse('profile', args=[user.profile.id], request=rf.request())
    assert user.username not in data
    assert response.status_code == 200



@pytest.mark.django_db
def test_get_detail_profile_not_authenticated(api_client, user, rf):
    response = api_client.get(reverse("profile-detail", args=[user.profile.id]))
    data = response.data
    assert data['name'] == user.profile.name
    assert user.profile.profile_pic.url in data['profile_pic']
    assert data['gender'] == user.profile.gender.gender_name
    assert data['profile_api'] == reverse('profile-detail', args=[user.profile.id], request=rf.request())
    assert data['profile_web'] == reverse('profile', args=[user.profile.id], request=rf.request())
    assert len(data['todo']['results']) == data['todo']['count']
    assert len(data['todo']['results']) == ToDo.objects.filter(Q(public=True) & Q(created_by=user)).count()
    assert response.status_code == 200


@pytest.mark.django_db
def test_get_detail_profile_authenticated(api_client, user, rf):
    api_client.force_login(user)
    response = api_client.get(reverse("profile-detail", args=[user.profile.id]))
    data = response.data
    assert data['name'] == user.profile.name
    assert user.profile.profile_pic.url in data['profile_pic']
    assert data['gender'] == user.profile.gender.gender_name
    assert data['profile_api'] == reverse('profile-detail', args=[user.profile.id], request=rf.request())
    assert data['profile_web'] == reverse('profile', args=[user.profile.id], request=rf.request())
    assert len(data['todo']['results']) == data['todo']['count']
    assert len(data['todo']['results']) == ToDo.objects.filter(Q(public=True) & Q(created_by=user)).count()
    assert response.status_code == 200


@pytest.mark.django_db
def test_get_detail_profile_not_owner(api_client, user2, rf):
    api_client.force_login(user2)
    user = User.objects.get(pk=1)
    response = api_client.get(reverse("profile-detail", args=[user.profile.id]))
    data = response.data
    assert data['name'] == user.profile.name
    assert user.profile.profile_pic.url in data['profile_pic']
    assert data['gender'] == user.profile.gender.gender_name
    assert data['profile_api'] == reverse('profile-detail', args=[user.profile.id], request=rf.request())
    assert data['profile_web'] == reverse('profile', args=[user.profile.id], request=rf.request())
    assert len(data['todo']['results']) == data['todo']['count']
    assert len(data['todo']['results']) == ToDo.objects.filter(Q(public=True) & Q(created_by=user)).count()
    assert response.status_code == 200


@pytest.mark.django_db
def test_get_list_action_logged_profile_not_authenticated(api_client, user):
    response = api_client.get(reverse("profile-logged"))
    assert response.status_code == 401
    assert response.data['detail'] == 'Authentication credentials were not provided.'


@pytest.mark.django_db
def test_get_list_action_logged_profile_authenticated(api_client, user, rf):
    api_client.force_login(user)
    response = api_client.get(reverse("profile-logged"))
    data = response.data
    assert data['name'] == user.profile.name
    assert data['username'] == user.username
    assert data['email'] == user.email
    assert user.profile.profile_pic.url in data['profile_pic']
    assert data['gender'] == user.profile.gender.gender_name
    assert data['profile_api'] == reverse('profile-detail', args=[user.profile.id], request=rf.request())
    assert data['profile_web'] == reverse('profile', args=[user.profile.id], request=rf.request())
    assert len(data['todo']['results']) == data['todo']['count']
    assert len(data['todo']['results']) == ToDo.objects.filter(created_by=user).count()
    assert response.status_code == 200



@pytest.mark.django_db
def test_get_list_action_generate_token_profile_not_authenticated(api_client, user):
    response = api_client.get(reverse('profile-generate-token'))
    assert response.status_code == 401
    assert 'Authentication credentials were not provided.' == response.data['detail']


@pytest.mark.django_db
def test_get_list_action_generate_token_profile_already_exist(api_client, user):
    api_client.force_login(user)
    response = api_client.get(reverse('profile-generate-token'))
    assert response.status_code == 200
    assert user.auth_token.key == response.data['token']

# ACTION DETAIL GENERATE_TOKEN
@pytest.mark.django_db
def test_get_list_action_generate_token_profile_auth(api_client, user2):
    api_client.force_login(user2)
    response = api_client.get(reverse('profile-generate-token'))
    assert response.status_code == 200
    assert user2.auth_token.key == response.data['token']
