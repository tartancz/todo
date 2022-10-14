from .factories import ProfileFactory, GenderFactory
import pytest


@pytest.mark.django_db
def test_model_to_str():
    profile = ProfileFactory()
    gender = GenderFactory()

    assert str(profile) == profile.name
    assert str(gender) == gender.gender_name


@pytest.mark.django_db
def test_profile_pic_set_res():
    profile = ProfileFactory()
    profile.profile_pic.hight = 300
    profile.profile_pic.weidth = 300
