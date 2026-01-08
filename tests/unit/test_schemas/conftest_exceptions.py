MIN_STRING_LENGTH = 3
MAX_STRING_LENGTH = 60
MAX_PRICE = 10000
MIN_PRICE = 0
MAX_DURATION = 180
MIN_DURATION = 10


class ErrorMessages:
    STRING_TOO_LONG = "String should have at most 60 characters"
    STRING_TOO_SHORT = "String should have at least 3 characters"
    STRING_TYPE = "Input should be a valid string"
    STRING_EMPTY = "String should have at least 3 characters"
    STRING_SPACES = "String should have at least 3 characters"

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