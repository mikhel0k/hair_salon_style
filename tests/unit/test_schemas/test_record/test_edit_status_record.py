import pytest
from pydantic import ValidationError

from app.schemas.Record import EditRecordStatus

from tests.unit.test_schemas.conftest_exceptions import ErrorMessages, ErrorTypes, DataForId
from conftest import AllowedRecordStatuses


class TestEditStatusRecord:
    data_for_id = DataForId()
    status = AllowedRecordStatuses()

    @pytest.mark.parametrize("record_id, status",[
        (data_for_id.correct_id, AllowedRecordStatuses.Created),
        (data_for_id.big_correct_id, AllowedRecordStatuses.Created),
        (data_for_id.correct_id, AllowedRecordStatuses.Confirmed),
        (data_for_id.correct_id, AllowedRecordStatuses.Completed),
        (data_for_id.correct_id, AllowedRecordStatuses.Cancelled),
    ])
    def test_edit_status_record_correct(self, record_id, status):
        record = EditRecordStatus(
            id=record_id,
            status=status
        )
        assert isinstance(record, EditRecordStatus)
        assert record.id == record_id
        assert record.status == status

    @pytest.mark.parametrize("record_id, status, error_loc, error_type, error_msg",[
        (data_for_id.wrong_id_zero, AllowedRecordStatuses.Created,
         ("id",), ErrorTypes.GREATER_THAN_EQUAL, ErrorMessages.ID_GREATER_ONE),
        (data_for_id.wrong_negative_id, AllowedRecordStatuses.Created,
         ("id",), ErrorTypes.GREATER_THAN_EQUAL, ErrorMessages.ID_GREATER_ONE),
        (data_for_id.big_wrong_negative_id, AllowedRecordStatuses.Created,
         ("id",), ErrorTypes.GREATER_THAN_EQUAL, ErrorMessages.ID_GREATER_ONE),
        (data_for_id.wrong_id_str, AllowedRecordStatuses.Created,
         ("id",), ErrorTypes.INT_TYPE, ErrorMessages.INT_TYPE),
        (data_for_id.wrong_id_float, AllowedRecordStatuses.Created,
         ("id",), ErrorTypes.INT_TYPE, ErrorMessages.INT_TYPE),
        (data_for_id.wrong_id_str, AllowedRecordStatuses.Created,
         ("id",), ErrorTypes.INT_TYPE, ErrorMessages.INT_TYPE),
        (data_for_id.wrong_id_true, AllowedRecordStatuses.Created,
         ("id",), ErrorTypes.INT_TYPE, ErrorMessages.INT_TYPE),
        (data_for_id.wrong_id_false, AllowedRecordStatuses.Created,
         ("id",), ErrorTypes.INT_TYPE, ErrorMessages.INT_TYPE),
        (data_for_id.correct_id, AllowedRecordStatuses.wrong_status_string,
         ("status",), ErrorTypes.ENUM, ErrorMessages.ENUM_RECORD),
        (data_for_id.correct_id, AllowedRecordStatuses.wrong_status_none,
         ("status",), ErrorTypes.ENUM, ErrorMessages.ENUM_RECORD),
        (data_for_id.correct_id, AllowedRecordStatuses.wrong_status_empty,
         ("status",), ErrorTypes.ENUM, ErrorMessages.ENUM_RECORD),
        (data_for_id.correct_id, AllowedRecordStatuses.wrong_status_boolean,
         ("status",), ErrorTypes.ENUM, ErrorMessages.ENUM_RECORD),
        (data_for_id.correct_id, AllowedRecordStatuses.wrong_status_integer,
         ("status",), ErrorTypes.ENUM, ErrorMessages.ENUM_RECORD),
        (data_for_id.correct_id, AllowedRecordStatuses.wrong_status_float,
         ("status",), ErrorTypes.ENUM, ErrorMessages.ENUM_RECORD),
    ])
    def test_edit_status_record_wrong(self, record_id, status, error_loc, error_type, error_msg):
        with pytest.raises(ValidationError) as error:
            record = EditRecordStatus(
            id=record_id,
            status=status
        )
        errors = error.value.errors()
        assert len(errors) == 1
        error = errors[0]
        assert error["loc"] == error_loc
        assert error["type"] == error_type
        assert error_msg in error["msg"]

