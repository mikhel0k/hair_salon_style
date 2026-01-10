import pytest
from pydantic import ValidationError

from app.schemas.Record import EditRecordNote

from tests.unit.test_schemas.conftest_exceptions import ErrorMessages, ErrorTypes, DataForId
from conftest import AllowedRecordStatuses


class TestEditStatusRecord:
    data_for_id = DataForId()
    status = AllowedRecordStatuses()

    @pytest.mark.parametrize("record_id",[
        data_for_id.right_id, data_for_id.big_right_id,
    ])
    def test_edit_status_record_create(self, record_id):
        record = EditRecordNote(
            id=record_id
        )
        assert isinstance(record, EditRecordNote)
        assert record.id == record_id

    @pytest.mark.parametrize("record_id, error_loc, error_type, error_msg",[
        (data_for_id.wrong_id_zero, ("id",), ErrorTypes.GREATER_THAN_EQUAL, ErrorMessages.ID_GREATER_ONE),
        (data_for_id.wrong_negative_id, ("id",), ErrorTypes.GREATER_THAN_EQUAL, ErrorMessages.ID_GREATER_ONE),
        (data_for_id.big_wrong_negative_id, ("id",), ErrorTypes.GREATER_THAN_EQUAL, ErrorMessages.ID_GREATER_ONE),
        (data_for_id.wrong_id_str, ("id",), ErrorTypes.INT_TYPE, ErrorMessages.INT_TYPE),
        (data_for_id.wrong_id_float, ("id",), ErrorTypes.INT_TYPE, ErrorMessages.INT_TYPE),
        (data_for_id.wrong_id_str, ("id",), ErrorTypes.INT_TYPE, ErrorMessages.INT_TYPE),
        (data_for_id.wrong_id_true, ("id",), ErrorTypes.INT_TYPE, ErrorMessages.INT_TYPE),
        (data_for_id.wrong_id_false, ("id",), ErrorTypes.INT_TYPE, ErrorMessages.INT_TYPE),
    ])
    def test_edit_status_record_wrong(self, record_id, error_loc, error_type, error_msg):
        with pytest.raises(ValidationError) as error:
            record = EditRecordNote(
            id=record_id,
        )
        errors = error.value.errors()
        assert len(errors) == 1
        error = errors[0]
        assert error["loc"] == error_loc
        assert error["type"] == error_type
        assert error_msg in error["msg"]

