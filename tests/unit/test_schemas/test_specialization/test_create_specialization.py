import pytest
from pydantic import ValidationError

from app.schemas.Specialization import SpecializationCreate
from tests.unit.test_schemas.conftest import assert_single_validation_error
from tests.unit.test_schemas.test_specialization.conftest import Name
from tests.unit.test_schemas.conftest_exceptions import ErrorMessages, ErrorTypes

name = Name()


class TestCreateSpecialization:

    @pytest.mark.parametrize("name", [
        name.correct_name,
        name.correct_name_short,
        name.correct_name_long,
        name.correct_name_cyrillic,
    ])
    def test_create_specialization_correct(self, name):
        specialization = SpecializationCreate(name=name)
        assert isinstance(specialization, SpecializationCreate)
        assert specialization.name == name.title()

    @pytest.mark.parametrize("name_value, error_loc, error_type, error_msg", [
        (name.wrong_name_long, ("name",), ErrorTypes.STRING_TOO_LONG, ErrorMessages.SPEC_STRING_TOO_LONG),
        (name.wrong_name_short, ("name",), ErrorTypes.STRING_TOO_SHORT, ErrorMessages.SPEC_STRING_TOO_SHORT),
        (name.wrong_name_int, ("name",), ErrorTypes.STRING_TYPE, ErrorMessages.STRING_TYPE),
        (name.wrong_name_empty, ("name",), ErrorTypes.STRING_TOO_SHORT, ErrorMessages.SPEC_STRING_TOO_SHORT),
        (name.wrong_name_spaces, ("name",), ErrorTypes.STRING_TOO_SHORT, ErrorMessages.SPEC_STRING_TOO_SHORT),
        (name.wrong_name_none, ("name",), ErrorTypes.STRING_TYPE, ErrorMessages.STRING_TYPE),
        (name.wrong_invalid_character, ("name",), ErrorTypes.VALUE_ERROR, ErrorMessages.WRONG_INVALID_CHARACTER),
        (name.wrong_consecutive_spaces, ("name",), ErrorTypes.VALUE_ERROR, ErrorMessages.WRONG_CONSECUTIVE_SPACES),
        (name.wrong_consecutive_hyphens, ("name",), ErrorTypes.VALUE_ERROR, ErrorMessages.WRONG_CONSECUTIVE_HYPHENS),
        (name.wrong_consecutive_apostrophes, ("name",), ErrorTypes.VALUE_ERROR, ErrorMessages.WRONG_CONSECUTIVE_APOSTROPHES),
        (name.wrong_consecutive_underscores, ("name",), ErrorTypes.VALUE_ERROR, ErrorMessages.WRONG_CONSECUTIVE_UNDERSCORES),
        (name.wrong_start_with_hyphen, ("name",), ErrorTypes.VALUE_ERROR, ErrorMessages.WRONG_START_WITH_HYPHEN),
        (name.wrong_start_with_apostrophe, ("name",), ErrorTypes.VALUE_ERROR, ErrorMessages.WRONG_START_WITH_APOSTROPHE),
        (name.wrong_start_with_underscore, ("name",), ErrorTypes.VALUE_ERROR, ErrorMessages.WRONG_START_WITH_UNDERSCORE),
        (name.wrong_end_with_hyphen, ("name",), ErrorTypes.VALUE_ERROR, ErrorMessages.WRONG_END_WITH_HYPHEN),
        (name.wrong_end_with_apostrophe, ("name",), ErrorTypes.VALUE_ERROR, ErrorMessages.WRONG_END_WITH_APOSTROPHE),
        (name.wrong_end_with_underscore, ("name",), ErrorTypes.VALUE_ERROR, ErrorMessages.WRONG_END_WITH_UNDERSCORE),
        (name.wrong_space_and_hyphen_adjacent, ("name",), ErrorTypes.VALUE_ERROR, ErrorMessages.WRONG_SPACE_AND_HYPHEN_ADJACENT),
        (name.wrong_space_and_apostrophe_adjacent, ("name",), ErrorTypes.VALUE_ERROR, ErrorMessages.WRONG_SPACE_AND_APOSTROPHE_ADJACENT),
        (name.wrong_space_and_underscore_adjacent, ("name",), ErrorTypes.VALUE_ERROR, ErrorMessages.WRONG_SPACE_AND_UNDERSCORE_ADJACENT),
        (name.wrong_hyphen_and_space_adjacent, ("name",), ErrorTypes.VALUE_ERROR, ErrorMessages.WRONG_SPACE_AND_HYPHEN_ADJACENT),
        (name.wrong_apostrophe_and_space_adjacent, ("name",), ErrorTypes.VALUE_ERROR, ErrorMessages.WRONG_SPACE_AND_APOSTROPHE_ADJACENT),
        (name.wrong_underscore_and_space_adjacent, ("name",), ErrorTypes.VALUE_ERROR, ErrorMessages.WRONG_SPACE_AND_UNDERSCORE_ADJACENT),
    ])
    def test_create_specialization_wrong(self, name_value, error_loc, error_type, error_msg):
        with pytest.raises(ValidationError) as exc_info:
            SpecializationCreate(name=name_value)
        assert_single_validation_error(exc_info.value.errors(), error_loc, error_type, error_msg)