# DRF Custom Exception Handling

A centralized exception handling mechanism for Django REST Framework that produces consistent, structured error responses across the API — for business logic errors, DRF built-in errors, and unhandled exceptions alike.

## Structure

```
exceptions/
├──__init__.py
├── base.py       # BaseAPIException class
├── codes.py      # ErrorCode enum (business error codes)
└── handlers.py   # custom_exception_handler
```

## How it works

The handler covers three tiers of errors, in order:

1. **Business exceptions** (`BaseAPIException` subclasses)
   Raised intentionally in views/services for domain logic errors (e.g. `InsufficientBalanceError`). Carries a `code`, `detail`, and optional `extra_data`.

2. **DRF built-in exceptions** (`ValidationError`, `NotAuthenticated`, `PermissionDenied`, etc.)
   Delegated to DRF's default `exception_handler`, then reformatted into the same standardized shape.

3. **Unhandled exceptions** (DB errors, `ImportError`, bugs, etc.)
   Caught as a last resort, logged with full traceback (`logger.exception`), and returned as a generic 500 — no internal details leaked to the client.

## Response format

Every error response follows the same envelope:

```json
{
  "success": false,
  "status": 400,
  "code": "INSUFFICIENT_BALANCE",
  "message": "Not enough balance to complete this transaction.",
  "errors": null,
  "meta": {
    "error_id": "b3f1c2a4-...",
    "timestamp": "2026-07-29T12:34:56.789+00:00"
  }
}
```

- **`code`** — machine-readable string, uppercased, from `ErrorCode` for business errors or DRF's `default_code` otherwise.
- **`errors`** — field-level validation errors when present (DRF), or `extra_data` for business exceptions; `null` otherwise.
- **`meta.error_id`** — unique UUID per error occurrence, useful for correlating a user-facing error with server logs.

## Usage

### 1. Define error codes

```python
# codes.py
class ErrorCode(str, Enum):
    INTERNAL_SERVER_ERROR = "internal_server_error"
    INSUFFICIENT_BALANCE = "insufficient_balance"
```

### 2. Raise business exceptions

```python
from .base import BaseAPIException
from .codes import ErrorCode

class InsufficientBalanceError(BaseAPIException):
    default_code = ErrorCode.INSUFFICIENT_BALANCE
    default_detail = "Not enough balance to complete this transaction."

# in a view/service
raise InsufficientBalanceError(extra_data={"required": 100, "available": 40})
```

## Logging

- Business exceptions → `logger.warning`
- DRF 5xx → `logger.exception` (with traceback)
- DRF 4xx → `logger.info`
- Unhandled exceptions → `logger.exception` (with traceback)

All logs are tagged with `error_id`, request path, and `user_id` (when available) for traceability.

## Notes

- `BaseAPIException.status_code` is hardcoded to `400` at the class level — subclasses that need a different status (403, 404, 409...) must override it explicitly.
