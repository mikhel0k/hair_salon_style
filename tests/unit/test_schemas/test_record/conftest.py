from dataclasses import dataclass
from enum import Enum


@dataclass
class AllowedRecordStatuses:
    Created = "created"
    Confirmed = "confirmed"
    Rejected = "rejected"
    Cancelled = "cancelled"
    wrong_status_string = "string"
    wrong_status_none = None
    wrong_status_empty = ""
    wrong_status_boolean = True
    wrong_status_integer = 1
    wrong_status_float = 1.0
