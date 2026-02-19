import pytest


class TestNoteViewSet:
    def test_list_returns_notes_for_user(self, api_client, auth_headers, note):
        response = api_client.get("/api/notes", **auth_headers)
        assert response.status_code == 200
        results = response.data["results"]
        assert len(results) == 1
        assert results[0]["title"] == "Test Note"

    def test_list_unauthenticated_returns_401(self, api_client, note):
        response = api_client.get("/api/notes")
        assert response.status_code == 401

    def test_list_filter_by_category(self, api_client, auth_headers, user, note):
        from notes.models import Category, Note

        cat2 = Category.objects.create(
            name="Other", color="#000000", user=user
        )
        Note.objects.create(
            title="Note 2", content="C2", category=cat2, user=user
        )

        response = api_client.get(
            f"/api/notes?category={note.category_id}", **auth_headers
        )
        assert response.status_code == 200
        results = response.data["results"]
        assert len(results) == 1
        assert results[0]["id"] == note.id

    def test_create_note(self, api_client, auth_headers, category):
        response = api_client.post(
            "/api/notes",
            {"title": "New Note", "content": "New content", "category": category.id},
            format="json",
            **auth_headers,
        )
        assert response.status_code == 201
        assert response.data["title"] == "New Note"
        assert response.data["content"] == "New content"
        assert response.data["category"] == category.id

    def test_create_note_without_category(self, api_client, auth_headers):
        response = api_client.post(
            "/api/notes",
            {"title": "No Cat", "content": "Content", "category": None},
            format="json",
            **auth_headers,
        )
        assert response.status_code == 201
        assert response.data["category"] is None

    def test_retrieve_note(self, api_client, auth_headers, note):
        response = api_client.get(f"/api/notes/{note.id}", **auth_headers)
        assert response.status_code == 200
        assert response.data["title"] == "Test Note"

    def test_retrieve_note_of_other_user_returns_404(
        self, api_client, auth_headers, other_user
    ):
        from notes.models import Category, Note

        cat = Category.objects.create(
            name="Other", color="#000000", user=other_user
        )
        other_note = Note.objects.create(
            title="Other", content="C", category=cat, user=other_user
        )

        response = api_client.get(f"/api/notes/{other_note.id}", **auth_headers)
        assert response.status_code == 404

    def test_update_note(self, api_client, auth_headers, note):
        response = api_client.put(
            f"/api/notes/{note.id}",
            {"title": "Updated", "content": "Updated content", "category": note.category_id},
            format="json",
            **auth_headers,
        )
        assert response.status_code == 200
        assert response.data["title"] == "Updated"
        assert response.data["content"] == "Updated content"

    def test_partial_update_note(self, api_client, auth_headers, note):
        response = api_client.patch(
            f"/api/notes/{note.id}",
            {"title": "Patched Title"},
            format="json",
            **auth_headers,
        )
        assert response.status_code == 200
        assert response.data["title"] == "Patched Title"
        assert response.data["content"] == "Test content"

    def test_delete_note(self, api_client, auth_headers, note):
        response = api_client.delete(f"/api/notes/{note.id}", **auth_headers)
        assert response.status_code == 204
        assert not note.__class__.objects.filter(id=note.id).exists()
