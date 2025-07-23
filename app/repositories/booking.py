# coding: utf8

from app.models import BookingModel
from app.repositories.base import BaseRepository
from app.utils import paginate_format


class BookingRepository(BaseRepository):
    """Repository xử lý truy vấn dữ liệu cho đặt phòng.

    Class này cung cấp phương thức để lấy danh sách đặt phòng có phân trang và lọc theo các tiêu chí.

    Inheritance:
        BaseRepository: Kế thừa các phương thức cơ bản từ base repository
    """

    def __init__(self):
        super().__init__(BookingModel)

    def paginate_all(self, **kwargs) -> object:
        """Lấy danh sách đặt phòng có phân trang và lọc.

        Args:
            kwargs: Các tham số lọc và phân trang
                - customer_name (str, optional): Lọc theo tên khách hàng
                - phone (str, optional): Lọc theo số điện thoại
                - booking_from (datetime, optional): Lọc từ ngày đặt phòng
                - booking_to (datetime, optional): Lọc đến ngày đặt phòng
                - status (str, optional): Lọc theo trạng thái đặt phòng
                - created_from (datetime, optional): Lọc từ ngày tạo
                - created_to (datetime, optional): Lọc đến ngày tạo
                - page (int, optional): Trang (số) đích
                - size (int, optional): Số lượng item mỗi trang

        Returns:
            object: Đối tượng pagination đã được format thêm thông tin phân trang.
        """

        query = self.model.query.filter(
            self.model.is_deleted.is_(False)
        )

        if kwargs.get("customer_name"):
            query = query.filter(self.model.customer_name.ilike(f"%{kwargs.get('customer_name')}%"))

        if kwargs.get("phone"):
            query = query.filter(self.model.phone == kwargs.get('phone'))

        if kwargs.get("booking_from"):
            query = query.filter(self.model.booking_date >= kwargs.get('booking_from'))

        if kwargs.get("booking_to"):
            query = query.filter(self.model.booking_date <= kwargs.get('booking_to'))

        if kwargs.get("status"):
            query = query.filter(self.model.status == kwargs.get('status'))

        if kwargs.get("created_from"):
            query = query.filter(self.model.created_at >= kwargs.get('created_from'))

        if kwargs.get("created_to"):
            query = query.filter(self.model.created_at <= kwargs.get('created_to'))

        query = query.order_by(
            self.model.created_at.desc(),
            self.model.id.desc()
        ).paginate(
            page=kwargs.get("page"),
            per_page=kwargs.get("size")
        )
        return paginate_format(query)


booking_repo = BookingRepository()
