from dataclasses import dataclass

MIN_NAME_LENGTH = 3
MAX_NAME_LENGTH = 40


@dataclass
class Name:
    correct_name: str = "Barber"
    correct_name_short: str = "a" * MIN_NAME_LENGTH
    correct_name_long: str = "a" * MAX_NAME_LENGTH
    correct_name_сyrillic: str = "Парикмахер"
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