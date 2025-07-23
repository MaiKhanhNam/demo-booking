# coding: utf8

from loguru import logger

from flask import Blueprint

from app.constants.globals import DEFAULT_PAGE_NUMBER, DEFAULT_PAGE_LIMIT
from app.decorators import validate_request
from app.middlewares import format_response
from app.services import BookingService
from app.routes.base import BaseRoute
from app.utils import remove_none_in_dict

"""Routes quản lý đặt chỗ.

Module này cung cấp các endpoint API để quản lý đặt chỗ bao gồm:
- Phân trang và tìm kiếm đặt chỗ (GET /) -> dict
- Tạo đặt chỗ mới (POST /) -> dict
- Xem chi tiết đặt chỗ (GET /<id>) -> dict
- Cập nhật thông tin đặt chỗ (PUT /<id>) -> dict
- Xóa (xóa mềm) đặt chỗ (POST /delete/<id>) -> None

Tính hợp lệ của request được xử lý bởi decorator validate_request sử dụng các schema đã định nghĩa.
"""

booking_bp = Blueprint("bookings", __name__)


class BookingRoute(BaseRoute):
    """Xử lý các routes đặt chỗ.

    Định nghĩa các endpoint API cho việc quản lý đặt chỗ, kế thừa từ BaseRoute.
    Sử dụng các schema để kiểm tra tính hợp lệ của request.

    Schemas:
        PAGINATE_SCHEMA: Tham số phân trang và lọc
        CREATE_SCHEMA: Các trường bắt buộc để tạo đặt chỗ
        UPDATE_SCHEMA: Các trường tùy chọn để cập nhật đặt chỗ
    """

    # Schemas
    PAGINATE_SCHEMA = {
        "customer_name": {"type": str, "required": False, "location": "value"},
        "phone": {"type": str, "required": False, "location": "value"},
        "booking_from": {"type": str, "required": False, "location": "value"},
        "booking_to": {"type": str, "required": False, "location": "value"},
        "status": {"type": str, "required": False, "location": "value"},
        "created_from": {"type": str, "required": False, "location": "value"},
        "created_to": {"type": str, "required": False, "location": "value"},
        "page": {"type": int, "required": False, "location": "value", "default": DEFAULT_PAGE_NUMBER},
        "size": {"type": int, "required": False, "location": "value", "default": DEFAULT_PAGE_LIMIT},
    }
    CREATE_SCHEMA = {
        "customer_name": {"type": str, "required": True, "location": "json"},
        "phone": {"type": int, "required": True, "location": "json"},
        "booking_date": {"type": str, "required": True, "location": "json"},
        "note": {"type": str, "required": False, "location": "json"}
    }
    UPDATE_SCHEMA = {
        "customer_name": {"type": str, "required": False, "location": "json"},
        "phone": {"type": int, "required": False, "location": "json"},
        "booking_date": {"type": str, "required": False, "location": "json"},
        "note": {"type": str, "required": False, "location": "json"},
        "status": {"type": str, "required": False, "location": "json"}
    }

    def __init__(self):
        super().__init__(booking_bp)

    def register_routes(self) -> None:
        """Đăng ký tất cả các routes đặt chỗ với blueprint.

        Maps các URL endpoint tới các phương thức xử lý tương ứng.
        Tất cả routes đều được bảo vệ bởi xác thực và kiểm tra quyền hạn.
        """
        routes = [
            ("", "router_paginate_booking", self._paginate_booking, ["GET"]),
            ("", "router_create_booking", self._create_booking, ["POST"]),
            ("/<int:booking_id>", "router_get_booking", self._get_booking, ["GET"]),
            ("/<int:booking_id>", "router_update_booking", self._update_booking, ["PUT"]),
            ("/<int:booking_id>", "router_delete_booking", self._delete_booking, ["DELETE"]),
        ]

        for path, endpoint, view_func, methods in routes:
            self.blueprint.add_url_rule(path, endpoint, view_func=view_func, methods=methods)

    @format_response
    @validate_request(PAGINATE_SCHEMA)
    def _paginate_booking(self, **kwargs) -> dict:
        """Lấy danh sách đặt chỗ theo phân trang và bộ lọc.

        Args:
            **kwargs: Các tham số lọc:
                - customer_name (str, optional): Lọc theo tên khách hàng
                - phone (str, optional): Lọc theo số điện thoại
                - booking_from (datetime, optional): Thời gian đặt chỗ (từ)
                - booking_to (datetime, optional): Thời gian đặt chỗ (đến)
                - status (str, optional): Trạng thái đặt chỗ
                - created_from (datetime, optional): Thời gian tạo (từ)
                - created_to (datetime, optional): Thời gian tạo (đến)
                - page (int, optional): Trang (số) đích
                - size (int, optional): Số lượng trên một trang

        Output:
            dict: {
                data (list): Danh sách các đặt chỗ
                pagination (dict): Thông tin phân trang
            }
        """
        return BookingService.paginate_booking(**remove_none_in_dict(kwargs))

    @format_response
    @validate_request(CREATE_SCHEMA)
    def _create_booking(self, **kwargs) -> dict:
        """Tạo đặt chỗ mới.

        Args:
            **kwargs: Thông tin đặt chỗ:
                - customer_name (str): Tên khách hàng
                - phone (str): Số điện thoại
                - booking_date (datetime): Thời gian đặt chỗ

        Returns:
            dict: Thông tin đặt chỗ vừa tạo
        """
        return BookingService.create_booking(**remove_none_in_dict(kwargs))

    @format_response
    def _get_booking(self, booking_id: int) -> dict:
        """Lấy chi tiết thông tin đặt chỗ theo ID.

        Args:
            booking_id (int): ID của đặt chỗ cần lấy thông tin

        Returns:
            dict: Chi tiết thông tin đặt chỗ
        """
        return BookingService.get_booking(booking_id)

    @format_response
    @validate_request(UPDATE_SCHEMA)
    def _update_booking(self, booking_id: int, **kwargs) -> dict:
        """Cập nhật thông tin đặt chỗ theo ID.

        Args:
            booking_id (int): ID đặt chỗ cần cập nhật
            **kwargs: Các trường cần cập nhật:
                - customer_name (str, optional): Tên khách hàng mới
                - phone (str, optional): Số điện thoại mới
                - booking_date (datetime, optional): Thời gian đặt chỗ mới
                - status (str, optional): Trạng thái mới

        Returns:
            dict: Thông tin đặt chỗ sau khi cập nhật
        """
        kwargs["booking_id"] = booking_id
        return BookingService.update_booking(**remove_none_in_dict(kwargs))

    @format_response
    def _delete_booking(self, booking_id: int) -> None:
        """Xóa (xóa mềm) đặt chỗ theo ID.

        Args:
            booking_id (int): ID đặt chỗ cần xóa
        """
        return BookingService.delete_booking(**{"booking_id": booking_id})


BookingRoute().register_routes()
