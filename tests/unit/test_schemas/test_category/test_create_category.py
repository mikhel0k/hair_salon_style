import pytest
from pydantic import ValidationError

from app.schemas.Category import CategoryCreate
from conftest import Name, MAX_NAME_LENGTH, MIN_NAME_LENGTH


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

    @pytest.mark.parametrize("name_value, exc_message", [
        (name.wrong_name_long, f"String should have at most {MAX_NAME_LENGTH} characters"),
        (name.wrong_name_short,
         f"Value error, Field is too short. Minimum {MIN_NAME_LENGTH} characters. Got: '{name.wrong_name_short}'"),
        (name.wrong_name_int, "Field must be a string"),
        (name.wrong_name_empty,
         f"Value error, Field is too short. Minimum {MIN_NAME_LENGTH} characters. Got: '{name.wrong_name_empty}'"),
        (name.wrong_name_spaces,
         f"Value error, Field is too short. Minimum {MIN_NAME_LENGTH} characters. Got: ''"),
        (name.wrong_name_none, "Field must be a string"),
    ])
    def test_create_category_wrong_name(self, name_value, exc_message):
        with pytest.raises(ValidationError) as error:
            category = CategoryCreate(name=name_value)
        assert len(error.value.errors()) == 1
        assert error.value.errors()[0]["loc"] == ("name",)
        assert exc_message in error.value.errors()[0]["msg"]
