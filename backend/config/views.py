from django.db import connection
from django.http import JsonResponse


def health(request):
    """Health check endpoint for load balancers and monitoring."""
    try:
        connection.ensure_connection()
        return JsonResponse({"status": "ok", "database": "connected"})
    except Exception as e:
        return JsonResponse(
            {"status": "error", "database": str(e)},
            status=503,
        )
