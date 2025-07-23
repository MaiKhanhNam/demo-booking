# coding: utf8

from loguru import logger

from app import db
from app.utils import paginate_format
from app.models import BaseModel


class BaseRepository:
    """Repository cơ sở cho tất cả các repository trong hệ thống.

    Attributes:
        model: Model class được quản lý bởi repository
    """
    def __init__(self, model):
        """Khởi tạo repository với model tương ứng."""
        self.model = model

    def paginate_all(self, **kwargs) -> object:
        """Phân trang toàn bộ bản ghi.

        Args:
            **kwargs: Các tham số phân trang (page, size)

        Returns:
            object: Kết quả phân trang theo format chuẩn
        """
        entities = self.model.query.filter(
            self.model.is_deleted.is_(False)
        ).order_by(
            self.model.created_at.desc(),
            self.model.id.desc()
        ).paginate(
            page=kwargs.get("page"),
            per_page=kwargs.get("size")
        )
        return paginate_format(entities)

    def select_by_id(self, entity_id: int) -> BaseModel:
        """Lấy bản ghi theo ID.

        Args:
            entity_id: ID của bản ghi cần lấy

        Returns:
            object: Bản ghi tương ứng hoặc None nếu không tìm thấy
        """
        return self.model.query.filter(
            self.model.id == entity_id,
            self.model.is_deleted.is_(False)
        ).first()

    def insert(self, **kwargs) -> BaseModel:
        """Thêm mới bản ghi.

        Args:
            **kwargs: Các trường dữ liệu của bản ghi

        Returns:
            object: Bản ghi đã được thêm mới
        """
        entity = self.model(**kwargs)
        entity.save()
        return entity

    def update_by_id(self, entity_id: int, **kwargs) -> BaseModel:
        """Cập nhật bản ghi theo ID (yêu cầu entity đã được lock trước đó).

        Args:
            entity_id: ID của bản ghi cần cập nhật
            **kwargs: Các trường dữ liệu cần cập nhật

        Returns:
            object: Bản ghi sau khi cập nhật
        """
        entity = db.session.query(self.model).filter(self.model.id == entity_id).first()
        # Không cần kiểm tra sự tồn tại của bản ghi vì decorator đã lock và đảm bảo entity tồn tại
        for key, value in kwargs.items():
            if hasattr(entity, key):
                setattr(entity, key, value)

        logger.info(kwargs)

        db.session.flush()
        db.session.refresh(entity)
        return entity

    def delete_by_id(self, entity_id: int) -> None:
        """Xóa mềm bản ghi theo ID (yêu cầu entity đã được lock trước đó).

        Args:
            entity_id: ID của bản ghi cần xóa
        """
        entity = db.session.query(self.model).filter(self.model.id == entity_id).first()
        # Không cần kiểm tra sự tồn tại của bản ghi vì decorator đã lock và đảm bảo entity tồn tại
        entity.is_deleted = True
