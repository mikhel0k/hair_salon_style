from datetime import date, timedelta, time


class Date:
    right_today = date.today()
    right_tomorrow = right_today + timedelta(days=1)
    right_on_week_bigger = right_today + timedelta(days=7)
    right_date_string = "2030-01-01"
    wrong_yesterday = right_today - timedelta(days=1)
    wrong_on_week_smaller = right_tomorrow - timedelta(days=7)
    wrong_type_string = "string"
    wrong_type_integer = 1
    wrong_type_float = 1.0
    wrong_type_boolean = True
    wrong_type_empty = ""
    wrong_type_none = None


class Time:
    right_morning = time(8, 0)
    right_afternoon = time(12, 15)
    right_evening = time(19, 30)
    right_string = "12:20:00"
    wrong_time_string = "qwe"
    wrong_time_integer = 1
    wrong_time_float = 1.0
    wrong_time_boolean = True
    wrong_time_empty = ""
    wrong_time_none = None


class Status:
    right_free = "free"
    right_occupied = "occupied"
    wrong_status = "wrong_status"
    wrong_status_none = None
    wrong_status_empty = ""
    wrong_status_boolean = True
    wrong_status_integer = 1
    wrong_status_float = 1.0
