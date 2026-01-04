from dataclasses import dataclass

MIN_LENGTH = 3
MAX_LENGTH = 60


@dataclass
class Name:
    right_name: str = "haircut"
    right_name_short: str = "a" * MIN_LENGTH
    right_name_long: str = "a" * MAX_LENGTH
    right_name_сyrillic: str = "Стрижка"
    wrong_name_long: str = "a" * (MAX_LENGTH + 1)
    wrong_name_short: str = "a" * (MIN_LENGTH - 1)
    wrong_name_int: int = 1
    wrong_name_empty: str = ""
    wrong_name_spaces: str = "   "
    wrong_name_none: None = None