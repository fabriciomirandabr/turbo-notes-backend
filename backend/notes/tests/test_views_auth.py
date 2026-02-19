import pytest
from django.contrib.auth.models import User

from notes.models import Category


class TestSignupView:
    def test_signup_returns_tokens_and_creates_user(self, api_client, db):
        response = api_client.post(
            "/api/auth/signup",
            {"email": "newuser@example.com", "password": "secret123"},
            format="json",
        )
        assert response.status_code == 201
        assert "access" in response.data
        assert "refresh" in response.data
        assert User.objects.filter(username="newuser@example.com").exists()
        user = User.objects.get(username="newuser@example.com")
        assert Category.objects.filter(user=user).count() == 3

    def test_signup_duplicate_email_returns_400(self, api_client, user):
        response = api_client.post(
            "/api/auth/signup",
            {"email": user.email, "password": "secret123"},
            format="json",
        )
        assert response.status_code == 400
        assert "email" in response.data or "detail" in response.data

    def test_signup_password_too_short_returns_400(self, api_client, db):
        response = api_client.post(
            "/api/auth/signup",
            {"email": "new@example.com", "password": "12345"},
            format="json",
        )
        assert response.status_code == 400


class TestLoginView:
    def test_login_returns_tokens(self, api_client, user):
        response = api_client.post(
            "/api/auth/login",
            {"username": user.username, "password": "testpass123"},
            format="json",
        )
        assert response.status_code == 200
        assert "access" in response.data
        assert "refresh" in response.data

    def test_login_invalid_credentials_returns_401(self, api_client, user):
        response = api_client.post(
            "/api/auth/login",
            {"username": user.username, "password": "wrongpassword"},
            format="json",
        )
        assert response.status_code == 401


class TestRefreshView:
    def test_refresh_returns_new_access_token(self, api_client, user):
        login_resp = api_client.post(
            "/api/auth/login",
            {"username": user.username, "password": "testpass123"},
            format="json",
        )
        refresh_token = login_resp.data["refresh"]

        response = api_client.post(
            "/api/auth/refresh",
            {"refresh": refresh_token},
            format="json",
        )
        assert response.status_code == 200
        assert "access" in response.data
