# coding: utf8

from app import db


class BaseModel(db.Model):
    """Model cơ sở cho tất cả các model trong hệ thống.

    Attributes:
        created_at (int): Thời điểm tạo bản ghi
        updated_at (int): Thời điểm cập nhật bản ghi gần nhất

    Methods:
        save() -> BaseModel: Lưu bản ghi vào database
        to_dict() -> dict: Chuyển đổi model thành dictionary
        __repr__() -> str: Biểu diễn model dưới dạng chuỗi
    """
    __abstract__ = True

    created_at = db.Column(db.DateTime(timezone=True), nullable=False)
    updated_at = db.Column(db.DateTime(timezone=True), nullable=True)

    def save(self):
        """Lưu model vào database.

        Returns:
            self: Instance của model đã được lưu

        Raises:
            Exception: Nếu có lỗi trong quá trình lưu
        """
        try:
            db.session.add(self)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise Exception(e)
        return self

    def to_dict(self) -> dict:
        """Chuyển đổi model thành dict.

        Returns:
            Dict chứa tất cả các trường của model
        """
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}

    def __repr__(self) -> str:
        """Biểu diễn model dưới dạng chuỗi.

        Returns:
            Chuỗi biểu diễn model với tên class và các trường
        """
        return "%s(%s)" % (
            self.__class__.__name__,
            {
                column: value
                for column, value in self.to_dict().items()
            },
        )
