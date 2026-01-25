from datetime import date
from typing import Any

import phonenumbers


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
        raise ValueError("Field cannot start with a apostrophe")
    if value.startswith("_"):
        raise ValueError("Field cannot start with a underscore")
    if value.endswith("-"):
        raise ValueError("Field cannot end with a hyphen")
    if value.endswith("`"):
        raise ValueError("Field cannot end with a apostrophe")
    if value.endswith("_"):
        raise ValueError("Field cannot end with a underscore")
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