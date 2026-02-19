import pytest
from rest_framework import exceptions
from rest_framework.request import Request
from rest_framework.test import APIRequestFactory

from config.exceptions import exception_handler


class TestExceptionHandler:
    def test_validation_error_with_list_detail_returns_full_details(self):
        exc = exceptions.ValidationError({"email": ["This field is required."]})
        request = Request(APIRequestFactory().get("/"))
        context = {"request": request, "view": None}

        response = exception_handler(exc, context)

        assert response is not None
        assert "email" in response.data
        assert response.data["email"][0]["message"] == "This field is required."

    def test_validation_error_with_string_detail_returns_structured_format(self):
        exc = exceptions.ValidationError("Invalid data")
        request = Request(APIRequestFactory().get("/"))
        context = {"request": request, "view": None}

        response = exception_handler(exc, context)

        assert response is not None
        assert response.data is not None
        assert isinstance(response.data, (list, dict))

    def test_not_found_returns_proper_format(self):
        exc = exceptions.NotFound("Not found.")
        request = Request(APIRequestFactory().get("/"))
        context = {"request": request, "view": None}

        response = exception_handler(exc, context)

        assert response is not None
        assert "detail" in response.data

    def test_permission_denied_returns_proper_format(self):
        exc = exceptions.PermissionDenied("Permission denied.")
        request = Request(APIRequestFactory().get("/"))
        context = {"request": request, "view": None}

        response = exception_handler(exc, context)

        assert response is not None
        assert "detail" in response.data
