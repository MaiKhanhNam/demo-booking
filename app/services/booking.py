# coding: utf8

from loguru import logger

from app.constants.globals import KAFKA_BOOKING_TOPIC
from app.decorators import validate_func, transactional_with_lock
from app.enum import BookingStatus
from app.models import BookingModel
from app.repositories import booking_repo
from app.services.base import BaseService
from app.utils import kafka_producer


class BookingService(BaseService):
    """Service xử lý logic nghiệp vụ cho quản lý booking.

    Class này cung cấp các phương thức để:
    - CRUD thông tin booking (tạo, đọc, cập nhật, xóa)

    Inheritance:
        BaseService: Kế thừa các phương thức cơ bản từ base service
    """

    @classmethod
    @validate_func(
        **{
            "type": "object",
            "properties": {
                "customer_name": {"type": "string"},
                "phone": {"type": "integer"},
                "booking_from": {"type": "string", "format": "date-time"},
                "booking_to": {"type": "string", "format": "date-time"},
                "status": {"type": "string"},
                "created_from": {"type": "string", "format": "date-time"},
                "created_to": {"type": "string", "format": "date-time"},
                "page": {"type": "integer"},
                "size": {"type": "integer"},
            },
            "enum_type": {
                "status": BookingStatus
            }
        }
    )
    def paginate_booking(cls, args, **kwargs) -> dict:
        """Lấy danh sách booking có phân trang.

        Args:
            args: Schema validation args
            kwargs: Tham số lọc và phân trang
                customer_name (str, optional): Lọc theo tên khách hàng
                phone (int, optional): Lọc theo số điện thoại
                booking_from (string, optional): Lọc theo ngày đặt từ
                booking_to (string, optional): Lọc theo ngay đặt đến
                status (str, optional): Lọc theo tình trạng booking
                created_from (string, optional): Lọc theo ngày tạo từ
                created_to (string, optional): Lọc theo ngày tạo đến
                page (int, optional): Trang (số) đích
                size (int, optional): Số lượng trên một trang

        Returns:
            dict: Kết quả phân trang
        """
        list_booking = booking_repo.paginate_all(**kwargs)

        response_data = []
        for booking in list_booking.items:
            response_data.append(cls._format_booking_response(booking))

        return {
            "data": response_data,
            "pagination": {
                "has_next": list_booking.has_next,
                "has_previous": list_booking.has_previous,
                "next_page": list_booking.next_page,
                "previous_page": list_booking.previous_page,
                "current_page": list_booking.page,
                "total_pages": list_booking.pages,
                "per_page": list_booking.per_page,
                "total": list_booking.total
            }
        }

    @classmethod
    @validate_func(
        **{
            "type": "object",
            "properties": {
                "customer_name": {"type": "string"},
                "phone": {"type": "integer"},
                "booking_date": {"type": "string", "format": "date-time"},
                "note": {"type": "string"}
            },
            "required": ["customer_name", "phone", "booking_date"]
        }
    )
    def create_booking(cls, args, **kwargs) -> dict:
        """Tạo mới booking.

        Args:
            args: Schema validation args
            kwargs: Thông tin booking cần tạo
                customer_name (str): Tên khách hàng
                phone (int): Số điện thoại
                booking_date (string): Ngày đặt

        Returns:
            dict: Thông tin booking đã tạo
        """

        booking = booking_repo.insert(**kwargs)

        # Gửi thông báo qua Kafka sau khi tạo booking thành công
        kafka_producer.send(
            topic=KAFKA_BOOKING_TOPIC,
            key=str(booking.id),
            value={
                "event": "booking_created",
                "booking_id": booking.id
            }
        )

        return cls._format_booking_response(booking)

    @classmethod
    def get_booking(cls, booking_id: int) -> dict:
        """Lấy thông tin chi tiết của một booking.

        Args:
            booking_id (int): ID của booking cần lấy thông tin

        Returns:
            dict: Thông tin chi tiết của booking

        Raises:
            NotFound: Khi booking không tồn tại hoặc đã bị xóa
        """
        booking = cls.validate_entity_id(booking_repo, booking_id)
        return cls._format_booking_response(booking)

    @classmethod
    @transactional_with_lock(
        lock_models=[
            (BookingModel, lambda kwargs: BookingModel.id == kwargs.get("booking_id"))
        ]
    )
    @validate_func(
        **{
            "type": "object",
            "properties": {
                "booking_id": {"type": "integer"},
                "customer_name": {"type": "string"},
                "phone": {"type": "integer"},
                "booking_date": {"type": "string", "format": "date-time"},
                "note": {"type": "string"},
                "status": {"type": "string"}
            },
            "required": ["booking_id"],
            "enum_type": {
                "status": BookingStatus
            }
        }
    )
    def update_booking(cls, args, **kwargs) -> dict:
        """Cập nhật thông tin booking.

        Args:
            args: Schema validation args
            kwargs: Thông tin cập nhật
                booking_id (int): ID booking cần cập nhật
                customer_name (str, optional): Tên khách hàng mới
                phone (int, optional): Số điện thoại mới
                booking_date (string, optional): Ngày đặt mới
                status (int, optional): Tình trạng booking mới

        Returns:
            dict: Thông tin booking sau khi cập nhật

        Raises:
            NotFound: Khi booking cần cập nhật không tồn tại hoặc đã bị xóa
        """
        booking = booking_repo.update_by_id(kwargs.get("booking_id"), **kwargs)

        return cls._format_booking_response(booking)

    @classmethod
    @transactional_with_lock(
        lock_models=[
            (BookingModel, lambda kwargs: BookingModel.id == kwargs.get("booking_id"))
        ]
    )
    @validate_func(
        **{
            "type": "object",
            "properties": {
                "booking_id": {"type": "integer"}
            },
            "required": ["booking_id"]
        }
    )
    def delete_booking(cls, args, **kwargs) -> None:
        """Xóa booking.

        Args:
            args: Schema validation args
            kwargs: Thông tin
                booking_id: ID booking cần xóa

        Raises:
            NotFound: Khi booking cần cập nhật không tồn tại hoặc đã bị xóa
        """
        booking_repo.delete_by_id(kwargs.get("booking_id"))

    @classmethod
    def _format_booking_response(cls, booking) -> dict:
        """Định dạng dữ liệu response cho bản ghi booking.

        Args:
            booking (bookingModel): Booking entity

        Returns:
            dict: Formatted response data
        """
        return {
            "id": booking.id,
            "customer_name": booking.customer_name,
            "phone": booking.phone,
            "booking_date": booking.booking_date.isoformat(),
            "status": booking.status,
            "note": booking.note,
            "created_at": booking.created_at.isoformat(),
            "updated_at": booking.updated_at.isoformat() if booking.updated_at else None,
        }
