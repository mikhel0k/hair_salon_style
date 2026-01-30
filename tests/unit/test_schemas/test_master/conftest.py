from dataclasses import dataclass

from tests.unit.test_schemas.conftest import make_name_fixture

Name = make_name_fixture(min_length=3, max_length=30, default_name="Petr")


@dataclass
class Status:
    correct_active = "ACTIVE"
    correct_vacation = "VACATION"
    correct_dismissed = "DISMISSED"
    wrong_status_string = "string"
    wrong_status_none = None
    wrong_status_empty = ""
    wrong_status_boolean = True
    wrong_status_integer = 1
    wrong_status_float = 1.0


@dataclass
class Phone:
    correct_number_str_with_seven = "+79009009090"
    correct_number_str_with_eight = "89009009090"
    correct_number_int = 89009009090
    correct_number_str_with_seven_without_plus = "79009009090"
    wrong_number_str_with_two_without_plus = "29009009090"
    wrong_number_str_with_five_without_plus = "59009009090"
    wrong_number_str_with_two_with_plus = "+29009009090"
    wrong_number_str_with_five_with_plus = "+59009009090"
    wrong_number_str_with_eight_with_plus = "+89009009090"
    wrong_number_str_with_seven_short = "+790090090"
    wrong_number_int_short = 890090090
    wrong_number_str_with_seven_long = "+7900900909090"
    wrong_number_int_long = 8900900909090
    wrong_number_none = None
    wrong_number_empty = ""
    wrong_number_true = True
    wrong_number_false = False


@dataclass
class Email:
    correct_string_mail = "example@mail.ru"
    correct_string_gmail = "example@gmail.com"
    correct_string_yandex = "example@yandex.ru"
    correct_string_long = f"{'a'*(50-8)}@mail.ru"
    wrong_string_without_dog = "examplemail.ru"
    wrong_string_without_email = "example@.ru"
    wrong_string_mail_without_dot = "example@mailru"
    wrong_string_mail_without_ru = "example@mail."
    wrong_string_without_dog_mail = "example.ru"
    wrong_string_without_dot_ru = "example@mail"
    wrong_email_int = 1
    wrong_email_none = None
    wrong_email_empty = ""
    wrong_email_true = True
    wrong_email_false = False
