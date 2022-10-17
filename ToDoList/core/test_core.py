import pytest
import os
from .env_utils import get_env

def test_get_env_setted_env(monkeypatch):
    monkeypatch.setenv('setted_env', './static')
    assert get_env('setted_env') == './static'

def test_get_env_not_setted_env(monkeypatch):
    monkeypatch.delenv('not_setted_env')
    from django.core.exceptions import ImproperlyConfigured
    with pytest.raises(ImproperlyConfigured):
        get_env('not_setted_env')
