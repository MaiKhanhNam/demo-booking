# coding: utf8

from app.enum import HTTPStatusCode


class CommonException(Exception):
    """Lớp exception cơ sở cho các lỗi HTTP.

    Attributes:
        status_code: Mã trạng thái HTTP
        message: Thông báo lỗi mặc định
    """
    status_code = HTTPStatusCode.SERVER_ERROR_INTERNAL_SERVER_ERROR
    message = "Internal Server Error"

    def __init__(self, message: str = None):
        """Khởi tạo exception với thông báo tùy chỉnh.

        Args:
            message: Thông báo lỗi tùy chỉnh để ghi đè mặc định
        """
        self.message = message or self.__class__.message

    @property
    def to_dict(self) -> dict:
        """Chuyển đổi exception thành định dạng dict.

        Returns:
            dict: Dict chứa thông báo lỗi và mã lỗi
        """
        return {
            "message": self.message,
            "code": self.status_code.value if isinstance(self.status_code, HTTPStatusCode) else self.status_code,
        }


class BadRequest(CommonException):
    """Lỗi Bad Request (400)."""
    status_code = HTTPStatusCode.CLIENT_ERROR_BAD_REQUEST
    message = "Bad Request"


class Unauthorized(CommonException):
    """Lỗi Unauthorized (401)."""
    status_code = HTTPStatusCode.CLIENT_ERROR_UNAUTHORIZED
    message = "Unauthorized"


class Forbidden(CommonException):
    """Lỗi Forbidden (403)."""
    status_code = HTTPStatusCode.CLIENT_ERROR_FORBIDDEN
    message = "Forbidden"


class NotFound(CommonException):
    """Lỗi Not Found (404)."""
    status_code = HTTPStatusCode.CLIENT_ERROR_NOT_FOUND
    message = "Not Found"


class MethodNotAllowed(CommonException):
    """Lỗi Method Not Allowed (405)."""
    status_code = HTTPStatusCode.CLIENT_ERROR_METHOD_NOT_ALLOWED
    message = "Method Not Allowed"


class RequestTimeOut(CommonException):
    """Lỗi Request Timeout (408)."""
    status_code = HTTPStatusCode.CLIENT_ERROR_REQUEST_TIME_OUT
    message = "Request Time Out"


class RequestConflict(CommonException):
    """Lỗi Request Conflict (409)."""
    status_code = HTTPStatusCode.CLIENT_ERROR_REQUEST_CONFLICT
    message = "Request Conflict"


class UnprocessableEntity(CommonException):
    """Lỗi Unprocessable Entity (422)."""
    status_code = HTTPStatusCode.CLIENT_ERROR_UNPROCESSABLE_ENTITY
    message = "Unprocessable Entity"


class InternalServerError(CommonException):
    """Lỗi Internal Server Error (500)."""
    status_code = HTTPStatusCode.SERVER_ERROR_INTERNAL_SERVER_ERROR
    message = "Internal Server Error"
