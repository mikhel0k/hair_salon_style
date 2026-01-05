import decimal

import pytest
from pydantic import ValidationError

from app.schemas.Service import ServiceResponse
from app.models.Service import Service
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


class TestResponseService:
    name = Name()
    price = Price()
    duration = Duration()

    @pytest.mark.parametrize(
        "service, name, price, duration_minutes, category_id, description", [
            (Service(id=1, name=name.right_name, price=price.right_price, duration_minutes=duration.right_duration,
                     category_id=1, description="Some description"),
             name.right_name, price.right_price, duration.right_duration, 1, "Some description"),
            (Service(id=1, name=name.right_name_short, price=price.right_price, duration_minutes=duration.right_duration,
                     category_id=1, description="Some description"),
            name.right_name_short, price.right_price, duration.right_duration, 1, "Some description"),
            (Service(id=1, name=name.right_name_long, price=price.right_price, duration_minutes=duration.right_duration,
                     category_id=1, description="Some description"),
            name.right_name_long, price.right_price, duration.right_duration, 1, "Some description"),
            (Service(id=1, name=name.right_name_сyrillic, price=price.right_price, duration_minutes=duration.right_duration,
                     category_id=1, description="Some description"),
            name.right_name_сyrillic, price.right_price, duration.right_duration, 1, "Some description"),
            (Service(id=1, name=name.right_name, price=price.right_price_small, duration_minutes=duration.right_duration,
                     category_id=1, description="Some description"),
            name.right_name, price.right_price_small, duration.right_duration, 1, "Some description"),
            (Service(id=1, name=name.right_name, price=price.right_price_big, duration_minutes=duration.right_duration,
                     category_id=1, description="Some description"),
            name.right_name, price.right_price_big, duration.right_duration, 1, "Some description"),
            (Service(id=1, name=name.right_name, price=price.right_price_float, duration_minutes=duration.right_duration,
                     category_id=1, description="Some description"),
            name.right_name, price.right_price_float, duration.right_duration, 1, "Some description"),
            (Service(id=1, name=name.right_name, price=price.right_price_three_numbers_after_coma, duration_minutes=duration.right_duration,
                     category_id=1, description="Some description"),
            name.right_name, price.right_price_three_numbers_after_coma, duration.right_duration, 1, "Some description"),
            (Service(id=1, name=name.right_name, price=price.right_price_string, duration_minutes=duration.right_duration,
                     category_id=1, description="Some description"),
            name.right_name, price.right_price_string, duration.right_duration, 1, "Some description"),
            (Service(id=1, name=name.right_name, price=price.right_price_string_with_coma, duration_minutes=duration.right_duration,
                     category_id=1, description="Some description"),
            name.right_name, price.right_price_string_with_coma, duration.right_duration, 1, "Some description"),
            (Service(id=1, name=name.right_name, price=price.right_price, duration_minutes=duration.right_duration_small,
                     category_id=1, description="Some description"),
            name.right_name, price.right_price, duration.right_duration_small, 1, "Some description"),
            (Service(id=1, name=name.right_name, price=price.right_price, duration_minutes=duration.right_duration_big,
                     category_id=1, description="Some description"),
            name.right_name, price.right_price, duration.right_duration_big, 1, "Some description"),
            (Service(id=1, name=name.right_name, price=price.right_price, duration_minutes=duration.right_duration_string,
                     category_id=1, description="Some description"),
            name.right_name, price.right_price, duration.right_duration_string, 1, "Some description"),
        ]
    )
    def test_response_service(
            self,
            service,
            name,
            price,
            duration_minutes,
            category_id,
            description,
    ):
        service_response = ServiceResponse.model_validate(service)
        assert isinstance(service_response, ServiceResponse)
        assert service_response.id == 1
        assert service_response.name == name
        assert service_response.price == decimal.Decimal(str(price))
        assert service_response.duration_minutes == int(duration_minutes)
        assert service_response.category_id == category_id
        assert service_response.description == description

    @pytest.mark.parametrize(
        "service, error_field, error_type, message", [
            (Service(id=1, name=name.wrong_name_long, price=price.right_price,
                     duration_minutes=duration.right_duration, category_id=1, description="Some description"),
             ("name",), "string_too_long", f"String should have at most {MAX_NAME_LENGTH} characters"),
            (Service(id=1, name=name.wrong_name_short, price=price.right_price,
                     duration_minutes=duration.right_duration, category_id=1, description="Some description"),
             ("name",), "string_too_short", f"String should have at least {MIN_NAME_LENGTH} characters"),
            (Service(id=1, name=name.wrong_name_int, price=price.right_price,
                     duration_minutes=duration.right_duration, category_id=1, description="Some description"),
             ("name",), "string_type", f"Input should be a valid string"),
            (Service(id=1, name=name.wrong_name_empty, price=price.right_price,
                     duration_minutes=duration.right_duration, category_id=1, description="Some description"),
             ("name",), "string_too_short", f"String should have at least {MIN_NAME_LENGTH} characters"),
            (Service(id=1, name=name.wrong_name_spaces, price=price.right_price,
                     duration_minutes=duration.right_duration, category_id=1, description="Some description"),
             ("name",), "string_too_short", f"String should have at least {MIN_NAME_LENGTH} characters"),
            (Service(id=1, name=name.wrong_name_none, price=price.right_price,
                     duration_minutes=duration.right_duration, category_id=1, description="Some description"),
             ("name",), "string_type", f"Input should be a valid string"),
            (Service(id=1, name=name.right_name, price=price.wrong_price_zero,
                     duration_minutes=duration.right_duration, category_id=1, description="Some description"),
             ("price",), "value_error", f"Value error, Price must be greater than {MIN_PRICE}"),
            (Service(id=1, name=name.right_name, price=price.wrong_price_negative,
                     duration_minutes=duration.right_duration, category_id=1, description="Some description"),
             ("price",), "value_error", f"Value error, Price must be greater than {MIN_PRICE}"),
            (Service(id=1, name=name.right_name, price=price.wrong_price_negative_small,
                     duration_minutes=duration.right_duration, category_id=1, description="Some description"),
             ("price",), "value_error", f"Value error, Price must be greater than {MIN_PRICE}"),
            (Service(id=1, name=name.right_name, price=price.wrong_price_negative_big,
                     duration_minutes=duration.right_duration, category_id=1, description="Some description"),
             ("price",), "value_error", f"Value error, Price must be greater than {MIN_PRICE}"),
            (Service(id=1, name=name.right_name, price=price.wrong_price_big,
                     duration_minutes=duration.right_duration, category_id=1, description="Some description"),
             ("price",), "value_error", f"Value error, Price must be less than {MAX_PRICE}"),
            (Service(id=1, name=name.right_name, price=price.wrong_price_negative_float,
                     duration_minutes=duration.right_duration, category_id=1, description="Some description"),
             ("price",), "value_error", f"Value error, Price must be greater than {MIN_PRICE}"),
            (Service(id=1, name=name.right_name, price=price.wrong_price_negative_three_numbers_after_coma,
                     duration_minutes=duration.right_duration, category_id=1, description="Some description"),
             ("price",), "value_error", f"Value error, Price must be greater than {MIN_PRICE}"),
            (Service(id=1, name=name.right_name, price=price.wrong_price_string,
                     duration_minutes=duration.right_duration, category_id=1, description="Some description"),
             ("price",), "decimal_parsing", f"Input should be a valid decimal"),
            (Service(id=1, name=name.right_name, price=price.wrong_price_none,
                     duration_minutes=duration.right_duration, category_id=1, description="Some description"),
             ("price",), "decimal_type", f"Decimal input should be an integer, float, string or Decimal object"),
            (Service(id=1, name=name.right_name, price=price.right_price,
                     duration_minutes=duration.wrong_duration_zero, category_id=1, description="Some description"),
             ("duration_minutes",), "value_error", f"Value error, Duration must be greater than {MIN_DURATION}"),
            (Service(id=1, name=name.right_name, price=price.right_price,
                     duration_minutes=duration.wrong_duration_negative, category_id=1, description="Some description"),
             ("duration_minutes",), "value_error", f"Value error, Duration must be greater than {MIN_DURATION}"),
            (Service(id=1, name=name.right_name, price=price.right_price,
                     duration_minutes=duration.wrong_duration_negative_small, category_id=1, description="Some description"),
             ("duration_minutes",), "value_error", f"Value error, Duration must be greater than {MIN_DURATION}"),
            (Service(id=1, name=name.right_name, price=price.right_price,
                     duration_minutes=duration.wrong_duration_negative_big, category_id=1, description="Some description"),
             ("duration_minutes",), "value_error", f"Value error, Duration must be greater than {MIN_DURATION}"),
            (Service(id=1, name=name.right_name, price=price.right_price,
                     duration_minutes=duration.wrong_duration_big, category_id=1, description="Some description"),
             ("duration_minutes",), "value_error", f"Value error, Duration must be less than {MAX_DURATION//60} hours"),
            (Service(id=1, name=name.right_name, price=price.right_price,
                     duration_minutes=duration.wrong_duration_float, category_id=1, description="Some description"),
             ("duration_minutes",), "int_from_float", f"Input should be a valid integer, got a number with a fractional part"),
        ]
    )
    def test_create_service_wrong(
            self,
            service,
            error_field,
            error_type,
            message,
    ):
        with pytest.raises(ValidationError) as error:
            service_response = ServiceResponse.model_validate(service)
        assert len(error.value.errors()) == 1
        assert error.value.errors()[0]["loc"] == error_field
        assert error.value.errors()[0]["type"] == error_type
        assert error.value.errors()[0]["msg"] == message