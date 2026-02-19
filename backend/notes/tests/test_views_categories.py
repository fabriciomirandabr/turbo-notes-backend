import pytest
from notes.models import Category


class TestCategoryViewSet:
    def test_list_returns_categories_for_user(
        self, api_client, auth_headers, user, category
    ):
        response = api_client.get("/api/categories", **auth_headers)
        assert response.status_code == 200
        results = response.data["results"]
        assert len(results) >= 1
        names = [c["name"] for c in results]
        assert "Test Category" in names

    def test_list_unauthenticated_returns_401(self, api_client, category):
        response = api_client.get("/api/categories")
        assert response.status_code == 401

    def test_retrieve_category(self, api_client, auth_headers, category):
        response = api_client.get(
            f"/api/categories/{category.id}", **auth_headers
        )
        assert response.status_code == 200
        assert response.data["name"] == "Test Category"
        assert response.data["color"] == "#EF9C66"

    def test_retrieve_category_of_other_user_returns_404(
        self, api_client, auth_headers, other_user
    ):
        other_cat = Category.objects.create(
            name="Other Cat", color="#000000", user=other_user
        )
        response = api_client.get(
            f"/api/categories/{other_cat.id}", **auth_headers
        )
        assert response.status_code == 404
