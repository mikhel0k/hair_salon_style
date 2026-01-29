from dataclasses import dataclass

MIN_NAME_LENGTH = 3
MAX_NAME_LENGTH = 60
MAX_PRICE = 10000
MIN_PRICE = 0
MAX_DURATION = 180
MIN_DURATION = 10


@dataclass
class Name:
    correct_name: str = "Man`s haircut"
    correct_name_short: str = "a" * MIN_NAME_LENGTH
    correct_name_long: str = "a" * MAX_NAME_LENGTH
    correct_name_сyrillic: str = "Стрижка"
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
class Price:
    correct_price: float = 500
    correct_price_small: float = MIN_PRICE+1
    correct_price_big: float = MAX_PRICE
    correct_price_float: float = 500.50
    correct_price_three_numbers_after_coma: float = 500.555
    correct_price_string: str = "100"
    correct_price_string_with_coma: str = "500.50"
    wrong_price_zero: float = 0
    wrong_price_negative: float = -500
    wrong_price_negative_small: float = -1
    wrong_price_negative_big: float = -MAX_PRICE
    wrong_price_big: float = MAX_PRICE + 1
    wrong_price_negative_float: float = -500.50
    wrong_price_negative_three_numbers_after_coma: float = -500.555
    wrong_price_string = "asd"
    wrong_price_none = None

@dataclass
class Duration:
    correct_duration: int = 60
    correct_duration_small: int = MIN_DURATION + 1
    correct_duration_big: int = MAX_DURATION
    correct_duration_string: str = "60"
    wrong_duration_zero: int = 0
    wrong_duration_negative: int = -60
    wrong_duration_negative_small: int = -MIN_PRICE
    wrong_duration_negative_big: int = -1
    wrong_duration_big: int = MAX_DURATION + 1
    wrong_duration_float: float = 60.5

