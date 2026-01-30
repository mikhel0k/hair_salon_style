import pytest
from pydantic import ValidationError

from app.schemas.Schedule import ScheduleCreate
from tests.unit.test_schemas.test_schedule.conftest import (
    Time,
    default_times,
    times_to_tuple,
    build_schedule_wrong_cases,
)
from tests.unit.test_schemas.conftest import assert_single_validation_error
from tests.unit.test_schemas.conftest_exceptions import ErrorMessages, ErrorTypes, DataForId

WRONG_CASES = build_schedule_wrong_cases(Time(), DataForId(), ErrorTypes, ErrorMessages)


def _build_correct_cases():
    td = Time()
    did = DataForId()
    cases = []
    base = default_times(td)
    cases.append(times_to_tuple(base) + (did.correct_id,))
    for day in ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]:
        times = base.copy()
        times[f"{day}_start"] = td.correct_afternoon
        times[f"{day}_end"] = td.correct_evening
        cases.append(times_to_tuple(times) + (did.correct_id,))
    for day in ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]:
        times = base.copy()
        times[f"{day}_start"] = td.correct_morning
        times[f"{day}_end"] = td.correct_afternoon
        cases.append(times_to_tuple(times) + (did.correct_id,))
    for day in ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]:
        times = base.copy()
        times[f"{day}_start"] = None
        times[f"{day}_end"] = None
        cases.append(times_to_tuple(times) + (did.correct_id,))
    cases.append(times_to_tuple(base) + (did.big_correct_id,))
    return cases


CORRECT_CASES = _build_correct_cases()


time_data = Time()
data_for_id = DataForId()


class TestCreateSchedule:

    @pytest.mark.parametrize(
        "monday_start, monday_end, tuesday_start, tuesday_end, wednesday_start, wednesday_end, "
        "thursday_start, thursday_end, friday_start, friday_end, saturday_start, saturday_end, "
        "sunday_start, sunday_end, master_id",
        CORRECT_CASES,
    )
    def test_create_schedule_correct(
        self,
        monday_start, monday_end, tuesday_start, tuesday_end, wednesday_start, wednesday_end,
        thursday_start, thursday_end, friday_start, friday_end, saturday_start, saturday_end,
        sunday_start, sunday_end, master_id,
    ):
        schedule = ScheduleCreate(
            id=master_id,
            master_id=master_id,
            monday_start=monday_start,
            monday_end=monday_end,
            tuesday_start=tuesday_start,
            tuesday_end=tuesday_end,
            wednesday_start=wednesday_start,
            wednesday_end=wednesday_end,
            thursday_start=thursday_start,
            thursday_end=thursday_end,
            friday_start=friday_start,
            friday_end=friday_end,
            saturday_start=saturday_start,
            saturday_end=saturday_end,
            sunday_start=sunday_start,
            sunday_end=sunday_end,
        )
        assert isinstance(schedule, ScheduleCreate)
        assert schedule.master_id == master_id
        assert schedule.monday_start == monday_start
        assert schedule.monday_end == monday_end
        assert schedule.tuesday_start == tuesday_start
        assert schedule.tuesday_end == tuesday_end
        assert schedule.wednesday_start == wednesday_start
        assert schedule.wednesday_end == wednesday_end
        assert schedule.thursday_start == thursday_start
        assert schedule.thursday_end == thursday_end
        assert schedule.friday_start == friday_start
        assert schedule.friday_end == friday_end
        assert schedule.saturday_start == saturday_start
        assert schedule.saturday_end == saturday_end
        assert schedule.sunday_start == sunday_start
        assert schedule.sunday_end == sunday_end

    @pytest.mark.parametrize(
        "monday_start, monday_end, tuesday_start, tuesday_end, wednesday_start, wednesday_end, "
        "thursday_start, thursday_end, friday_start, friday_end, saturday_start, saturday_end, "
        "sunday_start, sunday_end, master_id, error_loc, error_type, error_msg",
        WRONG_CASES,
    )
    def test_create_schedule_wrong(
        self,
        monday_start, monday_end, tuesday_start, tuesday_end, wednesday_start, wednesday_end,
        thursday_start, thursday_end, friday_start, friday_end, saturday_start, saturday_end,
        sunday_start, sunday_end, master_id, error_loc, error_type, error_msg,
    ):
        with pytest.raises(ValidationError) as exc_info:
            ScheduleCreate(
                id=1,
                master_id=master_id,
                monday_start=monday_start,
                monday_end=monday_end,
                tuesday_start=tuesday_start,
                tuesday_end=tuesday_end,
                wednesday_start=wednesday_start,
                wednesday_end=wednesday_end,
                thursday_start=thursday_start,
                thursday_end=thursday_end,
                friday_start=friday_start,
                friday_end=friday_end,
                saturday_start=saturday_start,
                saturday_end=saturday_end,
                sunday_start=sunday_start,
                sunday_end=sunday_end,
            )
        assert_single_validation_error(exc_info.value.errors(), error_loc, error_type, error_msg)
