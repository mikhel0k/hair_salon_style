from datetime import date, timedelta, time

import pytest
from pydantic import ValidationError

from app.schemas.UserFlow import MakeRecord


class TestMakeRecord:
    def test_make_record_tomorrow(self):
        data = {
            "phone_number": "+78005553535",
            "date": date.today() + timedelta(days=1),
            "time": time(13, 30),
            "notes": "I want drink bear"
        }
        make_record = MakeRecord(**data)
        assert make_record.phone_number == data["phone_number"]
        assert make_record.date == data["date"]
        assert make_record.time == data["time"]
        assert make_record.notes == data["notes"]

    def test_make_record_today(self):
        data = {
            "phone_number": "+78005553535",
            "date": date.today(),
            "time": time(13, 30),
            "notes": "I want drink bear"
        }
        make_record = MakeRecord(**data)
        assert make_record.phone_number == data["phone_number"]
        assert make_record.date == data["date"]
        assert make_record.time == data["time"]
        assert make_record.notes == data["notes"]


    def test_make_record_yesterday(self):
        data = {
            "phone_number": "+78005553535",
            "date": date.today() - timedelta(days=1),
            "time": time(13, 30),
            "notes": "I want drink bear"
        }
        with pytest.raises(ValidationError) as exc_info:
            make_record = MakeRecord(**data)
        assert len(exc_info.value.errors()) == 1
        assert exc_info.value.errors()[0]["type"] == "value_error"
        assert "Date must be in the future" in str(exc_info.value)
    
    def test_make_record(self):
        data = {
            "phone_number": "+78005553535",
            "date": date.today(),
            "time": time(13, 30),
            "notes": "I want drink bear"
        }
        make_record = MakeRecord(**data)
        assert make_record.phone_number == data["phone_number"]
        assert make_record.date == data["date"]
        assert make_record.time == data["time"]
        assert make_record.notes == data["notes"]

    def test_make_record_with_another_number(self):
        data = {
            "phone_number": "88005553535",
            "date": date.today(),
            "time": time(13, 30),
            "notes": "I want drink bear"
        }
        make_record = MakeRecord(**data)
        assert make_record.phone_number == "+78005553535"
        assert make_record.date == data["date"]
        assert make_record.time == data["time"]
        assert make_record.notes == data["notes"]

    def test_make_record_with_another_country_number(self):
        data = {
            "phone_number": "+68005553535",
            "date": date.today(),
            "time": time(13, 30),
            "notes": "I want drink bear"
        }
        with pytest.raises(ValidationError) as exc_info:
            MakeRecord(**data)
        assert len(exc_info.value.errors()) == 1
        assert exc_info.value.errors()[0]["type"] == "value_error"
        assert "Invalid phone format" in str(exc_info.value)

    def test_make_record_with_short_number(self):
        data = {
            "phone_number": "+7800555353",
            "date": date.today(),
            "time": time(13, 30),
            "notes": "I want drink bear"
        }
        with pytest.raises(ValidationError) as exc_info:
            MakeRecord(**data)
        assert len(exc_info.value.errors()) == 1
        assert exc_info.value.errors()[0]["type"] == "value_error"
        assert "Invalid phone format" in str(exc_info.value)

    def test_make_record_with_long_number(self):
        data = {
            "phone_number": "+780055535353",
            "date": date.today(),
            "time": time(13, 30),
            "notes": "I want drink bear"
        }
        with pytest.raises(ValidationError) as exc_info:
            MakeRecord(**data)
        assert len(exc_info.value.errors()) == 1
        assert exc_info.value.errors()[0]["type"] == "value_error"
        assert "Invalid phone format" in str(exc_info.value)

    def test_make_record_without_phone_number(self):
        data = {
            "date": date.today(),
            "time": time(13, 30),
            "notes": "I want drink bear"
        }
        with pytest.raises(ValidationError) as exc_info:
            MakeRecord(**data)
        assert len(exc_info.value.errors()) == 1
        assert exc_info.value.errors()[0]["type"] == "missing"
        assert "Field required" in str(exc_info.value)

    def test_make_record_without_date(self):
        data = {
            "phone_number": "+78005553535",
            "time": time(13, 30),
            "notes": "I want drink bear"
        }
        with pytest.raises(ValidationError) as exc_info:
            MakeRecord(**data)
        assert len(exc_info.value.errors()) == 1
        assert exc_info.value.errors()[0]["type"] == "missing"
        assert "Field required" in str(exc_info.value)

    def test_make_record_without_time(self):
        data = {
            "phone_number": "+78005553535",
            "date": date.today(),
            "notes": "I want drink bear"
        }
        with pytest.raises(ValidationError) as exc_info:
            MakeRecord(**data)
        assert len(exc_info.value.errors()) == 1
        assert exc_info.value.errors()[0]["type"] == "missing"
        assert "Field required" in str(exc_info.value)


    def test_make_record_without_notes(self):
        data = {
            "phone_number": "+78005553535",
            "date": date.today(),
            "time": time(13, 30),
        }
        make_record = MakeRecord(**data)
        assert make_record.phone_number == data["phone_number"]
        assert make_record.date == data["date"]
        assert make_record.time == data["time"]
        assert make_record.notes is None

    def test_make_record_without_none_in_number(self):
        data = {
            "phone_number": None,
            "date": date.today(),
            "time": time(13, 30),
            "notes": "I want drink bear"
        }
        with pytest.raises(ValidationError) as exc_info:
            MakeRecord(**data)
        assert len(exc_info.value.errors()) == 1
        assert exc_info.value.errors()[0]["type"] == "value_error"
        assert "phone_number cannot be empty" in str(exc_info.value)

    def test_make_record_with_int(self):
        data = {
            "phone_number": 88005553535,
            "date": date.today(),
            "time": time(13, 30),
            "notes": "I want drink bear"
        }
        make_record = MakeRecord(**data)
        assert make_record.phone_number == "+78005553535"
        assert make_record.date == data["date"]
        assert make_record.time == data["time"]
        assert make_record.notes == data["notes"]
