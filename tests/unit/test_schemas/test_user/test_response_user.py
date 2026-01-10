import phonenumbers
import pytest
from pydantic import ValidationError

from app.models import User
from app.schemas.User import UserResponse
from conftest import Phone
from tests.unit.test_schemas.conftest_exceptions import ErrorMessages, ErrorTypes, DataForId


class TestResponseUser:
    phone = Phone()
    data_for_id = DataForId()

    @pytest.mark.parametrize("user, phone, user_id", [
        (User(phone_number=phone.right_number_int, id=data_for_id.right_id),
         phone.right_number_int, data_for_id.right_id),
        (User(phone_number=phone.right_number_str_with_eight, id=data_for_id.right_id),
         phone.right_number_str_with_eight, data_for_id.right_id),
        (User(phone_number=phone.right_number_str_with_seven, id=data_for_id.right_id),
         phone.right_number_str_with_seven, data_for_id.right_id),
        (User(phone_number=phone.right_number_str_with_seven_without_plus, id=data_for_id.right_id),
         phone.right_number_str_with_seven_without_plus, data_for_id.right_id),
        (User(phone_number=phone.right_number_int, id=data_for_id.big_right_id),
         phone.right_number_int, data_for_id.big_right_id),
    ])
    def test_response_user_right(self, user, phone, user_id):
        user = UserResponse.model_validate(user)
        assert isinstance(user, UserResponse)
        assert user.id==user_id
        parsed = phonenumbers.parse(str(phone), "RU")
        if phonenumbers.is_valid_number(parsed):
            assert user.phone_number == phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.E164)

    @pytest.mark.parametrize("user, error_loc, error_type, error_msg", [
        (User(phone_number=phone.wrong_number_str_with_two_without_plus, id=data_for_id.right_id),
         ("phone_number",), ErrorTypes.VALUE_ERROR, ErrorMessages.INVALID_PHONE_FORMAT),
        (User(phone_number=phone.wrong_number_str_with_five_without_plus, id=data_for_id.right_id),
         ("phone_number",), ErrorTypes.VALUE_ERROR, ErrorMessages.INVALID_PHONE_FORMAT),
        (User(phone_number=phone.wrong_number_str_with_two_with_plus, id=data_for_id.right_id),
         ("phone_number",), ErrorTypes.VALUE_ERROR, ErrorMessages.INVALID_PHONE_FORMAT),
        (User(phone_number=phone.wrong_number_str_with_five_with_plus, id=data_for_id.right_id),
         ("phone_number",), ErrorTypes.VALUE_ERROR, ErrorMessages.INVALID_PHONE_FORMAT),
        (User(phone_number=phone.wrong_number_str_with_eight_with_plus, id=data_for_id.right_id),
         ("phone_number",), ErrorTypes.VALUE_ERROR, ErrorMessages.INVALID_PHONE_FORMAT),
        (User(phone_number=phone.wrong_number_str_with_seven_short, id=data_for_id.right_id),
         ("phone_number",), ErrorTypes.VALUE_ERROR, ErrorMessages.INVALID_PHONE_FORMAT),
        (User(phone_number=phone.wrong_number_int_short, id=data_for_id.right_id),
         ("phone_number",), ErrorTypes.VALUE_ERROR, ErrorMessages.INVALID_PHONE_FORMAT),
        (User(phone_number=phone.wrong_number_str_with_seven_long, id=data_for_id.right_id),
         ("phone_number",), ErrorTypes.VALUE_ERROR, ErrorMessages.INVALID_PHONE_FORMAT),
        (User(phone_number=phone.wrong_number_int_long, id=data_for_id.right_id),
         ("phone_number",), ErrorTypes.VALUE_ERROR, ErrorMessages.INVALID_PHONE_FORMAT),
        (User(phone_number=phone.wrong_number_none, id=data_for_id.right_id),
         ("phone_number",), ErrorTypes.VALUE_ERROR, ErrorMessages.EMPTY_PHONE),
        (User(phone_number=phone.wrong_number_empty, id=data_for_id.right_id),
         ("phone_number",), ErrorTypes.VALUE_ERROR, ErrorMessages.EMPTY_PHONE),
        (User(phone_number=phone.wrong_number_true, id=data_for_id.right_id),
         ("phone_number",), ErrorTypes.VALUE_ERROR, ErrorMessages.INVALID_PHONE_FORMAT),
        (User(phone_number=phone.wrong_number_false, id=data_for_id.right_id),
         ("phone_number",), ErrorTypes.VALUE_ERROR, ErrorMessages.EMPTY_PHONE),
        (User(phone_number=phone.right_number_int, id=data_for_id.wrong_id_zero),
         ("id",), ErrorTypes.GREATER_THAN_EQUAL, ErrorMessages.ID_GREATER_ONE),
        (User(phone_number=phone.right_number_int, id=data_for_id.wrong_negative_id),
         ("id",), ErrorTypes.GREATER_THAN_EQUAL, ErrorMessages.ID_GREATER_ONE),
        (User(phone_number=phone.right_number_int, id=data_for_id.big_wrong_negative_id),
         ("id",), ErrorTypes.GREATER_THAN_EQUAL, ErrorMessages.ID_GREATER_ONE),
        (User(phone_number=phone.right_number_int, id=data_for_id.wrong_id_str),
         ("id",), ErrorTypes.INT_TYPE, ErrorMessages.INT_TYPE),
        (User(phone_number=phone.right_number_int, id=data_for_id.wrong_id_none),
         ("id",), ErrorTypes.INT_TYPE, ErrorMessages.INT_TYPE),
        (User(phone_number=phone.right_number_int, id=data_for_id.wrong_id_float),
         ("id",), ErrorTypes.INT_TYPE, ErrorMessages.INT_TYPE),
        (User(phone_number=phone.right_number_int, id=data_for_id.wrong_id_false),
         ("id",), ErrorTypes.INT_TYPE, ErrorMessages.INT_TYPE),
        (User(phone_number=phone.right_number_int, id=data_for_id.wrong_id_true),
         ("id",), ErrorTypes.INT_TYPE, ErrorMessages.INT_TYPE),
    ])
    def test_response_user_wrong(self, user, error_loc, error_type, error_msg):
        with pytest.raises(ValidationError) as error:
            specialization = UserResponse.model_validate(user)
        errors = error.value.errors()
        assert len(errors) == 1
        error = errors[0]
        assert error["loc"] == error_loc
        assert error["type"] == error_type
        assert error_msg in error["msg"]
