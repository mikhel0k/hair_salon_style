import pytest
from pydantic import ValidationError

from app.schemas.User import UserFind


class TestUserFind:
    def test_user_find(self):
        data = {
            "phone_number": "+78005553535",
        }
        user = UserFind(**data)
        assert user.phone_number == data["phone_number"]

    def test_user_find_with_another_number(self):
        data = {
            "phone_number": "88005553535",
        }
        user = UserFind(**data)
        assert user.phone_number == "+78005553535"

    def test_user_find_with_another_country_number(self):
        data = {
            "phone_number": "+68005553535",
        }
        with pytest.raises(ValidationError) as exc_info:
            UserFind(**data)
        assert len(exc_info.value.errors()) == 1
        assert exc_info.value.errors()[0]["type"] == "value_error"
        assert "Invalid phone format" in str(exc_info.value)

    def test_user_find_with_short_number(self):
        data = {
            "phone_number": "+7800555353",
        }
        with pytest.raises(ValidationError) as exc_info:
            UserFind(**data)
        assert len(exc_info.value.errors()) == 1
        assert exc_info.value.errors()[0]["type"] == "value_error"
        assert "Invalid phone format" in str(exc_info.value)

    def test_user_find_with_long_number(self):
        data = {
            "phone_number": "+780055535353",
        }
        with pytest.raises(ValidationError) as exc_info:
            UserFind(**data)
        assert len(exc_info.value.errors()) == 1
        assert exc_info.value.errors()[0]["type"] == "value_error"
        assert "Invalid phone format" in str(exc_info.value)

    def test_user_find_without_phone_number(self):
        data = {}
        with pytest.raises(ValidationError) as exc_info:
            UserFind(**data)
        assert len(exc_info.value.errors()) == 1
        assert exc_info.value.errors()[0]["type"] == "missing"
        assert "Field required" in str(exc_info.value)

    def test_user_find_without_none_in_number(self):
        data = {
            "phone_number": None,
        }
        with pytest.raises(ValidationError) as exc_info:
            UserFind(**data)
        assert len(exc_info.value.errors()) == 1
        assert exc_info.value.errors()[0]["type"] == "value_error"
        assert "phone_number cannot be empty" in str(exc_info.value)

    def test_user_find_with_int(self):
        data = {
            "phone_number": 88005553535,
        }
        user = UserFind(**data)
        assert user.phone_number == "+78005553535"

