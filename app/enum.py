# coding: utf8

import enum
from abc import ABCMeta


class EnumInterface(enum.Enum):
    """Interface cơ sở cho các enum trong hệ thống.

    Methods:
        __str__() -> str: Trả về tên enum viết thường
        __repr__() -> str: Trả về chuỗi biểu diễn của enum
        argparse(s: str) -> Any: Chuyển đổi chuỗi thành giá trị enum
        has_value(value: Any) -> bool: Kiểm tra giá trị có tồn tại trong enum
    """
    __metaclass__ = ABCMeta

    # magic methods for argparse compatibility

    def __str__(self) -> str:
        """Chuyển đổi enum thành chuỗi viết thường."""
        return self.name.lower()

    def __repr__(self) -> str:
        """Biểu diễn enum dưới dạng chuỗi."""
        return str(self)

    @classmethod
    def argparse(cls, s: str):
        """Chuyển đổi chuỗi thành giá trị enum cho argparse.

        Args:
            s: Chuỗi cần chuyển đổi

        Returns:
            Giá trị enum tương ứng hoặc chuỗi gốc nếu không tìm thấy
        """
        try:
            return cls[s.upper()]
        except KeyError:
            return s

    @classmethod
    def has_value(cls, value) -> bool:
        """Kiểm tra giá trị có tồn tại trong enum.

        Args:
            value: Giá trị cần kiểm tra

        Returns:
            True nếu giá trị tồn tại, False nếu không
        """
        return value in cls._value2member_map_


class BookingStatus(EnumInterface):
    """Enum xác định tình trạng booking."""
    NEW = "new"
    CONTACTED = "contacted"
    APPROVED = "approved"
    REJECTED = "rejected"
    USED = "used"
    NOSHOW = "noshow"
    CANCEL = "cancel"


class HTTPStatusCode(EnumInterface):
    """Enum mã trạng thái HTTP."""
    CLIENT_ERROR_BAD_REQUEST = 400
    CLIENT_ERROR_UNAUTHORIZED = 401
    CLIENT_ERROR_FORBIDDEN = 403
    CLIENT_ERROR_NOT_FOUND = 404
    CLIENT_ERROR_METHOD_NOT_ALLOWED = 405
    CLIENT_ERROR_REQUEST_TIME_OUT = 408
    CLIENT_ERROR_REQUEST_CONFLICT = 409
    CLIENT_ERROR_UNPROCESSABLE_ENTITY = 422
    SERVER_ERROR_INTERNAL_SERVER_ERROR = 500
    SERVER_ERROR_BAD_GATEWAY = 502
    SERVER_ERROR_SERVICE_UNAVAILABLE = 503
    SERVER_ERROR_GATEWAY_TIMEOUT = 504
