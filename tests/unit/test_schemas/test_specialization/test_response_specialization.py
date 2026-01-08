import pytest
from pydantic import ValidationError

from app.schemas.Specialization import SpecializationResponse
from app.models.Specialization import Specialization
from conftest import Name
from tests.unit.test_schemas.conftest_exceptions import ErrorMessages, ErrorTypes


class TestResponseSpecialization:
    name = Name()

    @pytest.mark.parametrize("specialization, name, specialization_id", [
        (Specialization(name=name.right_name, id=1), name.right_name, 1),
        (Specialization(name=name.right_name_short, id=1), name.right_name_short, 1),
        (Specialization(name=name.right_name_long, id=1), name.right_name_long, 1),
        (Specialization(name=name.right_name_сyrillic, id=1), name.right_name_сyrillic, 1),
        (Specialization(name=name.right_name, id=2), name.right_name, 2),
    ])
    def test_response_specialization_right_name(self, specialization, name, specialization_id):
        specialization = SpecializationResponse.model_validate(specialization)
        assert isinstance(specialization, SpecializationResponse)
        assert specialization.name == name.title()
        assert specialization.id == specialization_id

    @pytest.mark.parametrize("specialization, error_type, error_msg", [
        (Specialization(name=name.wrong_name_short, id=1),
        ErrorTypes.STRING_TOO_SHORT, ErrorMessages.SPEC_STRING_TOO_SHORT),
        (Specialization(name=name.wrong_name_long, id=1),
        ErrorTypes.STRING_TOO_LONG, ErrorMessages.SPEC_STRING_TOO_LONG),
        (Specialization(name=name.wrong_name_int, id=1), ErrorTypes.STRING_TYPE, ErrorMessages.STRING_TYPE),
        (Specialization(name=name.wrong_name_spaces, id=1),
        ErrorTypes.STRING_TOO_SHORT, ErrorMessages.SPEC_STRING_TOO_SHORT),
        (Specialization(name=name.wrong_name_empty, id=1),
        ErrorTypes.STRING_TOO_SHORT, ErrorMessages.SPEC_STRING_TOO_SHORT),
        (Specialization(name=name.wrong_name_none, id=1),
        ErrorTypes.STRING_TYPE, ErrorMessages.STRING_TYPE),
        (Specialization(name=name.wrong_invalid_character, id=1),
        ErrorTypes.VALUE_ERROR, ErrorMessages.WRONG_INVALID_CHARACTER),
        (Specialization(name=name.wrong_consecutive_spaces, id=1),
        ErrorTypes.VALUE_ERROR, ErrorMessages.WRONG_CONSECUTIVE_SPACES),
        (Specialization(name=name.wrong_consecutive_hyphens, id=1),
        ErrorTypes.VALUE_ERROR, ErrorMessages.WRONG_CONSECUTIVE_HYPHENS),
        (Specialization(name=name.wrong_consecutive_apostrophes, id=1),
        ErrorTypes.VALUE_ERROR, ErrorMessages.WRONG_CONSECUTIVE_APOSTROPHES),
        (Specialization(name=name.wrong_consecutive_underscores, id=1),
        ErrorTypes.VALUE_ERROR, ErrorMessages.WRONG_CONSECUTIVE_UNDERSCORES),
        (Specialization(name=name.wrong_start_with_hyphen, id=1),
        ErrorTypes.VALUE_ERROR, ErrorMessages.WRONG_START_WITH_HYPHEN),
        (Specialization(name=name.wrong_start_with_apostrophe, id=1),
        ErrorTypes.VALUE_ERROR, ErrorMessages.WRONG_START_WITH_APOSTROPHE),
        (Specialization(name=name.wrong_start_with_underscore, id=1),
        ErrorTypes.VALUE_ERROR, ErrorMessages.WRONG_START_WITH_UNDERSCORE),
        (Specialization(name=name.wrong_end_with_hyphen, id=1),
        ErrorTypes.VALUE_ERROR, ErrorMessages.WRONG_END_WITH_HYPHEN),
        (Specialization(name=name.wrong_end_with_apostrophe, id=1),
        ErrorTypes.VALUE_ERROR, ErrorMessages.WRONG_END_WITH_APOSTROPHE),
        (Specialization(name=name.wrong_end_with_underscore, id=1),
        ErrorTypes.VALUE_ERROR, ErrorMessages.WRONG_END_WITH_UNDERSCORE),
        (Specialization(name=name.wrong_space_and_hyphen_adjacent, id=1),
        ErrorTypes.VALUE_ERROR, ErrorMessages.WRONG_SPACE_AND_HYPHEN_ADJACENT),
        (Specialization(name=name.wrong_space_and_apostrophe_adjacent, id=1),
        ErrorTypes.VALUE_ERROR, ErrorMessages.WRONG_SPACE_AND_APOSTROPHE_ADJACENT),
        (Specialization(name=name.wrong_space_and_underscore_adjacent, id=1),
        ErrorTypes.VALUE_ERROR, ErrorMessages.WRONG_SPACE_AND_UNDERSCORE_ADJACENT),
        (Specialization(name=name.wrong_hyphen_and_space_adjacent, id=1),
        ErrorTypes.VALUE_ERROR, ErrorMessages.WRONG_SPACE_AND_HYPHEN_ADJACENT),
        (Specialization(name=name.wrong_apostrophe_and_space_adjacent, id=1),
        ErrorTypes.VALUE_ERROR, ErrorMessages.WRONG_SPACE_AND_APOSTROPHE_ADJACENT),
        (Specialization(name=name.wrong_underscore_and_space_adjacent, id=1),
        ErrorTypes.VALUE_ERROR, ErrorMessages.WRONG_SPACE_AND_UNDERSCORE_ADJACENT),
    ])
    def test_response_specialization_wrong_name(self, specialization, error_type, error_msg):
        with pytest.raises(ValidationError) as error:
            specialization = SpecializationResponse.model_validate(specialization)
        errors = error.value.errors()
        assert len(errors) == 1
        error = errors[0]
        assert error["type"] == error_type
        assert error_msg in error["msg"]