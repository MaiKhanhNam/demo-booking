# 📘 Booking API Documentation

API quản lý đặt chỗ khách hàng (Booking): gồm các chức năng **tạo**, **xem**, **cập nhật**, **xoá mềm** và **tìm kiếm phân trang**.

---

## 🌐 API Base Configuration

| Thành phần       | Giá trị                    | Ghi chú                         |
| ---------------- | -------------------------- | ------------------------------- |
| **Host**         | `localhost`                | Máy chủ cục bộ                  |
| **Port**         | `5000`                     | Cổng mặc định của Flask         |
| **Prefix**       | `/v1`                      | Tiền tố cho tất cả endpoint     |
| **Full URL mẫu** | `http://localhost:5000/v1` | Gắn thêm path endpoint phía sau |

Ví dụ, endpoint lấy danh sách bookings sẽ là:

```
GET http://localhost:5000/v1/bookings
```

---

Bạn muốn mình cập nhật lại tất cả các endpoint theo cấu trúc này không?


---

## 📦 Middleware: `@format_response`

Tất cả API đều sử dụng middleware này để chuẩn hóa đầu ra.

| Field     | Type               | Description                                 |
| --------- | ------------------ | ------------------------------------------- |
| `success` | `boolean`          | `true` nếu thành công, ngược lại là `false` |
| `data`    | `object` \ `array` | Kết quả trả về (nếu có)                     |
| `error`   | `object`           | Chỉ có khi lỗi; gồm `code`, `message`       |

---

## 📂 Booking Object Format

| Field           | Type                   | Description                                 |
| --------------- | ---------------------- | ------------------------------------------- |
| `id`            | `integer`              | ID đặt chỗ                                  |
| `customer_name` | `string`               | Tên khách hàng                              |
| `phone`         | `string`               | Số điện thoại                               |
| `booking_date`  | `string` (timestamptz) | Thời gian đặt chỗ                           |
| `status`        | `string`               | Trạng thái đặt chỗ (`new`, `approved`, ...) |
| `note`          | `string or null`       | Ghi chú bổ sung                             |
| `created_at`    | `string` (timestamptz) | Ngày tạo                                    |
| `updated_at`    | `string or null`       | Ngày cập nhật gần nhất                      |

---

## 📍 1. `GET /bookings` — Lấy danh sách đặt chỗ

### 🔸 Query Parameters

| Key             | Type                 | Required  | Description                  |
| --------------- | -------------------- | --------- | ---------------------------- |
| `customer_name` | `string`               | ❌        | Lọc theo tên khách hàng      |
| `phone`         | `string`               | ❌        | Lọc theo số điện thoại       |
| `booking_from`  | `string` (timestamptz) | ❌        | Từ ngày đặt chỗ              |
| `booking_to`    | `string` (timestamptz) | ❌        | Đến ngày đặt chỗ             |
| `status`        | `string`               | ❌        | Trạng thái                   |
| `created_from`  | `string` (timestamptz) | ❌        | Ngày tạo từ                  |
| `created_to`    | `string` (timestamptz) | ❌        | Ngày tạo đến                 |
| `page`          | `integer`              | ❌        | Trang (mặc định: 1)          |
| `size`          | `integer`              | ❌        | Số dòng/trang (mặc định: 20) |

### 🔸 Response: Success

| Field              | Type      | Description                               |
| ------------------ | --------- | ----------------------------------------- |
| `data`             | `array`   | Danh sách đặt chỗ (List `Booking Object`) |
| `pagination`       | `object`  | Thông tin phân trang                      |
| └─ `current_page`  | `integer` | Trang hiện tại                            |
| └─ `has_next`      | `boolean` | Có trang sau không                        |
| └─ `has_previous`  | `boolean` | Có trang trước không                      |
| └─ `next_page`     | `integer` | Trang tiếp theo                           |
| └─ `previous_page` | `integer` | Trang trước đó                            |
| └─ `total`         | `integer` | Tổng số bản ghi                           |
| └─ `per_page`      | `integer` | Kích thước trang                          |
| └─ `total_pages`   | `integer` | Tổng số trang                             |

