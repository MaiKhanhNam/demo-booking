# coding: utf8

from loguru import logger

import random
import string


def paginate_format(pagination) -> object:
    """
    Format đối tượng pagination với các thông tin bổ sung.

    Args:
        pagination: Đối tượng pagination cần format

    Returns:
        pagination: Đối tượng pagination đã được format thêm thông tin pages,
                   has_previous, has_next, next_page, previous_page
    """
    pagination.__dict__["pages"] = int(pagination.total / pagination.per_page) + (
        1 if pagination.total % pagination.per_page > 0 else 0
    )
    pagination.__dict__["has_previous"] = pagination.page > 1
    pagination.__dict__["has_next"] = pagination.page < pagination.pages
    pagination.__dict__["next_page"] = pagination.page + 1 if pagination.has_next else None
    pagination.__dict__["previous_page"] = pagination.page - 1 if pagination.has_previous else None
    return pagination


def remove_none_in_dict(data: dict) -> dict:
    """
    Loại bỏ các cặp key-value có value là None trong dict.

    Args:
        data: Dictionary cần xử lý

    Returns:
        dict: Dictionary mới đã loại bỏ các giá trị None
    """
    return {key: value for key, value in data.items() if value is not None}
