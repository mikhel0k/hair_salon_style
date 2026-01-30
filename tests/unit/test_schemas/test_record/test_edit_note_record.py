import pytest
from pydantic import ValidationError

from app.schemas.Record import EditRecordNote
from tests.unit.test_schemas.conftest import assert_single_validation_error
from tests.unit.test_schemas.conftest_exceptions import ErrorMessages, ErrorTypes, DataForId
from tests.unit.test_schemas.test_record.conftest import AllowedRecordStatuses

data_for_id = DataForId()


class TestEditNoteRecord:

    @pytest.mark.parametrize("record_id, notes", [
        (data_for_id.correct_id, None),
        (data_for_id.big_correct_id, None),
        (data_for_id.correct_id, "Customer requested morning appointment"),
    ])
    def test_edit_note_record_correct(self, record_id, notes):
        record = EditRecordNote(id=record_id, notes=notes)
        assert isinstance(record, EditRecordNote)
        assert record.id == record_id
        assert record.notes == notes

    @pytest.mark.parametrize("record_id, error_loc, error_type, error_msg",[
        (data_for_id.wrong_id_zero, ("id",), ErrorTypes.GREATER_THAN_EQUAL, ErrorMessages.ID_GREATER_ONE),
        (data_for_id.wrong_negative_id, ("id",), ErrorTypes.GREATER_THAN_EQUAL, ErrorMessages.ID_GREATER_ONE),
        (data_for_id.big_wrong_negative_id, ("id",), ErrorTypes.GREATER_THAN_EQUAL, ErrorMessages.ID_GREATER_ONE),
        (data_for_id.wrong_id_str, ("id",), ErrorTypes.INT_TYPE, ErrorMessages.INT_TYPE),
        (data_for_id.wrong_id_float, ("id",), ErrorTypes.INT_TYPE, ErrorMessages.INT_TYPE),
        (data_for_id.wrong_id_none, ("id",), ErrorTypes.INT_TYPE, ErrorMessages.INT_TYPE),
        (data_for_id.wrong_id_true, ("id",), ErrorTypes.INT_TYPE, ErrorMessages.INT_TYPE),
        (data_for_id.wrong_id_false, ("id",), ErrorTypes.INT_TYPE, ErrorMessages.INT_TYPE),
    ])
    def test_edit_note_record_wrong(self, record_id, error_loc, error_type, error_msg):
        with pytest.raises(ValidationError) as exc_info:
            EditRecordNote(id=record_id)
        assert_single_validation_error(exc_info.value.errors(), error_loc, error_type, error_msg)

