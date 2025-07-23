-- Tạo schema nếu chưa tồn tại
CREATE SCHEMA IF NOT EXISTS booking;

-- Tạo ENUM cho trạng thái booking
CREATE TYPE booking.booking_status AS ENUM ('new', 'contacted', 'approved', 'rejected', 'used', 'noshow', 'cancel');

-- Tạo bảng booking chính
CREATE TABLE "booking"."booking" (
  "id" serial8,
  "customer_name" varchar(100) NOT NULL,
  "phone" int8 NOT NULL,
  "booking_date" timestamptz NOT NULL,
  "status" "booking"."booking_status" DEFAULT 'new' NOT NULL,
  "note" text,
  "created_at" timestamptz DEFAULT now() NOT NULL,
  "updated_at" timestamptz,
  "is_deleted" bool DEFAULT FALSE NOT NULL,
  PRIMARY KEY ("id")
);

-- Tạo các index cần thiết
CREATE INDEX "b_status" ON "booking"."booking" ("status");
CREATE INDEX "b_booking_date" ON "booking"."booking" ("booking_date");
CREATE INDEX "b_is_deleted" ON "booking"."booking" ("is_deleted");
CREATE INDEX "b_phone" ON "booking"."booking" ("phone");
CREATE INDEX "b_customer_name" ON "booking"."booking" ("customer_name");

-- Tạo function tự động cập nhật updated_at
CREATE OR REPLACE FUNCTION update_updated_at()
RETURNS TRIGGER AS $$
BEGIN
  NEW.updated_at = now();
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Tạo trigger để cập nhật updated_at
CREATE TRIGGER set_updated_at
BEFORE UPDATE ON booking.booking
FOR EACH ROW
EXECUTE FUNCTION update_updated_at();