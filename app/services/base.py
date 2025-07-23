# coding: utf8

from loguru import logger

from app.exceptions.exception import NotFound
from app.models import BaseModel


class BaseService:
    """Service cơ sở cho tất cả các service trong hệ thống.

    Class này cung cấp các phương thức chung về validate và xử lý giao dịch
    được sử dụng bởi các service con.
    """

    @classmethod
    def validate_entity_id(cls, repo, entity_id: int) -> BaseModel:
        """Kiểm tra sự tồn tại của entity.

        Args:
            repo: Repository của entity cần kiểm tra
            entity_id: ID của entity cần kiểm tra

        Returns:
            object: Entity tương ứng nếu tồn tại

        Raises:
            NotFound: Nếu entity không tồn tại
        """
        entity = repo.select_by_id(entity_id)
        if not entity:
            raise NotFound(f"#{entity_id} không tồn tại trên hệ thống")
        return entity
