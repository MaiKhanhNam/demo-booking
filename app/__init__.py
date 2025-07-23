# coding: utf8

from loguru import logger

from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

from app.routes import register_routes
from config import Config

db: SQLAlchemy = SQLAlchemy()
"""SQLAlchemy instance để tương tác với database."""


def create_app() -> Flask:
    """Tạo và cấu hình ứng dụng Flask.

    Returns:
        Ứng dụng Flask đã được cấu hình

    Note:
        - Khởi tạo CORS cho API endpoints /v1/*
        - Khởi tạo kết nối database
        - Đăng ký routes
        - Cấu hình middleware
    """
    app = Flask(__name__)
    CORS(app, resources={r"/v1/*": {"origins": "*"}})
    app.config.from_object(Config)

    db.init_app(app)
    register_routes(app)

    # Đăng ký middleware hoặc các xử lý khác (nếu cần)
    @app.before_request
    def log_request() -> None:
        """Middleware ghi log trước mỗi request."""
        pass

    return app
