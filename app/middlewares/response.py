# coding: utf8

from flask import jsonify, Response
from loguru import logger
from werkzeug.exceptions import HTTPException
from functools import wraps

from app.exceptions.exception import CommonException


def format_response(f) -> callable:
    """
    Định dạng response trả về cho client.

    Args:
        f: Hàm cần được định dạng response

    Returns:
        callable: Hàm đã được wrap với xử lý response
    """
    @wraps(f)
    def decorated_function(*args, **kwargs) -> Response | tuple[Response, int]:
        """
        Hàm wrapper xử lý response.

        Args:
            *args: Tham số positional
            **kwargs: Tham số keyword

        Returns:
            Response | tuple[Response, int]: Response đã được định dạng hoặc tuple gồm response và status code

        Raises:
            CommonException: Lỗi nghiệp vụ
            HTTPException: Lỗi HTTP
            Exception: Các lỗi khác
        """
        try:
            logger.info(1)
            response = f(*args, **kwargs)

            # Nếu response đã là Response object
            if isinstance(response, Response):
                return response

            # Format success response
            if isinstance(response, tuple):
                data, status_code = response
            else:
                data, status_code = response, 200

            response_data = {
                "success": True
            }
            if data:
                response_data['data'] = data

            return jsonify(response_data), status_code

        except Exception as error:
            logger.info(2)
            # Format error response
            if isinstance(error, CommonException):
                logger.warning(f"HTTP_STATUS_CODE: {error.status_code.value} - {error.to_dict}")
                return jsonify({
                    "success": False,
                    "error": error.to_dict
                }), error.status_code.value

            if isinstance(error, HTTPException):
                return jsonify({
                    "success": False,
                    "error": {
                        "code": error.code,
                        "message": error.description
                    }
                }), error.code

            logger.exception(error)
            return jsonify({
                "success": False,
                "error": {
                    "code": 500,
                    "message": "Internal Server Error"
                }
            }), 500

    return decorated_function
