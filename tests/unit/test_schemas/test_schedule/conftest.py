from dataclasses import dataclass
from datetime import time


@dataclass
class Time:
    correct_morning = time(8, 0)
    correct_afternoon = time(12, 15)
    correct_evening = time(19, 30)
    correct_string = "12:20:00"
    wrong_morning = time(7, 0)
    wrong_evening = time(21, 0)
    wrong_small_work_start = time(9, 0)
    wrong_small_work_end = time(10, 0)
    wrong_time_string = "qwe"
    wrong_time_true = True
    wrong_time_false = False
    wrong_time_empty = ""
    wrong_time_none = None
    correct_time_none = None


TIME_FIELDS = [
    "monday_start", "monday_end", "tuesday_start", "tuesday_end",
    "wednesday_start", "wednesday_end", "thursday_start", "thursday_end",
    "friday_start", "friday_end", "saturday_start", "saturday_end",
    "sunday_start", "sunday_end",
]


def default_times(time_data):
    return {
        "monday_start": time_data.correct_morning,
        "monday_end": time_data.correct_evening,
        "tuesday_start": time_data.correct_morning,
        "tuesday_end": time_data.correct_evening,
        "wednesday_start": time_data.correct_morning,
        "wednesday_end": time_data.correct_evening,
        "thursday_start": time_data.correct_morning,
        "thursday_end": time_data.correct_evening,
        "friday_start": time_data.correct_morning,
        "friday_end": time_data.correct_evening,
        "saturday_start": time_data.correct_morning,
        "saturday_end": time_data.correct_evening,
        "sunday_start": time_data.correct_morning,
        "sunday_end": time_data.correct_evening,
    }


def times_to_tuple(times):
    return tuple(times[f] for f in TIME_FIELDS)


def build_schedule_wrong_cases(time_data, data_for_id, ErrorTypes, ErrorMessages):
    cases = []
    correct_id = data_for_id.correct_id
    base = default_times(time_data)

    for field in TIME_FIELDS:
        times = base.copy()
        times[field] = time_data.wrong_time_none
        case = times_to_tuple(times) + (correct_id, (), ErrorTypes.VALUE_ERROR, ErrorMessages.NOT_TWO_NONE)
        cases.append(case)

    for field in [f for f in TIME_FIELDS if f.endswith("_start")]:
        times = base.copy()
        times[field] = time_data.wrong_morning
        case = times_to_tuple(times) + (correct_id, (), ErrorTypes.VALUE_ERROR, ErrorMessages.TOO_EARLY)
        cases.append(case)

    for field in [f for f in TIME_FIELDS if f.endswith("_end")]:
        times = base.copy()
        times[field] = time_data.wrong_evening
        case = times_to_tuple(times) + (correct_id, (), ErrorTypes.VALUE_ERROR, ErrorMessages.TOO_LATE)
        cases.append(case)

    for day in ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]:
        times = base.copy()
        times[f"{day}_start"] = time_data.wrong_small_work_start
        times[f"{day}_end"] = time_data.wrong_small_work_end
        case = times_to_tuple(times) + (correct_id, (), ErrorTypes.VALUE_ERROR, ErrorMessages.TO_SHORT)
        cases.append(case)

    invalid_time_cases = (
        [(f, time_data.wrong_time_string, ErrorTypes.TIME_PARSING, ErrorMessages.SHORT_TIME) for f in TIME_FIELDS]
        + [(f, time_data.wrong_time_true, ErrorTypes.TIME_TYPE, ErrorMessages.VALID_TIME) for f in TIME_FIELDS]
        + [(f, time_data.wrong_time_false, ErrorTypes.TIME_TYPE, ErrorMessages.VALID_TIME) for f in TIME_FIELDS]
        + [(f, time_data.wrong_time_empty, ErrorTypes.TIME_PARSING, ErrorMessages.SHORT_TIME) for f in TIME_FIELDS]
    )
    for field, wrong_val, err_type, err_msg in invalid_time_cases:
        times = base.copy()
        times[field] = wrong_val
        case = times_to_tuple(times) + (correct_id, (field,), err_type, err_msg)
        cases.append(case)

    for wrong_id in [
        data_for_id.wrong_id_zero,
        data_for_id.wrong_negative_id,
        data_for_id.big_wrong_negative_id,
    ]:
        case = times_to_tuple(base) + (wrong_id, ("master_id",), ErrorTypes.GREATER_THAN_EQUAL, ErrorMessages.ID_GREATER_ONE)
        cases.append(case)

    for wrong_id in [
        data_for_id.wrong_id_str,
        data_for_id.wrong_id_none,
        data_for_id.wrong_id_false,
        data_for_id.wrong_id_true,
        data_for_id.wrong_id_float,
    ]:
        case = times_to_tuple(base) + (wrong_id, ("master_id",), ErrorTypes.INT_TYPE, ErrorMessages.INT_TYPE)
        cases.append(case)

    return cases
