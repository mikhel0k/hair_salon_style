import phonenumbers
import pytest

from app.schemas.Master import MasterUpdate
from conftest import Name, Phone, Email, Status
from tests.unit.test_schemas.conftest_exceptions import ErrorMessages, ErrorTypes, DataForId


class TestUpdateMaster:
    name = Name()
    phone_number = Phone()
    email = Email()
    status = Status()
    data_for_id = DataForId()

    @pytest.mark.parametrize("specialization_id, name, phone, email, status", [
        (data_for_id.right_id, name.right_name, phone_number.right_number_str_with_eight, email.right_string_mail, Status.right_active),
        (data_for_id.right_id, name.right_name_short, phone_number.right_number_str_with_eight, email.right_string_mail, Status.right_active),
        (data_for_id.right_id, name.right_name_long, phone_number.right_number_str_with_eight, email.right_string_mail, Status.right_active),
        (data_for_id.right_id, name.right_name_сyrillic, phone_number.right_number_str_with_eight, email.right_string_mail, Status.right_active),
        (data_for_id.right_id, name.right_name, phone_number.right_number_str_with_seven, email.right_string_mail, Status.right_active),
        (data_for_id.right_id, name.right_name, phone_number.right_number_int, email.right_string_mail, Status.right_active),
        (data_for_id.right_id, name.right_name, phone_number.right_number_str_with_eight, email.right_string_gmail, Status.right_active),
        (data_for_id.right_id, name.right_name, phone_number.right_number_str_with_eight, email.right_string_yandex, Status.right_active),
        (data_for_id.right_id, name.right_name, phone_number.right_number_str_with_eight, email.right_string_long, Status.right_active),
        (data_for_id.right_id, name.right_name, phone_number.right_number_str_with_eight, email.right_string_mail, Status.right_vacation),
        (data_for_id.right_id, name.right_name, phone_number.right_number_str_with_eight, email.right_string_mail, Status.right_dismissed),
        (data_for_id.big_right_id, name.right_name, phone_number.right_number_str_with_eight, email.right_string_mail, Status.right_active),
        (data_for_id.right_id, None, None, None, None),
        (None, name.right_name, None, None, None),
        (None, None, phone_number.right_number_str_with_eight, None, None),
        (None, None, None, email.right_string_mail, None),
        (None, None, None, None, Status.right_active),
    ])
    def test_update_master_right(self, specialization_id, name, phone, email, status):
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

