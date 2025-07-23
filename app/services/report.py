# coding: utf8

from loguru import logger

from app.repositories import booking_repo
from app.services.base import BaseService


class ReportService(BaseService):
    """Service xử lý logic nghiệp vụ cho báo cáo số lượng booking.

    Class này cung cấp các phương thức để:
    - Lấy số lượng booking theo ngày

    Inheritance:
        BaseService: Kế thừa các phương thức cơ bản từ base service
    """

    @classmethod
    def summary_by_date(cls) -> dict:
        """Lấy số lượng booking theo ngày.

        Returns:
            dict: Kết quả tổng hợp số lượng booking theo ngày
        """
        list_booking = booking_repo.count_by_booking_date()

        return {r.booking_date: r.total for r in list_booking}
