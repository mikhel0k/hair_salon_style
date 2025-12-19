from datetime import date, time, timedelta

import pytest
from pydantic import ValidationError

from app.schemas import RecordCreate
from app.schemas.Record import ALLOWED_STATUSES


class TestRecordCreate:
    def test_record_create_with_all_field(self):
        data = {
            "date": date.today(),
            "time": time(14, 30),
            "status": "created",
            "price": 300,
            "notes": "I want drink beer",
            "user_id": 1
        }
        record = RecordCreate(**data)
        assert record.date == data["date"]
        assert record.time == data["time"]
        assert record.status == data["status"]
        assert record.price == data["price"]
        assert record.notes == data["notes"]
        assert record.user_id == data["user_id"]

    def test_record_create_with_only_non_optional_fields(self):
        data = {
            "date": date.today(),
            "time": time(14, 30),
            "user_id": 1
        }
        record = RecordCreate(**data)
        assert record.date == data["date"]
        assert record.time == data["time"]
        assert record.user_id == data["user_id"]
        assert record.price is None
        assert record.status is None
        assert record.notes is None

    def test_record_create_with_only_none_in_price(self):
        data = {
            "date": date.today(),
            "time": time(14, 30),
            "user_id": 1,
            "price": None,
        }
        record = RecordCreate(**data)
        assert record.date == data["date"]
        assert record.time == data["time"]
        assert record.user_id == data["user_id"]
        assert record.price is None
        assert record.status is None
        assert record.notes is None

    def test_record_create_yesterday(self):
        data = {
            "date": date.today() - timedelta(1),
            "time": time(14, 30),
            "user_id": 1
        }
        with pytest.raises(ValidationError) as exc_info:
            record = RecordCreate(**data)
        assert "Date must be in the future" in str(exc_info.value)

    def test_record_create_without_date(self):
        data = {
            "time": time(14, 30),
            "user_id": 1
        }
        with pytest.raises(ValidationError) as exc_info:
            record = RecordCreate(**data)
        assert any(error["type"] == "missing" for error in exc_info.value.errors())

    def test_record_create_without_time(self):
        data = {
            "date": date.today(),
            "user_id": 1
        }
        with pytest.raises(ValidationError) as exc_info:
            record = RecordCreate(**data)
        assert any(error["type"] == "missing" for error in exc_info.value.errors())

    def test_record_create_without_user_id(self):
        data = {
            "date": date.today(),
            "time": time(14, 30),
        }
        with pytest.raises(ValidationError) as exc_info:
            record = RecordCreate(**data)
        assert any(error["type"] == "missing" for error in exc_info.value.errors())

    def test_record_create_with_wrong_status(self):
        data = {
            "date": date.today(),
            "time": time(14, 30),
            "status": "maked",
            "user_id": 1
        }
        with pytest.raises(ValidationError) as exc_info:
            record = RecordCreate(**data)
        assert len(exc_info.value.errors()) == 1
        assert exc_info.value.errors()[0]["type"] == "value_error"
        assert "Status must be one of ['created', 'confirmed', 'rejected', 'cancelled']" in str(exc_info.value)

    def test_record_create_with_all_statuses(self):
        for status in ALLOWED_STATUSES:
            data = {
                "date": date.today(),
                "time": time(14, 30),
                "status": status,
                "user_id": 1
            }
            record = RecordCreate(**data)
            assert record.date == data["date"]
            assert record.time == data["time"]
            assert record.status == data["status"]
            assert record.user_id == data["user_id"]
            assert record.price is None
            assert record.notes is None

    def test_record_create_with_negative_price(self):
        data = {
            "date": date.today(),
            "time": time(14, 30),
            "user_id": 1,
            "price": -100,
        }
        with pytest.raises(ValidationError) as exc_info:
            record = RecordCreate(**data)
        assert len(exc_info.value.errors()) == 1
        assert exc_info.value.errors()[0]["type"] == "value_error"
        assert "Price must be greater or equal than 0" in str(exc_info.value)

    def test_record_create_with_zero_price_should_pass(self):
        data = {
            "date": date.today(),
            "time": time(14, 30),
            "user_id": 1,
            "price": 0.0,
        }
        record = RecordCreate(**data)
        assert record.date == data["date"]
        assert record.time == data["time"]
        assert record.status is None
        assert record.user_id == data["user_id"]
        assert record.price == data["price"]
        assert record.notes is None