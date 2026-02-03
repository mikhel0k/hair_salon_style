import pytest
from pydantic import ValidationError

from app.schemas.Master import MasterUpdate
from tests.unit.test_schemas.conftest import assert_single_validation_error
from tests.unit.test_schemas.test_master.conftest import Name, Status
from tests.unit.test_schemas.conftest_exceptions import ErrorMessages, ErrorTypes, DataForId

name = Name()
status = Status()
data_for_id = DataForId()


class TestUpdateMaster:

    @pytest.mark.parametrize("specialization_id, name_val, status_val", [
        (data_for_id.correct_id, name.correct_name, Status.correct_active),
        (data_for_id.correct_id, name.correct_name_short, Status.correct_active),
        (data_for_id.correct_id, name.correct_name_long, Status.correct_active),
        (data_for_id.correct_id, name.correct_name_cyrillic, Status.correct_active),
        (data_for_id.correct_id, name.correct_name, Status.correct_vacation),
        (data_for_id.correct_id, name.correct_name, Status.correct_dismissed),
        (data_for_id.big_correct_id, name.correct_name, Status.correct_active),
        (data_for_id.correct_id, None, None),
        (None, name.correct_name, None),
        (None, None, Status.correct_active),
    ])
    def test_update_master_correct(self, specialization_id, name_val, status_val):
        master = MasterUpdate(
            specialization_id=specialization_id,
            name=name_val,
            status=status_val,
        )
        assert isinstance(master, MasterUpdate)
        assert master.specialization_id == specialization_id
        if name_val:
            assert master.name == name_val.title()
        else:
            assert master.name is None
        assert master.status == status_val

    @pytest.mark.parametrize(
        "name_val, status_val, specialization_id, error_loc, error_type, error_msg", [
            (name.wrong_name_long, status.correct_active, data_for_id.correct_id,
             ("name",), ErrorTypes.STRING_TOO_LONG, ErrorMessages.STRING_TOO_LONG_30),
            (name.wrong_name_short, status.correct_active, data_for_id.correct_id,
             ("name",), ErrorTypes.STRING_TOO_SHORT, ErrorMessages.STRING_TOO_SHORT),
            (name.wrong_name_int, status.correct_active, data_for_id.correct_id,
             ("name",), ErrorTypes.VALUE_ERROR, ErrorMessages.FIELD_MUST_BE_STRING),
            (name.wrong_name_empty, status.correct_active, data_for_id.correct_id,
             ("name",), ErrorTypes.STRING_TOO_SHORT, ErrorMessages.STRING_TOO_SHORT),
            (name.wrong_name_spaces, status.correct_active, data_for_id.correct_id,
             ("name",), ErrorTypes.STRING_TOO_SHORT, ErrorMessages.STRING_TOO_SHORT),
            (name.wrong_invalid_character, status.correct_active, data_for_id.correct_id,
             ("name",), ErrorTypes.VALUE_ERROR, ErrorMessages.WRONG_INVALID_CHARACTER),
            (name.wrong_consecutive_spaces, status.correct_active, data_for_id.correct_id,
             ("name",), ErrorTypes.VALUE_ERROR, ErrorMessages.WRONG_CONSECUTIVE_SPACES),
            (name.wrong_consecutive_hyphens, status.correct_active, data_for_id.correct_id,
             ("name",), ErrorTypes.VALUE_ERROR, ErrorMessages.WRONG_CONSECUTIVE_HYPHENS),
            (name.wrong_consecutive_apostrophes, status.correct_active, data_for_id.correct_id,
             ("name",), ErrorTypes.VALUE_ERROR, ErrorMessages.WRONG_CONSECUTIVE_APOSTROPHES),
            (name.wrong_consecutive_underscores, status.correct_active, data_for_id.correct_id,
             ("name",), ErrorTypes.VALUE_ERROR, ErrorMessages.WRONG_CONSECUTIVE_UNDERSCORES),
            (name.wrong_start_with_hyphen, status.correct_active, data_for_id.correct_id,
             ("name",), ErrorTypes.VALUE_ERROR, ErrorMessages.WRONG_START_WITH_HYPHEN),
            (name.wrong_start_with_apostrophe, status.correct_active, data_for_id.correct_id,
             ("name",), ErrorTypes.VALUE_ERROR, ErrorMessages.WRONG_START_WITH_APOSTROPHE),
            (name.wrong_start_with_underscore, status.correct_active, data_for_id.correct_id,
             ("name",), ErrorTypes.VALUE_ERROR, ErrorMessages.WRONG_START_WITH_UNDERSCORE),
            (name.wrong_end_with_hyphen, status.correct_active, data_for_id.correct_id,
             ("name",), ErrorTypes.VALUE_ERROR, ErrorMessages.WRONG_END_WITH_HYPHEN),
            (name.wrong_end_with_apostrophe, status.correct_active, data_for_id.correct_id,
             ("name",), ErrorTypes.VALUE_ERROR, ErrorMessages.WRONG_END_WITH_APOSTROPHE),
            (name.wrong_end_with_underscore, status.correct_active, data_for_id.correct_id,
             ("name",), ErrorTypes.VALUE_ERROR, ErrorMessages.WRONG_END_WITH_UNDERSCORE),
            (name.wrong_space_and_hyphen_adjacent, status.correct_active, data_for_id.correct_id,
             ("name",), ErrorTypes.VALUE_ERROR, ErrorMessages.WRONG_SPACE_AND_HYPHEN_ADJACENT),
            (name.wrong_space_and_apostrophe_adjacent, status.correct_active, data_for_id.correct_id,
             ("name",), ErrorTypes.VALUE_ERROR, ErrorMessages.WRONG_SPACE_AND_APOSTROPHE_ADJACENT),
            (name.wrong_space_and_underscore_adjacent, status.correct_active, data_for_id.correct_id,
             ("name",), ErrorTypes.VALUE_ERROR, ErrorMessages.WRONG_SPACE_AND_UNDERSCORE_ADJACENT),
            (name.wrong_hyphen_and_space_adjacent, status.correct_active, data_for_id.correct_id,
             ("name",), ErrorTypes.VALUE_ERROR, ErrorMessages.WRONG_SPACE_AND_HYPHEN_ADJACENT),
            (name.wrong_apostrophe_and_space_adjacent, status.correct_active, data_for_id.correct_id,
             ("name",), ErrorTypes.VALUE_ERROR, ErrorMessages.WRONG_SPACE_AND_APOSTROPHE_ADJACENT),
            (name.wrong_underscore_and_space_adjacent, status.correct_active, data_for_id.correct_id,
             ("name",), ErrorTypes.VALUE_ERROR, ErrorMessages.WRONG_SPACE_AND_UNDERSCORE_ADJACENT),
            (name.correct_name, status.wrong_status_string, data_for_id.correct_id,
             ("status",), ErrorTypes.ENUM, ErrorMessages.ENUM_MASTER),
            (name.correct_name, status.wrong_status_empty, data_for_id.correct_id,
             ("status",), ErrorTypes.ENUM, ErrorMessages.ENUM_MASTER),
            (name.correct_name, status.wrong_status_boolean, data_for_id.correct_id,
             ("status",), ErrorTypes.ENUM, ErrorMessages.ENUM_MASTER),
            (name.correct_name, status.wrong_status_integer, data_for_id.correct_id,
             ("status",), ErrorTypes.ENUM, ErrorMessages.ENUM_MASTER),
            (name.correct_name, status.wrong_status_float, data_for_id.correct_id,
             ("status",), ErrorTypes.ENUM, ErrorMessages.ENUM_MASTER),
            (name.correct_name, status.correct_active, data_for_id.wrong_id_zero,
             ("specialization_id",), ErrorTypes.GREATER_THAN_EQUAL, ErrorMessages.ID_GREATER_ONE),
            (name.correct_name, status.correct_active, data_for_id.wrong_negative_id,
             ("specialization_id",), ErrorTypes.GREATER_THAN_EQUAL, ErrorMessages.ID_GREATER_ONE),
            (name.correct_name, status.correct_active, data_for_id.wrong_id_str,
             ("specialization_id",), ErrorTypes.INT_TYPE, ErrorMessages.INT_TYPE),
            (name.correct_name, status.correct_active, data_for_id.wrong_id_float,
             ("specialization_id",), ErrorTypes.INT_TYPE, ErrorMessages.INT_TYPE),
            (name.correct_name, status.correct_active, data_for_id.wrong_id_true,
             ("specialization_id",), ErrorTypes.INT_TYPE, ErrorMessages.INT_TYPE),
            (name.correct_name, status.correct_active, data_for_id.wrong_id_false,
             ("specialization_id",), ErrorTypes.INT_TYPE, ErrorMessages.INT_TYPE),
        ]
    )
    def test_update_master_wrong(self, name_val, status_val, specialization_id, error_loc, error_type, error_msg):
        with pytest.raises(ValidationError) as exc_info:
            MasterUpdate(
                specialization_id=specialization_id,
                name=name_val,
                status=status_val,
            )
        assert_single_validation_error(exc_info.value.errors(), error_loc, error_type, error_msg)
