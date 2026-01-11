from dataclasses import dataclass
from datetime import time


@dataclass
class Time:
    right_morning = time(8, 0)
    right_afternoon = time(12, 15)
    right_evening = time(19, 30)
    right_string = "12:20:00"
    wrong_morning = time(7, 0)
    wrong_evening = time(21, 0)
    wrong_small_work_start = time(9, 0)
    wrong_small_work_end = time(10, 0)
    wrong_time_string = "qwe"
    wrong_time_true = True
    wrong_time_false = False
    wrong_time_empty = ""
    wrong_time_none = None
    right_time_none = None