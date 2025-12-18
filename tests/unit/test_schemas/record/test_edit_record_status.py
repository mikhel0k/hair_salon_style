import pytest
from pydantic import ValidationError

from app.schemas import EditRecordStatus


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