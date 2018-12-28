import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tests.settings')

import django
django.setup()

import pytest
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token

from .views import UserViewSet


User = get_user_model()


@pytest.fixture
def user_data():
    return {
        'username': 'quan',
        'email': 'user@agriconnect.vn'
    }


@pytest.mark.django_db
class TestUserViewSet:
    def setup(self):
        u = User.objects.create_superuser('admin', 'admin@agriconnect.vn', '123456')
        t = Token(user=u)
        t.save()
        self.token = t.key

    def test_create(self, client, user_data):
        user_data['access_token'] = self.token
        r = client.post('/users/', user_data, content_type='application/json')
        assert r.status_code == 201

    def test_absent_token(self, client, user_data):
        r = client.post('/users/', user_data, content_type='application/json')
        assert r.status_code == 401

    def test_invalid_token(self, client, user_data):
        user_data['access_token'] = 'blahblah'
        r = client.post('/users/', user_data, content_type='application/json')
        assert r.status_code == 401

    def test_change_field(self, settings, client, user_data):
        settings.DRF_BODY_TOKEN_FIELD = 'secret'
        user_data['secret'] = self.token
        r = client.post('/users/', user_data, content_type='application/json')
        assert r.status_code == 201
