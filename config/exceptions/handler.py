import logging
import uuid
from datetime import datetime, timezone
from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status

from .base import BaseAPIException
from .codes import ErrorCode

logger = logging.getLogger("api.errors")


def custom_exception_handler(exc, context):
  request = context.get("request")
  error_id = str(uuid.uuid4())
  timestamp = datetime.now(timezone.utc).isoformat()

  # handle business exceptions
  if isinstance(exc, BaseAPIException):
    # extract code
    code = exc.code
    if hasattr(code, "value"):
      code = code.value
    code = str(code).upper()

    # log with rich context
    logger.warning(
      f"Business Exception [{code}]: {exc.detail}",
      extra={
        "error_id": error_id,
        "path": request.path if request else None,
        "user_id": getattr(request.user, "id", None)
        if request and hasattr(request, "user")
        else None,
      },
    )

    # return response
    return Response(
      {
        "success": False,
        "status": exc.status_code,
        "code": code,
        "message": str(exc.detail),
        "errors": exc.extra_data if exc.extra_data else None,
        "meta": {
          "error_id": error_id,
          "timestamp": timestamp,
        },
      },
      status=exc.status_code,
    )

  # handle DRF based exceptions (validation, auth, permissions, etc.)
  response = exception_handler(exc, context)

  if response is not None:
    # extract code
    code = getattr(exc, "default_code", "error")
    code = str(code).upper()

    # extract message from DRF's response
    message = response.data.get("detail", "An error occurred.")

    # extract field-level errors if present
    errors = response.data if "detail" not in response.data else None

    # log based on severity
    if response.status_code >= 500:
      logger.exception(f"DRF 5xx: {type(exc).__name__}")
    else:
      logger.info(f"DRF 4xx: {type(exc).__name__}")

    # return standardized response
    return Response(
      {
        "success": False,
        "status": response.status_code,
        "code": code,
        "message": message,
        "errors": errors,
        "meta": {
          "error_id": error_id,
          "timestamp": timestamp,
        },
      },
      status=response.status_code,
    )

  # unhandled Non-DRF exceptions (database errors, import errors, etc.)
  logger.exception(f"Unhandled 500: {type(exc).__name__}")

  return Response(
    {
      "success": False,
      "status": status.HTTP_500_INTERNAL_SERVER_ERROR,
      "code": ErrorCode.INTERNAL_SERVER_ERROR.value,
      "message": "An unexpected error occurred.",
      "meta": {
        "error_id": error_id,
        "timestamp": timestamp,
      },
    },
    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
  )
