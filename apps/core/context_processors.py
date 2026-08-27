from django.db import DatabaseError, OperationalError, ProgrammingError

from .models import BusinessConfig


def business(request):
    """
    Expose the business configuration to every template as ``business``.

    Swallows database errors so that a page can still render before the first
    migration has run, which otherwise makes a fresh deploy fail confusingly.
    """
    try:
        return {"business": BusinessConfig.cached()}
    except (OperationalError, ProgrammingError, DatabaseError):
        return {"business": None}
