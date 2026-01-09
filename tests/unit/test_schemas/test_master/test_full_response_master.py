import phonenumbers
import pytest

from app.schemas.Master import MasterFullResponse
from app.schemas.Specialization import SpecializationResponse
from conftest import Name, Phone, Email, Status
from tests.unit.test_schemas.conftest_exceptions import ErrorMessages, ErrorTypes, DataForId


class TestFullResponseMaster:
    name = Name()
    phone_number = Phone()
    email = Email()
    status = Status()
    data_for_id = DataForId()
    specialization = SpecializationResponse(
        id=1,
        name="Barber",
    )

    @pytest.mark.parametrize("master_data, master_id, specialization_id, name, phone, email, status", [
        (MasterFullResponse(id=data_for_id.right_id, specialization_id=data_for_id.right_id, name=name.right_name,
                        phone=phone_number.right_number_str_with_eight, email=email.right_string_mail,
                        status=status.right_active, specialization=specialization),
         data_for_id.right_id, data_for_id.right_id, name.right_name, phone_number.right_number_str_with_eight,
         email.right_string_mail, status.right_active),
        (MasterFullResponse(id=data_for_id.right_id, specialization_id=data_for_id.right_id, name=name.right_name_short, 
                        phone=phone_number.right_number_str_with_eight, email=email.right_string_mail, 
                        status=status.right_active, specialization=specialization),
         data_for_id.right_id, data_for_id.right_id, name.right_name_short, phone_number.right_number_str_with_eight, 
         email.right_string_mail, status.right_active),
        (MasterFullResponse(id=data_for_id.right_id, specialization_id=data_for_id.right_id, name=name.right_name_long,
                        phone=phone_number.right_number_str_with_eight, email=email.right_string_mail,
                        status=status.right_active, specialization=specialization),
         data_for_id.right_id, data_for_id.right_id, name.right_name_long, phone_number.right_number_str_with_eight,
         email.right_string_mail, status.right_active),
        (MasterFullResponse(id=data_for_id.right_id, specialization_id=data_for_id.right_id, name=name.right_name_сyrillic,
                        phone=phone_number.right_number_str_with_eight, email=email.right_string_mail,
                        status=status.right_active, specialization=specialization),
         data_for_id.right_id, data_for_id.right_id, name.right_name_сyrillic, phone_number.right_number_str_with_eight,
         email.right_string_mail, status.right_active),
        (MasterFullResponse(id=data_for_id.right_id, specialization_id=data_for_id.right_id, name=name.right_name,
                        phone=phone_number.right_number_str_with_seven, email=email.right_string_mail,
                        status=status.right_active, specialization=specialization),
         data_for_id.right_id, data_for_id.right_id, name.right_name, phone_number.right_number_str_with_seven,
         email.right_string_mail, status.right_active),
        (MasterFullResponse(id=data_for_id.right_id, specialization_id=data_for_id.right_id, name=name.right_name,
                        phone=phone_number.right_number_int, email=email.right_string_mail,
                        status=status.right_active, specialization=specialization),
         data_for_id.right_id, data_for_id.right_id, name.right_name, phone_number.right_number_int,
         email.right_string_mail, status.right_active),
        (MasterFullResponse(id=data_for_id.right_id, specialization_id=data_for_id.right_id, name=name.right_name,
                        phone=phone_number.right_number_str_with_eight, email=email.right_string_gmail,
                        status=status.right_active, specialization=specialization),
         data_for_id.right_id, data_for_id.right_id, name.right_name, phone_number.right_number_str_with_eight,
         email.right_string_gmail, status.right_active),
        (MasterFullResponse(id=data_for_id.right_id, specialization_id=data_for_id.right_id, name=name.right_name,
                        phone=phone_number.right_number_str_with_eight, email=email.right_string_yandex,
                        status=status.right_active, specialization=specialization),
         data_for_id.right_id, data_for_id.right_id, name.right_name, phone_number.right_number_str_with_eight,
         email.right_string_yandex, status.right_active),
        (MasterFullResponse(id=data_for_id.right_id, specialization_id=data_for_id.right_id, name=name.right_name,
                        phone=phone_number.right_number_str_with_eight, email=email.right_string_long,
                        status=status.right_active, specialization=specialization),
         data_for_id.right_id, data_for_id.right_id, name.right_name, phone_number.right_number_str_with_eight,
         email.right_string_long, status.right_active),
        (MasterFullResponse(id=data_for_id.right_id, specialization_id=data_for_id.right_id, name=name.right_name,
                        phone=phone_number.right_number_str_with_eight, email=email.right_string_mail,
                        status=status.right_vacation, specialization=specialization),
         data_for_id.right_id, data_for_id.right_id, name.right_name, phone_number.right_number_str_with_eight,
         email.right_string_mail, status.right_vacation),
        (MasterFullResponse(id=data_for_id.right_id, specialization_id=data_for_id.right_id, name=name.right_name,
                        phone=phone_number.right_number_str_with_eight, email=email.right_string_mail,
                        status=status.right_dismissed, specialization=specialization),
         data_for_id.right_id, data_for_id.right_id, name.right_name, phone_number.right_number_str_with_eight,
         email.right_string_mail, status.right_dismissed),
        (MasterFullResponse(id=data_for_id.right_id, specialization_id=data_for_id.big_right_id, name=name.right_name,
                        phone=phone_number.right_number_str_with_eight, email=email.right_string_mail,
                        status=status.right_active, specialization=specialization),
         data_for_id.right_id, data_for_id.big_right_id, name.right_name, phone_number.right_number_str_with_eight,
         email.right_string_mail, status.right_active),
        (MasterFullResponse(id=data_for_id.big_right_id, specialization_id=data_for_id.right_id, name=name.right_name,
                        phone=phone_number.right_number_str_with_eight, email=email.right_string_mail,
                        status=status.right_active, specialization=specialization),
         data_for_id.big_right_id, data_for_id.right_id, name.right_name, phone_number.right_number_str_with_eight,
         email.right_string_mail, status.right_active),
    ])
    def test_full_response_master_right(self, master_data, master_id, specialization_id, name, phone, email, status):
        master = MasterFullResponse.model_validate(master_data)
        assert isinstance(master, MasterFullResponse)
        assert master.specialization_id == specialization_id
        assert master.name == name.title()
        parsed = phonenumbers.parse(str(phone), "RU")
        if phonenumbers.is_valid_number(parsed):
            assert master.phone == phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.E164)
        assert master.email == email
        assert master.status == status
        assert master.specialization.id == 1
        assert master.specialization.name == "Barber"

