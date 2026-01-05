from dataclasses import dataclass

MIN_NAME_LENGTH = 3
MAX_NAME_LENGTH = 40


@dataclass
class Name:
    right_name: str = "Barber"
    right_name_short: str = "a" * MIN_NAME_LENGTH
    right_name_long: str = "a" * MAX_NAME_LENGTH
    right_name_сyrillic: str = "Парикмахер"
    wrong_name_long: str = "a" * (MAX_NAME_LENGTH + 1)
    wrong_name_short: str = "a" * (MIN_NAME_LENGTH - 1)
    wrong_name_int: int = 1
    wrong_name_empty: str = ""
    wrong_name_spaces: str = "   "
    wrong_name_none: None = None