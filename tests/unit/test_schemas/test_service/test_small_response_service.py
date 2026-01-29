import decimal
import pytest
from pydantic import ValidationError

from app.schemas.Service import ServiceResponseSmall
from app.models.Service import Service
from conftest import Name, Price
from tests.unit.test_schemas.conftest_exceptions import ErrorMessages, ErrorTypes, DataForId


class TestResponseServiceSmall:
    name = Name()
    price = Price()
    data_for_id = DataForId()

    @pytest.mark.parametrize(
        "service, service_id, name, price, description", [
            (Service(id=data_for_id.correct_id, name=name.correct_name, price=price.correct_price, description="Some description"),
             data_for_id.correct_id, name.correct_name, price.correct_price, "Some description"),
            (Service(id=data_for_id.correct_id, name=name.correct_name_short, price=price.correct_price, description="Some description"),
             data_for_id.correct_id, name.correct_name_short, price.correct_price, "Some description"),
            (Service(id=data_for_id.correct_id, name=name.correct_name_long, price=price.correct_price, description="Some description"),
             data_for_id.correct_id, name.correct_name_long, price.correct_price, "Some description"),
            (Service(id=data_for_id.correct_id, name=name.correct_name_сyrillic, price=price.correct_price, description="Some description"),
             data_for_id.correct_id, name.correct_name_сyrillic, price.correct_price, "Some description"),
            (Service(id=data_for_id.correct_id, name=name.correct_name, price=price.correct_price_small, description="Some description"),
             data_for_id.correct_id, name.correct_name, price.correct_price_small, "Some description"),
            (Service(id=data_for_id.correct_id, name=name.correct_name, price=price.correct_price_big, description="Some description"),
             data_for_id.correct_id, name.correct_name, price.correct_price_big, "Some description"),
            (Service(id=data_for_id.correct_id, name=name.correct_name, price=price.correct_price_float, description="Some description"),
             data_for_id.correct_id, name.correct_name, price.correct_price_float, "Some description"),
            (Service(id=data_for_id.correct_id, name=name.correct_name, price=price.correct_price_three_numbers_after_coma,
                     description="Some description"),
             data_for_id.correct_id, name.correct_name, price.correct_price_three_numbers_after_coma, "Some description"),
            (Service(id=data_for_id.correct_id, name=name.correct_name, price=price.correct_price_string, description="Some description"),
             data_for_id.correct_id, name.correct_name, price.correct_price_string, "Some description"),
            (Service(id=data_for_id.correct_id, name=name.correct_name, price=price.correct_price_string_with_coma,
                     description="Some description"),
             data_for_id.correct_id, name.correct_name, price.correct_price_string_with_coma, "Some description"),
            (Service(id=data_for_id.big_correct_id, name=name.correct_name, price=price.correct_price, description="Some description"),
             data_for_id.big_correct_id, name.correct_name, price.correct_price, "Some description"),
        ]
    )
    def test_response_service_small_correct(
            self,
            service,
            service_id,
            name,
            price,
            description,
    ):
        service_response = ServiceResponseSmall.model_validate(service)
        assert isinstance(service_response, ServiceResponseSmall)
        assert service_response.id == service_id
        assert service_response.name == name.title()
        assert service_response.price == decimal.Decimal(str(price))
        assert service_response.description == description

    @pytest.mark.parametrize(
        "service, error_loc, error_type, error_msg", [
            (Service(id=data_for_id.correct_id, name=name.wrong_name_long, price=price.correct_price, description="Some description"),
            ("name",), ErrorTypes.STRING_TOO_LONG, ErrorMessages.STRING_TOO_LONG),
            (Service(id=data_for_id.correct_id, name=name.wrong_name_short, price=price.correct_price, description="Some description"),
            ("name",), ErrorTypes.STRING_TOO_SHORT, ErrorMessages.STRING_TOO_SHORT),
            (Service(id=data_for_id.correct_id, name=name.wrong_name_int, price=price.correct_price, description="Some description"),
            ("name",), ErrorTypes.STRING_TYPE, ErrorMessages.STRING_TYPE),
            (Service(id=data_for_id.correct_id, name=name.wrong_name_empty, price=price.correct_price, description="Some description"),
            ("name",), ErrorTypes.STRING_TOO_SHORT, ErrorMessages.STRING_EMPTY),
            (Service(id=data_for_id.correct_id, name=name.wrong_name_spaces, price=price.correct_price, description="Some description"),
            ("name",), ErrorTypes.STRING_TOO_SHORT, ErrorMessages.STRING_SPACES),
            (Service(id=data_for_id.correct_id, name=name.wrong_name_none, price=price.correct_price, description="Some description"),
            ("name",), ErrorTypes.STRING_TYPE, ErrorMessages.STRING_TYPE),
            (Service(id=data_for_id.correct_id, name=name.wrong_invalid_character, price=price.correct_price, description="Some description"),
            ("name",), ErrorTypes.VALUE_ERROR, ErrorMessages.WRONG_INVALID_CHARACTER),
            (Service(id=data_for_id.correct_id, name=name.wrong_consecutive_spaces, price=price.correct_price, description="Some description"),
            ("name",), ErrorTypes.VALUE_ERROR, ErrorMessages.WRONG_CONSECUTIVE_SPACES),
            (Service(id=data_for_id.correct_id, name=name.wrong_consecutive_hyphens, price=price.correct_price, description="Some description"),
            ("name",), ErrorTypes.VALUE_ERROR, ErrorMessages.WRONG_CONSECUTIVE_HYPHENS),
            (Service(id=data_for_id.correct_id, name=name.wrong_consecutive_apostrophes, price=price.correct_price,description="Some description"),
            ("name",), ErrorTypes.VALUE_ERROR, ErrorMessages.WRONG_CONSECUTIVE_APOSTROPHES),
            (Service(id=data_for_id.correct_id, name=name.wrong_consecutive_underscores, price=price.correct_price, description="Some description"),
            ("name",), ErrorTypes.VALUE_ERROR, ErrorMessages.WRONG_CONSECUTIVE_UNDERSCORES),
            (Service(id=data_for_id.correct_id, name=name.wrong_start_with_hyphen, price=price.correct_price, description="Some description"),
            ("name",), ErrorTypes.VALUE_ERROR, ErrorMessages.WRONG_START_WITH_HYPHEN),
            (Service(id=data_for_id.correct_id, name=name.wrong_start_with_apostrophe, price=price.correct_price, description="Some description"),
            ("name",), ErrorTypes.VALUE_ERROR, ErrorMessages.WRONG_START_WITH_APOSTROPHE),
            (Service(id=data_for_id.correct_id, name=name.wrong_start_with_underscore, price=price.correct_price, description="Some description"),
            ("name",), ErrorTypes.VALUE_ERROR, ErrorMessages.WRONG_START_WITH_UNDERSCORE),
            (Service(id=data_for_id.correct_id, name=name.wrong_end_with_hyphen, price=price.correct_price, description="Some description"),
            ("name",), ErrorTypes.VALUE_ERROR, ErrorMessages.WRONG_END_WITH_HYPHEN),
            (Service(id=data_for_id.correct_id, name=name.wrong_end_with_apostrophe, price=price.correct_price, description="Some description"),
            ("name",), ErrorTypes.VALUE_ERROR, ErrorMessages.WRONG_END_WITH_APOSTROPHE),
            (Service(id=data_for_id.correct_id, name=name.wrong_end_with_underscore, price=price.correct_price, description="Some description"),
            ("name",), ErrorTypes.VALUE_ERROR, ErrorMessages.WRONG_END_WITH_UNDERSCORE),
            (Service(id=data_for_id.correct_id, name=name.wrong_space_and_hyphen_adjacent, price=price.correct_price, description="Some description"),
            ("name",), ErrorTypes.VALUE_ERROR, ErrorMessages.WRONG_SPACE_AND_HYPHEN_ADJACENT),
            (Service(id=data_for_id.correct_id, name=name.wrong_space_and_apostrophe_adjacent, price=price.correct_price, description="Some description"),
            ("name",), ErrorTypes.VALUE_ERROR, ErrorMessages.WRONG_SPACE_AND_APOSTROPHE_ADJACENT),
            (Service(id=data_for_id.correct_id, name=name.wrong_space_and_underscore_adjacent, price=price.correct_price, description="Some description"),
            ("name",), ErrorTypes.VALUE_ERROR, ErrorMessages.WRONG_SPACE_AND_UNDERSCORE_ADJACENT),
            (Service(id=data_for_id.correct_id, name=name.wrong_hyphen_and_space_adjacent, price=price.correct_price, description="Some description"),
            ("name",), ErrorTypes.VALUE_ERROR, ErrorMessages.WRONG_SPACE_AND_HYPHEN_ADJACENT),
            (Service(id=data_for_id.correct_id, name=name.wrong_apostrophe_and_space_adjacent, price=price.correct_price, description="Some description"),
            ("name",), ErrorTypes.VALUE_ERROR, ErrorMessages.WRONG_SPACE_AND_APOSTROPHE_ADJACENT),
            (Service(id=data_for_id.correct_id, name=name.wrong_underscore_and_space_adjacent, price=price.correct_price, description="Some description"),
            ("name",), ErrorTypes.VALUE_ERROR, ErrorMessages.WRONG_SPACE_AND_UNDERSCORE_ADJACENT),
            (Service(id=data_for_id.correct_id, name=name.correct_name, price=price.wrong_price_zero, description="Some description"),
            ("price",), ErrorTypes.GREATER_THAN_EQUAL, ErrorMessages.PRICE_TOO_LOW),
            (Service(id=data_for_id.correct_id, name=name.correct_name, price=price.wrong_price_negative, description="Some description"),
            ("price",), ErrorTypes.GREATER_THAN_EQUAL, ErrorMessages.PRICE_TOO_LOW),
            (Service(id=data_for_id.correct_id, name=name.correct_name, price=price.wrong_price_negative_small, description="Some description"),
            ("price",), ErrorTypes.GREATER_THAN_EQUAL, ErrorMessages.PRICE_TOO_LOW),
            (Service(id=data_for_id.correct_id, name=name.correct_name, price=price.wrong_price_negative_big, description="Some description"),
            ("price",), ErrorTypes.GREATER_THAN_EQUAL, ErrorMessages.PRICE_TOO_LOW),
            (Service(id=data_for_id.correct_id, name=name.correct_name, price=price.wrong_price_big, description="Some description"),
            ("price",), ErrorTypes.LESS_THAN_EQUAL, ErrorMessages.PRICE_TOO_HIGH),
            (Service(id=data_for_id.correct_id, name=name.correct_name, price=price.wrong_price_negative_float, description="Some description"),
            ("price",), ErrorTypes.GREATER_THAN_EQUAL, ErrorMessages.PRICE_TOO_LOW),
            (Service(id=data_for_id.correct_id, name=name.correct_name, price=price.wrong_price_negative_three_numbers_after_coma, description="Some description"),
            ("price",), ErrorTypes.GREATER_THAN_EQUAL, ErrorMessages.PRICE_TOO_LOW),
            (Service(id=data_for_id.correct_id, name=name.correct_name, price=price.wrong_price_string, description="Some description"),
            ("price",), ErrorTypes.DECIMAL_PARSING, ErrorMessages.PRICE_NOT_DECIMAL),
            (Service(id=data_for_id.correct_id, name=name.correct_name, price=price.wrong_price_none, description="Some description"),
            ("price",), ErrorTypes.DECIMAL_TYPE, ErrorMessages.PRICE_NONE_TYPE),
            (Service(id=data_for_id.wrong_id_zero, name=name.correct_name, price=price.correct_price, description="Some description"),
            ("id",), ErrorTypes.GREATER_THAN_EQUAL, ErrorMessages.ID_GREATER_ONE),
            (Service(id=data_for_id.wrong_negative_id, name=name.correct_name, price=price.correct_price, description="Some description"),
            ("id",), ErrorTypes.GREATER_THAN_EQUAL, ErrorMessages.ID_GREATER_ONE),
            (Service(id=data_for_id.big_wrong_negative_id, name=name.correct_name, price=price.correct_price, description="Some description"),
            ("id",), ErrorTypes.GREATER_THAN_EQUAL, ErrorMessages.ID_GREATER_ONE),
            (Service(id=data_for_id.wrong_id_str, name=name.correct_name, price=price.correct_price, description="Some description"),
            ("id",), ErrorTypes.INT_TYPE, ErrorMessages.INT_TYPE),
            (Service(id=data_for_id.wrong_id_none, name=name.correct_name, price=price.correct_price, description="Some description"),
            ("id",), ErrorTypes.INT_TYPE, ErrorMessages.INT_TYPE),
            (Service(id=data_for_id.wrong_id_float, name=name.correct_name, price=price.correct_price, description="Some description"),
            ("id",), ErrorTypes.INT_TYPE, ErrorMessages.INT_TYPE),
            (Service(id=data_for_id.wrong_id_true, name=name.correct_name, price=price.correct_price, description="Some description"),
            ("id",), ErrorTypes.INT_TYPE, ErrorMessages.INT_TYPE),
            (Service(id=data_for_id.wrong_id_false, name=name.correct_name, price=price.correct_price, description="Some description"),
            ("id",), ErrorTypes.INT_TYPE, ErrorMessages.INT_TYPE),
        ]
    )
    def test_response_service_small_wrong(
            self,
            service,
            error_loc,
            error_type,
            error_msg,
    ):
        with pytest.raises(ValidationError) as error:
            service_response = ServiceResponseSmall.model_validate(service)
        errors = error.value.errors()
        assert len(errors) == 1
        error = errors[0]
        assert error["loc"] == error_loc
        assert error["type"] == error_type
        assert error_msg in error["msg"]