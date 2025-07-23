# coding: utf8

from loguru import logger

from flask import Blueprint

from app.middlewares import format_response
from app.services import ReportService
from app.routes.base import BaseRoute
from app.utils import remove_none_in_dict

"""Routes báo cáo thông tin đặt chỗ.

Module này cung cấp các endpoint API để báo cáo thông tin đặt chỗ bao gồm:
- Tổng hợp số lượng đặt chỗ theo ngày (GET /summary) -> dict
"""

report_bp = Blueprint("reports", __name__)


class ReportRoute(BaseRoute):
    """Xử lý các routes báo cáo thông tin đặt chỗ.

    Định nghĩa các endpoint API cho việc báo cáo thông tin đặt chỗ, kế thừa từ BaseRoute.
    """

    def __init__(self):
        super().__init__(report_bp)

    def register_routes(self) -> None:
        """Đăng ký tất cả các routes báo cáo thông tin đặt chỗ với blueprint.

        Maps các URL endpoint tới các phương thức xử lý tương ứng.
        """
        routes = [
            ("/summary", "router_report_summary", self._report_summary, ["GET"]),
        ]

        for path, endpoint, view_func, methods in routes:
            self.blueprint.add_url_rule(path, endpoint, view_func=view_func, methods=methods)

    @format_response
    def _report_summary(self) -> dict:
        """Tổng hợp số lượng đặt chỗ theo ngày

        Output:
            dict: Danh sách tổng các đặt chỗ theo ngày
        """
        return ReportService.summary_by_date()


ReportRoute().register_routes()
