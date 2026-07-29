from enum import Enum

class ErrorCode(str, Enum):
	# for business logic error codes
	INTERNAL_SERVER_ERROR = "INTERNAL_SERVER_ERROR"