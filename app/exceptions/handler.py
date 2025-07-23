# coding: utf8

from flask import jsonify
from loguru import logger
from werkzeug.exceptions import HTTPException

from .exception import CommonException


def api_error_handler(error):
    if isinstance(error, CommonException):
        logger.warning(f"HTTP_STATUS_CODE: {error.status_code.value} - {error.to_dict}")
        return jsonify(error.to_dict), error.status_code.value

    if isinstance(error, HTTPException):
        return (
            jsonify({"success": False, "error": {"code": error.code, "message": error.description}}),
            error.code,
        )

    logger.exception(error)
    return jsonify({"success": False, "error": {"code": 500, "message": "Internal Server Error"}}), 500
