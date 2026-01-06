from datetime import date
from typing import Any

import phonenumbers


def name_validator(value: Any):
    if not isinstance(value, str):
        raise ValueError("Field must be a string")
    value = value.strip()
    for i in value:
        if not i.isalpha() and i != " " and i != "-":
            raise ValueError(f"Invalid character: {i}")
    if len(value) < 3:
        raise ValueError(f"Field is too short. Minimum 3 characters. Got: '{value}'")
    if value.replace(" ", "").replace("-", "") == "":
        raise ValueError("Field must contain at least one letter")
    if "  " in value:
        raise ValueError("Field cannot contain consecutive spaces")
    if "--" in value:
        raise ValueError("Field cannot contain consecutive hyphens")
    if value.startswith("-"):
        raise ValueError("Field cannot start with a hyphen")
    if value.endswith("-"):
        raise ValueError("Field cannot end with a hyphen")
    if " -" in value or "- " in value:
        raise ValueError("Space and hyphen cannot be adjacent")
    return value.title()


def phone_validator(value: Any):
    if not value:
        raise ValueError("phone_number cannot be empty")

    try:
        parsed = phonenumbers.parse(str(value), "RU")
        if phonenumbers.is_valid_number(parsed):
            return phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.E164)
        raise ValueError('Invalid phone')
    except Exception as e:
        raise ValueError(f'Invalid phone format: {e}')


def date_validator(value: Any):
    if value is None:
        raise ValueError("Date cannot be null")
    if value < date.today():
        raise ValueError("Date cannot be in the past")
    return value