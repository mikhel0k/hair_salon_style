import pytest
from pydantic import ValidationError

from app.schemas.Specialization import SpecializationResponse
from app.models.Specialization import Specialization
from conftest import Name
from tests.unit.test_schemas.conftest_exceptions import ErrorMessages, ErrorTypes, DataForId


class TestResponseSpecialization:
    name = Name()
    data_for_id = DataForId()

    @pytest.mark.parametrize("specialization, name, specialization_id", [
        (Specialization(name=name.correct_name, id=data_for_id.correct_id), name.correct_name, data_for_id.correct_id),
        (Specialization(name=name.correct_name_short, id=data_for_id.correct_id), name.correct_name_short, data_for_id.correct_id),
        (Specialization(name=name.correct_name_long, id=data_for_id.correct_id), name.correct_name_long, data_for_id.correct_id),
        (Specialization(name=name.correct_name_сyrillic, id=data_for_id.correct_id), name.correct_name_сyrillic, data_for_id.correct_id),
        (Specialization(name=name.correct_name, id=data_for_id.big_correct_id), name.correct_name, data_for_id.big_correct_id),
    ])
    def test_response_specialization_correct(self, specialization, name, specialization_id):
        specialization = SpecializationResponse.model_validate(specialization)
        assert isinstance(specialization, SpecializationResponse)
        assert specialization.name == name.title()
        assert specialization.id == specialization_id

    @pytest.mark.parametrize("specialization, error_loc, error_type, error_msg", [
        (Specialization(name=name.wrong_name_short, id=data_for_id.correct_id),
         ("name",), ErrorTypes.STRING_TOO_SHORT, ErrorMessages.SPEC_STRING_TOO_SHORT),
        (Specialization(name=name.wrong_name_long, id=data_for_id.correct_id),
        ("name",), ErrorTypes.STRING_TOO_LONG, ErrorMessages.SPEC_STRING_TOO_LONG),
        (Specialization(name=name.wrong_name_int, id=data_for_id.correct_id),
         ("name",), ErrorTypes.STRING_TYPE, ErrorMessages.STRING_TYPE),
        (Specialization(name=name.wrong_name_spaces, id=data_for_id.correct_id),
        ("name",), ErrorTypes.STRING_TOO_SHORT, ErrorMessages.SPEC_STRING_TOO_SHORT),
        (Specialization(name=name.wrong_name_empty, id=data_for_id.correct_id),
        ("name",), ErrorTypes.STRING_TOO_SHORT, ErrorMessages.SPEC_STRING_TOO_SHORT),
        (Specialization(name=name.wrong_name_none, id=data_for_id.correct_id),
        ("name",), ErrorTypes.STRING_TYPE, ErrorMessages.STRING_TYPE),
        (Specialization(name=name.wrong_invalid_character, id=data_for_id.correct_id),
        ("name",), ErrorTypes.VALUE_ERROR, ErrorMessages.WRONG_INVALID_CHARACTER),
        (Specialization(name=name.wrong_consecutive_spaces, id=data_for_id.correct_id),
        ("name",), ErrorTypes.VALUE_ERROR, ErrorMessages.WRONG_CONSECUTIVE_SPACES),
        (Specialization(name=name.wrong_consecutive_hyphens, id=data_for_id.correct_id),
        ("name",), ErrorTypes.VALUE_ERROR, ErrorMessages.WRONG_CONSECUTIVE_HYPHENS),
        (Specialization(name=name.wrong_consecutive_apostrophes, id=data_for_id.correct_id),
        ("name",), ErrorTypes.VALUE_ERROR, ErrorMessages.WRONG_CONSECUTIVE_APOSTROPHES),
        (Specialization(name=name.wrong_consecutive_underscores, id=data_for_id.correct_id),
        ("name",), ErrorTypes.VALUE_ERROR, ErrorMessages.WRONG_CONSECUTIVE_UNDERSCORES),
        (Specialization(name=name.wrong_start_with_hyphen, id=data_for_id.correct_id),
        ("name",), ErrorTypes.VALUE_ERROR, ErrorMessages.WRONG_START_WITH_HYPHEN),
        (Specialization(name=name.wrong_start_with_apostrophe, id=data_for_id.correct_id),
        ("name",), ErrorTypes.VALUE_ERROR, ErrorMessages.WRONG_START_WITH_APOSTROPHE),
        (Specialization(name=name.wrong_start_with_underscore, id=data_for_id.correct_id),
        ("name",), ErrorTypes.VALUE_ERROR, ErrorMessages.WRONG_START_WITH_UNDERSCORE),
        (Specialization(name=name.wrong_end_with_hyphen, id=data_for_id.correct_id),
        ("name",), ErrorTypes.VALUE_ERROR, ErrorMessages.WRONG_END_WITH_HYPHEN),
        (Specialization(name=name.wrong_end_with_apostrophe, id=data_for_id.correct_id),
        ("name",), ErrorTypes.VALUE_ERROR, ErrorMessages.WRONG_END_WITH_APOSTROPHE),
        (Specialization(name=name.wrong_end_with_underscore, id=data_for_id.correct_id),
        ("name",), ErrorTypes.VALUE_ERROR, ErrorMessages.WRONG_END_WITH_UNDERSCORE),
        (Specialization(name=name.wrong_space_and_hyphen_adjacent, id=data_for_id.correct_id),
        ("name",), ErrorTypes.VALUE_ERROR, ErrorMessages.WRONG_SPACE_AND_HYPHEN_ADJACENT),
        (Specialization(name=name.wrong_space_and_apostrophe_adjacent, id=data_for_id.correct_id),
        ("name",), ErrorTypes.VALUE_ERROR, ErrorMessages.WRONG_SPACE_AND_APOSTROPHE_ADJACENT),
        (Specialization(name=name.wrong_space_and_underscore_adjacent, id=data_for_id.correct_id),
        ("name",), ErrorTypes.VALUE_ERROR, ErrorMessages.WRONG_SPACE_AND_UNDERSCORE_ADJACENT),
        (Specialization(name=name.wrong_hyphen_and_space_adjacent, id=data_for_id.correct_id),
        ("name",), ErrorTypes.VALUE_ERROR, ErrorMessages.WRONG_SPACE_AND_HYPHEN_ADJACENT),
        (Specialization(name=name.wrong_apostrophe_and_space_adjacent, id=data_for_id.correct_id),
        ("name",), ErrorTypes.VALUE_ERROR, ErrorMessages.WRONG_SPACE_AND_APOSTROPHE_ADJACENT),
        (Specialization(name=name.wrong_underscore_and_space_adjacent, id=data_for_id.correct_id),
        ("name",), ErrorTypes.VALUE_ERROR, ErrorMessages.WRONG_SPACE_AND_UNDERSCORE_ADJACENT),
        (Specialization(name=name.correct_name, id=data_for_id.wrong_id_zero),
        ("id",), ErrorTypes.GREATER_THAN_EQUAL, ErrorMessages.ID_GREATER_ONE),
        (Specialization(name=name.correct_name, id=data_for_id.wrong_negative_id),
        ("id",), ErrorTypes.GREATER_THAN_EQUAL, ErrorMessages.ID_GREATER_ONE),
        (Specialization(name=name.correct_name, id=data_for_id.big_wrong_negative_id),
        ("id",), ErrorTypes.GREATER_THAN_EQUAL, ErrorMessages.ID_GREATER_ONE),
        (Specialization(name=name.correct_name, id=data_for_id.wrong_id_str),
        ("id",), ErrorTypes.INT_TYPE, ErrorMessages.INT_TYPE),
        (Specialization(name=name.correct_name, id=data_for_id.wrong_id_none),
        ("id",), ErrorTypes.INT_TYPE, ErrorMessages.INT_TYPE),
        (Specialization(name=name.correct_name, id=data_for_id.wrong_id_float),
        ("id",), ErrorTypes.INT_TYPE, ErrorMessages.INT_TYPE),
        (Specialization(name=name.correct_name, id=data_for_id.wrong_id_true),
        ("id",), ErrorTypes.INT_TYPE, ErrorMessages.INT_TYPE),
        (Specialization(name=name.correct_name, id=data_for_id.wrong_id_false),
        ("id",), ErrorTypes.INT_TYPE, ErrorMessages.INT_TYPE),
    ])
    def test_response_specialization_wrong(self, specialization, error_loc, error_type, error_msg):
        with pytest.raises(ValidationError) as error:
            specialization = SpecializationResponse.model_validate(specialization)
        errors = error.value.errors()
        assert len(errors) == 1
        error = errors[0]
        assert error["loc"] == error_loc
        assert error["type"] == error_type
        assert error_msg in error["msg"]