import pytest
import pytest_django.asserts
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from django.urls import reverse
from user.views import ProfileView
from todo.models import ToDo
from django.db.models import Q


def test_cant_access_login_while_logged(admin_user, client):
    response_login = client.get(reverse("login"))
    response_register = client.get(reverse("register"))
    client.force_login(admin_user)
    response_login_auth = client.get(reverse("login"))
    response_register_auth = client.get(reverse("register"))
    assert response_login.status_code == 200
    assert response_register.status_code == 200
    assert response_login_auth.status_code == 301
    assert response_register_auth.status_code == 301


@pytest.mark.django_db()
def test_registration_bad_data(client, load_fixtures):
    data = {
        "username": "test",
        "email": "test@test.test",
        "password1": "heslo34",
        "password2": "heslo1234",
        "name": "test_name",
        "gender": 1,
    }
    response = client.post(reverse("register"), data=data)
    assert response.status_code == 400


@pytest.mark.django_db()
def test_profile_is_created_on_registration(client, load_fixtures):
    data = {
        "username": "test",
        "email": "test@test.test",
        "password1": "heslo1234",
        "password2": "heslo1234",
        "name": "test_name",
        "gender": 1,
    }

    response = client.post(reverse("register"), data=data)

    User = get_user_model()
    user = User.objects.get(username="test")

    assert response.status_code == 301
    assert user.username == "test"
    assert user.profile.name == "test_name"
    assert user.profile.gender.id == 1


@pytest.mark.parametrize(
    "email, name, gender",
    [
        ["test@test.test", "testing", 1],
        ["tes@llll.df", "asdasd", 2],
    ],
)
@pytest.mark.django_db()
def test_update_profile(user, client, email, name, gender):
    client.force_login(user)
    response_get = client.get(reverse("profile-update"))
    data = {
        "email": email,
        "name": name,
        "gender": gender,
    }
    response = client.post(reverse("profile-update"), data=data)
    user.refresh_from_db()
    assert user.email == email
    assert response.status_code == 301
    assert user.profile.name == name
    assert user.profile.gender.id == gender
    assert response_get.status_code == 200

@pytest.mark.parametrize(
    "email, name, gender",
    [
        ["test@test", "testing", 1],
    ],
)
@pytest.mark.django_db()
def test_bad_data_profile_profile(user, client, email, name, gender):
    data = {
        "email": email,
        "name": name,
        "gender": gender,
    }
    client.force_login(user)
    response = client.post(reverse("profile-update"), data=data)
    assert response.status_code == 400




@pytest.mark.django_db
def test_delete_user(user, client):
    client.force_login(user)
    response_get = client.get(reverse("profile-delete"))

    assert response_get.context["random"] == user.profile.delete_number
    assert response_get.status_code == 200

    response_bad_post = client.post(
        reverse("profile-delete"), data={"number": (user.profile.delete_number + 1)}
    )
    assert response_bad_post.status_code == 400

    response_good_post = client.post(
        reverse("profile-delete"), data={"number": user.profile.delete_number}
    )
    with pytest.raises(ObjectDoesNotExist) as exc_info:
        user.refresh_from_db()

    assert "User matching query does not exist." in str(exc_info.value)
    assert response_good_post.status_code == 301


def test_login_required(client):
    response = client.get(reverse('profile-update'))
    assert response.status_code == 302
    assert reverse('login') in response.url
    response = client.get(reverse('profile-delete'))
    assert response.status_code == 302
    assert reverse('login') in response.url

@pytest.mark.django_db
def test_profile_view(user, rf, client):
    response = client.get(reverse('profile', args=[user.pk]))
    assert response.context['base'] == 'user/auth/user_auth_base.html'
    todos = ToDo.objects.filter(Q(created_by=user) & Q(public=True))
    pytest_django.asserts.assertQuerysetEqual(response.context['todos'], todos)


@pytest.mark.django_db
def test_profile_view_auth_owner(user, rf, client):
    client.force_login(user)
    response = client.get(reverse('profile', args=[user.pk]))
    assert response.context['base'] == 'user/logged/user_logged_base.html'
    todos = ToDo.objects.filter(created_by=user)
    pytest_django.asserts.assertQuerysetEqual(response.context['todos'], todos)


@pytest.mark.django_db
def test_profile_view_auth_not_owner(user, user2, rf, client):
    client.force_login(user2)
    response = client.get(reverse('profile', args=[user.pk]))
    assert response.context['base'] == 'user/logged/user_logged_base.html'
    todos = ToDo.objects.filter(Q(created_by=user) & Q(public=True))
    pytest_django.asserts.assertQuerysetEqual(response.context['todos'], todos)