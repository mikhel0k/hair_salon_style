import pytest
from pydantic import ValidationError

from app.schemas.Category import CategoryResponse
from app.models.Category import Category
from conftest import Name
from tests.unit.test_schemas.conftest_exceptions import ErrorMessages, ErrorTypes, DataForId


class TestResponseCategory:
    name = Name()
    data_for_id = DataForId()

    @pytest.mark.parametrize("category, name, category_id", [
        (Category(name=name.right_name, id=data_for_id.right_id), name.right_name, data_for_id.right_id),
        (Category(name=name.right_name_short, id=data_for_id.right_id), name.right_name_short, data_for_id.right_id),
        (Category(name=name.right_name_long, id=data_for_id.right_id), name.right_name_long, data_for_id.right_id),
        (Category(name=name.right_name_сyrillic, id=data_for_id.right_id), name.right_name_сyrillic, data_for_id.right_id),
        (Category(name=name.right_name, id=data_for_id.big_right_id), name.right_name, data_for_id.big_right_id),
    ])
    def test_response_category_right_name(self, category, name, category_id):
        category = CategoryResponse.model_validate(category)
        assert isinstance(category, CategoryResponse)
        assert category.name == name.title()
        assert category.id == category_id

    @pytest.mark.parametrize("category, error_loc, error_type, error_msg", [
        (Category(name=name.wrong_name_short, id=data_for_id.right_id),
         ("name",), ErrorTypes.STRING_TOO_SHORT, ErrorMessages.STRING_TOO_SHORT),
        (Category(name=name.wrong_name_long, id=data_for_id.right_id),
         ("name",), ErrorTypes.STRING_TOO_LONG, ErrorMessages.STRING_TOO_LONG),
        (Category(name=name.wrong_name_int, id=data_for_id.right_id),
         ("name",), ErrorTypes.STRING_TYPE, ErrorMessages.STRING_TYPE),
        (Category(name=name.wrong_name_spaces, id=data_for_id.right_id),
         ("name",), ErrorTypes.STRING_TOO_SHORT, ErrorMessages.STRING_TOO_SHORT),
        (Category(name=name.wrong_name_empty, id=data_for_id.right_id),
         ("name",), ErrorTypes.STRING_TOO_SHORT, ErrorMessages.STRING_TOO_SHORT),
        (Category(name=name.wrong_invalid_character, id=data_for_id.right_id),
         ("name",), ErrorTypes.VALUE_ERROR, ErrorMessages.WRONG_INVALID_CHARACTER),
        (Category(name=name.wrong_consecutive_spaces, id=data_for_id.right_id),
         ("name",), ErrorTypes.VALUE_ERROR, ErrorMessages.WRONG_CONSECUTIVE_SPACES),
        (Category(name=name.wrong_consecutive_hyphens, id=data_for_id.right_id),
         ("name",), ErrorTypes.VALUE_ERROR, ErrorMessages.WRONG_CONSECUTIVE_HYPHENS),
        (Category(name=name.wrong_consecutive_apostrophes, id=data_for_id.right_id),
         ("name",), ErrorTypes.VALUE_ERROR, ErrorMessages.WRONG_CONSECUTIVE_APOSTROPHES),
        (Category(name=name.wrong_consecutive_underscores, id=data_for_id.right_id),
         ("name",), ErrorTypes.VALUE_ERROR, ErrorMessages.WRONG_CONSECUTIVE_UNDERSCORES),
        (Category(name=name.wrong_start_with_hyphen, id=data_for_id.right_id),
         ("name",), ErrorTypes.VALUE_ERROR, ErrorMessages.WRONG_START_WITH_HYPHEN),
        (Category(name=name.wrong_start_with_apostrophe, id=data_for_id.right_id),
         ("name",), ErrorTypes.VALUE_ERROR, ErrorMessages.WRONG_START_WITH_APOSTROPHE),
        (Category(name=name.wrong_start_with_underscore, id=data_for_id.right_id),
         ("name",), ErrorTypes.VALUE_ERROR, ErrorMessages.WRONG_START_WITH_UNDERSCORE),
        (Category(name=name.wrong_end_with_hyphen, id=data_for_id.right_id),
         ("name",), ErrorTypes.VALUE_ERROR, ErrorMessages.WRONG_END_WITH_HYPHEN),
        (Category(name=name.wrong_end_with_apostrophe, id=data_for_id.right_id),
         ("name",), ErrorTypes.VALUE_ERROR, ErrorMessages.WRONG_END_WITH_APOSTROPHE),
        (Category(name=name.wrong_end_with_underscore, id=data_for_id.right_id),
         ("name",), ErrorTypes.VALUE_ERROR, ErrorMessages.WRONG_END_WITH_UNDERSCORE),
        (Category(name=name.wrong_space_and_hyphen_adjacent, id=data_for_id.right_id),
         ("name",), ErrorTypes.VALUE_ERROR, ErrorMessages.WRONG_SPACE_AND_HYPHEN_ADJACENT),
        (Category(name=name.wrong_space_and_apostrophe_adjacent, id=data_for_id.right_id),
         ("name",), ErrorTypes.VALUE_ERROR, ErrorMessages.WRONG_SPACE_AND_APOSTROPHE_ADJACENT),
        (Category(name=name.wrong_space_and_underscore_adjacent, id=data_for_id.right_id),
         ("name",), ErrorTypes.VALUE_ERROR, ErrorMessages.WRONG_SPACE_AND_UNDERSCORE_ADJACENT),
        (Category(name=name.wrong_hyphen_and_space_adjacent, id=data_for_id.right_id),
         ("name",), ErrorTypes.VALUE_ERROR, ErrorMessages.WRONG_SPACE_AND_HYPHEN_ADJACENT),
        (Category(name=name.wrong_apostrophe_and_space_adjacent, id=data_for_id.right_id),
         ("name",), ErrorTypes.VALUE_ERROR, ErrorMessages.WRONG_SPACE_AND_APOSTROPHE_ADJACENT),
        (Category(name=name.wrong_underscore_and_space_adjacent, id=data_for_id.right_id),
         ("name",), ErrorTypes.VALUE_ERROR, ErrorMessages.WRONG_SPACE_AND_UNDERSCORE_ADJACENT),
        (Category(name=name.right_name, id=data_for_id.wrong_id_zero),
         ("id",), ErrorTypes.GREATER_THAN_EQUAL, ErrorMessages.ID_GREATER_ONE),
        (Category(name=name.right_name, id=data_for_id.wrong_negative_id),
         ("id",), ErrorTypes.GREATER_THAN_EQUAL, ErrorMessages.ID_GREATER_ONE),
        (Category(name=name.right_name, id=data_for_id.big_wrong_negative_id),
         ("id",), ErrorTypes.GREATER_THAN_EQUAL, ErrorMessages.ID_GREATER_ONE),
        (Category(name=name.right_name, id=data_for_id.wrong_id_str),
         ("id",), ErrorTypes.INT_TYPE, ErrorMessages.INT_TYPE),
        (Category(name=name.right_name, id=data_for_id.wrong_id_none),
         ("id",), ErrorTypes.INT_TYPE, ErrorMessages.INT_TYPE),
        (Category(name=name.right_name, id=data_for_id.wrong_id_float),
         ("id",), ErrorTypes.INT_TYPE, ErrorMessages.INT_TYPE),
        (Category(name=name.right_name, id=data_for_id.wrong_id_true),
         ("id",), ErrorTypes.INT_TYPE, ErrorMessages.INT_TYPE),
        (Category(name=name.right_name, id=data_for_id.wrong_id_false),
         ("id",), ErrorTypes.INT_TYPE, ErrorMessages.INT_TYPE),
    ])
    def test_response_category_wrong_name(self, category, error_loc, error_type, error_msg):
        with pytest.raises(ValidationError) as error:
            category = CategoryResponse.model_validate(category)
        errors = error.value.errors()
        assert len(errors) == 1
        error = errors[0]
        assert error["loc"] == error_loc
        assert error["type"] == error_type
        assert error_msg in error["msg"]