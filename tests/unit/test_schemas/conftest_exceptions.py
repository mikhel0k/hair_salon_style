from dataclasses import dataclass

@dataclass
class ErrorMessages:
    STRING_TOO_LONG = "String should have at most 60 characters"
    STRING_TOO_LONG_30 = "String should have at most 30 characters"
    STRING_TOO_SHORT = "String should have at least 3 characters"
    STRING_TYPE = "Input should be a valid string"
    STRING_EMPTY = "String should have at least 3 characters"
    STRING_SPACES = "String should have at least 3 characters"
    PHONE_NUMBER_TOO_SHORT = "String should have at least 8 characters"

    PRICE_TOO_LOW = "Input should be greater than or equal to 1"
    PRICE_TOO_HIGH = "Input should be less than or equal to 10000"
    PRICE_NOT_DECIMAL = "Input should be a valid decimal"
    PRICE_NONE_TYPE = "Decimal input should be an integer, float, string or Decimal object"

    DURATION_TOO_LOW = "Input should be greater than or equal to 10"
    DURATION_TOO_HIGH = "Input should be less than or equal to 180"
    DURATION_NOT_INT = "Input should be a valid integer, got a number with a fractional part"

    SPEC_STRING_TOO_LONG = "String should have at most 40 characters"
    SPEC_STRING_TOO_SHORT = "String should have at least 3 characters"

    WRONG_INVALID_CHARACTER = "Invalid character"
    WRONG_CONSECUTIVE_SPACES = "Field cannot contain consecutive spaces"
    WRONG_CONSECUTIVE_HYPHENS = "Field cannot contain consecutive hyphens"
    WRONG_CONSECUTIVE_APOSTROPHES = "Field cannot contain consecutive apostrophes"
    WRONG_CONSECUTIVE_UNDERSCORES = "Field cannot contain consecutive underscores"
    WRONG_START_WITH_HYPHEN = "Field cannot start with a hyphen"
    WRONG_START_WITH_APOSTROPHE = "Field cannot start with a apostrophe"
    WRONG_START_WITH_UNDERSCORE = "Field cannot start with a underscore"
    WRONG_END_WITH_HYPHEN = "Field cannot end with a hyphen"
    WRONG_END_WITH_APOSTROPHE = "Field cannot end with a apostrophe"
    WRONG_END_WITH_UNDERSCORE = "Field cannot end with a underscore"
    WRONG_SPACE_AND_HYPHEN_ADJACENT = "Space and hyphen cannot be adjacent"
    WRONG_SPACE_AND_APOSTROPHE_ADJACENT = "Space and apostrophe cannot be adjacent"
    WRONG_SPACE_AND_UNDERSCORE_ADJACENT = "Space and underscore cannot be adjacent"

    DATE_IN_THE_PAST = "Value error, Date cannot be in the past"
    VALID_DATE = "Input should be a valid date"
    SHORT_DATE = "Input should be a valid date or datetime, input is too short"
    WRONG_DATE = "Datetimes provided to dates should have zero time - e.g. be exact dates"
    SHORT_TIME = "Input should be in a valid time format, input is too short"
    VALID_TIME = "Input should be a valid time"

    ENUM_CELL = "Input should be 'free' or 'occupied'"
    ENUM_MASTER = "Input should be 'active', 'vacation' or 'dismissed'"
    ENUM_RECORD = "Input should be 'created', 'confirmed', 'completed' or 'cancelled'"

    ID_GREATER_ONE = "Input should be greater than or equal to 1"
    INT_TYPE = "Input should be a valid integer"
    INVALID_PHONE_FORMAT = "Value error, Invalid phone format"
    EMPTY_PHONE = "Value error, phone_number cannot be empty"

    EMAIL_MISS_DOG = "An email address must have an @-sign."
    EMAIL_MISS_PERIOD = "value is not a valid email address: An email address cannot have a period immediately after the @-sign."
    EMAIL_INVALID_PERIOD = "value is not a valid email address: The part after the @-sign is not valid. It should have a period."
    EMAIL_END_WITH_PERIOD = "value is not a valid email address: An email address cannot end with a period."
    VAIT_STRING = "Value error, Field must be a string"

    NOT_TWO_NONE = "Value error, start and end times must both be None or not None"
    TO_EARLY = "Value error, Start time must be after 8 o`clock"
    TO_LATE = "Value error, End time must be before 20 o`clock"
    TO_SHORT = "Value error, Work time must be minimum 120 minutes"

    LESS_THAN_EQUAL_5 = "Input should be less than or equal to 5"


@dataclass
class ErrorTypes:
    STRING_TOO_LONG = "string_too_long"
    STRING_TOO_SHORT = "string_too_short"
    STRING_TYPE = "string_type"
    DECIMAL_PARSING = "decimal_parsing"
    DECIMAL_TYPE = "decimal_type"
    GREATER_THAN_EQUAL = "greater_than_equal"
    LESS_THAN_EQUAL = "less_than_equal"
    INT_FROM_FLOAT = "int_from_float"
    VALUE_ERROR = "value_error"
    DATE_FROM_DATETIME_PARSING = "date_from_datetime_parsing"
    DATE_FROM_DATETIME_INEXACT = "date_from_datetime_inexact"
    DATE_TIPE = "date_type"
    TIME_PARSING = "time_parsing"
    TIME_TYPE = "time_type"
    ENUM = "enum"
    INT_TYPE = "int_type"

@dataclass
class DataForId:
    right_id = 1
    big_right_id = 1123124
    wrong_id_zero = 0
    wrong_negative_id = -1
    big_wrong_negative_id = -1123124
    wrong_id_str = "string"
    wrong_id_none = None
    wrong_id_float = 1.5
    wrong_id_true = True
    wrong_id_false = False
