from datetime import date, timedelta, time

import pytest
from pydantic import ValidationError

from app.schemas import RecordUpdate


class TestRecordUpdate:
    def test_record_update_date_tomorrow(self):
        data = {
            "id": 1,
            "date": date.today() + timedelta(days=1),
        }
        record = RecordUpdate(**data)

        assert record.id == data["id"]
        assert record.date == data["date"]
        assert record.time is None
        assert record.status is None
        assert record.notes is None
        assert record.price is None

    def test_record_update_today(self):
        data = {
            "id": 1,
            "date": date.today(),
        }
        record = RecordUpdate(**data)

        assert record.id == data["id"]
        assert record.date == data["date"]
        assert record.time is None
        assert record.status is None
        assert record.notes is None
        assert record.price is None

    def test_record_update_yesterday(self):
        data = {
            "id": 1,
            "date": date.today() - timedelta(days=1),
        }
        with pytest.raises(ValidationError) as exc_info:
            record = RecordUpdate(**data)
        assert len(exc_info.value.errors()) == 1
        assert exc_info.value.errors()[0]["type"] == "value_error"
        assert "Date must be in the future" in str(exc_info.value)

    def test_record_update_time(self):
        data = {
            "id": 1,
            "time": time(14, 30),
        }
        record = RecordUpdate(**data)

        assert record.id == data["id"]
        assert record.date is None
        assert record.time == data["time"]
        assert record.status is None
        assert record.notes is None
        assert record.price is None

    def test_record_update_date_and_time(self):
        data = {
            "id": 1,
            "date": date.today() + timedelta(days=1),
            "time": time(14, 30),
        }
        record = RecordUpdate(**data)

        assert record.id == data["id"]
        assert record.date == data["date"]
        assert record.time == data["time"]
        assert record.status is None
        assert record.notes is None
        assert record.price is None

    def test_record_update_status(self):
        data = {
            "id": 1,
            "status": "created",
        }
        record = RecordUpdate(**data)

        assert record.id == data["id"]
        assert record.date is None
        assert record.time is None
        assert record.status == data["status"]
        assert record.notes is None
        assert record.price is None

    def test_record_update_not_valid_status(self):
        data = {
            "id": 1,
            "status": "qwe",
        }
        with pytest.raises(ValidationError) as exc_info:
            record = RecordUpdate(**data)
        assert len(exc_info.value.errors()) == 1
        assert exc_info.value.errors()[0]["type"] == "value_error"
        assert "Status must be one of" in str(exc_info.value)

    def test_record_update_notes(self):
        data = {
            "id": 1,
            "notes": "Note",
        }
        record = RecordUpdate(**data)

        assert record.id == data["id"]
        assert record.date is None
        assert record.time is None
        assert record.status is None
        assert record.notes == data["notes"]
        assert record.price is None

    def test_record_update_price(self):
        data = {
            "id": 1,
            "price": 550.0,
        }
        record = RecordUpdate(**data)

        assert record.id == data["id"]
        assert record.date is None
        assert record.time is None
        assert record.status is None
        assert record.notes is None
        assert record.price == data["price"]

    def test_record_update_price_smaller_zero(self):
        data = {
            "id": 1,
            "price": -100,
        }
        with pytest.raises(ValidationError) as exc_info:
            record = RecordUpdate(**data)
        assert len(exc_info.value.errors()) == 1
        assert exc_info.value.errors()[0]["type"] == "value_error"
        assert "Price must be greater or equal than 0" in str(exc_info.value)