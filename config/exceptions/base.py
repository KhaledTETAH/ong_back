from rest_framework.exceptions import APIException
from rest_framework.status import HTTP_400_BAD_REQUEST
from .codes import ErrorCode

class BaseAPIException(APIException):
	status_code = HTTP_400_BAD_REQUEST
	default_code = ErrorCode.INTERNAL_SERVER_ERROR
	default_detail = "An unexpected error occurred."

	def __init__(self, detail=None, code=None, extra_data=None):
		self.detail = detail or self.default_detail
		self.code = code or self.default_code
		self.extra_data = extra_data or {}
		super().__init__(detail=self.detail, code=self.code)