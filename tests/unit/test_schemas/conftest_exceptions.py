class ErrorMessages:

    STRING_TOO_LONG = "60 characters"
    STRING_TOO_LONG_30 = "30 characters"
    STRING_TOO_SHORT = "at least 3 characters"
    STRING_TOO_SHORT_8 = "at least 8 characters"
    STRING_TYPE = "valid string"
    STRING_EMPTY = "at least 3 characters"
    STRING_SPACES = "at least 3 characters"
    PHONE_NUMBER_TOO_SHORT = "at least 8 characters"

    PRICE_TOO_LOW = "greater than or equal to 1"
    PRICE_TOO_HIGH = "less than or equal to 10000"
    PRICE_NOT_DECIMAL = "valid decimal"
    PRICE_NONE_TYPE = "integer, float, string or Decimal"

    DURATION_TOO_LOW = "greater than or equal to 10"
    DURATION_TOO_HIGH = "less than or equal to 180"
    DURATION_NOT_INT = "fractional part"

    SPEC_STRING_TOO_LONG = "40 characters"
    SPEC_STRING_TOO_SHORT = "at least 3 characters"

    WRONG_INVALID_CHARACTER = "Invalid character"
    WRONG_CONSECUTIVE_SPACES = "consecutive spaces"
    WRONG_CONSECUTIVE_HYPHENS = "consecutive hyphens"
    WRONG_CONSECUTIVE_APOSTROPHES = "consecutive apostrophes"
    WRONG_CONSECUTIVE_UNDERSCORES = "consecutive underscores"
    WRONG_START_WITH_HYPHEN = "start with a hyphen"
    WRONG_START_WITH_APOSTROPHE = "start with an apostrophe"
    WRONG_START_WITH_UNDERSCORE = "start with an underscore"
    WRONG_END_WITH_HYPHEN = "end with a hyphen"
    WRONG_END_WITH_APOSTROPHE = "end with an apostrophe"
    WRONG_END_WITH_UNDERSCORE = "end with an underscore"
    WRONG_SPACE_AND_HYPHEN_ADJACENT = ("Space and hyphen cannot be adjacent", "start with a hyphen")
    WRONG_SPACE_AND_APOSTROPHE_ADJACENT = ("Space and apostrophe cannot be adjacent", "start with an apostrophe")
    WRONG_SPACE_AND_UNDERSCORE_ADJACENT = ("Space and underscore cannot be adjacent", "start with an underscore")

    DATE_IN_THE_PAST = "Date cannot be in the past"
    VALID_DATE = "valid date"
    SHORT_DATE = "too short"
    WRONG_DATE = "zero time"
    SHORT_TIME = "time format"
    VALID_TIME = "valid time"

    ENUM_CELL = "FREE"
    ENUM_MASTER = "ACTIVE"
    ENUM_RECORD = "CREATED"

    ID_GREATER_ONE = "greater than or equal to 1"
    INT_TYPE = "valid integer"
    INVALID_PHONE_FORMAT = "Invalid phone"
    EMPTY_PHONE = "cannot be empty"

    EMAIL_MISS_DOG = "@-sign"
    EMAIL_MISS_PERIOD = "period immediately after"
    EMAIL_INVALID_PERIOD = "period"
    EMAIL_END_WITH_PERIOD = "end with a period"
    FIELD_MUST_BE_STRING = "must be a string"

    NOT_TWO_NONE = "both be None or not None"
    TOO_EARLY = "after 8"
    TOO_LATE = "before 20"
    TO_SHORT = "120 minutes"
    BOOL_TYPE = "valid boolean"
    LESS_THAN_EQUAL_5 = "less than or equal to 5"


class ErrorTypes:

    BOOL_TYPE = "bool_type"
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
    DATE_TYPE = "date_type"
    TIME_PARSING = "time_parsing"
    TIME_TYPE = "time_type"
    ENUM = "enum"
    INT_TYPE = "int_type"


class DataForId:

    correct_id = 1
    big_correct_id = 1123124
    wrong_id_zero = 0
    wrong_negative_id = -1
    big_wrong_negative_id = -1123124
    wrong_id_str = "string"
    wrong_id_none = None
    wrong_id_float = 1.5
    wrong_id_true = True
    wrong_id_false = False
