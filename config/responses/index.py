from rest_framework.response import Response


class SuccessResponse(Response):
  """
  Standard success response for DRF.
  Usage: return SuccessResponse(data=my_data, message="Fetched successfully")
  """

  def __init__(self, data=None, message="Success", status=200, headers=None, **kwargs):
    # structure the data to match your error format
    formatted_data = {
      "success": True,
      "status_code": status,
      "message": message,
      "data": data,
    }

    # initialize the standard DRF Response
    super().__init__(data=formatted_data, status=status, headers=headers, **kwargs)
