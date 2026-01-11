import pytest
from pydantic import ValidationError

from app.schemas.Schedule import ScheduleCreate
from conftest import Time
from tests.unit.test_schemas.conftest_exceptions import ErrorMessages, ErrorTypes, DataForId


class TestCreateSchedule:
    time_data = Time()
    data_for_id = DataForId

    @pytest.mark.parametrize(
            "monday_start, monday_end, tuesday_start, tuesday_end, wednesday_start, wednesday_end, thursday_start,\
            thursday_end, friday_start, friday_end, saturday_start, saturday_end, sunday_start, sunday_end, master_id",
        [
            (
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, data_for_id.right_id
            ),
            (
                time_data.right_afternoon, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, data_for_id.right_id
            ),
            (
                time_data.right_morning, time_data.right_evening, time_data.right_afternoon, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, data_for_id.right_id
            ),
            (
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_afternoon, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, data_for_id.right_id
            ),
            (
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, time_data.right_afternoon, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, data_for_id.right_id
            ),
            (
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_afternoon, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, data_for_id.right_id
            ),
            (
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, time_data.right_afternoon, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, data_for_id.right_id
            ),
            (
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_afternoon, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, data_for_id.right_id
            ),
            (
                time_data.right_morning, time_data.right_afternoon, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, data_for_id.right_id
            ),
            (
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_afternoon,
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, data_for_id.right_id
            ),
            (
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_afternoon, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, data_for_id.right_id
            ),
            (
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_afternoon,
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, data_for_id.right_id
            ),
            (
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_afternoon, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, data_for_id.right_id
            ),
            (
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_afternoon,
                time_data.right_morning, time_data.right_evening, data_for_id.right_id
            ),
            (
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_afternoon, data_for_id.right_id
            ),
            (
                time_data.right_afternoon, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, data_for_id.right_id
            ),
            (
                time_data.right_morning, time_data.right_evening, time_data.right_afternoon, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, data_for_id.right_id
            ),
            (
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_afternoon, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, data_for_id.right_id
            ),
            (
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, time_data.right_afternoon, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, data_for_id.right_id
            ),
            (
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_afternoon, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, data_for_id.right_id
            ),
            (
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, time_data.right_afternoon, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, data_for_id.right_id
            ),
            (
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_afternoon, time_data.right_evening, data_for_id.right_id
            ),
            (
                None, None, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, data_for_id.right_id
            ),
            (
                time_data.right_morning, time_data.right_evening, None, None,
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, data_for_id.right_id
            ),
            (
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                None, None, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, data_for_id.right_id
            ),
            (
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, None, None,
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, data_for_id.right_id
            ),
            (
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                None, None, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, data_for_id.right_id
            ),
            (
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, None, None,
                time_data.right_morning, time_data.right_evening, data_for_id.right_id
            ),
            (
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                None, None, data_for_id.right_id
            ),
            (
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, data_for_id.big_right_id
            ),
        ]
    )
    def test_create_schedule_right(
            self,
            monday_start,
            monday_end,
            tuesday_start,
            tuesday_end,
            wednesday_start,
            wednesday_end,
            thursday_start,
            thursday_end,
            friday_start,
            friday_end,
            saturday_start,
            saturday_end,
            sunday_start,
            sunday_end,
            master_id,
    ):
        schedule = ScheduleCreate(
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
            """monday_start, monday_end, tuesday_start, tuesday_end, wednesday_start, wednesday_end, thursday_start,
            thursday_end, friday_start, friday_end, saturday_start, saturday_end, sunday_start, sunday_end, master_id, 
            error_loc, error_type, error_msg,""",
        [
            (
                time_data.wrong_time_none, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, data_for_id.right_id,
                (), ErrorTypes.VALUE_ERROR, ErrorMessages.NOT_TWO_NONE
            ),
            (
                time_data.right_morning, time_data.wrong_time_none, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, data_for_id.right_id,
                (), ErrorTypes.VALUE_ERROR, ErrorMessages.NOT_TWO_NONE
            ),
            (
                time_data.right_morning, time_data.right_evening, time_data.wrong_time_none, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, data_for_id.right_id,
                (), ErrorTypes.VALUE_ERROR, ErrorMessages.NOT_TWO_NONE
            ),
            (
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.wrong_time_none,
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, data_for_id.right_id,
                (), ErrorTypes.VALUE_ERROR, ErrorMessages.NOT_TWO_NONE
            ),
            (
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.wrong_time_none, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, data_for_id.right_id,
                (), ErrorTypes.VALUE_ERROR, ErrorMessages.NOT_TWO_NONE
            ),
            (
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.wrong_time_none, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, data_for_id.right_id,
                (), ErrorTypes.VALUE_ERROR, ErrorMessages.NOT_TWO_NONE
            ),
            (
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, time_data.wrong_time_none, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, data_for_id.right_id,
                (), ErrorTypes.VALUE_ERROR, ErrorMessages.NOT_TWO_NONE
            ),
            (
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.wrong_time_none,
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, data_for_id.right_id,
                (), ErrorTypes.VALUE_ERROR, ErrorMessages.NOT_TWO_NONE
            ),
            (
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.wrong_time_none, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, data_for_id.right_id,
                (), ErrorTypes.VALUE_ERROR, ErrorMessages.NOT_TWO_NONE
            ),
            (
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.wrong_time_none, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, data_for_id.right_id,
                (), ErrorTypes.VALUE_ERROR, ErrorMessages.NOT_TWO_NONE
            ),
            (
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, time_data.wrong_time_none, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, data_for_id.right_id,
                (), ErrorTypes.VALUE_ERROR, ErrorMessages.NOT_TWO_NONE
            ),
            (
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.wrong_time_none,
                time_data.right_morning, time_data.right_evening, data_for_id.right_id,
                (), ErrorTypes.VALUE_ERROR, ErrorMessages.NOT_TWO_NONE
            ),
            (
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.wrong_time_none, time_data.right_evening, data_for_id.right_id,
                (), ErrorTypes.VALUE_ERROR, ErrorMessages.NOT_TWO_NONE
            ),
            (
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.wrong_time_none, data_for_id.right_id,
                (), ErrorTypes.VALUE_ERROR, ErrorMessages.NOT_TWO_NONE
            ),
            (
                time_data.wrong_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, data_for_id.right_id,
                (), ErrorTypes.VALUE_ERROR, ErrorMessages.TO_EARLY
            ),
            (
                time_data.right_morning, time_data.right_evening, time_data.wrong_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, data_for_id.right_id,
                (), ErrorTypes.VALUE_ERROR, ErrorMessages.TO_EARLY
            ),
            (
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.wrong_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, data_for_id.right_id,
                (), ErrorTypes.VALUE_ERROR, ErrorMessages.TO_EARLY
            ),
            (
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, time_data.wrong_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, data_for_id.right_id,
                (), ErrorTypes.VALUE_ERROR, ErrorMessages.TO_EARLY
            ),
            (
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.wrong_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, data_for_id.right_id,
                (), ErrorTypes.VALUE_ERROR, ErrorMessages.TO_EARLY
            ),
            (
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, time_data.wrong_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, data_for_id.right_id,
                (), ErrorTypes.VALUE_ERROR, ErrorMessages.TO_EARLY
            ),
            (
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.wrong_morning, time_data.right_evening, data_for_id.right_id,
                (), ErrorTypes.VALUE_ERROR, ErrorMessages.TO_EARLY
            ),
            (
                time_data.right_morning, time_data.wrong_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, data_for_id.right_id,
                (), ErrorTypes.VALUE_ERROR, ErrorMessages.TO_LATE
            ),
            (
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.wrong_evening,
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, data_for_id.right_id,
                (), ErrorTypes.VALUE_ERROR, ErrorMessages.TO_LATE
            ),
            (
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.wrong_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, data_for_id.right_id,
                (), ErrorTypes.VALUE_ERROR, ErrorMessages.TO_LATE
            ),
            (
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.wrong_evening,
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, data_for_id.right_id,
                (), ErrorTypes.VALUE_ERROR, ErrorMessages.TO_LATE
            ),
            (
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.wrong_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, data_for_id.right_id,
                (), ErrorTypes.VALUE_ERROR, ErrorMessages.TO_LATE
            ),
            (
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.wrong_evening,
                time_data.right_morning, time_data.right_evening, data_for_id.right_id,
                (), ErrorTypes.VALUE_ERROR, ErrorMessages.TO_LATE
            ),
            (
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.wrong_evening, data_for_id.right_id,
                (), ErrorTypes.VALUE_ERROR, ErrorMessages.TO_LATE
            ),
            (
                time_data.wrong_small_work_start, time_data.wrong_small_work_end, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, data_for_id.right_id,
                (), ErrorTypes.VALUE_ERROR, ErrorMessages.TO_SHORT
            ),
            (
                time_data.right_morning, time_data.right_evening, time_data.wrong_small_work_start, time_data.wrong_small_work_end,
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, data_for_id.right_id,
                (), ErrorTypes.VALUE_ERROR, ErrorMessages.TO_SHORT
            ),
            (
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.wrong_small_work_start, time_data.wrong_small_work_end, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, data_for_id.right_id,
                (), ErrorTypes.VALUE_ERROR, ErrorMessages.TO_SHORT
            ),
            (
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, time_data.wrong_small_work_start, time_data.wrong_small_work_end,
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, data_for_id.right_id,
                (), ErrorTypes.VALUE_ERROR, ErrorMessages.TO_SHORT
            ),
            (
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.wrong_small_work_start, time_data.wrong_small_work_end, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, data_for_id.right_id,
                (), ErrorTypes.VALUE_ERROR, ErrorMessages.TO_SHORT
            ),
            (
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, time_data.wrong_small_work_start, time_data.wrong_small_work_end,
                time_data.right_morning, time_data.right_evening, data_for_id.right_id,
                (), ErrorTypes.VALUE_ERROR, ErrorMessages.TO_SHORT
            ),
            (
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.wrong_small_work_start, time_data.wrong_small_work_end, data_for_id.right_id,
                (), ErrorTypes.VALUE_ERROR, ErrorMessages.TO_SHORT
            ),
            (
                time_data.wrong_time_string, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, data_for_id.right_id,
                ('monday_start',), ErrorTypes.TIME_PARSING, ErrorMessages.SHORT_TIME
            ),
            (
                time_data.wrong_time_true, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, data_for_id.right_id,
                ('monday_start',), ErrorTypes.TIME_TYPE, ErrorMessages.VALID_TIME
            ),
            (
                time_data.wrong_time_false, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, data_for_id.right_id,
                ('monday_start',), ErrorTypes.TIME_TYPE, ErrorMessages.VALID_TIME
            ),
            (
                time_data.wrong_time_empty, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, data_for_id.right_id,
                ('monday_start',), ErrorTypes.TIME_PARSING, ErrorMessages.SHORT_TIME
            ),
            (
                time_data.right_morning, time_data.wrong_time_string, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, data_for_id.right_id,
                ('monday_end',), ErrorTypes.TIME_PARSING, ErrorMessages.SHORT_TIME
            ),
            (
                time_data.right_morning, time_data.wrong_time_true, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, data_for_id.right_id,
                ('monday_end',), ErrorTypes.TIME_TYPE, ErrorMessages.VALID_TIME
            ),
            (
                time_data.right_morning, time_data.wrong_time_false, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, data_for_id.right_id,
                ('monday_end',), ErrorTypes.TIME_TYPE, ErrorMessages.VALID_TIME
            ),
            (
                time_data.right_morning, time_data.wrong_time_empty, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, data_for_id.right_id,
                ('monday_end',), ErrorTypes.TIME_PARSING, ErrorMessages.SHORT_TIME
            ),
            (
                time_data.right_morning, time_data.right_evening, time_data.wrong_time_string, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, data_for_id.right_id,
                ('tuesday_start',), ErrorTypes.TIME_PARSING, ErrorMessages.SHORT_TIME
            ),
            (
                time_data.right_morning, time_data.right_evening, time_data.wrong_time_true, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, data_for_id.right_id,
                ('tuesday_start',), ErrorTypes.TIME_TYPE, ErrorMessages.VALID_TIME
            ),
            (
                time_data.right_morning, time_data.right_evening, time_data.wrong_time_false, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, data_for_id.right_id,
                ('tuesday_start',), ErrorTypes.TIME_TYPE, ErrorMessages.VALID_TIME
            ),
            (
                time_data.right_morning, time_data.right_evening, time_data.wrong_time_empty, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, data_for_id.right_id,
                ('tuesday_start',), ErrorTypes.TIME_PARSING, ErrorMessages.SHORT_TIME
            ),
            (
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.wrong_time_string,
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, data_for_id.right_id,
                ('tuesday_end',), ErrorTypes.TIME_PARSING, ErrorMessages.SHORT_TIME
            ),
            (
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.wrong_time_true,
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, data_for_id.right_id,
                ('tuesday_end',), ErrorTypes.TIME_TYPE, ErrorMessages.VALID_TIME
            ),
            (
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.wrong_time_false,
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, data_for_id.right_id,
                ('tuesday_end',), ErrorTypes.TIME_TYPE, ErrorMessages.VALID_TIME
            ),
            (
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.wrong_time_empty,
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, data_for_id.right_id,
                ('tuesday_end',), ErrorTypes.TIME_PARSING, ErrorMessages.SHORT_TIME
            ),
            (
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.wrong_time_string, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, data_for_id.right_id,
                ('wednesday_start',), ErrorTypes.TIME_PARSING, ErrorMessages.SHORT_TIME
            ),
            (
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.wrong_time_true, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, data_for_id.right_id,
                ('wednesday_start',), ErrorTypes.TIME_TYPE, ErrorMessages.VALID_TIME
            ),
            (
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.wrong_time_false, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, data_for_id.right_id,
                ('wednesday_start',), ErrorTypes.TIME_TYPE, ErrorMessages.VALID_TIME
            ),
            (
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.wrong_time_empty, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, data_for_id.right_id,
                ('wednesday_start',), ErrorTypes.TIME_PARSING, ErrorMessages.SHORT_TIME
            ),
            (
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.wrong_time_string, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, data_for_id.right_id,
                ('wednesday_end',), ErrorTypes.TIME_PARSING, ErrorMessages.SHORT_TIME
            ),
            (
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.wrong_time_true, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, data_for_id.right_id,
                ('wednesday_end',), ErrorTypes.TIME_TYPE, ErrorMessages.VALID_TIME
            ),
            (
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.wrong_time_false, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, data_for_id.right_id,
                ('wednesday_end',), ErrorTypes.TIME_TYPE, ErrorMessages.VALID_TIME
            ),
            (
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.wrong_time_empty, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, data_for_id.right_id,
                ('wednesday_end',), ErrorTypes.TIME_PARSING, ErrorMessages.SHORT_TIME
            ),
            (
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, time_data.wrong_time_string, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, data_for_id.right_id,
                ('thursday_start',), ErrorTypes.TIME_PARSING, ErrorMessages.SHORT_TIME
            ),
            (
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, time_data.wrong_time_true, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, data_for_id.right_id,
                ('thursday_start',), ErrorTypes.TIME_TYPE, ErrorMessages.VALID_TIME
            ),
            (
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, time_data.wrong_time_false, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, data_for_id.right_id,
                ('thursday_start',), ErrorTypes.TIME_TYPE, ErrorMessages.VALID_TIME
            ),
            (
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, time_data.wrong_time_empty, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, data_for_id.right_id,
                ('thursday_start',), ErrorTypes.TIME_PARSING, ErrorMessages.SHORT_TIME
            ),
            (
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.wrong_time_string,
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, data_for_id.right_id,
                ('thursday_end',), ErrorTypes.TIME_PARSING, ErrorMessages.SHORT_TIME
            ),
            (
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.wrong_time_true,
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, data_for_id.right_id,
                ('thursday_end',), ErrorTypes.TIME_TYPE, ErrorMessages.VALID_TIME
            ),
            (
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.wrong_time_false,
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, data_for_id.right_id,
                ('thursday_end',), ErrorTypes.TIME_TYPE, ErrorMessages.VALID_TIME
            ),
            (
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.wrong_time_empty,
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, data_for_id.right_id,
                ('thursday_end',), ErrorTypes.TIME_PARSING, ErrorMessages.SHORT_TIME
            ),
            (
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.wrong_time_string, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, data_for_id.right_id,
                ('friday_start',), ErrorTypes.TIME_PARSING, ErrorMessages.SHORT_TIME
            ),
            (
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.wrong_time_true, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, data_for_id.right_id,
                ('friday_start',), ErrorTypes.TIME_TYPE, ErrorMessages.VALID_TIME
            ),
            (
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.wrong_time_false, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, data_for_id.right_id,
                ('friday_start',), ErrorTypes.TIME_TYPE, ErrorMessages.VALID_TIME
            ),
            (
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.wrong_time_empty, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, data_for_id.right_id,
                ('friday_start',), ErrorTypes.TIME_PARSING, ErrorMessages.SHORT_TIME
            ),
            (
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.wrong_time_string, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, data_for_id.right_id,
                ('friday_end',), ErrorTypes.TIME_PARSING, ErrorMessages.SHORT_TIME
            ),
            (
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.wrong_time_true, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, data_for_id.right_id,
                ('friday_end',), ErrorTypes.TIME_TYPE, ErrorMessages.VALID_TIME
            ),
            (
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.wrong_time_false, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, data_for_id.right_id,
                ('friday_end',), ErrorTypes.TIME_TYPE, ErrorMessages.VALID_TIME
            ),
            (
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.wrong_time_empty, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, data_for_id.right_id,
                ('friday_end',), ErrorTypes.TIME_PARSING, ErrorMessages.SHORT_TIME
            ),
            (
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, time_data.wrong_time_string, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, data_for_id.right_id,
                ('saturday_start',), ErrorTypes.TIME_PARSING, ErrorMessages.SHORT_TIME
            ),
            (
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, time_data.wrong_time_true, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, data_for_id.right_id,
                ('saturday_start',), ErrorTypes.TIME_TYPE, ErrorMessages.VALID_TIME
            ),
            (
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, time_data.wrong_time_false, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, data_for_id.right_id,
                ('saturday_start',), ErrorTypes.TIME_TYPE, ErrorMessages.VALID_TIME
            ),
            (
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, time_data.wrong_time_empty, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, data_for_id.right_id,
                ('saturday_start',), ErrorTypes.TIME_PARSING, ErrorMessages.SHORT_TIME
            ),
            (
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.wrong_time_string,
                time_data.right_morning, time_data.right_evening, data_for_id.right_id,
                ('saturday_end',), ErrorTypes.TIME_PARSING, ErrorMessages.SHORT_TIME
            ),
            (
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.wrong_time_true,
                time_data.right_morning, time_data.right_evening, data_for_id.right_id,
                ('saturday_end',), ErrorTypes.TIME_TYPE, ErrorMessages.VALID_TIME
            ),
            (
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.wrong_time_false,
                time_data.right_morning, time_data.right_evening, data_for_id.right_id,
                ('saturday_end',), ErrorTypes.TIME_TYPE, ErrorMessages.VALID_TIME
            ),
            (
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.wrong_time_empty,
                time_data.right_morning, time_data.right_evening, data_for_id.right_id,
                ('saturday_end',), ErrorTypes.TIME_PARSING, ErrorMessages.SHORT_TIME
            ),
            (
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.wrong_time_string, time_data.right_evening, data_for_id.right_id,
                ('sunday_start',), ErrorTypes.TIME_PARSING, ErrorMessages.SHORT_TIME
            ),
            (
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.wrong_time_true, time_data.right_evening, data_for_id.right_id,
                ('sunday_start',), ErrorTypes.TIME_TYPE, ErrorMessages.VALID_TIME
            ),
            (
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.wrong_time_false, time_data.right_evening, data_for_id.right_id,
                ('sunday_start',), ErrorTypes.TIME_TYPE, ErrorMessages.VALID_TIME
            ),
            (
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.wrong_time_empty, time_data.right_evening, data_for_id.right_id,
                ('sunday_start',), ErrorTypes.TIME_PARSING, ErrorMessages.SHORT_TIME
            ),
            (
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.wrong_time_string, data_for_id.right_id,
                ('sunday_end',), ErrorTypes.TIME_PARSING, ErrorMessages.SHORT_TIME
            ),
            (
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.wrong_time_true, data_for_id.right_id,
                ('sunday_end',), ErrorTypes.TIME_TYPE, ErrorMessages.VALID_TIME
            ),
            (
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.wrong_time_false, data_for_id.right_id,
                ('sunday_end',), ErrorTypes.TIME_TYPE, ErrorMessages.VALID_TIME
            ),
            (
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.wrong_time_empty, data_for_id.right_id,
                ('sunday_end',), ErrorTypes.TIME_PARSING, ErrorMessages.SHORT_TIME
            ),
            (
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, data_for_id.wrong_id_zero,
                ('master_id',), ErrorTypes.GREATER_THAN_EQUAL, ErrorMessages.ID_GREATER_ONE
            ),
            (
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, data_for_id.wrong_negative_id,
                ('master_id',), ErrorTypes.GREATER_THAN_EQUAL, ErrorMessages.ID_GREATER_ONE
            ),
            (
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, data_for_id.big_wrong_negative_id,
                ('master_id',), ErrorTypes.GREATER_THAN_EQUAL, ErrorMessages.ID_GREATER_ONE
            ),
            (
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, data_for_id.wrong_id_str,
                ('master_id',), ErrorTypes.INT_TYPE, ErrorMessages.INT_TYPE
            ),
            (
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, data_for_id.wrong_id_none,
                ('master_id',), ErrorTypes.INT_TYPE, ErrorMessages.INT_TYPE
            ),
            (
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, data_for_id.wrong_id_false,
                ('master_id',), ErrorTypes.INT_TYPE, ErrorMessages.INT_TYPE
            ),
            (
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, data_for_id.wrong_id_true,
                ('master_id',), ErrorTypes.INT_TYPE, ErrorMessages.INT_TYPE
            ),
            (
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, data_for_id.wrong_id_float,
                ('master_id',), ErrorTypes.INT_TYPE, ErrorMessages.INT_TYPE
            ),
        ]
    )
    def test_create_schedule_wrong(
            self,
            monday_start,
            monday_end,
            tuesday_start,
            tuesday_end,
            wednesday_start,
            wednesday_end,
            thursday_start,
            thursday_end,
            friday_start,
            friday_end,
            saturday_start,
            saturday_end,
            sunday_start,
            sunday_end,
            master_id,
            error_loc,
            error_type,
            error_msg,
    ):
        with pytest.raises(ValidationError) as error:
            schedule = ScheduleCreate(
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
        errors = error.value.errors()
        assert len(errors) == 1
        error = errors[0]
        assert error["loc"] == error_loc
        assert error["type"] == error_type
        assert error_msg in error["msg"]
