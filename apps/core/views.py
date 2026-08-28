from django.db import connection
from django.http import JsonResponse


def healthz(request):
    """
    Liveness and database check, for uptime monitoring and deploy verification.

    Returns 503 when the database is unreachable so a broken deploy is obvious
    rather than silently serving pages that fail later.
    """
    checks = {"app": "ok"}
    status = 200

    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            cursor.fetchone()
        checks["database"] = "ok"
    except Exception as exc:  # noqa: BLE001 - report any failure, never raise
        checks["database"] = f"error: {exc.__class__.__name__}"
        status = 503

    return JsonResponse(checks, status=status)
