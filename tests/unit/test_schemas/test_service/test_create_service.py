import decimal

import pytest
from pydantic import ValidationError

from app.schemas.Service import ServiceCreate
from tests.unit.test_schemas.test_service.conftest import (
    Name,
    Price,
    Duration,
    MIN_DURATION,
    MAX_DURATION,
    MIN_PRICE,
    MAX_PRICE,
    MAX_NAME_LENGTH,
    MIN_NAME_LENGTH,
)


class TestCreateService:
    name = Name()
    price = Price()
    duration = Duration()

    @pytest.mark.parametrize(
        "name, price, duration_minutes, category_id, description", [
            (name.right_name, price.right_price, duration.right_duration, 1, "Some description"),
            (name.right_name_short, price.right_price, duration.right_duration, 1, "Some description"),
            (name.right_name_long, price.right_price, duration.right_duration, 1, "Some description"),
            (name.right_name_сyrillic, price.right_price, duration.right_duration, 1, "Some description"),
            (name.right_name, price.right_price_small, duration.right_duration, 1, "Some description"),
            (name.right_name, price.right_price_big, duration.right_duration, 1, "Some description"),
            (name.right_name, price.right_price_float, duration.right_duration, 1, "Some description"),
            (name.right_name, price.right_price_three_numbers_after_coma, duration.right_duration, 1, "Some description"),
            (name.right_name, price.right_price_string, duration.right_duration, 1, "Some description"),
            (name.right_name, price.right_price_string_with_coma, duration.right_duration, 1, "Some description"),
            (name.right_name, price.right_price, duration.right_duration_small, 1, "Some description"),
            (name.right_name, price.right_price, duration.right_duration_big, 1, "Some description"),
            (name.right_name, price.right_price, duration.right_duration_string, 1, "Some description"),
        ]
    )
    def test_create_service(
            self,
            name,
            price,
            duration_minutes,
            category_id,
            description,
    ):
        service = ServiceCreate(
            name=name,
            price=price,
            duration_minutes=duration_minutes,
            category_id=category_id,
            description=description,
        )
        assert isinstance(service, ServiceCreate)
        assert service.name == name
        assert service.price == decimal.Decimal(str(price))
        assert service.duration_minutes == int(duration_minutes)
        assert service.category_id == category_id
        assert service.description == description

    @pytest.mark.parametrize(
        "name, price, duration_minutes, category_id, description, error_field, error_type, message", [
            (name.wrong_name_long, price.right_price, duration.right_duration, 1, "Some description",
             ("name",), "string_too_long", f"String should have at most {MAX_NAME_LENGTH} characters"),
            (name.wrong_name_short, price.right_price, duration.right_duration, 1, "Some description",
             ("name",), "string_too_short", f"String should have at least {MIN_NAME_LENGTH} characters"),
            (name.wrong_name_int, price.right_price, duration.right_duration, 1, "Some description",
             ("name",), "string_type", f"Input should be a valid string"),
            (name.wrong_name_empty, price.right_price, duration.right_duration, 1, "Some description",
             ("name",), "string_too_short", f"String should have at least {MIN_NAME_LENGTH} characters"),
            (name.wrong_name_spaces, price.right_price, duration.right_duration, 1, "Some description",
             ("name",), "string_too_short", f"String should have at least {MIN_NAME_LENGTH} characters"),
            (name.wrong_name_none, price.right_price, duration.right_duration, 1, "Some description",
             ("name",), "string_type", f"Input should be a valid string"),
            (name.right_name, price.wrong_price_zero, duration.right_duration, 1, "Some description",
             ("price",), "value_error", f"Value error, Price must be greater than {MIN_PRICE}"),
            (name.right_name, price.wrong_price_negative, duration.right_duration, 1, "Some description",
             ("price",), "value_error", f"Value error, Price must be greater than {MIN_PRICE}"),
            (name.right_name, price.wrong_price_negative_small, duration.right_duration, 1, "Some description",
             ("price",), "value_error", f"Value error, Price must be greater than {MIN_PRICE}"),
            (name.right_name, price.wrong_price_negative_big, duration.right_duration, 1, "Some description",
             ("price",), "value_error", f"Value error, Price must be greater than {MIN_PRICE}"),
            (name.right_name, price.wrong_price_big, duration.right_duration, 1, "Some description",
             ("price",), "value_error", f"Value error, Price must be less than {MAX_PRICE}"),
            (name.right_name, price.wrong_price_negative_float, duration.right_duration, 1, "Some description",
             ("price",), "value_error", f"Value error, Price must be greater than {MIN_PRICE}"),
            (name.right_name, price.wrong_price_negative_three_numbers_after_coma, duration.right_duration, 1, "Some description",
             ("price",), "value_error", f"Value error, Price must be greater than {MIN_PRICE}"),
            (name.right_name, price.wrong_price_string, duration.right_duration, 1, "Some description",
             ("price",), "decimal_parsing", f"Input should be a valid decimal"),
            (name.right_name, price.wrong_price_none, duration.right_duration, 1, "Some description",
             ("price",), "decimal_type", f"Decimal input should be an integer, float, string or Decimal object"),
            (name.right_name, price.right_price, duration.wrong_duration_zero, 1, "Some description",
             ("duration_minutes",), "value_error", f"Value error, Duration must be greater than {MIN_DURATION}"),
            (name.right_name, price.right_price, duration.wrong_duration_negative, 1, "Some description",
             ("duration_minutes",), "value_error", f"Value error, Duration must be greater than {MIN_DURATION}"),
            (name.right_name, price.right_price, duration.wrong_duration_negative_small, 1, "Some description",
             ("duration_minutes",), "value_error", f"Value error, Duration must be greater than {MIN_DURATION}"),
            (name.right_name, price.right_price, duration.wrong_duration_negative_big, 1, "Some description",
             ("duration_minutes",), "value_error", f"Value error, Duration must be greater than {MIN_DURATION}"),
            (name.right_name, price.right_price, duration.wrong_duration_big, 1, "Some description",
             ("duration_minutes",), "value_error", f"Value error, Duration must be less than 3 hours"),
            (name.right_name, price.right_price, duration.wrong_duration_float, 1, "Some description",
             ("duration_minutes",), "int_from_float", f"Input should be a valid integer, got a number with a fractional part"),
        ]
    )
    def test_create_service_wrong(
            self,
            name,
            price,
            duration_minutes,
            category_id,
            description,
            error_field,
            error_type,
            message,
    ):
        with pytest.raises(ValidationError) as error:
            service = ServiceCreate(
                name=name,
                price=price,
                duration_minutes=duration_minutes,
                category_id=category_id,
                description=description,
            )
        assert len(error.value.errors()) == 1
        assert error.value.errors()[0]["loc"] == error_field
        assert error.value.errors()[0]["type"] == error_type
        assert error.value.errors()[0]["msg"] == message