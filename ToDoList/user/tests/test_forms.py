import pytest
import io

from .factories import UserFactory, GenderFactory, ProfileFactory

from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile

from user.forms import (
    UserModifiedCreationForm,
    UserModifiedUpdateForm,
    ProfileCreationForm,
    ProfileUpdateForm,
)


@pytest.mark.parametrize("name", ["test", "iDontKnow", "James"])
@pytest.mark.django_db
def test_profile_creation_form(name):
    data = {"name": name, "gender": GenderFactory()}
    profile_form = ProfileCreationForm(data=data)
    profile = profile_form.save(commit=False)
    profile.user = UserFactory()
    profile.save()

    assert profile_form.is_valid()
    assert get_user_model().objects.all().count() == 1
    assert profile.name == name
    assert profile.gender is not None


@pytest.mark.parametrize(
    "name, profile_pic",
    [
        ["test", "profile_pics/default_profile.jpg"],
        ["help", "profile_pics/default_profile.jpg"],
    ],
)
@pytest.mark.django_db
def test_profile_update_form(name, profile_pic):
    gender = GenderFactory()
    data = {
        "name": name,
        "gender": gender,
    }
    profile_form = ProfileUpdateForm(instance=ProfileFactory(), data=data)
    profile = profile_form.save(commit=False)
    profile.profile_pic = profile_pic
    profile.save()
    assert profile.name == name
    assert profile.gender == gender
    assert profile.profile_pic.name == profile_pic
