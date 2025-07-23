# coding: utf8

from loguru import logger

from app import db
from app.enum import BookingStatus
from app.models import BaseModel
from sqlalchemy.dialects.postgresql import ENUM, TIMESTAMP
from sqlalchemy.sql import func

booking_status_enum = ENUM(
    *[e.value for e in BookingStatus],
    name='booking_status',
    schema='booking',
    create_type=False
)


class BookingModel(BaseModel):
    """
    Model đại diện cho bảng booking trong database.
    Lưu thông tin đặt chỗ của khách hàng.
    """

    __tablename__ = 'booking'

    id = db.Column(db.BigInteger, primary_key=True)
    customer_name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.BigInteger, nullable=False)
    booking_date = db.Column(TIMESTAMP(timezone=True), nullable=False)
    status = db.Column(booking_status_enum, nullable=False, default='new')
    note = db.Column(db.String, nullable=True)
    created_at = db.Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now())
    updated_at = db.Column(TIMESTAMP(timezone=True))
    is_deleted = db.Column(db.Boolean, nullable=False, default=False)

    def __init__(self, *args, **kwargs):
        """
        Khởi tạo một đối tượng BookingModel.

        Args:
            customer_name (str): Tên khách hàng.
            phone (int): Số điện thoại đã chuẩn hóa.
            booking_date: Ngày đặt chỗ.
        """
        self.customer_name = kwargs.get("customer_name") or ""
        self.phone = kwargs.get("phone") or 0
        self.booking_date = kwargs.get("booking_date")
        self.note = kwargs.get("note") or ""
