from dataclasses import dataclass

MIN_NAME_LENGTH = 3
MAX_NAME_LENGTH = 60
MAX_PRICE = 10000
MIN_PRICE = 0
MAX_DURATION = 180
MIN_DURATION = 0


@dataclass
class Name:
    right_name: str = "man`s haircut"
    right_name_short: str = "a" * MIN_NAME_LENGTH
    right_name_long: str = "a" * MAX_NAME_LENGTH
    right_name_сyrillic: str = "Стрижка"
    wrong_name_long: str = "a" * (MAX_NAME_LENGTH + 1)
    wrong_name_short: str = "a" * (MIN_NAME_LENGTH - 1)
    wrong_name_int: int = 1
    wrong_name_empty: str = ""
    wrong_name_spaces: str = "   "
    wrong_name_none: None = None


class Price:
    right_price: float = 500
    right_price_small: float = MIN_PRICE+1
    right_price_big: float = MAX_PRICE
    right_price_float: float = 500.50
    right_price_three_numbers_after_coma: float = 500.555
    right_price_string: str = "100"
    right_price_string_with_coma: str = "500.50"
    wrong_price_zero: float = 0
    wrong_price_negative: float = -500
    wrong_price_negative_small: float = -1
    wrong_price_negative_big: float = -MAX_PRICE
    wrong_price_big: float = MAX_PRICE + 1
    wrong_price_negative_float: float = -500.50
    wrong_price_negative_three_numbers_after_coma: float = -500.555
    wrong_price_string = "asd"
    wrong_price_none = None


class Duration:
    right_duration: int = 60
    right_duration_small: int = MIN_DURATION + 1
    right_duration_big: int = MAX_DURATION
    right_duration_string: str = "60"
    wrong_duration_zero: int = 0
    wrong_duration_negative: int = -60
    wrong_duration_negative_small: int = -MIN_PRICE
    wrong_duration_negative_big: int = -1
    wrong_duration_big: int = MAX_DURATION + 1
    wrong_duration_float: float = 60.5

