from dataclasses import dataclass
from datetime import date, timedelta, time

@dataclass
class Date:
    correct_today = date.today()
    correct_tomorrow = correct_today + timedelta(days=1)
    correct_on_week_bigger = correct_today + timedelta(days=7)
    correct_date_string = "2030-01-01"
    wrong_yesterday = correct_today - timedelta(days=1)
    wrong_on_week_smaller = correct_tomorrow - timedelta(days=7)
    wrong_type_string = "string"
    wrong_type_integer = 1
    wrong_type_float = 1.0
    wrong_type_boolean = True
    wrong_type_empty = ""
    wrong_type_none = None

@dataclass
class Time:
    correct_morning = time(8, 0)
    correct_afternoon = time(12, 15)
    correct_evening = time(19, 30)
    correct_string = "12:20:00"
    wrong_time_string = "qwe"
    wrong_time_integer = 1
    wrong_time_float = 1.0
    wrong_time_boolean = True
    wrong_time_empty = ""
    wrong_time_none = None

@dataclass
class Status:
    correct_free = "FREE"
    correct_occupied = "OCCUPIED"
    wrong_status = "wrong_status"
    wrong_status_none = None
    wrong_status_empty = ""
    wrong_status_boolean = True
    wrong_status_integer = 1
    wrong_status_float = 1.0
