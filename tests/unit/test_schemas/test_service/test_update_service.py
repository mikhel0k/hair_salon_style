import decimal
import pytest
from pydantic import ValidationError

from app.schemas.Service import ServiceUpdate
from conftest import Name, Price, Duration
from tests.unit.test_schemas.conftest_exceptions import ErrorMessages, ErrorTypes, DataForId


class TestUpdateService:
    name = Name()
    price = Price()
    duration = Duration()
    data_for_id = DataForId()

    @pytest.mark.parametrize(
        "name, price, duration_minutes, category_id, description", [
            (name.right_name, price.right_price, duration.right_duration, data_for_id.right_id, "Some description"),
            (name.right_name_short, price.right_price, duration.right_duration, data_for_id.right_id, "Some description"),
            (name.right_name_long, price.right_price, duration.right_duration, data_for_id.right_id, "Some description"),
            (name.right_name_сyrillic, price.right_price, duration.right_duration, data_for_id.right_id, "Some description"),
            (name.right_name, price.right_price_small, duration.right_duration, data_for_id.right_id, "Some description"),
            (name.right_name, price.right_price_big, duration.right_duration, data_for_id.right_id, "Some description"),
            (name.right_name, price.right_price_float, duration.right_duration, data_for_id.right_id, "Some description"),
            (name.right_name, price.right_price_three_numbers_after_coma, duration.right_duration, data_for_id.right_id,
             "Some description"),
            (name.right_name, price.right_price_string, duration.right_duration, data_for_id.right_id, "Some description"),
            (name.right_name, price.right_price_string_with_coma, duration.right_duration, data_for_id.right_id, "Some description"),
            (name.right_name, price.right_price, duration.right_duration_small, data_for_id.right_id, "Some description"),
            (name.right_name, price.right_price, duration.right_duration_big, data_for_id.right_id, "Some description"),
            (name.right_name, price.right_price, duration.right_duration_string, data_for_id.right_id, "Some description"),
            (name.right_name, price.right_price, duration.right_duration, data_for_id.big_right_id, "Some description"),
            (name.right_name, None, None, None, None),
            (None, price.right_price, None, None, None),
            (None, None, duration.right_duration, None, None),
            (None, None, None, data_for_id.right_id, None),
            (None, None, None, None, "Some description"),
        ]
    )
    def test_update_service(
            self,
            name,
            price,
            duration_minutes,
            category_id,
            description,
    ):
        service = ServiceUpdate(
            name=name,
            price=price,
            duration_minutes=duration_minutes,
            category_id=category_id,
            description=description,
        )
        assert isinstance(service, ServiceUpdate)
        if name:
            assert service.name == name.title()
        else:
            assert service.name is None

        if price:
            assert service.price == decimal.Decimal(str(price))
        else:
            assert service.price is None

        if duration_minutes:
            assert service.duration_minutes == int(duration_minutes)
        else:
            assert service.duration_minutes is None

        assert service.category_id == category_id
        assert service.description == description

    @pytest.mark.parametrize(
        "name, price, duration_minutes, category_id, error_loc, error_type, error_msg", [
            (name.wrong_name_long, price.right_price, duration.right_duration, data_for_id.right_id,
            ("name",), ErrorTypes.STRING_TOO_LONG, ErrorMessages.STRING_TOO_LONG),
            (name.wrong_name_short, price.right_price, duration.right_duration, data_for_id.right_id,
            ("name",), ErrorTypes.STRING_TOO_SHORT, ErrorMessages.STRING_TOO_SHORT),
            (name.wrong_name_int, price.right_price, duration.right_duration, data_for_id.right_id,
            ("name",), ErrorTypes.STRING_TYPE, ErrorMessages.STRING_TYPE),
            (name.wrong_name_empty, price.right_price, duration.right_duration, data_for_id.right_id,
            ("name",), ErrorTypes.STRING_TOO_SHORT, ErrorMessages.STRING_TOO_SHORT),
            (name.wrong_name_spaces, price.right_price, duration.right_duration, data_for_id.right_id,
            ("name",), ErrorTypes.STRING_TOO_SHORT, ErrorMessages.STRING_TOO_SHORT),
            (name.wrong_invalid_character, price.right_price, duration.right_duration, data_for_id.right_id,
            ("name",), ErrorTypes.VALUE_ERROR, ErrorMessages.WRONG_INVALID_CHARACTER),
            (name.wrong_consecutive_spaces, price.right_price, duration.right_duration, data_for_id.right_id,
            ("name",), ErrorTypes.VALUE_ERROR, ErrorMessages.WRONG_CONSECUTIVE_SPACES),
            (name.wrong_consecutive_hyphens, price.right_price, duration.right_duration, data_for_id.right_id,
            ("name",), ErrorTypes.VALUE_ERROR, ErrorMessages.WRONG_CONSECUTIVE_HYPHENS),
            (name.wrong_consecutive_apostrophes, price.right_price, duration.right_duration, data_for_id.right_id,
            ("name",), ErrorTypes.VALUE_ERROR, ErrorMessages.WRONG_CONSECUTIVE_APOSTROPHES),
            (name.wrong_consecutive_underscores, price.right_price, duration.right_duration, data_for_id.right_id,
            ("name",), ErrorTypes.VALUE_ERROR, ErrorMessages.WRONG_CONSECUTIVE_UNDERSCORES),
            (name.wrong_start_with_hyphen, price.right_price, duration.right_duration, data_for_id.right_id,
            ("name",), ErrorTypes.VALUE_ERROR, ErrorMessages.WRONG_START_WITH_HYPHEN),
            (name.wrong_start_with_apostrophe, price.right_price, duration.right_duration, data_for_id.right_id,
            ("name",), ErrorTypes.VALUE_ERROR, ErrorMessages.WRONG_START_WITH_APOSTROPHE),
            (name.wrong_start_with_underscore, price.right_price, duration.right_duration, data_for_id.right_id,
            ("name",), ErrorTypes.VALUE_ERROR, ErrorMessages.WRONG_START_WITH_UNDERSCORE),
            (name.wrong_end_with_hyphen, price.right_price, duration.right_duration, data_for_id.right_id,
            ("name",), ErrorTypes.VALUE_ERROR, ErrorMessages.WRONG_END_WITH_HYPHEN),
            (name.wrong_end_with_apostrophe, price.right_price, duration.right_duration, data_for_id.right_id,
            ("name",), ErrorTypes.VALUE_ERROR, ErrorMessages.WRONG_END_WITH_APOSTROPHE),
            (name.wrong_end_with_underscore, price.right_price, duration.right_duration, data_for_id.right_id,
            ("name",), ErrorTypes.VALUE_ERROR, ErrorMessages.WRONG_END_WITH_UNDERSCORE),
            (name.wrong_space_and_hyphen_adjacent, price.right_price, duration.right_duration, data_for_id.right_id,
            ("name",), ErrorTypes.VALUE_ERROR, ErrorMessages.WRONG_SPACE_AND_HYPHEN_ADJACENT),
            (name.wrong_space_and_apostrophe_adjacent, price.right_price, duration.right_duration, data_for_id.right_id,
            ("name",), ErrorTypes.VALUE_ERROR, ErrorMessages.WRONG_SPACE_AND_APOSTROPHE_ADJACENT),
            (name.wrong_space_and_underscore_adjacent, price.right_price, duration.right_duration, data_for_id.right_id,
            ("name",), ErrorTypes.VALUE_ERROR, ErrorMessages.WRONG_SPACE_AND_UNDERSCORE_ADJACENT),
            (name.wrong_hyphen_and_space_adjacent, price.right_price, duration.right_duration, data_for_id.right_id,
            ("name",), ErrorTypes.VALUE_ERROR, ErrorMessages.WRONG_SPACE_AND_HYPHEN_ADJACENT),
            (name.wrong_apostrophe_and_space_adjacent, price.right_price, duration.right_duration, data_for_id.right_id,
            ("name",), ErrorTypes.VALUE_ERROR, ErrorMessages.WRONG_SPACE_AND_APOSTROPHE_ADJACENT),
            (name.wrong_underscore_and_space_adjacent, price.right_price, duration.right_duration, data_for_id.right_id,
            ("name",), ErrorTypes.VALUE_ERROR, ErrorMessages.WRONG_SPACE_AND_UNDERSCORE_ADJACENT),
            (name.right_name, price.wrong_price_zero, duration.right_duration, data_for_id.right_id,
            ("price",), ErrorTypes.GREATER_THAN_EQUAL, ErrorMessages.PRICE_TOO_LOW),
            (name.right_name, price.wrong_price_negative, duration.right_duration, data_for_id.right_id,
            ("price",), ErrorTypes.GREATER_THAN_EQUAL, ErrorMessages.PRICE_TOO_LOW),
            (name.right_name, price.wrong_price_negative_small, duration.right_duration, data_for_id.right_id,
            ("price",), ErrorTypes.GREATER_THAN_EQUAL, ErrorMessages.PRICE_TOO_LOW),
            (name.right_name, price.wrong_price_negative_big, duration.right_duration, data_for_id.right_id,
            ("price",), ErrorTypes.GREATER_THAN_EQUAL, ErrorMessages.PRICE_TOO_LOW),
            (name.right_name, price.wrong_price_big, duration.right_duration, data_for_id.right_id,
            ("price",), ErrorTypes.LESS_THAN_EQUAL, ErrorMessages.PRICE_TOO_HIGH),
            (name.right_name, price.wrong_price_negative_float, duration.right_duration, data_for_id.right_id,
            ("price",), ErrorTypes.GREATER_THAN_EQUAL, ErrorMessages.PRICE_TOO_LOW),
            (name.right_name, price.wrong_price_negative_three_numbers_after_coma, duration.right_duration, data_for_id.right_id,
            ("price",), ErrorTypes.GREATER_THAN_EQUAL, ErrorMessages.PRICE_TOO_LOW),
            (name.right_name, price.wrong_price_string, duration.right_duration, data_for_id.right_id,
            ("price",), ErrorTypes.DECIMAL_PARSING, ErrorMessages.PRICE_NOT_DECIMAL),
            (name.right_name, price.right_price, duration.wrong_duration_zero, data_for_id.right_id,
            ("duration_minutes",), ErrorTypes.GREATER_THAN_EQUAL, ErrorMessages.DURATION_TOO_LOW),
            (name.right_name, price.right_price, duration.wrong_duration_negative, data_for_id.right_id,
            ("duration_minutes",), ErrorTypes.GREATER_THAN_EQUAL, ErrorMessages.DURATION_TOO_LOW),
            (name.right_name, price.right_price, duration.wrong_duration_negative_small, data_for_id.right_id,
            ("duration_minutes",), ErrorTypes.GREATER_THAN_EQUAL, ErrorMessages.DURATION_TOO_LOW),
            (name.right_name, price.right_price, duration.wrong_duration_negative_big, data_for_id.right_id,
            ("duration_minutes",), ErrorTypes.GREATER_THAN_EQUAL, ErrorMessages.DURATION_TOO_LOW),
            (name.right_name, price.right_price, duration.wrong_duration_big, data_for_id.right_id,
            ("duration_minutes",), ErrorTypes.LESS_THAN_EQUAL, ErrorMessages.DURATION_TOO_HIGH),
            (name.right_name, price.right_price, duration.wrong_duration_float, data_for_id.right_id,
            ("duration_minutes",), ErrorTypes.INT_FROM_FLOAT, ErrorMessages.DURATION_NOT_INT),
            (name.right_name, price.right_price, duration.right_duration, data_for_id.wrong_id_zero,
            ("category_id",), ErrorTypes.GREATER_THAN_EQUAL, ErrorMessages.ID_GREATER_ONE),
            (name.right_name, price.right_price, duration.right_duration, data_for_id.wrong_negative_id,
            ("category_id",), ErrorTypes.GREATER_THAN_EQUAL, ErrorMessages.ID_GREATER_ONE),
            (name.right_name, price.right_price, duration.right_duration, data_for_id.big_wrong_negative_id,
            ("category_id",), ErrorTypes.GREATER_THAN_EQUAL, ErrorMessages.ID_GREATER_ONE),
            (name.right_name, price.right_price, duration.right_duration, data_for_id.wrong_id_str,
            ("category_id",), ErrorTypes.INT_TYPE, ErrorMessages.INT_TYPE),
            (name.right_name, price.right_price, duration.right_duration, data_for_id.wrong_id_float,
            ("category_id",), ErrorTypes.INT_TYPE, ErrorMessages.INT_TYPE),
            (name.right_name, price.right_price, duration.right_duration, data_for_id.wrong_id_true,
            ("category_id",), ErrorTypes.INT_TYPE, ErrorMessages.INT_TYPE),
            (name.right_name, price.right_price, duration.right_duration, data_for_id.wrong_id_false,
            ("category_id",), ErrorTypes.INT_TYPE, ErrorMessages.INT_TYPE),
        ]
    )
    def test_update_service_wrong(
            self,
            name,
            price,
            duration_minutes,
            category_id,
            error_loc,
            error_type,
            error_msg,
    ):
        with pytest.raises(ValidationError) as error:
            service = ServiceUpdate(
                name=name,
                price=price,
                duration_minutes=duration_minutes,
                category_id=category_id,
                description="Some description",
            )
        errors = error.value.errors()
        assert len(errors) == 1
        error = errors[0]
        assert error["loc"] == error_loc
        assert error["type"] == error_type
        assert error_msg in error["msg"]