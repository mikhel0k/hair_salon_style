import decimal

import pytest
from pydantic import ValidationError

from app.schemas.Service import ServiceResponseSmall
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
        "service, name, price, description", [
            (Service(id=1, name=name.right_name, price=price.right_price, description="Some description"),
             name.right_name, price.right_price, "Some description"),
            (Service(id=1, name=name.right_name_short, price=price.right_price, description="Some description"),
            name.right_name_short, price.right_price, "Some description"),
            (Service(id=1, name=name.right_name_long, price=price.right_price, description="Some description"),
            name.right_name_long, price.right_price, "Some description"),
            (Service(id=1, name=name.right_name_сyrillic, price=price.right_price, description="Some description"),
            name.right_name_сyrillic, price.right_price, "Some description"),
            (Service(id=1, name=name.right_name, price=price.right_price_small, description="Some description"),
            name.right_name, price.right_price_small, "Some description"),
            (Service(id=1, name=name.right_name, price=price.right_price_big, description="Some description"),
            name.right_name, price.right_price_big, "Some description"),
            (Service(id=1, name=name.right_name, price=price.right_price_float, description="Some description"),
            name.right_name, price.right_price_float, "Some description"),
            (Service(id=1, name=name.right_name, price=price.right_price_three_numbers_after_coma, description="Some description"),
            name.right_name, price.right_price_three_numbers_after_coma, "Some description"),
            (Service(id=1, name=name.right_name, price=price.right_price_string, description="Some description"),
            name.right_name, price.right_price_string, "Some description"),
            (Service(id=1, name=name.right_name, price=price.right_price_string_with_coma, description="Some description"),
            name.right_name, price.right_price_string_with_coma, "Some description"),
        ]
    )
    def test_response_service(
            self,
            service,
            name,
            price,
            description,
    ):
        service_response = ServiceResponseSmall.model_validate(service)
        assert isinstance(service_response, ServiceResponseSmall)

        assert service_response.id == 1
        assert service_response.name == name
        assert service_response.price == decimal.Decimal(str(price))
        assert service_response.description == description

    @pytest.mark.parametrize(
        "service, error_field, error_type, message", [
            (Service(id=1, name=name.wrong_name_long, price=price.right_price, description="Some description"),
             ("name",), "string_too_long", f"String should have at most {MAX_NAME_LENGTH} characters"),
            (Service(id=1, name=name.wrong_name_short, price=price.right_price, description="Some description"),
             ("name",), "string_too_short", f"String should have at least {MIN_NAME_LENGTH} characters"),
            (Service(id=1, name=name.wrong_name_int, price=price.right_price, description="Some description"),
             ("name",), "string_type", f"Input should be a valid string"),
            (Service(id=1, name=name.wrong_name_empty, price=price.right_price, description="Some description"),
             ("name",), "string_too_short", f"String should have at least {MIN_NAME_LENGTH} characters"),
            (Service(id=1, name=name.wrong_name_spaces, price=price.right_price, description="Some description"),
             ("name",), "string_too_short", f"String should have at least {MIN_NAME_LENGTH} characters"),
            (Service(id=1, name=name.wrong_name_none, price=price.right_price, description="Some description"),
             ("name",), "string_type", f"Input should be a valid string"),
            (Service(id=1, name=name.right_name, price=price.wrong_price_zero, description="Some description"),
             ("price",), "value_error", f"Value error, Price must be greater than {MIN_PRICE}"),
            (Service(id=1, name=name.right_name, price=price.wrong_price_negative, description="Some description"),
             ("price",), "value_error", f"Value error, Price must be greater than {MIN_PRICE}"),
            (Service(id=1, name=name.right_name, price=price.wrong_price_negative_small, description="Some description"),
             ("price",), "value_error", f"Value error, Price must be greater than {MIN_PRICE}"),
            (Service(id=1, name=name.right_name, price=price.wrong_price_negative_big, description="Some description"),
             ("price",), "value_error", f"Value error, Price must be greater than {MIN_PRICE}"),
            (Service(id=1, name=name.right_name, price=price.wrong_price_big, description="Some description"),
             ("price",), "value_error", f"Value error, Price must be less than {MAX_PRICE}"),
            (Service(id=1, name=name.right_name, price=price.wrong_price_negative_float, description="Some description"),
             ("price",), "value_error", f"Value error, Price must be greater than {MIN_PRICE}"),
            (Service(id=1, name=name.right_name, price=price.wrong_price_negative_three_numbers_after_coma,
                     duration_minutes=duration.right_duration, category_id=1, description="Some description"),
             ("price",), "value_error", f"Value error, Price must be greater than {MIN_PRICE}"),
            (Service(id=1, name=name.right_name, price=price.wrong_price_string, description="Some description"),
             ("price",), "decimal_parsing", f"Input should be a valid decimal"),
            (Service(id=1, name=name.right_name, price=price.wrong_price_none, description="Some description"),
             ("price",), "decimal_type", f"Decimal input should be an integer, float, string or Decimal object"),
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
            service_response = ServiceResponseSmall.model_validate(service)
        assert len(error.value.errors()) == 1
        assert error.value.errors()[0]["loc"] == error_field
        assert error.value.errors()[0]["type"] == error_type
        assert error.value.errors()[0]["msg"] == message