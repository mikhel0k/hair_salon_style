from datetime import date, datetime
from typing import Any

import phonenumbers

REPORT_DATE_FORMATS = ("%Y-%m-%d", "%Y.%m.%d", "%d-%m-%Y", "%d.%m.%Y")


def name_validator(value: Any):
    if not isinstance(value, str):
        raise ValueError("Field must be a string")
    value = value.strip()
    for i in value:
        if not i.isalpha() and i != " " and i != "-" and i != "_" and i != "`":
            raise ValueError(f"Invalid character")
    if "  " in value:
        raise ValueError("Field cannot contain consecutive spaces")
    if "--" in value:
        raise ValueError("Field cannot contain consecutive hyphens")
    if "``" in value:
        raise ValueError("Field cannot contain consecutive apostrophes")
    if "__" in value:
        raise ValueError("Field cannot contain consecutive underscores")
    if value.startswith("-"):
        raise ValueError("Field cannot start with a hyphen")
    if value.startswith("`"):
        raise ValueError("Field cannot start with an apostrophe")
    if value.startswith("_"):
        raise ValueError("Field cannot start with an underscore")
    if value.endswith("-"):
        raise ValueError("Field cannot end with a hyphen")
    if value.endswith("`"):
        raise ValueError("Field cannot end with an apostrophe")
    if value.endswith("_"):
        raise ValueError("Field cannot end with an underscore")
    if " -" in value or "- " in value:
        raise ValueError("Space and hyphen cannot be adjacent")
    if " `" in value or "` " in value:
        raise ValueError("Space and apostrophe cannot be adjacent")
    if " _" in value or "_ " in value:
        raise ValueError("Space and underscore cannot be adjacent")

    return value.title()


def phone_validator(value: Any):
    if not value:
        raise ValueError("phone_number cannot be empty")

    try:
        parsed = phonenumbers.parse(str(value), "RU")
        if phonenumbers.is_valid_number(parsed):
            return phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.E164)
        raise ValueError('Invalid phone')
    except Exception:
        raise ValueError(f'Invalid phone format')


def date_validator(value: Any):
    if value is None:
        raise ValueError("Date cannot be null")
    if value < date.today():
        raise ValueError("Date cannot be in the past")
    return value


def parse_report_date(value: Any) -> date:
    """
    Парсит строку даты для отчёта. Поддерживает:
    YYYY-MM-DD (ISO), YYYY.MM.DD, DD-MM-YYYY, DD.MM.YYYY.
    """
    if isinstance(value, date):
        return value
    if not isinstance(value, str):
        raise ValueError("Date must be a string or date")
    value = value.strip()
    last_error = None
    for fmt in REPORT_DATE_FORMATS:
        try:
            return datetime.strptime(value, fmt).date()
        except ValueError as e:
            last_error = e
            continue
    if last_error and "day" in str(last_error).lower():
        raise ValueError(
            "Invalid date (e.g. day is out of range for month, like 31 February)"
        ) from last_error
    raise ValueError(
        "Invalid date format. Use YYYY-MM-DD, YYYY.MM.DD, DD-MM-YYYY or DD.MM.YYYY"
    ) from last_error