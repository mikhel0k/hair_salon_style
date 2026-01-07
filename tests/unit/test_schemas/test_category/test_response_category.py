import pytest
from pydantic import ValidationError

from app.schemas.Category import CategoryResponse
from app.models.Category import Category
from conftest import Name
from tests.unit.test_schemas.conftest_exceptions import ErrorMessages, ErrorTypes


class TestResponseCategory:
    name = Name()

    @pytest.mark.parametrize("category, name, category_id", [
        (Category(name=name.right_name, id=1), name.right_name, 1),
        (Category(name=name.right_name_short, id=1), name.right_name_short, 1),
        (Category(name=name.right_name_long, id=1), name.right_name_long, 1),
        (Category(name=name.right_name_сyrillic, id=1), name.right_name_сyrillic, 1),
        (Category(name=name.right_name, id=2), name.right_name, 2),
    ])
    def test_response_category_right_name(self, category, name, category_id):
        category = CategoryResponse.model_validate(category)
        assert isinstance(category, CategoryResponse)
        assert category.name == name.title()
        assert category.id == category_id

    @pytest.mark.parametrize("category, error_type, error_msg", [
        (Category(name=name.wrong_name_short, id=1), ErrorTypes.STRING_TOO_SHORT, ErrorMessages.STRING_TOO_SHORT),
        (Category(name=name.wrong_name_long, id=1), ErrorTypes.STRING_TOO_LONG, ErrorMessages.STRING_TOO_LONG),
        (Category(name=name.wrong_name_int, id=1), ErrorTypes.STRING_TYPE, ErrorMessages.STRING_TYPE),
        (Category(name=name.wrong_name_spaces, id=1), ErrorTypes.STRING_TOO_SHORT, ErrorMessages.STRING_TOO_SHORT),
        (Category(name=name.wrong_name_empty, id=1), ErrorTypes.STRING_TOO_SHORT, ErrorMessages.STRING_TOO_SHORT),
        (Category(name=name.wrong_name_none, id=1), ErrorTypes.STRING_TYPE, ErrorMessages.STRING_TYPE),
    ])
    def test_response_category_wrong_name(self, category, error_type, error_msg):
        with pytest.raises(ValidationError) as error:
            category = CategoryResponse.model_validate(category)
        assert len(error.value.errors()) == 1
        assert error.value.errors()[0]["loc"] == ("name",)
        assert error.value.errors()[0]["type"] == error_type
        assert error_msg in error.value.errors()[0]["msg"]