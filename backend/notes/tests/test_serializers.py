import pytest
from django.contrib.auth.models import User

from notes.models import Category, Note
from notes.serializers import CategorySerializer, NoteSerializer, SignupSerializer


class TestSignupSerializer:
    def test_valid_data_creates_user_and_categories(self, db):
        serializer = SignupSerializer(
            data={"email": "new@example.com", "password": "secret123"}
        )
        assert serializer.is_valid()
        user = serializer.save()
        assert user.username == "new@example.com"
        assert user.email == "new@example.com"
        assert User.objects.filter(username="new@example.com").exists()
        assert Category.objects.filter(user=user).count() == 3

    def test_duplicate_email_raises_validation_error(self, db, user):
        serializer = SignupSerializer(
            data={"email": user.email, "password": "secret123"}
        )
        assert not serializer.is_valid()
        assert "email" in serializer.errors
        assert serializer.errors["email"][0].code == "email_exists"

    def test_password_too_short_raises_validation_error(self, db):
        serializer = SignupSerializer(
            data={"email": "new@example.com", "password": "12345"}
        )
        assert not serializer.is_valid()
        assert "password" in serializer.errors

    def test_invalid_email_raises_validation_error(self, db):
        serializer = SignupSerializer(
            data={"email": "not-an-email", "password": "secret123"}
        )
        assert not serializer.is_valid()
        assert "email" in serializer.errors


class TestCategorySerializer:
    def test_get_note_count(self, user, category):
        Note.objects.create(
            title="N1", content="C1", category=category, user=user
        )
        Note.objects.create(
            title="N2", content="C2", category=category, user=user
        )
        serializer = CategorySerializer(category)
        assert serializer.data["note_count"] == 2

    def test_serializes_all_fields(self, category):
        serializer = CategorySerializer(category)
        assert "id" in serializer.data
        assert serializer.data["name"] == "Test Category"
        assert serializer.data["color"] == "#EF9C66"
        assert "note_count" in serializer.data


class TestNoteSerializer:
    def test_serializes_with_category_detail(self, note, category):
        serializer = NoteSerializer(note)
        assert serializer.data["title"] == "Test Note"
        assert serializer.data["content"] == "Test content"
        assert serializer.data["category"] == category.id
        assert serializer.data["category_detail"] is not None
        assert serializer.data["category_detail"]["name"] == category.name
        assert "created_at" in serializer.data
        assert "updated_at" in serializer.data

    def test_serializes_note_without_category(self, user):
        note = Note.objects.create(
            title="No Cat", content="Content", category=None, user=user
        )
        serializer = NoteSerializer(note)
        assert serializer.data["category"] is None
        assert serializer.data["category_detail"] is None
