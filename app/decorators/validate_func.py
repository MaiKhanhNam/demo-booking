# coding: utf8

from loguru import logger

from datetime import datetime
from jsonschema import validate, ValidationError, FormatChecker
from functools import wraps

from app.exceptions.exception import BadRequest


def validate_func(**schema) -> callable:
    """
    Decorator kiểm tra và xác thực tham số dựa trên JSON Schema.

    Args:
        **schema: JSON Schema định nghĩa cấu trúc và ràng buộc của tham số

    Returns:
        Decorator function
    """
    # Đảm bảo schema có properties
    if schema and "properties" not in schema:
        schema["properties"] = {}

    def decorated(func):
        def validate_required(params: dict) -> None:
            """
            Kiểm tra các trường bắt buộc trong params.

            Args:
                params: Các tham số cần kiểm tra

            Raises:
                BadRequest: Nếu thiếu trường bắt buộc
            """
            for field in schema.get("required", []):
                if field not in params or not params[field]:
                    raise BadRequest(f"{get_field_name(field)} bắt buộc")

        def get_field_name(field: str) -> str:
            """
            Lấy tên cho trường từ schema nếu có.

            Args:
                field: Tên trường cần lấy

            Returns:
                Tên của trường hoặc tên trường gốc nếu không có tên của trường
            """
            try:
                if field in schema["properties"] and "name" in schema["properties"][field]:
                    return schema["properties"][field]["name"]
            except (KeyError, TypeError) as e:
                logger.debug(e)
            return field

        def validate_properties(params: dict) -> None:
            """
            Kiểm tra tính hợp lệ của các tham số dựa trên schema.

            Args:
                params: Các tham số cần kiểm tra

            Raises:
                BadRequest: Nếu tham số không hợp lệ
            """
            try:
                validate(instance=params, schema=schema, format_checker=FormatChecker())
            except ValidationError as exp:
                exp_info = list(exp.schema_path)
                error_type = ("type", "format", "pattern", "maxLength", "minLength")
                if set(exp_info).intersection(set(error_type)):
                    try:
                        field = exp_info[1]
                        field_name = get_field_name(field)
                        message = f"{field_name} không hợp lệ"
                    except IndexError:
                        message = "Dữ liệu không hợp lệ"
                else:
                    message = exp.message
                raise BadRequest(message)

        def remove_unexpected_params(params: dict) -> dict:
            """
            Loại bỏ các tham số không được định nghĩa trong schema.

            Args:
                params: Các tham số đầu vào

            Returns:
                Dict chỉ chứa các tham số hợp lệ theo schema
            """
            return {field: value for field, value in params.items() if field in schema.get("properties", {}).keys()}

        # def parse_params(params: dict) -> dict:
        #     """
        #     Chuyển đổi các tham số theo định nghĩa enum_type và list_enum_type trong schema.
        #
        #     Args:
        #         params: Các tham số cần chuyển đổi
        #
        #     Returns:
        #         Dict các tham số đã được chuyển đổi
        #
        #     Raises:
        #         BadRequest: Nếu giá trị không phù hợp với enum định nghĩa
        #     """
            # Xử lý enum_type
            # if "enum_type" in schema:
            #     for field in schema["enum_type"]:
            #         if field in params:
            #             if not schema["enum_type"][field].has_value(params[field]):
            #                 raise BadRequest(f"{get_field_name(field)} không đưa vào giá trị hợp lệ")
            #             else:
            #                 params[field] = schema["enum_type"][field](params[field])
            #
            # # Xử lý list_enum_type
            # if "list_enum_type" in schema:
            #     for field in schema["list_enum_type"]:
            #         if field in params:
            #             if not isinstance(params[field], list):
            #                 raise BadRequest(f"{get_field_name(field)} phải là danh sách giá trị hợp lệ")
            #
            #             list_field_item = params[field]
            #             params[field] = []
            #             for field_item in list_field_item:
            #                 if not schema["list_enum_type"][field].has_value(field_item):
            #                     raise BadRequest(f"{get_field_name(field)} có giá trị không hợp lệ")
            #                 else:
            #                     params[field].append(schema["list_enum_type"][field](field_item))
            # return params

        @wraps(func)
        def resource_verb(*args, **kwargs):
            """
            Wrapper function thực hiện kiểm tra và xử lý tham số theo schema.

            Args:
                *args: Các tham số vị trí của hàm gốc
                **kwargs: Các tham số từ khóa của hàm gốc

            Returns:
                Kết quả từ hàm gốc sau khi đã xử lý tham số
            """
            if not schema:
                return func(*args, **kwargs)

            # Lọc các tham số hợp lệ
            req_args = remove_unexpected_params(kwargs)

            # Kiểm tra các trường bắt buộc
            if "required" in schema:
                validate_required(req_args)

            # Kiểm tra tính hợp lệ của các tham số
            validate_properties(req_args)

            # Chuyển đổi các tham số enum
            # parsed_args = parse_params(req_args)

            # Thêm parsed_args vào args
            new_args = args + (req_args,)

            # Gọi hàm gốc với các tham số đã được xử lý
            return func(*new_args, **req_args)

        return resource_verb

    return decorated
