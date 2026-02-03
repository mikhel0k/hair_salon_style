import pytest
from pydantic import ValidationError

from app.models import Master
from app.schemas.Master import MasterResponse
from tests.unit.test_schemas.conftest import assert_single_validation_error
from tests.unit.test_schemas.test_master.conftest import Name, Status
from tests.unit.test_schemas.conftest_exceptions import ErrorMessages, ErrorTypes, DataForId

name = Name()
status = Status()
data_for_id = DataForId()


class TestResponseMaster:

    @pytest.mark.parametrize("master_data, master_id, specialization_id, name_val, status_val", [
        (Master(id=data_for_id.correct_id, specialization_id=data_for_id.correct_id, name=name.correct_name,
                status=status.correct_active),
         data_for_id.correct_id, data_for_id.correct_id, name.correct_name, status.correct_active),
        (Master(id=data_for_id.correct_id, specialization_id=data_for_id.correct_id, name=name.correct_name_short,
                status=status.correct_active),
         data_for_id.correct_id, data_for_id.correct_id, name.correct_name_short, status.correct_active),
        (Master(id=data_for_id.correct_id, specialization_id=data_for_id.correct_id, name=name.correct_name_long,
                status=status.correct_active),
         data_for_id.correct_id, data_for_id.correct_id, name.correct_name_long, status.correct_active),
        (Master(id=data_for_id.correct_id, specialization_id=data_for_id.correct_id, name=name.correct_name_cyrillic,
                status=status.correct_active),
         data_for_id.correct_id, data_for_id.correct_id, name.correct_name_cyrillic, status.correct_active),
        (Master(id=data_for_id.correct_id, specialization_id=data_for_id.correct_id, name=name.correct_name,
                status=status.correct_vacation),
         data_for_id.correct_id, data_for_id.correct_id, name.correct_name, status.correct_vacation),
        (Master(id=data_for_id.correct_id, specialization_id=data_for_id.correct_id, name=name.correct_name,
                status=status.correct_dismissed),
         data_for_id.correct_id, data_for_id.correct_id, name.correct_name, status.correct_dismissed),
        (Master(id=data_for_id.correct_id, specialization_id=data_for_id.big_correct_id, name=name.correct_name,
                status=status.correct_active),
         data_for_id.correct_id, data_for_id.big_correct_id, name.correct_name, status.correct_active),
        (Master(id=data_for_id.big_correct_id, specialization_id=data_for_id.correct_id, name=name.correct_name,
                status=status.correct_active),
         data_for_id.big_correct_id, data_for_id.correct_id, name.correct_name, status.correct_active),
    ])
    def test_response_master_correct(self, master_data, master_id, specialization_id, name_val, status_val):
        master = MasterResponse.model_validate(master_data)
        assert isinstance(master, MasterResponse)
        assert master.id == master_id
        assert master.specialization_id == specialization_id
        assert master.name == name_val.title()
        assert master.status == status_val

    @pytest.mark.parametrize(
        "master_data, error_loc, error_type, error_msg", [
            (Master(name=name.wrong_name_long, status=status.correct_active, specialization_id=data_for_id.correct_id, id=data_for_id.correct_id),
             ("name",), ErrorTypes.STRING_TOO_LONG, ErrorMessages.STRING_TOO_LONG_30),
            (Master(name=name.wrong_name_short, status=status.correct_active, specialization_id=data_for_id.correct_id, id=data_for_id.correct_id),
             ("name",), ErrorTypes.STRING_TOO_SHORT, ErrorMessages.STRING_TOO_SHORT),
            (Master(name=name.wrong_name_int, status=status.correct_active, specialization_id=data_for_id.correct_id, id=data_for_id.correct_id),
             ("name",), ErrorTypes.STRING_TYPE, ErrorMessages.STRING_TYPE),
            (Master(name=name.wrong_name_empty, status=status.correct_active, specialization_id=data_for_id.correct_id, id=data_for_id.correct_id),
             ("name",), ErrorTypes.STRING_TOO_SHORT, ErrorMessages.STRING_TOO_SHORT),
            (Master(name=name.wrong_name_spaces, status=status.correct_active, specialization_id=data_for_id.correct_id, id=data_for_id.correct_id),
             ("name",), ErrorTypes.STRING_TOO_SHORT, ErrorMessages.STRING_TOO_SHORT),
            (Master(name=name.wrong_name_none, status=status.correct_active, specialization_id=data_for_id.correct_id, id=data_for_id.correct_id),
             ("name",), ErrorTypes.STRING_TYPE, ErrorMessages.STRING_TYPE),
            (Master(name=name.wrong_invalid_character, status=status.correct_active, specialization_id=data_for_id.correct_id, id=data_for_id.correct_id),
             ("name",), ErrorTypes.VALUE_ERROR, ErrorMessages.WRONG_INVALID_CHARACTER),
            (Master(name=name.wrong_consecutive_spaces, status=status.correct_active, specialization_id=data_for_id.correct_id, id=data_for_id.correct_id),
             ("name",), ErrorTypes.VALUE_ERROR, ErrorMessages.WRONG_CONSECUTIVE_SPACES),
            (Master(name=name.wrong_consecutive_hyphens, status=status.correct_active, specialization_id=data_for_id.correct_id, id=data_for_id.correct_id),
             ("name",), ErrorTypes.VALUE_ERROR, ErrorMessages.WRONG_CONSECUTIVE_HYPHENS),
            (Master(name=name.wrong_consecutive_apostrophes, status=status.correct_active, specialization_id=data_for_id.correct_id, id=data_for_id.correct_id),
             ("name",), ErrorTypes.VALUE_ERROR, ErrorMessages.WRONG_CONSECUTIVE_APOSTROPHES),
            (Master(name=name.wrong_consecutive_underscores, status=status.correct_active, specialization_id=data_for_id.correct_id, id=data_for_id.correct_id),
             ("name",), ErrorTypes.VALUE_ERROR, ErrorMessages.WRONG_CONSECUTIVE_UNDERSCORES),
            (Master(name=name.wrong_start_with_hyphen, status=status.correct_active, specialization_id=data_for_id.correct_id, id=data_for_id.correct_id),
             ("name",), ErrorTypes.VALUE_ERROR, ErrorMessages.WRONG_START_WITH_HYPHEN),
            (Master(name=name.wrong_start_with_apostrophe, status=status.correct_active, specialization_id=data_for_id.correct_id, id=data_for_id.correct_id),
             ("name",), ErrorTypes.VALUE_ERROR, ErrorMessages.WRONG_START_WITH_APOSTROPHE),
            (Master(name=name.wrong_start_with_underscore, status=status.correct_active, specialization_id=data_for_id.correct_id, id=data_for_id.correct_id),
             ("name",), ErrorTypes.VALUE_ERROR, ErrorMessages.WRONG_START_WITH_UNDERSCORE),
            (Master(name=name.wrong_end_with_hyphen, status=status.correct_active, specialization_id=data_for_id.correct_id, id=data_for_id.correct_id),
             ("name",), ErrorTypes.VALUE_ERROR, ErrorMessages.WRONG_END_WITH_HYPHEN),
            (Master(name=name.wrong_end_with_apostrophe, status=status.correct_active, specialization_id=data_for_id.correct_id, id=data_for_id.correct_id),
             ("name",), ErrorTypes.VALUE_ERROR, ErrorMessages.WRONG_END_WITH_APOSTROPHE),
            (Master(name=name.wrong_end_with_underscore, status=status.correct_active, specialization_id=data_for_id.correct_id, id=data_for_id.correct_id),
             ("name",), ErrorTypes.VALUE_ERROR, ErrorMessages.WRONG_END_WITH_UNDERSCORE),
            (Master(name=name.wrong_space_and_hyphen_adjacent, status=status.correct_active, specialization_id=data_for_id.correct_id, id=data_for_id.correct_id),
             ("name",), ErrorTypes.VALUE_ERROR, ErrorMessages.WRONG_SPACE_AND_HYPHEN_ADJACENT),
            (Master(name=name.wrong_space_and_apostrophe_adjacent, status=status.correct_active, specialization_id=data_for_id.correct_id, id=data_for_id.correct_id),
             ("name",), ErrorTypes.VALUE_ERROR, ErrorMessages.WRONG_SPACE_AND_APOSTROPHE_ADJACENT),
            (Master(name=name.wrong_space_and_underscore_adjacent, status=status.correct_active, specialization_id=data_for_id.correct_id, id=data_for_id.correct_id),
             ("name",), ErrorTypes.VALUE_ERROR, ErrorMessages.WRONG_SPACE_AND_UNDERSCORE_ADJACENT),
            (Master(name=name.wrong_hyphen_and_space_adjacent, status=status.correct_active, specialization_id=data_for_id.correct_id, id=data_for_id.correct_id),
             ("name",), ErrorTypes.VALUE_ERROR, ErrorMessages.WRONG_SPACE_AND_HYPHEN_ADJACENT),
            (Master(name=name.wrong_apostrophe_and_space_adjacent, status=status.correct_active, specialization_id=data_for_id.correct_id, id=data_for_id.correct_id),
             ("name",), ErrorTypes.VALUE_ERROR, ErrorMessages.WRONG_SPACE_AND_APOSTROPHE_ADJACENT),
            (Master(name=name.wrong_underscore_and_space_adjacent, status=status.correct_active, specialization_id=data_for_id.correct_id, id=data_for_id.correct_id),
             ("name",), ErrorTypes.VALUE_ERROR, ErrorMessages.WRONG_SPACE_AND_UNDERSCORE_ADJACENT),
            (Master(name=name.correct_name, status=status.wrong_status_string, specialization_id=data_for_id.correct_id, id=data_for_id.correct_id),
             ("status",), ErrorTypes.ENUM, ErrorMessages.ENUM_MASTER),
            (Master(name=name.correct_name, status=status.wrong_status_none, specialization_id=data_for_id.correct_id, id=data_for_id.correct_id),
             ("status",), ErrorTypes.ENUM, ErrorMessages.ENUM_MASTER),
            (Master(name=name.correct_name, status=status.wrong_status_empty, specialization_id=data_for_id.correct_id, id=data_for_id.correct_id),
             ("status",), ErrorTypes.ENUM, ErrorMessages.ENUM_MASTER),
            (Master(name=name.correct_name, status=status.wrong_status_boolean, specialization_id=data_for_id.correct_id, id=data_for_id.correct_id),
             ("status",), ErrorTypes.ENUM, ErrorMessages.ENUM_MASTER),
            (Master(name=name.correct_name, status=status.wrong_status_integer, specialization_id=data_for_id.correct_id, id=data_for_id.correct_id),
             ("status",), ErrorTypes.ENUM, ErrorMessages.ENUM_MASTER),
            (Master(name=name.correct_name, status=status.wrong_status_float, specialization_id=data_for_id.correct_id, id=data_for_id.correct_id),
             ("status",), ErrorTypes.ENUM, ErrorMessages.ENUM_MASTER),
            (Master(name=name.correct_name, status=status.correct_active, specialization_id=data_for_id.wrong_id_zero, id=data_for_id.correct_id),
             ("specialization_id",), ErrorTypes.GREATER_THAN_EQUAL, ErrorMessages.ID_GREATER_ONE),
            (Master(name=name.correct_name, status=status.correct_active, specialization_id=data_for_id.wrong_negative_id, id=data_for_id.correct_id),
             ("specialization_id",), ErrorTypes.GREATER_THAN_EQUAL, ErrorMessages.ID_GREATER_ONE),
            (Master(name=name.correct_name, status=status.correct_active, specialization_id=data_for_id.wrong_id_str, id=data_for_id.correct_id),
             ("specialization_id",), ErrorTypes.INT_TYPE, ErrorMessages.INT_TYPE),
            (Master(name=name.correct_name, status=status.correct_active, specialization_id=data_for_id.wrong_id_none, id=data_for_id.correct_id),
             ("specialization_id",), ErrorTypes.INT_TYPE, ErrorMessages.INT_TYPE),
            (Master(name=name.correct_name, status=status.correct_active, specialization_id=data_for_id.wrong_id_float, id=data_for_id.correct_id),
             ("specialization_id",), ErrorTypes.INT_TYPE, ErrorMessages.INT_TYPE),
            (Master(name=name.correct_name, status=status.correct_active, specialization_id=data_for_id.wrong_id_true, id=data_for_id.correct_id),
             ("specialization_id",), ErrorTypes.INT_TYPE, ErrorMessages.INT_TYPE),
            (Master(name=name.correct_name, status=status.correct_active, specialization_id=data_for_id.wrong_id_false, id=data_for_id.correct_id),
             ("specialization_id",), ErrorTypes.INT_TYPE, ErrorMessages.INT_TYPE),
            (Master(name=name.correct_name, status=status.correct_active, specialization_id=data_for_id.correct_id, id=data_for_id.wrong_id_zero),
             ("id",), ErrorTypes.GREATER_THAN_EQUAL, ErrorMessages.ID_GREATER_ONE),
            (Master(name=name.correct_name, status=status.correct_active, specialization_id=data_for_id.correct_id, id=data_for_id.wrong_negative_id),
             ("id",), ErrorTypes.GREATER_THAN_EQUAL, ErrorMessages.ID_GREATER_ONE),
            (Master(name=name.correct_name, status=status.correct_active, specialization_id=data_for_id.correct_id, id=data_for_id.wrong_id_str),
             ("id",), ErrorTypes.INT_TYPE, ErrorMessages.INT_TYPE),
            (Master(name=name.correct_name, status=status.correct_active, specialization_id=data_for_id.correct_id, id=data_for_id.wrong_id_none),
             ("id",), ErrorTypes.INT_TYPE, ErrorMessages.INT_TYPE),
            (Master(name=name.correct_name, status=status.correct_active, specialization_id=data_for_id.correct_id, id=data_for_id.wrong_id_float),
             ("id",), ErrorTypes.INT_TYPE, ErrorMessages.INT_TYPE),
            (Master(name=name.correct_name, status=status.correct_active, specialization_id=data_for_id.correct_id, id=data_for_id.wrong_id_true),
             ("id",), ErrorTypes.INT_TYPE, ErrorMessages.INT_TYPE),
            (Master(name=name.correct_name, status=status.correct_active, specialization_id=data_for_id.correct_id, id=data_for_id.wrong_id_false),
             ("id",), ErrorTypes.INT_TYPE, ErrorMessages.INT_TYPE),
        ]
    )
    def test_response_master_wrong(self, master_data, error_loc, error_type, error_msg):
        with pytest.raises(ValidationError) as exc_info:
            MasterResponse.model_validate(master_data)
        assert_single_validation_error(exc_info.value.errors(), error_loc, error_type, error_msg)
