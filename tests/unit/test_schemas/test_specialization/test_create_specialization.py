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
        (name.wrong_invalid_character, ErrorTypes.VALUE_ERROR, ErrorMessages.WRONG_INVALID_CHARACTER),
        (name.wrong_consecutive_spaces, ErrorTypes.VALUE_ERROR, ErrorMessages.WRONG_CONSECUTIVE_SPACES),
        (name.wrong_consecutive_hyphens, ErrorTypes.VALUE_ERROR, ErrorMessages.WRONG_CONSECUTIVE_HYPHENS),
        (name.wrong_consecutive_apostrophes, ErrorTypes.VALUE_ERROR, ErrorMessages.WRONG_CONSECUTIVE_APOSTROPHES),
        (name.wrong_consecutive_underscores, ErrorTypes.VALUE_ERROR, ErrorMessages.WRONG_CONSECUTIVE_UNDERSCORES),
        (name.wrong_start_with_hyphen, ErrorTypes.VALUE_ERROR, ErrorMessages.WRONG_START_WITH_HYPHEN),
        (name.wrong_start_with_apostrophe, ErrorTypes.VALUE_ERROR, ErrorMessages.WRONG_START_WITH_APOSTROPHE),
        (name.wrong_start_with_underscore, ErrorTypes.VALUE_ERROR, ErrorMessages.WRONG_START_WITH_UNDERSCORE),
        (name.wrong_end_with_hyphen, ErrorTypes.VALUE_ERROR, ErrorMessages.WRONG_END_WITH_HYPHEN),
        (name.wrong_end_with_apostrophe, ErrorTypes.VALUE_ERROR, ErrorMessages.WRONG_END_WITH_APOSTROPHE),
        (name.wrong_end_with_underscore, ErrorTypes.VALUE_ERROR, ErrorMessages.WRONG_END_WITH_UNDERSCORE),
        (name.wrong_space_and_hyphen_adjacent, ErrorTypes.VALUE_ERROR, ErrorMessages.WRONG_SPACE_AND_HYPHEN_ADJACENT),
        (name.wrong_space_and_apostrophe_adjacent, ErrorTypes.VALUE_ERROR, ErrorMessages.WRONG_SPACE_AND_APOSTROPHE_ADJACENT),
        (name.wrong_space_and_underscore_adjacent, ErrorTypes.VALUE_ERROR, ErrorMessages.WRONG_SPACE_AND_UNDERSCORE_ADJACENT),
        (name.wrong_hyphen_and_space_adjacent, ErrorTypes.VALUE_ERROR, ErrorMessages.WRONG_SPACE_AND_HYPHEN_ADJACENT),
        (name.wrong_apostrophe_and_space_adjacent, ErrorTypes.VALUE_ERROR, ErrorMessages.WRONG_SPACE_AND_APOSTROPHE_ADJACENT),
        (name.wrong_underscore_and_space_adjacent, ErrorTypes.VALUE_ERROR, ErrorMessages.WRONG_SPACE_AND_UNDERSCORE_ADJACENT),
    ])
    def test_create_specialization_wrong_name(self, name_value, error_type, error_msg):
        with pytest.raises(ValidationError) as error:
            specialization = SpecializationCreate(name=name_value)
        errors = error.value.errors()
        assert len(errors) == 1
        error = errors[0]
        assert error["type"] == error_type
        assert error_msg in error["msg"]