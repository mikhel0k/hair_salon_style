from dataclasses import dataclass

from tests.unit.test_schemas.conftest import make_name_fixture

Name = make_name_fixture(min_length=3, max_length=60, default_name="Man`s haircut")

MIN_PRICE = 0
MAX_PRICE = 10000
MIN_DURATION = 10
MAX_DURATION = 180


@dataclass
class Price:
    correct_price: float = 500
    correct_price_small: float = MIN_PRICE + 1
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
