from http import HTTPStatus

import pytest
from pytest_factoryboy import register
from rest_framework.test import APIClient

from apps.core.factories import UserFactory

register(UserFactory)  # fixtures: user & user_factory


@pytest.fixture()
def staff():
    return UserFactory(is_staff=True)


@pytest.fixture()
def client():
    return APIClient()


@pytest.fixture()
def logged_client(client, user):
    client.force_authenticate(user)
    client.user = user
    return client


@pytest.fixture()
def staff_client(client, staff):
    client.force_authenticate(staff)
    client.user = staff
    return client
