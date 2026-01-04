import pytest
from pydantic import ValidationError

from app.schemas.Category import CategoryResponse
from app.models.Category import Category
from conftest import Name, MAX_NAME_LENGTH, MIN_NAME_LENGTH


class TestCreateCategory:
    name = Name()
    @pytest.mark.parametrize("category, name, category_id", [
        (Category(name = name.right_name, id = 1), name.right_name, 1),
        (Category(name = name.right_name_short, id = 1), name.right_name_short, 1),
        (Category(name = name.right_name_long, id = 1), name.right_name_long, 1),
        (Category(name = name.right_name_сyrillic, id = 1), name.right_name_сyrillic, 1),
        (Category(name = name.right_name, id = 2), name.right_name, 2),
    ])
    def test_create_category_right_name(self, category, name, category_id):
        category = CategoryResponse.model_validate(category)
        assert isinstance(category, CategoryResponse)
        assert category.name == name
        assert category.id == category_id

    @pytest.mark.parametrize("category, exc_message", [
        (Category(name = name.wrong_name_short, id = 1), f"String should have at least {MIN_NAME_LENGTH} characters"),
        (Category(name = name.wrong_name_long, id = 1), f"String should have at most {MAX_NAME_LENGTH} characters"),
        (Category(name = name.wrong_name_int, id = 1), "Input should be a valid string"),
        (Category(name = name.wrong_name_spaces, id = 1), f"String should have at least {MIN_NAME_LENGTH} characters"),
        (Category(name = name.wrong_name_empty, id = 1), f"String should have at least {MIN_NAME_LENGTH} characters"),
        (Category(name = name.wrong_name_none, id = 1), "Input should be a valid string"),
    ])
    def test_create_category_wrong_name(self, category, exc_message):
        with pytest.raises(ValidationError) as error:
            category = CategoryResponse.model_validate(category)
        assert len(error.value.errors()) == 1
        assert error.value.errors()[0]["loc"] == ("name",)
        assert exc_message in error.value.errors()[0]["msg"]
