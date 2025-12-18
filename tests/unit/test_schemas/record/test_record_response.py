from datetime import date, time, timedelta

import pytest
from pydantic import ValidationError

from app.models import Record
from app.schemas import RecordResponse


class TestRecordResponse:
    def test_record_response(self):
        data = {
            "id": 1,
            "date": date.today(),
            "time": time(14, 30),
            "status": "created",
            "notes": "Notes",
            "price": 500,
            "user_id": 1,
        }
        record = RecordResponse(**data)

        assert record.id == data["id"]
        assert record.date == data["date"]
        assert record.time == data["time"]
        assert record.status == data["status"]
        assert record.notes == data["notes"]
        assert record.price == data["price"]
        assert record.user_id == data["user_id"]

    def test_record_response_from_model(self):
        data = {
            "id": 1,
            "date": date.today(),
            "time": time(14, 30),
            "status": "created",
            "notes": "Notes",
            "price": 500,
            "user_id": 1,
        }
        data_model = Record(**data)
        record = RecordResponse.model_validate(data_model)

        assert record.id == data["id"]
        assert record.date == data["date"]
        assert record.time == data["time"]
        assert record.status == data["status"]
        assert record.notes == data["notes"]
        assert record.price == data["price"]
        assert record.user_id == data["user_id"]

    def test_record_response_from_model_with_empty_notes(self):
        data = {
            "id": 1,
            "date": date.today(),
            "time": time(14, 30),
            "status": "created",
            "price": 500,
            "user_id": 1,
        }
        data_model = Record(**data)
        record = RecordResponse.model_validate(data_model)

        assert record.id == data["id"]
        assert record.date == data["date"]
        assert record.time == data["time"]
        assert record.status == data["status"]
        assert record.notes is None
        assert record.price == data["price"]
        assert record.user_id == data["user_id"]

    def test_record_response_from_model_with_none_in_notes(self):
        data = {
            "id": 1,
            "date": date.today(),
            "time": time(14, 30),
            "status": "created",
            "price": 500,
            "notes": None,
            "user_id": 1,
        }
        data_model = Record(**data)
        record = RecordResponse.model_validate(data_model)

        assert record.id == data["id"]
        assert record.date == data["date"]
        assert record.time == data["time"]
        assert record.status == data["status"]
        assert record.notes == data["notes"]
        assert record.price == data["price"]
        assert record.user_id == data["user_id"]

    def test_record_response_from_model_with_wrong_status(self):
        data = {
            "id": 1,
            "date": date.today(),
            "time": time(14, 30),
            "status": "qwe",
            "notes": "Notes",
            "price": 500,
            "user_id": 1,
        }
        data_model = Record(**data)
        with pytest.raises(ValidationError) as exc_info:
            record = RecordResponse.model_validate(data_model)

        assert len(exc_info.value.errors()) == 1
        assert exc_info.value.errors()[0]["type"] == "value_error"
        assert "Status must be one of" in str(exc_info.value)

    def test_record_response_from_model_with_wrong_price(self):
        data = {
            "id": 1,
            "date": date.today(),
            "time": time(14, 30),
            "status": "created",
            "notes": "Notes",
            "price": -50,
            "user_id": 1,
        }
        data_model = Record(**data)
        with pytest.raises(ValidationError) as exc_info:
            record = RecordResponse.model_validate(data_model)

        assert len(exc_info.value.errors()) == 1
        assert exc_info.value.errors()[0]["type"] == "value_error"
        assert "Price must be greater or equal than 0" in str(exc_info.value)

    def test_record_response_from_model_with_past_date_should_pass(self):
        data = {
            "id": 1,
            "date": date.today() - timedelta(days=1),
            "time": time(14, 30),
            "status": "created",
            "notes": "Notes",
            "price": 500,
            "user_id": 1,
        }
        data_model = Record(**data)
        record = RecordResponse.model_validate(data_model)

        assert record.id == data["id"]
        assert record.date == data["date"]
        assert record.time == data["time"]
        assert record.status == data["status"]
        assert record.notes == data["notes"]
        assert record.price == data["price"]
        assert record.user_id == data["user_id"]

    def test_record_response_with_zero_price(self):
        data = {
            "id": 1,
            "date": date.today(),
            "time": time(14, 30),
            "status": "created",
            "notes": "Notes",
            "price": 0,
            "user_id": 1,
        }
        record = RecordResponse(**data)

        assert record.id == data["id"]
        assert record.date == data["date"]
        assert record.time == data["time"]
        assert record.status == data["status"]
        assert record.notes == data["notes"]
        assert record.price == data["price"]
        assert record.user_id == data["user_id"]

    def test_record_response_tomorrow(self):
        data = {
            "id": 1,
            "date": date.today() + timedelta(days=1),
            "time": time(14, 30),
            "status": "created",
            "notes": "Notes",
            "price": 500,
            "user_id": 1,
        }
        record = RecordResponse(**data)

        assert record.id == data["id"]
        assert record.date == data["date"]
        assert record.time == data["time"]
        assert record.status == data["status"]
        assert record.notes == data["notes"]
        assert record.price == data["price"]
        assert record.user_id == data["user_id"]