import phonenumbers
import pytest
from pydantic import ValidationError

from app.schemas.User import UserFind
from conftest import Phone
from tests.unit.test_schemas.conftest_exceptions import ErrorMessages, ErrorTypes


class TestFindUser:
    phone = Phone()

    @pytest.mark.parametrize("phone", [
        phone.correct_number_int,
        phone.correct_number_str_with_eight,
        phone.correct_number_str_with_seven,
        phone.correct_number_str_with_seven_without_plus
    ])
    def test_find_user_correct(self, phone):
        user = UserFind(phone_number=phone)
        assert isinstance(user, UserFind)
        parsed = phonenumbers.parse(str(phone), "RU")
        if phonenumbers.is_valid_number(parsed):
            assert user.phone_number == phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.E164)

    @pytest.mark.parametrize("phone, error_loc, error_type, error_msg", [
        (phone.wrong_number_str_with_two_without_plus,
         ("phone_number",), ErrorTypes.VALUE_ERROR, ErrorMessages.INVALID_PHONE_FORMAT),
        (phone.wrong_number_str_with_five_without_plus,
         ("phone_number",), ErrorTypes.VALUE_ERROR, ErrorMessages.INVALID_PHONE_FORMAT),
        (phone.wrong_number_str_with_two_with_plus,
         ("phone_number",), ErrorTypes.VALUE_ERROR, ErrorMessages.INVALID_PHONE_FORMAT),
        (phone.wrong_number_str_with_five_with_plus,
         ("phone_number",), ErrorTypes.VALUE_ERROR, ErrorMessages.INVALID_PHONE_FORMAT),
        (phone.wrong_number_str_with_eight_with_plus,
         ("phone_number",), ErrorTypes.VALUE_ERROR, ErrorMessages.INVALID_PHONE_FORMAT),
        (phone.wrong_number_str_with_seven_short,
         ("phone_number",), ErrorTypes.VALUE_ERROR, ErrorMessages.INVALID_PHONE_FORMAT),
        (phone.wrong_number_int_short,
         ("phone_number",), ErrorTypes.VALUE_ERROR, ErrorMessages.INVALID_PHONE_FORMAT),
        (phone.wrong_number_str_with_seven_long,
         ("phone_number",), ErrorTypes.VALUE_ERROR, ErrorMessages.INVALID_PHONE_FORMAT),
        (phone.wrong_number_int_long,
         ("phone_number",), ErrorTypes.VALUE_ERROR, ErrorMessages.INVALID_PHONE_FORMAT),
        (phone.wrong_number_none,
         ("phone_number",), ErrorTypes.VALUE_ERROR, ErrorMessages.EMPTY_PHONE),
        (phone.wrong_number_empty,
         ("phone_number",), ErrorTypes.VALUE_ERROR, ErrorMessages.EMPTY_PHONE),
        (phone.wrong_number_true,
         ("phone_number",), ErrorTypes.VALUE_ERROR, ErrorMessages.INVALID_PHONE_FORMAT),
        (phone.wrong_number_false,
         ("phone_number",), ErrorTypes.VALUE_ERROR, ErrorMessages.EMPTY_PHONE),
    ])
    def test_find_user_wrong(self, phone, error_loc, error_type, error_msg):
        with pytest.raises(ValidationError) as error:
            user = UserFind(phone_number=phone)
        errors = error.value.errors()
        assert len(errors) == 1
        error = errors[0]
        assert error["loc"] == error_loc
        assert error["type"] == error_type
        assert error_msg in error["msg"]
