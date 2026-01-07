import pytest
from pydantic import ValidationError

from app.schemas.Category import CategoryCreate
from conftest import Name
from tests.unit.test_schemas.conftest_exceptions import ErrorMessages, ErrorTypes


class TestCreateCategory:
    name = Name()

    @pytest.mark.parametrize("name", [
        name.right_name,
        name.right_name_short,
        name.right_name_long,
        name.right_name_сyrillic,
    ])
    def test_create_category_right_name(self, name):
        category = CategoryCreate(name=name)
        assert isinstance(category, CategoryCreate)
        assert category.name == name.title()

    @pytest.mark.parametrize("name_value, error_type, error_msg", [
        (name.wrong_name_long, ErrorTypes.STRING_TOO_LONG, ErrorMessages.STRING_TOO_LONG),
        (name.wrong_name_short, ErrorTypes.STRING_TOO_SHORT, ErrorMessages.STRING_TOO_SHORT),
        (name.wrong_name_int, ErrorTypes.STRING_TYPE, ErrorMessages.STRING_TYPE),
        (name.wrong_name_empty, ErrorTypes.STRING_TOO_SHORT, ErrorMessages.STRING_TOO_SHORT),
        (name.wrong_name_spaces, ErrorTypes.STRING_TOO_SHORT, ErrorMessages.SPEC_STRING_TOO_SHORT),
        (name.wrong_name_none, ErrorTypes.STRING_TYPE, ErrorMessages.STRING_TYPE),
    ])
    def test_create_category_wrong_name(self, name_value, error_type, error_msg):
        with pytest.raises(ValidationError) as error:
            category = CategoryCreate(name=name_value)
        assert len(error.value.errors()) == 1
        assert error.value.errors()[0]["loc"] == ("name",)
        assert error.value.errors()[0]["type"] == error_type
        assert error_msg in error.value.errors()[0]["msg"]