# coding: utf8

from loguru import logger

import os


class Config:
    """Cấu hình ứng dụng Flask.

    Attributes:
        DB_TYPE (str): Loại database (ví dụ: postgresql)
        DB_DRIVER (str): Driver database (ví dụ: psycopg2)
        POSTGRES_USER (str): Tên người dùng PostgreSQL
        POSTGRES_PASS (str): Mật khẩu PostgreSQL
        POSTGRES_HOST (str): Host PostgreSQL
        POSTGRES_PORT (str): Port PostgreSQL
        POSTGRES_DBNAME (str): Tên database PostgreSQL
        POSTGRES_SCHEMA (str): Schema PostgreSQL
        SQLALCHEMY_DATABASE_URI (str): URI kết nối database
        SQLALCHEMY_TRACK_MODIFICATIONS (bool): Cờ theo dõi sửa đổi
        SQLALCHEMY_ENGINE_OPTIONS (dict): Tùy chọn engine SQLAlchemy
        SECRET_KEY (str): Khóa bí mật cho ứng dụng
        DEBUG (bool): Chế độ debug
    """
    DB_TYPE = os.environ.get("DB_TYPE", "<your-db-type>")
    DB_DRIVER = os.environ.get("DB_DRIVER", "<your-db-driver>")
    POSTGRES_USER = os.environ.get("POSTGRES_USER", "<your-postgres-user>")
    POSTGRES_PASS = os.environ.get("POSTGRES_PASS", "<your-postgres-pass>")
    POSTGRES_HOST = os.environ.get("POSTGRES_HOST", "<your-postgres-host>")
    POSTGRES_PORT = os.environ.get("POSTGRES_PORT", "<your-postgres-port>")
    POSTGRES_DBNAME = os.environ.get("POSTGRES_DBNAME", "<your-postgres-dbname>")
    POSTGRES_SCHEMA = os.environ.get("POSTGRES_SCHEMA", "<your-postgres-schema>")

    SQLALCHEMY_DATABASE_URI = (
        f"{DB_TYPE}+{DB_DRIVER}://{POSTGRES_USER}:{POSTGRES_PASS}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DBNAME}"
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        "pool_pre_ping": True,
        "pool_recycle": 280,
        "connect_args": {
            "options": f"-c search_path={POSTGRES_SCHEMA}"
        }
    }
    DEBUG = os.getenv("FLASK_ENV", "development") == "development"

    # Kafka config
    KAFKA_URL = os.environ.get("KAFKA_BROKER", "<your-kafka-url>")
    KAFKA_PORT = os.environ.get("KAFKA_BROKER", "<your-kafka-port>")
    KAFKA_BROKER = f"{KAFKA_URL}:{KAFKA_PORT}"
