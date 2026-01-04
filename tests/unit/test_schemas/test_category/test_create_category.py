import pytest
from pydantic import ValidationError

from app.schemas.Category import CategoryCreate
from conftest import Name, MAX_LENGTH, MIN_LENGTH


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
        assert category.name == name

    @pytest.mark.parametrize("name_value, exc_message", [
        (name.wrong_name_long, f"String should have at most {MAX_LENGTH} characters"),
        (name.wrong_name_short, f"String should have at least {MIN_LENGTH} characters"),
        (name.wrong_name_int, "Input should be a valid string"),
        (name.wrong_name_empty, f"String should have at least {MIN_LENGTH} characters"),
        (name.wrong_name_spaces, f"String should have at least {MIN_LENGTH} characters"),
        (name.wrong_name_none, "Input should be a valid string"),
    ])
    def test_create_category_wrong_name(self, name_value, exc_message):
        with pytest.raises(ValidationError) as error:
            category = CategoryCreate(name=name_value)
        assert len(error.value.errors()) == 1
        assert error.value.errors()[0]["loc"] == ("name",)
        assert exc_message in error.value.errors()[0]["msg"]
