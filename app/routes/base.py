# coding: utf8

class BaseRoute:
    """Route cơ sở cho tất cả các route trong hệ thống.

    Class này định nghĩa cấu trúc cơ bản cho các route, yêu cầu các class con
    phải implement phương thức register_routes().

    Attributes:
        blueprint (Blueprint): Flask Blueprint được sử dụng cho route
    """

    def __init__(self, blueprint):
        """Khởi tạo route với blueprint tương ứng.

        Args:
            blueprint (Blueprint): Flask Blueprint được sử dụng cho route
        """
        self.blueprint = blueprint

    def register_routes(self):
        """Đăng ký các routes cho blueprint.

        Method này cần được implement bởi các class con.
        Mỗi class con sẽ định nghĩa các routes cụ thể của mình.

        Raises:
            NotImplementedError: Khi method không được implement bởi class con
        """
        raise NotImplementedError("Subclasses must implement register_routes")
