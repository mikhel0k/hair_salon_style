import decimal
import pytest
from pydantic import ValidationError

from app.schemas.Service import ServiceCreate
from conftest import Name, Price, Duration
from tests.unit.test_schemas.conftest_exceptions import ErrorMessages, ErrorTypes


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
            (name.right_name, price.right_price_three_numbers_after_coma, duration.right_duration, 1,
             "Some description"),
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
        assert service.name == name.title()
        assert service.price == decimal.Decimal(str(price))
        assert service.duration_minutes == int(duration_minutes)
        assert service.category_id == category_id
        assert service.description == description

    @pytest.mark.parametrize(
        "name, price, duration_minutes, error_loc, error_type, error_msg", [
            (name.wrong_name_long, price.right_price, duration.right_duration,
             ("name",), ErrorTypes.STRING_TOO_LONG, ErrorMessages.STRING_TOO_LONG),
            (name.wrong_name_short, price.right_price, duration.right_duration,
             ("name",), ErrorTypes.STRING_TOO_SHORT, ErrorMessages.STRING_TOO_SHORT),
            (name.wrong_name_int, price.right_price, duration.right_duration,
             ("name",), ErrorTypes.STRING_TYPE, ErrorMessages.STRING_TYPE),
            (name.wrong_name_empty, price.right_price, duration.right_duration,
             ("name",), ErrorTypes.STRING_TOO_SHORT, ErrorMessages.STRING_TOO_SHORT),
            (name.wrong_name_spaces, price.right_price, duration.right_duration,
             ("name",), ErrorTypes.STRING_TOO_SHORT, ErrorMessages.STRING_TOO_SHORT),
            (name.wrong_name_none, price.right_price, duration.right_duration,
             ("name",), ErrorTypes.STRING_TYPE, ErrorMessages.STRING_TYPE),
            (name.right_name, price.wrong_price_zero, duration.right_duration,
             ("price",), ErrorTypes.GREATER_THAN_EQUAL, ErrorMessages.PRICE_TOO_LOW),
            (name.right_name, price.wrong_price_negative, duration.right_duration,
             ("price",), ErrorTypes.GREATER_THAN_EQUAL, ErrorMessages.PRICE_TOO_LOW),
            (name.right_name, price.wrong_price_negative_small, duration.right_duration,
             ("price",), ErrorTypes.GREATER_THAN_EQUAL, ErrorMessages.PRICE_TOO_LOW),
            (name.right_name, price.wrong_price_negative_big, duration.right_duration,
             ("price",), ErrorTypes.GREATER_THAN_EQUAL, ErrorMessages.PRICE_TOO_LOW),
            (name.right_name, price.wrong_price_big, duration.right_duration,
             ("price",), ErrorTypes.LESS_THAN_EQUAL, ErrorMessages.PRICE_TOO_HIGH),
            (name.right_name, price.wrong_price_negative_float, duration.right_duration,
             ("price",), ErrorTypes.GREATER_THAN_EQUAL, ErrorMessages.PRICE_TOO_LOW),
            (name.right_name, price.wrong_price_negative_three_numbers_after_coma, duration.right_duration,
             ("price",), ErrorTypes.GREATER_THAN_EQUAL, ErrorMessages.PRICE_TOO_LOW),
            (name.right_name, price.wrong_price_string, duration.right_duration,
             ("price",), ErrorTypes.DECIMAL_PARSING, ErrorMessages.PRICE_NOT_DECIMAL),
            (name.right_name, price.wrong_price_none, duration.right_duration,
             ("price",), ErrorTypes.DECIMAL_TYPE, ErrorMessages.PRICE_NONE_TYPE),
            (name.right_name, price.right_price, duration.wrong_duration_zero,
             ("duration_minutes",), ErrorTypes.GREATER_THAN_EQUAL, ErrorMessages.DURATION_TOO_LOW),
            (name.right_name, price.right_price, duration.wrong_duration_negative,
             ("duration_minutes",), ErrorTypes.GREATER_THAN_EQUAL, ErrorMessages.DURATION_TOO_LOW),
            (name.right_name, price.right_price, duration.wrong_duration_negative_small,
             ("duration_minutes",), ErrorTypes.GREATER_THAN_EQUAL, ErrorMessages.DURATION_TOO_LOW),
            (name.right_name, price.right_price, duration.wrong_duration_negative_big,
             ("duration_minutes",), ErrorTypes.GREATER_THAN_EQUAL, ErrorMessages.DURATION_TOO_LOW),
            (name.right_name, price.right_price, duration.wrong_duration_big,
             ("duration_minutes",), ErrorTypes.LESS_THAN_EQUAL, ErrorMessages.DURATION_TOO_HIGH),
            (name.right_name, price.right_price, duration.wrong_duration_float,
             ("duration_minutes",), ErrorTypes.INT_FROM_FLOAT, ErrorMessages.DURATION_NOT_INT),
        ]
    )
    def test_create_service_wrong(
            self,
            name,
            price,
            duration_minutes,
            error_loc,
            error_type,
            error_msg,
    ):
        with pytest.raises(ValidationError) as error:
            service = ServiceCreate(
                name=name,
                price=price,
                duration_minutes=duration_minutes,
                category_id=1,
                description="Some description",
            )
        errors = error.value.errors()
        assert len(errors) == 1
        error = errors[0]
        assert error["type"] == error_type
        assert error_msg in error["msg"]