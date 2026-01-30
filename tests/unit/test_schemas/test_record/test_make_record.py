import phonenumbers
import pytest
from pydantic import ValidationError

from app.schemas.UserFlow import MakeRecord
from tests.unit.test_schemas.conftest import assert_single_validation_error
from tests.unit.test_schemas.test_record.conftest import Phone
from tests.unit.test_schemas.conftest_exceptions import ErrorMessages, ErrorTypes, DataForId

phone = Phone()
data_for_id = DataForId()


class TestMakeRecord:

    @pytest.mark.parametrize("phone, master_id, service_id, cell_id, notes", [
        (phone.correct_number_int, data_for_id.correct_id,
         data_for_id.correct_id, data_for_id.correct_id, None),
        (phone.correct_number_str_with_eight, data_for_id.correct_id,
         data_for_id.correct_id, data_for_id.correct_id, None),
        (phone.correct_number_str_with_seven, data_for_id.correct_id,
         data_for_id.correct_id, data_for_id.correct_id, None),
        (phone.correct_number_str_with_seven_without_plus, data_for_id.correct_id,
         data_for_id.correct_id, data_for_id.correct_id, None),
        (phone.correct_number_int, data_for_id.big_correct_id,
         data_for_id.correct_id, data_for_id.correct_id, None),
        (phone.correct_number_int, data_for_id.correct_id,
         data_for_id.big_correct_id, data_for_id.correct_id, None),
        (phone.correct_number_int, data_for_id.correct_id,
         data_for_id.correct_id, data_for_id.big_correct_id, None),
        (phone.correct_number_int, data_for_id.correct_id,
         data_for_id.correct_id, data_for_id.correct_id, "Customer requested morning appointment"),
    ])
    def test_make_record_correct(self, phone, master_id, service_id, cell_id, notes):
        record = MakeRecord(
            phone_number=phone,
            master_id=master_id,
            service_id=service_id,
            cell_id=cell_id,
            notes=notes,
        )
        assert isinstance(record, MakeRecord)
        assert record.master_id == master_id
        assert record.service_id == service_id
        assert record.cell_id == cell_id
        assert record.notes == notes
        parsed = phonenumbers.parse(str(phone), "RU")
        if phonenumbers.is_valid_number(parsed):
            assert record.phone_number == phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.E164)

    @pytest.mark.parametrize("phone, master_id, service_id, cell_id, error_loc, error_type, error_msg", [
        (phone.wrong_number_str_with_two_without_plus,data_for_id.correct_id,
         data_for_id.correct_id, data_for_id.correct_id,
         ("phone_number",), ErrorTypes.VALUE_ERROR, ErrorMessages.INVALID_PHONE_FORMAT),
        (phone.wrong_number_str_with_five_without_plus,data_for_id.correct_id,
         data_for_id.correct_id, data_for_id.correct_id,
         ("phone_number",), ErrorTypes.VALUE_ERROR, ErrorMessages.INVALID_PHONE_FORMAT),
        (phone.wrong_number_str_with_two_with_plus,data_for_id.correct_id,
         data_for_id.correct_id, data_for_id.correct_id,
         ("phone_number",), ErrorTypes.VALUE_ERROR, ErrorMessages.INVALID_PHONE_FORMAT),
        (phone.wrong_number_str_with_five_with_plus,data_for_id.correct_id,
         data_for_id.correct_id, data_for_id.correct_id,
         ("phone_number",), ErrorTypes.VALUE_ERROR, ErrorMessages.INVALID_PHONE_FORMAT),
        (phone.wrong_number_str_with_eight_with_plus,data_for_id.correct_id,
         data_for_id.correct_id, data_for_id.correct_id,
         ("phone_number",), ErrorTypes.VALUE_ERROR, ErrorMessages.INVALID_PHONE_FORMAT),
        (phone.wrong_number_str_with_seven_short,data_for_id.correct_id,
         data_for_id.correct_id, data_for_id.correct_id,
         ("phone_number",), ErrorTypes.VALUE_ERROR, ErrorMessages.INVALID_PHONE_FORMAT),
        (phone.wrong_number_int_short,data_for_id.correct_id,
         data_for_id.correct_id, data_for_id.correct_id,
         ("phone_number",), ErrorTypes.VALUE_ERROR, ErrorMessages.INVALID_PHONE_FORMAT),
        (phone.wrong_number_str_with_seven_long,data_for_id.correct_id,
         data_for_id.correct_id, data_for_id.correct_id,
         ("phone_number",), ErrorTypes.VALUE_ERROR, ErrorMessages.INVALID_PHONE_FORMAT),
        (phone.wrong_number_int_long,data_for_id.correct_id,
         data_for_id.correct_id, data_for_id.correct_id,
         ("phone_number",), ErrorTypes.VALUE_ERROR, ErrorMessages.INVALID_PHONE_FORMAT),
        (phone.wrong_number_none,data_for_id.correct_id,
         data_for_id.correct_id, data_for_id.correct_id,
         ("phone_number",), ErrorTypes.VALUE_ERROR, ErrorMessages.EMPTY_PHONE),
        (phone.wrong_number_empty,data_for_id.correct_id,
         data_for_id.correct_id, data_for_id.correct_id,
         ("phone_number",), ErrorTypes.VALUE_ERROR, ErrorMessages.EMPTY_PHONE),
        (phone.wrong_number_true,data_for_id.correct_id,
         data_for_id.correct_id, data_for_id.correct_id,
         ("phone_number",), ErrorTypes.VALUE_ERROR, ErrorMessages.INVALID_PHONE_FORMAT),
        (phone.wrong_number_false,data_for_id.correct_id,
         data_for_id.correct_id, data_for_id.correct_id,
         ("phone_number",), ErrorTypes.VALUE_ERROR, ErrorMessages.EMPTY_PHONE),
        (phone.correct_number_int,data_for_id.wrong_id_zero,
         data_for_id.correct_id, data_for_id.correct_id,
         ("master_id",), ErrorTypes.GREATER_THAN_EQUAL, ErrorMessages.ID_GREATER_ONE),
        (phone.correct_number_int,data_for_id.wrong_negative_id,
         data_for_id.correct_id, data_for_id.correct_id,
         ("master_id",), ErrorTypes.GREATER_THAN_EQUAL, ErrorMessages.ID_GREATER_ONE),
        (phone.correct_number_int,data_for_id.big_wrong_negative_id,
         data_for_id.correct_id, data_for_id.correct_id,
         ("master_id",), ErrorTypes.GREATER_THAN_EQUAL, ErrorMessages.ID_GREATER_ONE),
        (phone.correct_number_int,data_for_id.wrong_id_str,
         data_for_id.correct_id, data_for_id.correct_id,
         ("master_id",), ErrorTypes.INT_TYPE, ErrorMessages.INT_TYPE),
        (phone.correct_number_int,data_for_id.wrong_id_none,
         data_for_id.correct_id, data_for_id.correct_id,
         ("master_id",), ErrorTypes.INT_TYPE, ErrorMessages.INT_TYPE),
        (phone.correct_number_int,data_for_id.wrong_id_float,
         data_for_id.correct_id, data_for_id.correct_id,
         ("master_id",), ErrorTypes.INT_TYPE, ErrorMessages.INT_TYPE),
        (phone.correct_number_int,data_for_id.wrong_id_true,
         data_for_id.correct_id, data_for_id.correct_id,
         ("master_id",), ErrorTypes.INT_TYPE, ErrorMessages.INT_TYPE),
        (phone.correct_number_int,data_for_id.wrong_id_false,
         data_for_id.correct_id, data_for_id.correct_id,
         ("master_id",), ErrorTypes.INT_TYPE, ErrorMessages.INT_TYPE),
        (phone.correct_number_int, data_for_id.correct_id,
         data_for_id.wrong_id_zero, data_for_id.correct_id,
         ("service_id",), ErrorTypes.GREATER_THAN_EQUAL, ErrorMessages.ID_GREATER_ONE),
        (phone.correct_number_int, data_for_id.correct_id,
         data_for_id.wrong_negative_id, data_for_id.correct_id,
         ("service_id",), ErrorTypes.GREATER_THAN_EQUAL, ErrorMessages.ID_GREATER_ONE),
        (phone.correct_number_int, data_for_id.correct_id,
         data_for_id.big_wrong_negative_id, data_for_id.correct_id,
         ("service_id",), ErrorTypes.GREATER_THAN_EQUAL, ErrorMessages.ID_GREATER_ONE),
        (phone.correct_number_int, data_for_id.correct_id,
         data_for_id.wrong_id_str, data_for_id.correct_id,
         ("service_id",), ErrorTypes.INT_TYPE, ErrorMessages.INT_TYPE),
        (phone.correct_number_int, data_for_id.correct_id,
         data_for_id.wrong_id_none, data_for_id.correct_id,
         ("service_id",), ErrorTypes.INT_TYPE, ErrorMessages.INT_TYPE),
        (phone.correct_number_int, data_for_id.correct_id,
         data_for_id.wrong_id_float, data_for_id.correct_id,
         ("service_id",), ErrorTypes.INT_TYPE, ErrorMessages.INT_TYPE),
        (phone.correct_number_int, data_for_id.correct_id,
         data_for_id.wrong_id_true, data_for_id.correct_id,
         ("service_id",), ErrorTypes.INT_TYPE, ErrorMessages.INT_TYPE),
        (phone.correct_number_int, data_for_id.correct_id,
         data_for_id.wrong_id_false, data_for_id.correct_id,
         ("service_id",), ErrorTypes.INT_TYPE, ErrorMessages.INT_TYPE),
        (phone.correct_number_int, data_for_id.correct_id,
         data_for_id.correct_id, data_for_id.wrong_id_zero,
         ("cell_id",), ErrorTypes.GREATER_THAN_EQUAL, ErrorMessages.ID_GREATER_ONE),
        (phone.correct_number_int, data_for_id.correct_id,
         data_for_id.correct_id, data_for_id.wrong_negative_id,
         ("cell_id",), ErrorTypes.GREATER_THAN_EQUAL, ErrorMessages.ID_GREATER_ONE),
        (phone.correct_number_int, data_for_id.correct_id,
         data_for_id.correct_id, data_for_id.big_wrong_negative_id,
         ("cell_id",), ErrorTypes.GREATER_THAN_EQUAL, ErrorMessages.ID_GREATER_ONE),
        (phone.correct_number_int, data_for_id.correct_id,
         data_for_id.correct_id, data_for_id.wrong_id_str,
         ("cell_id",), ErrorTypes.INT_TYPE, ErrorMessages.INT_TYPE),
        (phone.correct_number_int, data_for_id.correct_id,
         data_for_id.correct_id, data_for_id.wrong_id_none,
         ("cell_id",), ErrorTypes.INT_TYPE, ErrorMessages.INT_TYPE),
        (phone.correct_number_int, data_for_id.correct_id,
         data_for_id.correct_id, data_for_id.wrong_id_float,
         ("cell_id",), ErrorTypes.INT_TYPE, ErrorMessages.INT_TYPE),
        (phone.correct_number_int, data_for_id.correct_id,
         data_for_id.correct_id, data_for_id.wrong_id_true,
         ("cell_id",), ErrorTypes.INT_TYPE, ErrorMessages.INT_TYPE),
        (phone.correct_number_int, data_for_id.correct_id,
         data_for_id.correct_id, data_for_id.wrong_id_false,
         ("cell_id",), ErrorTypes.INT_TYPE, ErrorMessages.INT_TYPE),
    ])
    def test_make_record_wrong(self, phone, master_id, service_id, cell_id, error_loc, error_type, error_msg):
        with pytest.raises(ValidationError) as exc_info:
            MakeRecord(phone_number=phone, master_id=master_id, service_id=service_id, cell_id=cell_id)
        assert_single_validation_error(exc_info.value.errors(), error_loc, error_type, error_msg)