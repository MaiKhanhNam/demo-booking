# coding: utf8

from loguru import logger

from functools import wraps
from flask import request

from app.exceptions.exception import BadRequest

import json


def is_empty(value, value_type: type) -> bool:
    """Kiểm tra giá trị có rỗng hay không.

    Args:
        value: Giá trị cần kiểm tra
        value_type: Kiểu dữ liệu của giá trị

    Returns:
        bool: True nếu giá trị rỗng, False nếu không
    """
    if value_type == list:
        return value == []
    if value_type == dict:
        return value == {}
    return value in [None, "", 0]


def parse_boolean(value, param_name: str, param_required: bool, param_default) -> bool:
    """Parse giá trị boolean từ request.

    Args:
        value: Giá trị cần parse
        param_name: Tên tham số
        param_required: Có bắt buộc hay không
        param_default: Giá trị mặc định

    Returns:
        bool: Giá trị boolean đã parse

    Raises:
        BadRequest: Nếu giá trị không hợp lệ
    """
    if value in [None, ""]:
        if param_required:
            raise BadRequest(f"Trường {param_name} bắt buộc")
        return param_default

    if str(value).lower() in ["true", "1", "yes"]:
        return True
    if str(value).lower() in ["false", "0", "no"]:
        return False
    raise BadRequest(f"Trường {param_name} không hợp lệ")


def parse_collection(value, param_name: str, param_type: type) -> list | dict:
    """Parse giá trị collection (list/dict) từ request.

    Args:
        value: Giá trị cần parse
        param_name: Tên tham số
        param_type: Kiểu dữ liệu mong muốn (list/dict)

    Returns:
        list hoặc dict: Collection đã parse

    Raises:
        BadRequest: Nếu giá trị không hợp lệ
    """
    try:
        if isinstance(value, str):
            value = json.loads(value)
        if not isinstance(value, param_type):
            raise BadRequest(f"Trường {param_name} không hợp lệ")
        return value
    except json.JSONDecodeError:
        raise BadRequest(f"Trường {param_name} không hợp lệ")


def validate_bounds(value, param_name: str, param_type: type, min_value, max_value) -> None:
    """Kiểm tra giới hạn của giá trị.

    Args:
        value: Giá trị cần kiểm tra
        param_name: Tên tham số
        param_type: Kiểu dữ liệu
        min_value: Giá trị tối thiểu
        max_value: Giá trị tối đa

    Raises:
        BadRequest: Nếu giá trị nằm ngoài giới hạn
    """
    if param_type in [str, list, dict]:
        if min_value is not None and len(value) < min_value:
            raise BadRequest(f"Độ dài của {param_name} phải lớn hơn {min_value}")
        if max_value is not None and len(value) > max_value:
            raise BadRequest(f"Độ dài của {param_name} phải nhỏ hơn {max_value}")
    elif param_type in [int, float]:
        if min_value is not None and value < min_value:
            raise BadRequest(f"Giá trị tối thiểu của {param_name} phải lớn hơn {min_value}")
        if max_value is not None and value > max_value:
            raise BadRequest(f"Giá trị tối đa của {param_name} phải nhỏ hơn {max_value}")


def parse_number(value, param_name: str, param_type: type) -> int | float:
    """Parse giá trị số từ request.

    Args:
        value: Giá trị cần parse
        param_name: Tên tham số
        param_type: Kiểu số mong muốn (int/float)

    Returns:
        int hoặc float: Giá trị số đã parse

    Raises:
        BadRequest: Nếu giá trị không hợp lệ
    """
    if not value:
        return value
    try:
        return param_type(value)
    except Exception:
        raise BadRequest(f"Trường {param_name} không hợp lệ")


def log_request(url: str, data: dict) -> None:
    """Log thông tin request.

    Args:
        url: URL của request
        data: Dữ liệu request
    """
    logger.info("- Start log ----------------------------------------------------")
    logger.info("Request URL:")
    logger.info(url)
    logger.info("Request data:")
    logger.info(data)
    logger.info("- End log ------------------------------------------------------")


def validate_request(params: dict) -> callable:
    """Decorator validate request parameters.

    Args:
        params: Dictionary chứa thông tin validate cho từng tham số.
               Mỗi tham số có thể có các thuộc tính:
               - type: Kiểu dữ liệu (mặc định: str)
               - required: Có bắt buộc không (mặc định: False)
               - default: Giá trị mặc định (mặc định: None)
               - location: Vị trí lấy giá trị (json/value, mặc định: json)
               - min: Giá trị tối thiểu
               - max: Giá trị tối đa

    Returns:
        function: Decorated function
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            validated_data = {}

            for param_name, param_attrs in params.items():
                param_type = param_attrs.get("type", str)
                param_required = param_attrs.get("required", False)
                param_default = param_attrs.get("default", None)
                param_location = param_attrs.get("location", "json")
                min_value = param_attrs.get("min", None)
                max_value = param_attrs.get("max", None)

                # Get param value
                if param_location == "json":
                    param_value = request.json.get(param_name) if request.is_json else None
                elif param_location == "value":
                    param_value = request.args.get(param_name)
                else:
                    param_value = None

                # Handle boolean
                if param_type == bool:
                    param_value = parse_boolean(param_value, param_name, param_required, param_default)

                # Check empty
                if is_empty(param_value, param_type):
                    if param_required:
                        raise BadRequest(f"Trường {param_name} bắt buộc")
                    param_value = param_default

                # Parse collections
                if param_type in [list, dict]:
                    param_value = parse_collection(param_value, param_name, param_type)

                # Validate bounds
                if param_value not in [None, 0, "", [], {}]:
                    validate_bounds(param_value, param_name, param_type, min_value, max_value)

                # Parse numbers
                if param_type in [int, float]:
                    param_value = parse_number(param_value, param_name, param_type)
                # Parse other types
                elif param_type != bool:
                    try:
                        param_value = param_type(param_value) if param_value is not None else None
                    except (ValueError, TypeError):
                        raise BadRequest(f"Trường {param_name} không hợp lệ")

                if param_value not in [None, 0, "", [], {}]:
                    validated_data[param_name] = param_value

            kwargs.update(validated_data)
            log_request(request.url, kwargs)
            return func(*args, **kwargs)
        return wrapper
    return decorator
