from datetime import date, time, timedelta

import pytest
from pydantic import ValidationError

from app.models import Record
from app.schemas.Record import (
RecordResponse,
RecordCreate,
RecordUpdate,
EditRecordStatus,
EditRecordNote,
ALLOWED_STATUSES,
)


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

    def test_record_with_only_non_optional_fields(self):
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

    def test_record_with_only_none_in_price(self):
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

    def test_record_with_wrong_date(self):
        data = {
            "date": date.today() - timedelta(1),
            "time": time(14, 30),
            "user_id": 1
        }
        with pytest.raises(ValidationError) as exc_info:
            record = RecordCreate(**data)
        assert "Date must be in the future" in str(exc_info.value)

    def test_record_without_date(self):
        data = {
            "time": time(14, 30),
            "user_id": 1
        }
        with pytest.raises(ValidationError) as exc_info:
            record = RecordCreate(**data)
        assert any(error["type"] == "missing" for error in exc_info.value.errors())

    def test_record_without_time(self):
        data = {
            "date": date.today(),
            "user_id": 1
        }
        with pytest.raises(ValidationError) as exc_info:
            record = RecordCreate(**data)
        assert any(error["type"] == "missing" for error in exc_info.value.errors())

    def test_record_without_user_id(self):
        data = {
            "date": date.today(),
            "time": time(14, 30),
        }
        with pytest.raises(ValidationError) as exc_info:
            record = RecordCreate(**data)
        assert any(error["type"] == "missing" for error in exc_info.value.errors())

    def test_record_with_wrong_status(self):
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

    def test_record_with_all_statuses(self):
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

    def test_record_with_negative_price(self):
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

    def test_record_with_zero_price_should_pass(self):
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


class TestEditRecordStatus:
    def test_edit_record_status_to_created(self):
        data = {
            "id": 1,
            "status": "created",
        }
        record = EditRecordStatus(**data)
        assert record.id == data["id"]
        assert record.status == data["status"]

    def test_edit_record_status_to_confirmed(self):
        data = {
            "id": 1,
            "status": "confirmed",
        }
        record = EditRecordStatus(**data)
        assert record.id == data["id"]
        assert record.status == data["status"]

    def test_edit_record_status_to_rejected(self):
        data = {
            "id": 1,
            "status": "rejected",
        }
        record = EditRecordStatus(**data)
        assert record.id == data["id"]
        assert record.status == data["status"]

    def test_edit_record_status_to_cancelled(self):
        data = {
            "id": 1,
            "status": "cancelled",
        }
        record = EditRecordStatus(**data)
        assert record.id == data["id"]
        assert record.status == data["status"]

    def test_edit_record_status_to_unconfirmed(self):
        data = {
            "id": 1,
            "status": "qwe",
        }
        with pytest.raises(ValidationError) as exc_info:
            record = EditRecordStatus(**data)
        assert len(exc_info.value.errors()) == 1
        assert exc_info.value.errors()[0]["type"] == "value_error"
        assert "Status must be one of" in str(exc_info.value)


class TestEditRecordNote:
    pass