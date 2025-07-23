# coding: utf8

from loguru import logger

from app.constants.globals import TIMEOUT_VALUE
from app.exceptions.exception import NotFound
from functools import wraps

from app import db


def transactional_with_lock(lock_models: list = None) -> callable:
    """
    Decorator quản lý transaction và lock bản ghi trong database.

    Args:
        lock_models: Danh sách các tuple (model, filter_func), trong đó:
            - model: SQLAlchemy model class
            - filter_func: Hàm nhận kwargs và trả về điều kiện filter

    Returns:
        wrapper: Hàm decorator đã được wrap

    Raises:
        Exception: Khi không tìm thấy bản ghi cần lock
    """
    def decorator(func: callable) -> callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            """
            Hàm wrapper cho decorator transactional_with_lock.

            Args:
                *args: Tham số positional của hàm gốc
                **kwargs: Tham số keyword của hàm gốc

            Returns:
                Kết quả từ hàm gốc

            Raises:
                Exception: Khi có lỗi trong quá trình thực thi transaction
            """
            if lock_models:
                if not isinstance(lock_models, list):
                    raise ValueError("lock_models phải là một list của các tuple (model, filter_func)")
                for model, filter_func in lock_models:
                    if not callable(filter_func):
                        raise ValueError("filter_func phải là một callable function")

            session = db.session
            locked_records = []

            try:
                # Lock các bản ghi nếu có
                if lock_models:
                    for model, filter_func in lock_models:
                        record = session.query(model).filter(
                            filter_func(kwargs),
                            model.is_deleted.is_(False)
                        ).with_for_update(nowait=True, timeout=TIMEOUT_VALUE).first()
                        if not record:
                            raise NotFound(f"Bản ghi không tồn tại hoặc đã bị xóa")
                        locked_records.append(record)

                # Gọi hàm chính
                result = func(*args, **kwargs)

                # Commit transaction
                session.commit()
                return result

            except Exception as e:
                session.rollback()
                raise e

            finally:
                session.close()

        return wrapper

    return decorator
