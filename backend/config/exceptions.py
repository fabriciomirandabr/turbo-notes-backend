from rest_framework import exceptions
from rest_framework.views import exception_handler as drf_exception_handler


def exception_handler(exc, context):
    response = drf_exception_handler(exc, context)
    if response is not None and isinstance(exc, exceptions.APIException):
        full_details = exc.get_full_details()
        if not isinstance(exc.detail, (list, dict)):
            response.data = {"detail": full_details}
        else:
            response.data = full_details
    return response
