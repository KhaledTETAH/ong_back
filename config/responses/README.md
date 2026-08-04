# DRF Standard Success Response Handling

A companion mechanism to the [custom exception handler](./README.md) that standardizes **successful** API responses — so every endpoint, whether using `StandardModelViewSet` or a manual view, returns the same response envelope.

## Structure

```
core/
├── viewsets.py   # StandardModelViewSet
└── responses.py  # SuccessResponse
```

## How it works

Two complementary tools, for two different scenarios:

1. **`StandardModelViewSet`**
   A drop-in replacement for `viewsets.ModelViewSet`. Overrides `finalize_response` to automatically wrap `list`, `retrieve`, `create`, `update`, `partial_update`, and `destroy` responses — no need to touch each action.

2. **`SuccessResponse`**
   A `Response` subclass for manual/custom actions (e.g. `@action` methods, plain `APIView`s) where you want the same envelope but need to set your own message or data shape explicitly.

`StandardModelViewSet` checks for `'success' in response.data` before wrapping, so returning a `SuccessResponse` from inside a viewset action is safe — it won't be double-wrapped.

## Response format

```json
{
  "success": true,
  "status_code": 200,
  "message": "Data retrieved successfully.",
  "data": { "id": 1, "name": "Example" }
}
```

Paginated list responses additionally include a `pagination` block:

```json
{
  "success": true,
  "status_code": 200,
  "message": "Data retrieved successfully.",
  "data": [{ "id": 1 }, { "id": 2 }],
  "pagination": {
    "count": 42,
    "next": "http://api.example.com/items/?page=3",
    "previous": "http://api.example.com/items/?page=1"
  }
}
```

Empty responses (e.g. `204 No Content` on `DELETE`) are normalized instead of left empty:

```json
{
  "success": true,
  "status_code": 204,
  "message": "Action completed successfully.",
  "data": null
}
```

## Usage

### 1. Use the base viewset

```python
from core.viewsets import StandardModelViewSet


class ProductViewSet(StandardModelViewSet):
  queryset = Product.objects.all()
  serializer_class = ProductSerializer
```

`list`, `retrieve`, `create`, `update`, `partial_update`, and `destroy` are wrapped automatically — nothing else to do.

### 2. Use `SuccessResponse` for custom actions

```python
from core.responses import SuccessResponse


class ProductViewSet(StandardModelViewSet):
  ...

  @action(detail=True, methods=["post"])
  def archive(self, request, pk=None):
    product = self.get_object()
    product.archive()
    return SuccessResponse(
      data=ProductSerializer(product).data, message="Product archived successfully."
    )
```

### 3. Use `SuccessResponse` in plain APIViews

```python
from rest_framework.views import APIView
from core.responses import SuccessResponse


class StatsView(APIView):
  def get(self, request):
    return SuccessResponse(data={"total_users": 1024}, message="Stats retrieved.")
```

## Auto-generated messages

When a response isn't pre-wrapped, `StandardModelViewSet` picks a default message based on the HTTP method:

| Method      | Default message                |
| ----------- | ------------------------------ |
| GET         | Data retrieved successfully.   |
| POST        | Resource created successfully. |
| PUT / PATCH | Resource updated successfully. |
| DELETE      | Resource deleted successfully. |
