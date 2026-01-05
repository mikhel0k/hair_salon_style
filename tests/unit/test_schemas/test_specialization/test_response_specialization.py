import pytest
from pydantic import ValidationError

from app.schemas.Specialization import SpecializationResponse
from app.models.Specialization import Specialization
from conftest import Name, MAX_NAME_LENGTH, MIN_NAME_LENGTH


class TestCreateSpecialization:
    name = Name()
    @pytest.mark.parametrize("specialization, name, specialization_id", [
        (Specialization(name = name.right_name, id = 1), name.right_name, 1),
        (Specialization(name = name.right_name_short, id = 1), name.right_name_short, 1),
        (Specialization(name = name.right_name_long, id = 1), name.right_name_long, 1),
        (Specialization(name = name.right_name_сyrillic, id = 1), name.right_name_сyrillic, 1),
        (Specialization(name = name.right_name, id = 2), name.right_name, 2),
    ])
    def test_create_specialization_right_name(self, specialization, name, specialization_id):
        specialization = SpecializationResponse.model_validate(specialization)
        assert isinstance(specialization, SpecializationResponse)
        assert specialization.name == name
        assert specialization.id == specialization_id

    @pytest.mark.parametrize("specialization, exc_message", [
        (Specialization(name = name.wrong_name_short, id = 1), f"String should have at least {MIN_NAME_LENGTH} characters"),
        (Specialization(name = name.wrong_name_long, id = 1), f"String should have at most {MAX_NAME_LENGTH} characters"),
        (Specialization(name = name.wrong_name_int, id = 1), "Input should be a valid string"),
        (Specialization(name = name.wrong_name_spaces, id = 1), f"String should have at least {MIN_NAME_LENGTH} characters"),
        (Specialization(name = name.wrong_name_empty, id = 1), f"String should have at least {MIN_NAME_LENGTH} characters"),
        (Specialization(name = name.wrong_name_none, id = 1), "Input should be a valid string"),
    ])
    def test_create_specialization_wrong_name(self, specialization, exc_message):
        with pytest.raises(ValidationError) as error:
            specialization = SpecializationResponse.model_validate(specialization)
        assert len(error.value.errors()) == 1
        assert error.value.errors()[0]["loc"] == ("name",)
        assert exc_message in error.value.errors()[0]["msg"]
