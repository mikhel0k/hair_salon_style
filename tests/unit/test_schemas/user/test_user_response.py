import pytest
from pydantic import ValidationError

from app.models import User
from app.schemas.User import UserResponse


class TestUserResponse:
    def test_user_response(self):
        data = {
            "id": 1,
            "phone_number": "+78005553535",
        }
        user_model = User(**data)
        user = UserResponse.model_validate(user_model)
        assert user.phone_number == data["phone_number"]

    def test_user_response_with_another_number(self):
        data = {
            "id": 1,
            "phone_number": "88005553535",
        }
        user_model = User(**data)
        user = UserResponse.model_validate(user_model)
        assert user.phone_number == "+78005553535"

    def test_user_response_with_another_country_number(self):
        data = {
            "id": 1,
            "phone_number": "+68005553535",
        }
        with pytest.raises(ValidationError) as exc_info:
            user_model = User(**data)
            user = UserResponse.model_validate(user_model)
        assert len(exc_info.value.errors()) == 1
        assert exc_info.value.errors()[0]["type"] == "value_error"
        assert "Invalid phone format" in str(exc_info.value)

    def test_user_response_with_short_number(self):
        data = {
            "id": 1,
            "phone_number": "+7800555353",
        }
        with pytest.raises(ValidationError) as exc_info:
            user_model = User(**data)
            user = UserResponse.model_validate(user_model)
        assert len(exc_info.value.errors()) == 1
        assert exc_info.value.errors()[0]["type"] == "value_error"
        assert "Invalid phone format" in str(exc_info.value)

    def test_user_response_with_long_number(self):
        data = {
            "id": 1,
            "phone_number": "+780055535353",
        }
        with pytest.raises(ValidationError) as exc_info:
            user_model = User(**data)
            user = UserResponse.model_validate(user_model)
        assert len(exc_info.value.errors()) == 1
        assert exc_info.value.errors()[0]["type"] == "value_error"
        assert "Invalid phone format" in str(exc_info.value)

    def test_user_response_without_phone_number(self):
        data = {
            "id": 1,
        }
        with pytest.raises(ValidationError) as exc_info:
            user_model = User(**data)
            user = UserResponse.model_validate(user_model)
        assert len(exc_info.value.errors()) == 1
        assert exc_info.value.errors()[0]["type"] == "value_error"
        assert "phone_number cannot be empty" in str(exc_info.value)

    def test_user_response_without_id(self):
        data = {
            "phone_number": "+78005553535",
        }
        with pytest.raises(ValidationError) as exc_info:
            user_model = User(**data)
            user = UserResponse.model_validate(user_model)
        assert len(exc_info.value.errors()) == 1
        assert exc_info.value.errors()[0]["type"] == "int_type"
        assert "Input should be a valid integer" in str(exc_info.value)

    def test_user_response_with_none_in_id(self):
        data = {
            "id": None,
            "phone_number": "+78005553535",
        }
        with pytest.raises(ValidationError) as exc_info:
            user_model = User(**data)
            user = UserResponse.model_validate(user_model)
        assert len(exc_info.value.errors()) == 1
        assert exc_info.value.errors()[0]["type"] == "int_type"
        assert "Input should be a valid integer" in str(exc_info.value)

    def test_user_response_without_none_in_number(self):
        data = {
            "id": 1,
            "phone_number": None,
        }
        with pytest.raises(ValidationError) as exc_info:
            user_model = User(**data)
            user = UserResponse.model_validate(user_model)
        assert len(exc_info.value.errors()) == 1
        assert exc_info.value.errors()[0]["type"] == "value_error"
        assert "phone_number cannot be empty" in str(exc_info.value)

    def test_user_response_with_int(self):
        data = {
            "id": 1,
            "phone_number": 88005553535,
        }
        user_model = User(**data)
        user = UserResponse.model_validate(user_model)
        assert user.phone_number == "+78005553535"

    def test_user_response_with_big_id(self):
        data = {
            "id": 1111111111111111111,
            "phone_number": "+78005553535",
        }
        user_model = User(**data)
        user = UserResponse.model_validate(user_model)
        assert user.phone_number == data["phone_number"]