---

## 📍 2. `POST /bookings` — Tạo đặt chỗ mới

### 🔸 Request Body

| Key             | Type                   | Required | Description      |
| --------------- | ---------------------- | -------- | ---------------- |
| `customer_name` | `string`               | ✅       | Tên khách hàng   |
| `phone`         | `integer`              | ✅       | Số điện thoại    |
| `booking_date`  | `string` (timestamptz) | ✅       | Ngày giờ đặt chỗ |
| `note`          | `string`               | ❌       | Ghi chú          |

### 🔸 Response: `Booking object` như định nghĩa ở trên

---

## 📍 3. `GET /bookings/<booking_id>` — Lấy chi tiết

### 🔸 URL Path

| Key          | Type      | Required | Description                 |
| ------------ | --------- | -------- | --------------------------- |
| `booking_id` | `integer` | ✅       | ID của bản ghi cần truy vấn |

### 🔸 Response: `Booking object`

---

## 📍 4. `PUT /bookings/<booking_id>` — Cập nhật đặt chỗ

### 🔸 URL Path

| Key          | Type      | Required | Description                 |
| ------------ | -------   | -------- | --------------------------- |
| `booking_id` | `integer` | ✅       | ID của bản ghi cần cập nhật |

### 🔸 Request Body (các trường tùy chọn)

| Key             | Type                   | Required | Description          |
| --------------- | ---------------------- | -------- | -------------------- |
| `customer_name` | `string`               | ❌       | Tên khách hàng mới   |
| `phone`         | `integer`              | ❌       | Số điện thoại mới    |
| `booking_date`  | `string` (timestamptz) | ❌       | Ngày giờ đặt chỗ mới |
| `status`        | `string`               | ❌       | Trạng thái mới       |
| `note`          | `string`               | ❌       | Ghi chú mới          |

### 🔸 Response: `Booking object` sau cập nhật

---

## 📍 5. `DELETE /bookings/<booking_id>` — Xoá mềm đặt chỗ

### 🔸 URL Path

| Key          | Type      | Required | Description            |
| ------------ | --------- | -------- | ---------------------- |
| `booking_id` | `integer` | ✅       | ID của bản ghi cần xoá |

### 🔸 Response

| Field     | Type      | Description               |
| --------- | --------- | ------------------------- |
| `success` | `boolean` | `true` nếu xoá thành công |

---

## 📌 Ghi chú

* Tất cả các trường `string` (timestamptz) phải sử dụng định dạng ISO 8601 có timezone (timestamptz), ví dụ: `YYYY-MM-DDTHH:mm:ss+07:00`.
* Xoá mềm = chỉ cập nhật cờ `is_deleted`, không xoá vật lý

---

## 📍 6. `GET /reports/summary` — Tổng hợp số lượng đặt chỗ theo ngày

### 🔸 Request

| Key | Type | Required | Description               |
| --- | ---- | -------- | ------------------------- |
| –   | –    | –        | Không có request payload. |

### 🔸 Response

| Key       | Type      | Description                         |
| --------- | --------- | ----------------------------------- |
| `success` | `boolean` | Trạng thái phản hồi (`true` nếu OK) |
| `data`    | `object`  | Dict `{ngày: số lượng đặt chỗ}`  |

#### 📄 Chi tiết `data`:

| Key (`ngày`) | Type      | Description                        |
| ------------ | --------- | ---------------------------------- |
| `DD/MM/YYYY` | `integer` | Số lượng đơn đặt chỗ trong ngày đó |

### 📝 Ghi chú

* Các key trong `data` là chuỗi ngày, định dạng `ngày/tháng/năm` (`DD/MM/YYYY`).
