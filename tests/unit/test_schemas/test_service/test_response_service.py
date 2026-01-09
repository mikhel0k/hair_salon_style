import decimal
import pytest
from pydantic import ValidationError

from app.schemas.Service import ServiceResponse
from app.models.Service import Service
from conftest import Name, Price, Duration
from tests.unit.test_schemas.conftest_exceptions import ErrorMessages, ErrorTypes


class TestResponseService:
    name = Name()
    price = Price()
    duration = Duration()

    @pytest.mark.parametrize(
        "service, name, price, duration_minutes, category_id, description", [
            (Service(id=1, name=name.right_name, price=price.right_price, duration_minutes=duration.right_duration,
                     category_id=1, description="Some description"),
             name.right_name, price.right_price, duration.right_duration, 1, "Some description"),
            (Service(id=1, name=name.right_name_short, price=price.right_price,
                     duration_minutes=duration.right_duration,
                     category_id=1, description="Some description"),
             name.right_name_short, price.right_price, duration.right_duration, 1, "Some description"),
            (Service(id=1, name=name.right_name_long, price=price.right_price, duration_minutes=duration.right_duration,
                     category_id=1, description="Some description"),
             name.right_name_long, price.right_price, duration.right_duration, 1, "Some description"),
            (Service(id=1, name=name.right_name_сyrillic, price=price.right_price,
                     duration_minutes=duration.right_duration,
                     category_id=1, description="Some description"),
             name.right_name_сyrillic, price.right_price, duration.right_duration, 1, "Some description"),
            (Service(id=1, name=name.right_name, price=price.right_price_small,
                     duration_minutes=duration.right_duration,
                     category_id=1, description="Some description"),
             name.right_name, price.right_price_small, duration.right_duration, 1, "Some description"),
            (Service(id=1, name=name.right_name, price=price.right_price_big, duration_minutes=duration.right_duration,
                     category_id=1, description="Some description"),
             name.right_name, price.right_price_big, duration.right_duration, 1, "Some description"),
            (Service(id=1, name=name.right_name, price=price.right_price_float,
                     duration_minutes=duration.right_duration,
                     category_id=1, description="Some description"),
             name.right_name, price.right_price_float, duration.right_duration, 1, "Some description"),
            (Service(id=1, name=name.right_name, price=price.right_price_three_numbers_after_coma,
                     duration_minutes=duration.right_duration,
                     category_id=1, description="Some description"),
             name.right_name, price.right_price_three_numbers_after_coma, duration.right_duration, 1,
             "Some description"),
            (Service(id=1, name=name.right_name, price=price.right_price_string,
                     duration_minutes=duration.right_duration,
                     category_id=1, description="Some description"),
             name.right_name, price.right_price_string, duration.right_duration, 1, "Some description"),
            (Service(id=1, name=name.right_name, price=price.right_price_string_with_coma,
                     duration_minutes=duration.right_duration,
                     category_id=1, description="Some description"),
             name.right_name, price.right_price_string_with_coma, duration.right_duration, 1, "Some description"),
            (Service(id=1, name=name.right_name, price=price.right_price,
                     duration_minutes=duration.right_duration_small,
                     category_id=1, description="Some description"),
             name.right_name, price.right_price, duration.right_duration_small, 1, "Some description"),
            (Service(id=1, name=name.right_name, price=price.right_price, duration_minutes=duration.right_duration_big,
                     category_id=1, description="Some description"),
             name.right_name, price.right_price, duration.right_duration_big, 1, "Some description"),
            (Service(id=1, name=name.right_name, price=price.right_price,
                     duration_minutes=duration.right_duration_string,
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
        assert service_response.name == name.title()
        assert service_response.price == decimal.Decimal(str(price))
        assert service_response.duration_minutes == int(duration_minutes)
        assert service_response.category_id == category_id
        assert service_response.description == description

    @pytest.mark.parametrize(
        "service, error_loc, error_type, error_msg", [
            (Service(id=1, name=name.wrong_name_long, price=price.right_price,
                 duration_minutes=duration.right_duration, category_id=1, description="Some description"),
            ("name",), ErrorTypes.STRING_TOO_LONG, ErrorMessages.STRING_TOO_LONG),
            (Service(id=1, name=name.wrong_name_short, price=price.right_price,
                 duration_minutes=duration.right_duration, category_id=1, description="Some description"),
            ("name",), ErrorTypes.STRING_TOO_SHORT, ErrorMessages.STRING_TOO_SHORT),
            (Service(id=1, name=name.wrong_name_int, price=price.right_price,
                 duration_minutes=duration.right_duration, category_id=1, description="Some description"),
            ("name",), ErrorTypes.STRING_TYPE, ErrorMessages.STRING_TYPE),
            (Service(id=1, name=name.wrong_name_empty, price=price.right_price,
                 duration_minutes=duration.right_duration, category_id=1, description="Some description"),
            ("name",), ErrorTypes.STRING_TOO_SHORT, ErrorMessages.STRING_EMPTY),
            (Service(id=1, name=name.wrong_name_spaces, price=price.right_price,
                 duration_minutes=duration.right_duration, category_id=1, description="Some description"),
            ("name",), ErrorTypes.STRING_TOO_SHORT, ErrorMessages.STRING_SPACES),
            (Service(id=1, name=name.wrong_name_none, price=price.right_price,
                 duration_minutes=duration.right_duration, category_id=1, description="Some description"),
            ("name",), ErrorTypes.STRING_TYPE, ErrorMessages.STRING_TYPE),
            (Service(id=1, name=name.wrong_invalid_character, price=price.right_price,
                     duration_minutes=duration.right_duration, category_id=1, description="Some description"),
             ("name",), ErrorTypes.VALUE_ERROR, ErrorMessages.WRONG_INVALID_CHARACTER),
            (Service(id=1, name=name.wrong_consecutive_spaces, price=price.right_price,
                     duration_minutes=duration.right_duration, category_id=1, description="Some description"),
             ("name",), ErrorTypes.VALUE_ERROR, ErrorMessages.WRONG_CONSECUTIVE_SPACES),
            (Service(id=1, name=name.wrong_consecutive_hyphens, price=price.right_price,
                     duration_minutes=duration.right_duration, category_id=1, description="Some description"),
             ("name",), ErrorTypes.VALUE_ERROR, ErrorMessages.WRONG_CONSECUTIVE_HYPHENS),
            (Service(id=1, name=name.wrong_consecutive_apostrophes, price=price.right_price,
                     duration_minutes=duration.right_duration, category_id=1, description="Some description"),
             ("name",), ErrorTypes.VALUE_ERROR, ErrorMessages.WRONG_CONSECUTIVE_APOSTROPHES),
            (Service(id=1, name=name.wrong_consecutive_underscores, price=price.right_price,
                     duration_minutes=duration.right_duration, category_id=1, description="Some description"),
             ("name",), ErrorTypes.VALUE_ERROR, ErrorMessages.WRONG_CONSECUTIVE_UNDERSCORES),
            (Service(id=1, name=name.wrong_start_with_hyphen, price=price.right_price,
                     duration_minutes=duration.right_duration, category_id=1, description="Some description"),
             ("name",), ErrorTypes.VALUE_ERROR, ErrorMessages.WRONG_START_WITH_HYPHEN),
            (Service(id=1, name=name.wrong_start_with_apostrophe, price=price.right_price,
                     duration_minutes=duration.right_duration, category_id=1, description="Some description"),
             ("name",), ErrorTypes.VALUE_ERROR, ErrorMessages.WRONG_START_WITH_APOSTROPHE),
            (Service(id=1, name=name.wrong_start_with_underscore, price=price.right_price,
                     duration_minutes=duration.right_duration, category_id=1, description="Some description"),
             ("name",), ErrorTypes.VALUE_ERROR, ErrorMessages.WRONG_START_WITH_UNDERSCORE),
            (Service(id=1, name=name.wrong_end_with_hyphen, price=price.right_price,
                     duration_minutes=duration.right_duration, category_id=1, description="Some description"),
             ("name",), ErrorTypes.VALUE_ERROR, ErrorMessages.WRONG_END_WITH_HYPHEN),
            (Service(id=1, name=name.wrong_end_with_apostrophe, price=price.right_price,
                     duration_minutes=duration.right_duration, category_id=1, description="Some description"),
             ("name",), ErrorTypes.VALUE_ERROR, ErrorMessages.WRONG_END_WITH_APOSTROPHE),
            (Service(id=1, name=name.wrong_end_with_underscore, price=price.right_price,
                     duration_minutes=duration.right_duration, category_id=1, description="Some description"),
             ("name",), ErrorTypes.VALUE_ERROR, ErrorMessages.WRONG_END_WITH_UNDERSCORE),
            (Service(id=1, name=name.wrong_space_and_hyphen_adjacent, price=price.right_price,
                     duration_minutes=duration.right_duration, category_id=1, description="Some description"),
             ("name",), ErrorTypes.VALUE_ERROR, ErrorMessages.WRONG_SPACE_AND_HYPHEN_ADJACENT),
            (Service(id=1, name=name.wrong_space_and_apostrophe_adjacent, price=price.right_price,
                     duration_minutes=duration.right_duration, category_id=1, description="Some description"),
             ("name",), ErrorTypes.VALUE_ERROR, ErrorMessages.WRONG_SPACE_AND_APOSTROPHE_ADJACENT),
            (Service(id=1, name=name.wrong_space_and_underscore_adjacent, price=price.right_price,
                     duration_minutes=duration.right_duration, category_id=1, description="Some description"),
             ("name",), ErrorTypes.VALUE_ERROR, ErrorMessages.WRONG_SPACE_AND_UNDERSCORE_ADJACENT),
            (Service(id=1, name=name.wrong_hyphen_and_space_adjacent, price=price.right_price,
                     duration_minutes=duration.right_duration, category_id=1, description="Some description"),
             ("name",), ErrorTypes.VALUE_ERROR, ErrorMessages.WRONG_SPACE_AND_HYPHEN_ADJACENT),
            (Service(id=1, name=name.wrong_apostrophe_and_space_adjacent, price=price.right_price,
                     duration_minutes=duration.right_duration, category_id=1, description="Some description"),
             ("name",), ErrorTypes.VALUE_ERROR, ErrorMessages.WRONG_SPACE_AND_APOSTROPHE_ADJACENT),
            (Service(id=1, name=name.wrong_underscore_and_space_adjacent, price=price.right_price,
                     duration_minutes=duration.right_duration, category_id=1, description="Some description"),
             ("name",), ErrorTypes.VALUE_ERROR, ErrorMessages.WRONG_SPACE_AND_UNDERSCORE_ADJACENT),
            (Service(id=1, name=name.right_name, price=price.wrong_price_zero,
                 duration_minutes=duration.right_duration, category_id=1, description="Some description"),
            ("price",), ErrorTypes.GREATER_THAN_EQUAL, ErrorMessages.PRICE_TOO_LOW),
            (Service(id=1, name=name.right_name, price=price.wrong_price_negative,
                 duration_minutes=duration.right_duration, category_id=1, description="Some description"),
            ("price",), ErrorTypes.GREATER_THAN_EQUAL, ErrorMessages.PRICE_TOO_LOW),
            (Service(id=1, name=name.right_name, price=price.wrong_price_negative_small,
                 duration_minutes=duration.right_duration, category_id=1, description="Some description"),
            ("price",), ErrorTypes.GREATER_THAN_EQUAL, ErrorMessages.PRICE_TOO_LOW),
            (Service(id=1, name=name.right_name, price=price.wrong_price_negative_big,
                 duration_minutes=duration.right_duration, category_id=1, description="Some description"),
            ("price",), ErrorTypes.GREATER_THAN_EQUAL, ErrorMessages.PRICE_TOO_LOW),
            (Service(id=1, name=name.right_name, price=price.wrong_price_big,
                 duration_minutes=duration.right_duration, category_id=1, description="Some description"),
            ("price",), ErrorTypes.LESS_THAN_EQUAL, ErrorMessages.PRICE_TOO_HIGH),
            (Service(id=1, name=name.right_name, price=price.wrong_price_negative_float,
                 duration_minutes=duration.right_duration, category_id=1, description="Some description"),
            ("price",), ErrorTypes.GREATER_THAN_EQUAL, ErrorMessages.PRICE_TOO_LOW),
            (Service(id=1, name=name.right_name, price=price.wrong_price_negative_three_numbers_after_coma,
                 duration_minutes=duration.right_duration, category_id=1, description="Some description"),
            ("price",), ErrorTypes.GREATER_THAN_EQUAL, ErrorMessages.PRICE_TOO_LOW),
            (Service(id=1, name=name.right_name, price=price.wrong_price_string,
                 duration_minutes=duration.right_duration, category_id=1, description="Some description"),
            ("price",), ErrorTypes.DECIMAL_PARSING, ErrorMessages.PRICE_NOT_DECIMAL),
            (Service(id=1, name=name.right_name, price=price.wrong_price_none,
                 duration_minutes=duration.right_duration, category_id=1, description="Some description"),
            ("price",), ErrorTypes.DECIMAL_TYPE, ErrorMessages.PRICE_NONE_TYPE),
            (Service(id=1, name=name.right_name, price=price.right_price,
                 duration_minutes=duration.wrong_duration_zero, category_id=1, description="Some description"),
            ("duration_minutes",), ErrorTypes.GREATER_THAN_EQUAL, ErrorMessages.DURATION_TOO_LOW),
            (Service(id=1, name=name.right_name, price=price.right_price,
                 duration_minutes=duration.wrong_duration_negative, category_id=1, description="Some description"),
            ("duration_minutes",), ErrorTypes.GREATER_THAN_EQUAL, ErrorMessages.DURATION_TOO_LOW),
            (Service(id=1, name=name.right_name, price=price.right_price,
                 duration_minutes=duration.wrong_duration_negative_small, category_id=1,
                 description="Some description"),
            ("duration_minutes",), ErrorTypes.GREATER_THAN_EQUAL, ErrorMessages.DURATION_TOO_LOW),
            (Service(id=1, name=name.right_name, price=price.right_price,
                 duration_minutes=duration.wrong_duration_negative_big, category_id=1,
                 description="Some description"),
            ("duration_minutes",), ErrorTypes.GREATER_THAN_EQUAL, ErrorMessages.DURATION_TOO_LOW),
            (Service(id=1, name=name.right_name, price=price.right_price,
                 duration_minutes=duration.wrong_duration_big, category_id=1, description="Some description"),
            ("duration_minutes",), ErrorTypes.LESS_THAN_EQUAL, ErrorMessages.DURATION_TOO_HIGH),
            (Service(id=1, name=name.right_name, price=price.right_price,
                 duration_minutes=duration.wrong_duration_float, category_id=1, description="Some description"),
            ("duration_minutes",), ErrorTypes.INT_FROM_FLOAT, ErrorMessages.DURATION_NOT_INT),

        ]
    )
    def test_response_service_wrong(
            self,
            service,
            error_loc,
            error_type,
            error_msg,
    ):
        with pytest.raises(ValidationError) as error:
            service_response = ServiceResponse.model_validate(service)
        errors = error.value.errors()
        assert len(errors) == 1
        error = errors[0]
        # assert error["loc"] == error_loc
        assert error["type"] == error_type
        assert error_msg in error["msg"]