import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIClient

from notes.models import Category, Note


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def user(db):
    return User.objects.create_user(
        username="test@example.com",
        email="test@example.com",
        password="testpass123",
    )


@pytest.fixture
def other_user(db):
    return User.objects.create_user(
        username="other@example.com",
        email="other@example.com",
        password="otherpass123",
    )


@pytest.fixture
def category(user):
    return Category.objects.create(
        name="Test Category",
        color="#EF9C66",
        user=user,
    )


@pytest.fixture
def note(user, category):
    return Note.objects.create(
        title="Test Note",
        content="Test content",
        category=category,
        user=user,
    )


@pytest.fixture
def auth_headers(api_client, user):
    response = api_client.post(
        "/api/auth/login",
        {"username": user.username, "password": "testpass123"},
        format="json",
    )
    token = response.data["access"]
    return {"HTTP_AUTHORIZATION": f"Bearer {token}"}
