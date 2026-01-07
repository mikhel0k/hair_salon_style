import pytest
from pydantic import ValidationError

from app.schemas.Specialization import SpecializationCreate
from conftest import Name
from tests.unit.test_schemas.conftest_exceptions import ErrorMessages, ErrorTypes


class TestCreateSpecialization:
    name = Name()

    @pytest.mark.parametrize("name", [
        name.right_name,
        name.right_name_short,
        name.right_name_long,
        name.right_name_сyrillic,
    ])
    def test_create_specialization_right_name(self, name):
        specialization = SpecializationCreate(name=name)
        assert isinstance(specialization, SpecializationCreate)
        assert specialization.name == name.title()

    @pytest.mark.parametrize("name_value, error_type, error_msg", [
        (name.wrong_name_long, ErrorTypes.STRING_TOO_LONG, ErrorMessages.SPEC_STRING_TOO_LONG),
        (name.wrong_name_short, ErrorTypes.STRING_TOO_SHORT, ErrorMessages.SPEC_STRING_TOO_SHORT),
        (name.wrong_name_int, ErrorTypes.STRING_TYPE, ErrorMessages.STRING_TYPE),
        (name.wrong_name_empty, ErrorTypes.STRING_TOO_SHORT, ErrorMessages.SPEC_STRING_TOO_SHORT),
        (name.wrong_name_spaces, ErrorTypes.STRING_TOO_SHORT, ErrorMessages.SPEC_STRING_TOO_SHORT),
        (name.wrong_name_none, ErrorTypes.STRING_TYPE, ErrorMessages.STRING_TYPE),
    ])
    def test_create_specialization_wrong_name(self, name_value, error_type, error_msg):
        with pytest.raises(ValidationError) as error:
            specialization = SpecializationCreate(name=name_value)
        errors = error.value.errors()
        assert len(errors) == 1
        error = errors[0]
        assert error["type"] == error_type
        assert error_msg in error["msg"]