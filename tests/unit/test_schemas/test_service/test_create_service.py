import decimal
import pytest
from pydantic import ValidationError

from app.schemas.Service import ServiceCreate
from tests.unit.test_schemas.conftest import assert_single_validation_error
from tests.unit.test_schemas.test_service.conftest import Name, Price, Duration
from tests.unit.test_schemas.conftest_exceptions import ErrorMessages, ErrorTypes, DataForId

name = Name()
price = Price()
duration = Duration()
data_for_id = DataForId()


class TestCreateService:

    @pytest.mark.parametrize(
        "name, price, duration_minutes, category_id, description", [
            (name.correct_name, price.correct_price, duration.correct_duration, data_for_id.correct_id, "Some description"),
            (name.correct_name_short, price.correct_price, duration.correct_duration, data_for_id.correct_id, "Some description"),
            (name.correct_name_long, price.correct_price, duration.correct_duration, data_for_id.correct_id, "Some description"),
            (name.correct_name_cyrillic, price.correct_price, duration.correct_duration, data_for_id.correct_id, "Some description"),
            (name.correct_name, price.correct_price_small, duration.correct_duration, data_for_id.correct_id, "Some description"),
            (name.correct_name, price.correct_price_big, duration.correct_duration, data_for_id.correct_id, "Some description"),
            (name.correct_name, price.correct_price_float, duration.correct_duration, data_for_id.correct_id, "Some description"),
            (name.correct_name, price.correct_price_three_numbers_after_coma, duration.correct_duration, data_for_id.correct_id,
             "Some description"),
            (name.correct_name, price.correct_price_string, duration.correct_duration, data_for_id.correct_id, "Some description"),
            (name.correct_name, price.correct_price_string_with_coma, duration.correct_duration, data_for_id.correct_id, "Some description"),
            (name.correct_name, price.correct_price, duration.correct_duration_small, data_for_id.correct_id, "Some description"),
            (name.correct_name, price.correct_price, duration.correct_duration_big, data_for_id.correct_id, "Some description"),
            (name.correct_name, price.correct_price, duration.correct_duration_string, data_for_id.correct_id, "Some description"),
            (name.correct_name, price.correct_price, duration.correct_duration_string, data_for_id.big_correct_id, "Some description"),
        ]
    )
    def test_create_service_correct(
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
            (name.wrong_name_long, price.correct_price, duration.correct_duration,
            ("name",), ErrorTypes.STRING_TOO_LONG, ErrorMessages.STRING_TOO_LONG),
            (name.wrong_name_short, price.correct_price, duration.correct_duration,
            ("name",), ErrorTypes.STRING_TOO_SHORT, ErrorMessages.STRING_TOO_SHORT),
            (name.wrong_name_int, price.correct_price, duration.correct_duration,
            ("name",), ErrorTypes.STRING_TYPE, ErrorMessages.STRING_TYPE),
            (name.wrong_name_empty, price.correct_price, duration.correct_duration,
            ("name",), ErrorTypes.STRING_TOO_SHORT, ErrorMessages.STRING_TOO_SHORT),
            (name.wrong_name_spaces, price.correct_price, duration.correct_duration,
            ("name",), ErrorTypes.STRING_TOO_SHORT, ErrorMessages.STRING_TOO_SHORT),
            (name.wrong_name_none, price.correct_price, duration.correct_duration,
            ("name",), ErrorTypes.STRING_TYPE, ErrorMessages.STRING_TYPE),
            (name.wrong_invalid_character, price.correct_price, duration.correct_duration,
            ("name",), ErrorTypes.VALUE_ERROR, ErrorMessages.WRONG_INVALID_CHARACTER),
            (name.wrong_consecutive_spaces, price.correct_price, duration.correct_duration,
            ("name",), ErrorTypes.VALUE_ERROR, ErrorMessages.WRONG_CONSECUTIVE_SPACES),
            (name.wrong_consecutive_hyphens, price.correct_price, duration.correct_duration,
            ("name",), ErrorTypes.VALUE_ERROR, ErrorMessages.WRONG_CONSECUTIVE_HYPHENS),
            (name.wrong_consecutive_apostrophes, price.correct_price, duration.correct_duration,
            ("name",), ErrorTypes.VALUE_ERROR, ErrorMessages.WRONG_CONSECUTIVE_APOSTROPHES),
            (name.wrong_consecutive_underscores, price.correct_price, duration.correct_duration,
            ("name",), ErrorTypes.VALUE_ERROR, ErrorMessages.WRONG_CONSECUTIVE_UNDERSCORES),
            (name.wrong_start_with_hyphen, price.correct_price, duration.correct_duration,
            ("name",), ErrorTypes.VALUE_ERROR, ErrorMessages.WRONG_START_WITH_HYPHEN),
            (name.wrong_start_with_apostrophe, price.correct_price, duration.correct_duration,
            ("name",), ErrorTypes.VALUE_ERROR, ErrorMessages.WRONG_START_WITH_APOSTROPHE),
            (name.wrong_start_with_underscore, price.correct_price, duration.correct_duration,
            ("name",), ErrorTypes.VALUE_ERROR, ErrorMessages.WRONG_START_WITH_UNDERSCORE),
            (name.wrong_end_with_hyphen, price.correct_price, duration.correct_duration,
            ("name",), ErrorTypes.VALUE_ERROR, ErrorMessages.WRONG_END_WITH_HYPHEN),
            (name.wrong_end_with_apostrophe, price.correct_price, duration.correct_duration,
            ("name",), ErrorTypes.VALUE_ERROR, ErrorMessages.WRONG_END_WITH_APOSTROPHE),
            (name.wrong_end_with_underscore, price.correct_price, duration.correct_duration,
            ("name",), ErrorTypes.VALUE_ERROR, ErrorMessages.WRONG_END_WITH_UNDERSCORE),
            (name.wrong_space_and_hyphen_adjacent, price.correct_price, duration.correct_duration,
            ("name",), ErrorTypes.VALUE_ERROR, ErrorMessages.WRONG_SPACE_AND_HYPHEN_ADJACENT),
            (name.wrong_space_and_apostrophe_adjacent, price.correct_price, duration.correct_duration,
            ("name",), ErrorTypes.VALUE_ERROR, ErrorMessages.WRONG_SPACE_AND_APOSTROPHE_ADJACENT),
            (name.wrong_space_and_underscore_adjacent, price.correct_price, duration.correct_duration,
            ("name",), ErrorTypes.VALUE_ERROR, ErrorMessages.WRONG_SPACE_AND_UNDERSCORE_ADJACENT),
            (name.wrong_hyphen_and_space_adjacent, price.correct_price, duration.correct_duration,
            ("name",), ErrorTypes.VALUE_ERROR, ErrorMessages.WRONG_SPACE_AND_HYPHEN_ADJACENT),
            (name.wrong_apostrophe_and_space_adjacent, price.correct_price, duration.correct_duration,
            ("name",), ErrorTypes.VALUE_ERROR, ErrorMessages.WRONG_SPACE_AND_APOSTROPHE_ADJACENT),
            (name.wrong_underscore_and_space_adjacent, price.correct_price, duration.correct_duration,
            ("name",), ErrorTypes.VALUE_ERROR, ErrorMessages.WRONG_SPACE_AND_UNDERSCORE_ADJACENT),
            (name.correct_name, price.wrong_price_zero, duration.correct_duration,
            ("price",), ErrorTypes.GREATER_THAN_EQUAL, ErrorMessages.PRICE_TOO_LOW),
            (name.correct_name, price.wrong_price_negative, duration.correct_duration,
            ("price",), ErrorTypes.GREATER_THAN_EQUAL, ErrorMessages.PRICE_TOO_LOW),
            (name.correct_name, price.wrong_price_negative_small, duration.correct_duration,
            ("price",), ErrorTypes.GREATER_THAN_EQUAL, ErrorMessages.PRICE_TOO_LOW),
            (name.correct_name, price.wrong_price_negative_big, duration.correct_duration,
            ("price",), ErrorTypes.GREATER_THAN_EQUAL, ErrorMessages.PRICE_TOO_LOW),
            (name.correct_name, price.wrong_price_big, duration.correct_duration,
            ("price",), ErrorTypes.LESS_THAN_EQUAL, ErrorMessages.PRICE_TOO_HIGH),
            (name.correct_name, price.wrong_price_negative_float, duration.correct_duration,
            ("price",), ErrorTypes.GREATER_THAN_EQUAL, ErrorMessages.PRICE_TOO_LOW),
            (name.correct_name, price.wrong_price_negative_three_numbers_after_coma, duration.correct_duration,
            ("price",), ErrorTypes.GREATER_THAN_EQUAL, ErrorMessages.PRICE_TOO_LOW),
            (name.correct_name, price.wrong_price_string, duration.correct_duration,
            ("price",), ErrorTypes.DECIMAL_PARSING, ErrorMessages.PRICE_NOT_DECIMAL),
            (name.correct_name, price.wrong_price_none, duration.correct_duration,
            ("price",), ErrorTypes.DECIMAL_TYPE, ErrorMessages.PRICE_NONE_TYPE),
            (name.correct_name, price.correct_price, duration.wrong_duration_zero,
            ("duration_minutes",), ErrorTypes.GREATER_THAN_EQUAL, ErrorMessages.DURATION_TOO_LOW),
            (name.correct_name, price.correct_price, duration.wrong_duration_negative,
            ("duration_minutes",), ErrorTypes.GREATER_THAN_EQUAL, ErrorMessages.DURATION_TOO_LOW),
            (name.correct_name, price.correct_price, duration.wrong_duration_negative_small,
            ("duration_minutes",), ErrorTypes.GREATER_THAN_EQUAL, ErrorMessages.DURATION_TOO_LOW),
            (name.correct_name, price.correct_price, duration.wrong_duration_negative_big,
            ("duration_minutes",), ErrorTypes.GREATER_THAN_EQUAL, ErrorMessages.DURATION_TOO_LOW),
            (name.correct_name, price.correct_price, duration.wrong_duration_big,
            ("duration_minutes",), ErrorTypes.LESS_THAN_EQUAL, ErrorMessages.DURATION_TOO_HIGH),
            (name.correct_name, price.correct_price, duration.wrong_duration_float,
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
        with pytest.raises(ValidationError) as exc_info:
            ServiceCreate(
                name=name,
                price=price,
                duration_minutes=duration_minutes,
                category_id=1,
                description="Some description",
            )
        assert_single_validation_error(exc_info.value.errors(), error_loc, error_type, error_msg)