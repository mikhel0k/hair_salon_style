from dataclasses import dataclass

MIN_NAME_LENGTH = 3
MAX_NAME_LENGTH = 30
MIN_EMAIL_LENGTH = 8
MAX_EMAIL_LENGTH = 50


@dataclass
class Status:
    right_active = "active"
    right_vacation = "vacation"
    right_dismissed = "dismissed"
    wrong_status_string = "string"
    wrong_status_none = None
    wrong_status_empty = ""
    wrong_status_boolean = True
    wrong_status_integer = 1
    wrong_status_float = 1.0


@dataclass
class Name:
    right_name: str = "Petr"
    right_name_short: str = "a" * MIN_NAME_LENGTH
    right_name_long: str = "a" * MAX_NAME_LENGTH
    right_name_сyrillic: str = "Стрижка"
    wrong_name_long: str = "a" * (MAX_NAME_LENGTH + 1)
    wrong_name_short: str = "a" * (MIN_NAME_LENGTH - 1)
    wrong_name_int: int = 1
    wrong_name_empty: str = ""
    wrong_name_spaces: str = "   "
    wrong_name_none: None = None
    wrong_invalid_character: str = f"{"a" * MIN_NAME_LENGTH}?"
    wrong_consecutive_spaces: str = f"{"a" * (MIN_NAME_LENGTH//2)}  {"a" * (MIN_NAME_LENGTH//2 + 1)}"
    wrong_consecutive_hyphens: str = f"{"a" * (MIN_NAME_LENGTH//2)}--{"a" * (MIN_NAME_LENGTH//2 + 1)}"
    wrong_consecutive_apostrophes: str = f"{"a" * (MIN_NAME_LENGTH//2)}``{"a" * (MIN_NAME_LENGTH//2 + 1)}"
    wrong_consecutive_underscores: str = f"{"a" * (MIN_NAME_LENGTH//2)}__{"a" * (MIN_NAME_LENGTH//2 + 1)}"
    wrong_start_with_hyphen: str = f"-{"a" * MIN_NAME_LENGTH}"
    wrong_start_with_apostrophe: str = f"`{"a" * MIN_NAME_LENGTH}"
    wrong_start_with_underscore: str = f"_{"a" * MIN_NAME_LENGTH}"
    wrong_end_with_hyphen: str = f"{"a" * MIN_NAME_LENGTH}-"
    wrong_end_with_apostrophe: str = f"{"a" * MIN_NAME_LENGTH}`"
    wrong_end_with_underscore: str = f"{"a" * MIN_NAME_LENGTH}_"
    wrong_space_and_hyphen_adjacent: str = f"{"a" * (MIN_NAME_LENGTH//2)} -{"a" * (MIN_NAME_LENGTH//2 + 1)}"
    wrong_space_and_apostrophe_adjacent: str = f"{"a" * (MIN_NAME_LENGTH//2)} `{"a" * (MIN_NAME_LENGTH//2 + 1)}"
    wrong_space_and_underscore_adjacent: str = f"{"a" * (MIN_NAME_LENGTH//2)} _{"a" * (MIN_NAME_LENGTH//2 + 1)}"
    wrong_hyphen_and_space_adjacent: str = f"{"a" * (MIN_NAME_LENGTH//2)}- {"a" * (MIN_NAME_LENGTH//2 + 1)}"
    wrong_apostrophe_and_space_adjacent: str = f"{"a" * (MIN_NAME_LENGTH//2)}` {"a" * (MIN_NAME_LENGTH//2 + 1)}"
    wrong_underscore_and_space_adjacent: str = f"{"a" * (MIN_NAME_LENGTH//2)}_ {"a" * (MIN_NAME_LENGTH//2 + 1)}"


@dataclass
class Phone:
    right_number_str_with_seven = "+79009009090"
    right_number_str_with_eight = "89009009090"
    right_number_int = 89009009090
    right_number_str_with_seven_without_plus = "79009009090"
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
    right_string_mail = "example@mail.ru"
    right_string_gmail = "example@gmail.com"
    right_string_yandex = "example@yandex.ru"
    right_string_long = f"{"a"*(50-8)}@mail.ru"
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
