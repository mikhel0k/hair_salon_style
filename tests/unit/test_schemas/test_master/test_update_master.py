import phonenumbers
import pytest
from pydantic import ValidationError

from app.schemas.Master import MasterUpdate
from conftest import Name, Phone, Email, Status
from tests.unit.test_schemas.conftest_exceptions import ErrorMessages, ErrorTypes, DataForId


class TestUpdateMaster:
    name = Name()
    phone = Phone()
    email = Email()
    status = Status()
    data_for_id = DataForId()

    @pytest.mark.parametrize("specialization_id, name, phone, email, status", [
        (data_for_id.correct_id, name.correct_name, phone.correct_number_str_with_eight, email.correct_string_mail, Status.correct_active),
        (data_for_id.correct_id, name.correct_name_short, phone.correct_number_str_with_eight, email.correct_string_mail, Status.correct_active),
        (data_for_id.correct_id, name.correct_name_long, phone.correct_number_str_with_eight, email.correct_string_mail, Status.correct_active),
        (data_for_id.correct_id, name.correct_name_сyrillic, phone.correct_number_str_with_eight, email.correct_string_mail, Status.correct_active),
        (data_for_id.correct_id, name.correct_name, phone.correct_number_str_with_seven, email.correct_string_mail, Status.correct_active),
        (data_for_id.correct_id, name.correct_name, phone.correct_number_int, email.correct_string_mail, Status.correct_active),
        (data_for_id.correct_id, name.correct_name, phone.correct_number_str_with_eight, email.correct_string_gmail, Status.correct_active),
        (data_for_id.correct_id, name.correct_name, phone.correct_number_str_with_eight, email.correct_string_yandex, Status.correct_active),
        (data_for_id.correct_id, name.correct_name, phone.correct_number_str_with_eight, email.correct_string_long, Status.correct_active),
        (data_for_id.correct_id, name.correct_name, phone.correct_number_str_with_eight, email.correct_string_mail, Status.correct_vacation),
        (data_for_id.correct_id, name.correct_name, phone.correct_number_str_with_eight, email.correct_string_mail, Status.correct_dismissed),
        (data_for_id.big_correct_id, name.correct_name, phone.correct_number_str_with_eight, email.correct_string_mail, Status.correct_active),
        (data_for_id.correct_id, None, None, None, None),
        (None, name.correct_name, None, None, None),
        (None, None, phone.correct_number_str_with_eight, None, None),
        (None, None, None, email.correct_string_mail, None),
        (None, None, None, None, Status.correct_active),
    ])
    def test_update_master_correct(self, specialization_id, name, phone, email, status):
        master = MasterUpdate(
            specialization_id=specialization_id,
            name=name,
            phone=phone,
            email=email,
            status=status,
        )
        assert isinstance(master, MasterUpdate)
        assert master.specialization_id == specialization_id
        if name:
            assert master.name == name.title()
        else:
            assert master.name is None
        if phone:
            parsed = phonenumbers.parse(str(phone), "RU")
            if phonenumbers.is_valid_number(parsed):
                assert master.phone == phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.E164)
            else:
                raise ValueError("Phone number must be valid")
        else:
            assert master.phone is None
        assert master.email == email
        assert master.status == status

    @pytest.mark.parametrize(
        "name, phone, email, status, specialization_id, error_loc, error_type, error_msg", [
            (name.wrong_name_long, phone.correct_number_str_with_eight, email.correct_string_mail,
             status.correct_active, data_for_id.correct_id,
             ("name",), ErrorTypes.STRING_TOO_LONG, ErrorMessages.STRING_TOO_LONG_30),
            (name.wrong_name_short, phone.correct_number_str_with_eight, email.correct_string_mail,
             status.correct_active, data_for_id.correct_id,
             ("name",), ErrorTypes.STRING_TOO_SHORT, ErrorMessages.STRING_TOO_SHORT),
            (name.wrong_name_int, phone.correct_number_str_with_eight, email.correct_string_mail,
             status.correct_active, data_for_id.correct_id,
             ("name",), ErrorTypes.VALUE_ERROR, ErrorMessages.VAIT_STRING), #1111111
            (name.wrong_name_empty, phone.correct_number_str_with_eight, email.correct_string_mail,
             status.correct_active, data_for_id.correct_id,
             ("name",), ErrorTypes.STRING_TOO_SHORT, ErrorMessages.STRING_TOO_SHORT),
            (name.wrong_name_spaces, phone.correct_number_str_with_eight, email.correct_string_mail,
             status.correct_active, data_for_id.correct_id,
             ("name",), ErrorTypes.STRING_TOO_SHORT, ErrorMessages.STRING_TOO_SHORT),
            (name.wrong_invalid_character, phone.correct_number_str_with_eight, email.correct_string_mail,
             status.correct_active, data_for_id.correct_id,
             ("name",), ErrorTypes.VALUE_ERROR, ErrorMessages.WRONG_INVALID_CHARACTER),
            (name.wrong_consecutive_spaces, phone.correct_number_str_with_eight, email.correct_string_mail,
             status.correct_active, data_for_id.correct_id,
             ("name",), ErrorTypes.VALUE_ERROR, ErrorMessages.WRONG_CONSECUTIVE_SPACES),
            (name.wrong_consecutive_hyphens, phone.correct_number_str_with_eight, email.correct_string_mail,
             status.correct_active, data_for_id.correct_id,
             ("name",), ErrorTypes.VALUE_ERROR, ErrorMessages.WRONG_CONSECUTIVE_HYPHENS),
            (name.wrong_consecutive_apostrophes, phone.correct_number_str_with_eight, email.correct_string_mail,
             status.correct_active, data_for_id.correct_id,
             ("name",), ErrorTypes.VALUE_ERROR, ErrorMessages.WRONG_CONSECUTIVE_APOSTROPHES),
            (name.wrong_consecutive_underscores, phone.correct_number_str_with_eight, email.correct_string_mail,
             status.correct_active, data_for_id.correct_id,
             ("name",), ErrorTypes.VALUE_ERROR, ErrorMessages.WRONG_CONSECUTIVE_UNDERSCORES),
            (name.wrong_start_with_hyphen, phone.correct_number_str_with_eight, email.correct_string_mail,
             status.correct_active, data_for_id.correct_id,
             ("name",), ErrorTypes.VALUE_ERROR, ErrorMessages.WRONG_START_WITH_HYPHEN),
            (name.wrong_start_with_apostrophe, phone.correct_number_str_with_eight, email.correct_string_mail,
             status.correct_active, data_for_id.correct_id,
             ("name",), ErrorTypes.VALUE_ERROR, ErrorMessages.WRONG_START_WITH_APOSTROPHE),
            (name.wrong_start_with_underscore, phone.correct_number_str_with_eight, email.correct_string_mail,
             status.correct_active, data_for_id.correct_id,
             ("name",), ErrorTypes.VALUE_ERROR, ErrorMessages.WRONG_START_WITH_UNDERSCORE),
            (name.wrong_end_with_hyphen, phone.correct_number_str_with_eight, email.correct_string_mail,
             status.correct_active, data_for_id.correct_id,
             ("name",), ErrorTypes.VALUE_ERROR, ErrorMessages.WRONG_END_WITH_HYPHEN),
            (name.wrong_end_with_apostrophe, phone.correct_number_str_with_eight, email.correct_string_mail,
             status.correct_active, data_for_id.correct_id,
             ("name",), ErrorTypes.VALUE_ERROR, ErrorMessages.WRONG_END_WITH_APOSTROPHE),
            (name.wrong_end_with_underscore, phone.correct_number_str_with_eight, email.correct_string_mail,
             status.correct_active, data_for_id.correct_id,
             ("name",), ErrorTypes.VALUE_ERROR, ErrorMessages.WRONG_END_WITH_UNDERSCORE),
            (name.wrong_space_and_hyphen_adjacent, phone.correct_number_str_with_eight, email.correct_string_mail,
             status.correct_active, data_for_id.correct_id,
             ("name",), ErrorTypes.VALUE_ERROR, ErrorMessages.WRONG_SPACE_AND_HYPHEN_ADJACENT),
            (name.wrong_space_and_apostrophe_adjacent, phone.correct_number_str_with_eight, email.correct_string_mail,
             status.correct_active, data_for_id.correct_id,
             ("name",), ErrorTypes.VALUE_ERROR, ErrorMessages.WRONG_SPACE_AND_APOSTROPHE_ADJACENT),
            (name.wrong_space_and_underscore_adjacent, phone.correct_number_str_with_eight, email.correct_string_mail,
             status.correct_active, data_for_id.correct_id,
             ("name",), ErrorTypes.VALUE_ERROR, ErrorMessages.WRONG_SPACE_AND_UNDERSCORE_ADJACENT),
            (name.wrong_hyphen_and_space_adjacent, phone.correct_number_str_with_eight, email.correct_string_mail,
             status.correct_active, data_for_id.correct_id,
             ("name",), ErrorTypes.VALUE_ERROR, ErrorMessages.WRONG_SPACE_AND_HYPHEN_ADJACENT),
            (name.wrong_apostrophe_and_space_adjacent, phone.correct_number_str_with_eight, email.correct_string_mail,
             status.correct_active, data_for_id.correct_id,
             ("name",), ErrorTypes.VALUE_ERROR, ErrorMessages.WRONG_SPACE_AND_APOSTROPHE_ADJACENT),
            (name.wrong_underscore_and_space_adjacent, phone.correct_number_str_with_eight, email.correct_string_mail,
             status.correct_active, data_for_id.correct_id,
             ("name",), ErrorTypes.VALUE_ERROR, ErrorMessages.WRONG_SPACE_AND_UNDERSCORE_ADJACENT),
            (name.correct_name, phone.wrong_number_str_with_two_without_plus, email.correct_string_mail,
             status.correct_active, data_for_id.correct_id,
             ("phone",), ErrorTypes.VALUE_ERROR, ErrorMessages.INVALID_PHONE_FORMAT),
            (name.correct_name, phone.wrong_number_str_with_five_without_plus, email.correct_string_mail,
             status.correct_active, data_for_id.correct_id,
             ("phone",), ErrorTypes.VALUE_ERROR, ErrorMessages.INVALID_PHONE_FORMAT),
            (name.correct_name, phone.wrong_number_str_with_two_with_plus, email.correct_string_mail,
             status.correct_active, data_for_id.correct_id,
             ("phone",), ErrorTypes.VALUE_ERROR, ErrorMessages.INVALID_PHONE_FORMAT),
            (name.correct_name, phone.wrong_number_str_with_five_with_plus, email.correct_string_mail,
             status.correct_active, data_for_id.correct_id,
             ("phone",), ErrorTypes.VALUE_ERROR, ErrorMessages.INVALID_PHONE_FORMAT),
            (name.correct_name, phone.wrong_number_str_with_eight_with_plus, email.correct_string_mail,
             status.correct_active, data_for_id.correct_id,
             ("phone",), ErrorTypes.VALUE_ERROR, ErrorMessages.INVALID_PHONE_FORMAT),
            (name.correct_name, phone.wrong_number_str_with_seven_short, email.correct_string_mail,
             status.correct_active, data_for_id.correct_id,
             ("phone",), ErrorTypes.VALUE_ERROR, ErrorMessages.INVALID_PHONE_FORMAT),
            (name.correct_name, phone.wrong_number_int_short, email.correct_string_mail,
             status.correct_active, data_for_id.correct_id,
             ("phone",), ErrorTypes.VALUE_ERROR, ErrorMessages.INVALID_PHONE_FORMAT),
            (name.correct_name, phone.wrong_number_str_with_seven_long, email.correct_string_mail,
             status.correct_active, data_for_id.correct_id,
             ("phone",), ErrorTypes.VALUE_ERROR, ErrorMessages.INVALID_PHONE_FORMAT),
            (name.correct_name, phone.wrong_number_int_long, email.correct_string_mail,
             status.correct_active, data_for_id.correct_id,
             ("phone",), ErrorTypes.VALUE_ERROR, ErrorMessages.INVALID_PHONE_FORMAT),
            (name.correct_name, phone.wrong_number_empty, email.correct_string_mail,
             status.correct_active, data_for_id.correct_id,
             ("phone",), ErrorTypes.STRING_TOO_SHORT, ErrorMessages.PHONE_NUMBER_TOO_SHORT),
            (name.correct_name, phone.wrong_number_true, email.correct_string_mail,
             status.correct_active, data_for_id.correct_id,
             ("phone",), ErrorTypes.VALUE_ERROR, ErrorMessages.INVALID_PHONE_FORMAT),
            (name.correct_name, phone.wrong_number_false, email.correct_string_mail,
             status.correct_active, data_for_id.correct_id,
             ("phone",), ErrorTypes.STRING_TYPE, ErrorMessages.STRING_TYPE),
            (name.correct_name, phone.correct_number_str_with_eight, email.wrong_string_without_dog,
             status.correct_active, data_for_id.correct_id,
             ("email",), ErrorTypes.VALUE_ERROR, ErrorMessages.EMAIL_MISS_DOG),
            (name.correct_name, phone.correct_number_str_with_eight, email.wrong_string_without_email,
             status.correct_active, data_for_id.correct_id,
             ("email",), ErrorTypes.VALUE_ERROR, ErrorMessages.EMAIL_MISS_PERIOD),
            (name.correct_name, phone.correct_number_str_with_eight, email.wrong_string_mail_without_dot,
             status.correct_active, data_for_id.correct_id,
             ("email",), ErrorTypes.VALUE_ERROR, ErrorMessages.EMAIL_INVALID_PERIOD),
            (name.correct_name, phone.correct_number_str_with_eight, email.wrong_string_mail_without_ru,
             status.correct_active, data_for_id.correct_id,
             ("email",), ErrorTypes.VALUE_ERROR, ErrorMessages.EMAIL_END_WITH_PERIOD),
            (name.correct_name, phone.correct_number_str_with_eight, email.wrong_string_without_dog_mail,
             status.correct_active, data_for_id.correct_id,
             ("email",), ErrorTypes.VALUE_ERROR, ErrorMessages.EMAIL_MISS_DOG),
            (name.correct_name, phone.correct_number_str_with_eight, email.wrong_string_without_dot_ru,
             status.correct_active, data_for_id.correct_id,
             ("email",), ErrorTypes.VALUE_ERROR, ErrorMessages.EMAIL_INVALID_PERIOD),
            (name.correct_name, phone.correct_number_str_with_eight, email.wrong_email_int,
             status.correct_active, data_for_id.correct_id,
             ("email",), ErrorTypes.STRING_TYPE, ErrorMessages.STRING_TYPE),
            (name.correct_name, phone.correct_number_str_with_eight, email.wrong_email_empty,
             status.correct_active, data_for_id.correct_id,
             ("email",), ErrorTypes.VALUE_ERROR, ErrorMessages.EMAIL_MISS_DOG),
            (name.correct_name, phone.correct_number_str_with_eight, email.wrong_email_true,
             status.correct_active, data_for_id.correct_id,
             ("email",), ErrorTypes.STRING_TYPE, ErrorMessages.STRING_TYPE),
            (name.correct_name, phone.correct_number_str_with_eight, email.wrong_email_false,
             status.correct_active, data_for_id.correct_id,
             ("email",), ErrorTypes.STRING_TYPE, ErrorMessages.STRING_TYPE),
            (name.correct_name, phone.correct_number_str_with_eight, email.correct_string_mail,
             status.wrong_status_string, data_for_id.correct_id,
             ("status",), ErrorTypes.ENUM, ErrorMessages.ENUM_MASTER),
            (name.correct_name, phone.correct_number_str_with_eight, email.correct_string_mail,
             status.wrong_status_empty, data_for_id.correct_id,
             ("status",), ErrorTypes.ENUM, ErrorMessages.ENUM_MASTER),
            (name.correct_name, phone.correct_number_str_with_eight, email.correct_string_mail,
             status.wrong_status_boolean, data_for_id.correct_id,
             ("status",), ErrorTypes.ENUM, ErrorMessages.ENUM_MASTER),
            (name.correct_name, phone.correct_number_str_with_eight, email.correct_string_mail,
             status.wrong_status_integer, data_for_id.correct_id,
             ("status",), ErrorTypes.ENUM, ErrorMessages.ENUM_MASTER),
            (name.correct_name, phone.correct_number_str_with_eight, email.correct_string_mail,
             status.wrong_status_float, data_for_id.correct_id,
             ("status",), ErrorTypes.ENUM, ErrorMessages.ENUM_MASTER),
            (name.correct_name, phone.correct_number_str_with_eight, email.correct_string_mail,
             status.correct_active, data_for_id.wrong_id_zero,
             ("specialization_id",), ErrorTypes.GREATER_THAN_EQUAL, ErrorMessages.ID_GREATER_ONE),
            (name.correct_name, phone.correct_number_str_with_eight, email.correct_string_mail,
             status.correct_active, data_for_id.wrong_negative_id,
             ("specialization_id",), ErrorTypes.GREATER_THAN_EQUAL, ErrorMessages.ID_GREATER_ONE),
            (name.correct_name, phone.correct_number_str_with_eight, email.correct_string_mail,
             status.correct_active, data_for_id.wrong_negative_id,
             ("specialization_id",), ErrorTypes.GREATER_THAN_EQUAL, ErrorMessages.ID_GREATER_ONE),
            (name.correct_name, phone.correct_number_str_with_eight, email.correct_string_mail,
             status.correct_active, data_for_id.wrong_id_str,
             ("specialization_id",), ErrorTypes.INT_TYPE, ErrorMessages.INT_TYPE),
            (name.correct_name, phone.correct_number_str_with_eight, email.correct_string_mail,
             status.correct_active, data_for_id.wrong_id_float,
             ("specialization_id",), ErrorTypes.INT_TYPE, ErrorMessages.INT_TYPE),
            (name.correct_name, phone.correct_number_str_with_eight, email.correct_string_mail,
             status.correct_active, data_for_id.wrong_id_true,
             ("specialization_id",), ErrorTypes.INT_TYPE, ErrorMessages.INT_TYPE),
            (name.correct_name, phone.correct_number_str_with_eight, email.correct_string_mail,
             status.correct_active, data_for_id.wrong_id_false,
             ("specialization_id",), ErrorTypes.INT_TYPE, ErrorMessages.INT_TYPE),
        ]
    )
    def test_update_master_wrong(self, name, phone, email, status, specialization_id, error_loc, error_type, error_msg):
        with pytest.raises(ValidationError) as error:
            master = MasterUpdate(
                specialization_id=specialization_id,
                name=name,
                phone=phone,
                email=email,
                status=status,
            )
        errors = error.value.errors()
        assert len(errors) == 1
        error = errors[0]
        assert error["loc"] == error_loc
        assert error["type"] == error_type
        assert error_msg in error["msg"]
