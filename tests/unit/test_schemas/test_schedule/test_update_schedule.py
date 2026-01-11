import pytest
from pydantic import ValidationError

from app.schemas.Schedule import ScheduleUpdate
from conftest import Time
from tests.unit.test_schemas.conftest_exceptions import ErrorMessages, ErrorTypes, DataForId


class TestUpdateSchedule:
    time_data = Time()
    data_for_id = DataForId

    @pytest.mark.parametrize(
            "monday_start, monday_end, tuesday_start, tuesday_end, wednesday_start, wednesday_end, thursday_start,\
            thursday_end, friday_start, friday_end, saturday_start, saturday_end, sunday_start, sunday_end",
        [
            (
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening 
            ),
            (
                time_data.right_afternoon, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening 
            ),
            (
                time_data.right_morning, time_data.right_evening, time_data.right_afternoon, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening 
            ),
            (
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_afternoon, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening 
            ),
            (
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, time_data.right_afternoon, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening 
            ),
            (
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_afternoon, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening 
            ),
            (
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, time_data.right_afternoon, time_data.right_evening,
                time_data.right_morning, time_data.right_evening 
            ),
            (
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_afternoon, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening 
            ),
            (
                time_data.right_morning, time_data.right_afternoon, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening 
            ),
            (
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_afternoon,
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening 
            ),
            (
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_afternoon, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening 
            ),
            (
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_afternoon,
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening 
            ),
            (
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_afternoon, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening 
            ),
            (
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_afternoon,
                time_data.right_morning, time_data.right_evening 
            ),
            (
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_afternoon 
            ),
            (
                time_data.right_afternoon, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening 
            ),
            (
                time_data.right_morning, time_data.right_evening, time_data.right_afternoon, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening 
            ),
            (
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_afternoon, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening 
            ),
            (
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, time_data.right_afternoon, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening 
            ),
            (
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_afternoon, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening 
            ),
            (
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, time_data.right_afternoon, time_data.right_evening,
                time_data.right_morning, time_data.right_evening 
            ),
            (
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_afternoon, time_data.right_evening 
            ),
            (
                None, None, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening 
            ),
            (
                time_data.right_morning, time_data.right_evening, None, None,
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening 
            ),
            (
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                None, None, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening 
            ),
            (
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, None, None,
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening 
            ),
            (
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                None, None, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening 
            ),
            (
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, None, None,
                time_data.right_morning, time_data.right_evening 
            ),
            (
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                None, None 
            ),
        ]
    )
    def test_update_schedule_right(
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
    ):
        schedule = ScheduleUpdate(
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
        assert isinstance(schedule, ScheduleUpdate)
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
            thursday_end, friday_start, friday_end, saturday_start, saturday_end, sunday_start, sunday_end, 
            error_loc, error_type, error_msg,""",
        [
            (
                time_data.wrong_time_none, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening ,
                (), ErrorTypes.VALUE_ERROR, ErrorMessages.NOT_TWO_NONE
            ),
            (
                time_data.right_morning, time_data.wrong_time_none, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening ,
                (), ErrorTypes.VALUE_ERROR, ErrorMessages.NOT_TWO_NONE
            ),
            (
                time_data.right_morning, time_data.right_evening, time_data.wrong_time_none, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening ,
                (), ErrorTypes.VALUE_ERROR, ErrorMessages.NOT_TWO_NONE
            ),
            (
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.wrong_time_none,
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening ,
                (), ErrorTypes.VALUE_ERROR, ErrorMessages.NOT_TWO_NONE
            ),
            (
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.wrong_time_none, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening ,
                (), ErrorTypes.VALUE_ERROR, ErrorMessages.NOT_TWO_NONE
            ),
            (
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.wrong_time_none, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening ,
                (), ErrorTypes.VALUE_ERROR, ErrorMessages.NOT_TWO_NONE
            ),
            (
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, time_data.wrong_time_none, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening ,
                (), ErrorTypes.VALUE_ERROR, ErrorMessages.NOT_TWO_NONE
            ),
            (
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.wrong_time_none,
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening ,
                (), ErrorTypes.VALUE_ERROR, ErrorMessages.NOT_TWO_NONE
            ),
            (
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.wrong_time_none, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening ,
                (), ErrorTypes.VALUE_ERROR, ErrorMessages.NOT_TWO_NONE
            ),
            (
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.wrong_time_none, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening ,
                (), ErrorTypes.VALUE_ERROR, ErrorMessages.NOT_TWO_NONE
            ),
            (
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, time_data.wrong_time_none, time_data.right_evening,
                time_data.right_morning, time_data.right_evening ,
                (), ErrorTypes.VALUE_ERROR, ErrorMessages.NOT_TWO_NONE
            ),
            (
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.wrong_time_none,
                time_data.right_morning, time_data.right_evening ,
                (), ErrorTypes.VALUE_ERROR, ErrorMessages.NOT_TWO_NONE
            ),
            (
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.wrong_time_none, time_data.right_evening ,
                (), ErrorTypes.VALUE_ERROR, ErrorMessages.NOT_TWO_NONE
            ),
            (
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.wrong_time_none ,
                (), ErrorTypes.VALUE_ERROR, ErrorMessages.NOT_TWO_NONE
            ),
            (
                time_data.wrong_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening ,
                (), ErrorTypes.VALUE_ERROR, ErrorMessages.TO_EARLY
            ),
            (
                time_data.right_morning, time_data.right_evening, time_data.wrong_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening ,
                (), ErrorTypes.VALUE_ERROR, ErrorMessages.TO_EARLY
            ),
            (
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.wrong_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening ,
                (), ErrorTypes.VALUE_ERROR, ErrorMessages.TO_EARLY
            ),
            (
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, time_data.wrong_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening ,
                (), ErrorTypes.VALUE_ERROR, ErrorMessages.TO_EARLY
            ),
            (
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.wrong_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening ,
                (), ErrorTypes.VALUE_ERROR, ErrorMessages.TO_EARLY
            ),
            (
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, time_data.wrong_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening ,
                (), ErrorTypes.VALUE_ERROR, ErrorMessages.TO_EARLY
            ),
            (
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.wrong_morning, time_data.right_evening ,
                (), ErrorTypes.VALUE_ERROR, ErrorMessages.TO_EARLY
            ),
            (
                time_data.right_morning, time_data.wrong_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening ,
                (), ErrorTypes.VALUE_ERROR, ErrorMessages.TO_LATE
            ),
            (
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.wrong_evening,
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening ,
                (), ErrorTypes.VALUE_ERROR, ErrorMessages.TO_LATE
            ),
            (
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.wrong_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening ,
                (), ErrorTypes.VALUE_ERROR, ErrorMessages.TO_LATE
            ),
            (
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.wrong_evening,
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening ,
                (), ErrorTypes.VALUE_ERROR, ErrorMessages.TO_LATE
            ),
            (
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.wrong_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening ,
                (), ErrorTypes.VALUE_ERROR, ErrorMessages.TO_LATE
            ),
            (
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.wrong_evening,
                time_data.right_morning, time_data.right_evening ,
                (), ErrorTypes.VALUE_ERROR, ErrorMessages.TO_LATE
            ),
            (
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.wrong_evening ,
                (), ErrorTypes.VALUE_ERROR, ErrorMessages.TO_LATE
            ),
            (
                time_data.wrong_small_work_start, time_data.wrong_small_work_end, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening ,
                (), ErrorTypes.VALUE_ERROR, ErrorMessages.TO_SHORT
            ),
            (
                time_data.right_morning, time_data.right_evening, time_data.wrong_small_work_start, time_data.wrong_small_work_end,
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening ,
                (), ErrorTypes.VALUE_ERROR, ErrorMessages.TO_SHORT
            ),
            (
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.wrong_small_work_start, time_data.wrong_small_work_end, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening ,
                (), ErrorTypes.VALUE_ERROR, ErrorMessages.TO_SHORT
            ),
            (
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, time_data.wrong_small_work_start, time_data.wrong_small_work_end,
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening ,
                (), ErrorTypes.VALUE_ERROR, ErrorMessages.TO_SHORT
            ),
            (
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.wrong_small_work_start, time_data.wrong_small_work_end, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening ,
                (), ErrorTypes.VALUE_ERROR, ErrorMessages.TO_SHORT
            ),
            (
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, time_data.wrong_small_work_start, time_data.wrong_small_work_end,
                time_data.right_morning, time_data.right_evening ,
                (), ErrorTypes.VALUE_ERROR, ErrorMessages.TO_SHORT
            ),
            (
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.wrong_small_work_start, time_data.wrong_small_work_end ,
                (), ErrorTypes.VALUE_ERROR, ErrorMessages.TO_SHORT
            ),
            (
                time_data.wrong_time_string, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening ,
                ('monday_start',), ErrorTypes.TIME_PARSING, ErrorMessages.SHORT_TIME
            ),
            (
                time_data.wrong_time_true, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening ,
                ('monday_start',), ErrorTypes.TIME_TYPE, ErrorMessages.VALID_TIME
            ),
            (
                time_data.wrong_time_false, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening ,
                ('monday_start',), ErrorTypes.TIME_TYPE, ErrorMessages.VALID_TIME
            ),
            (
                time_data.wrong_time_empty, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening ,
                ('monday_start',), ErrorTypes.TIME_PARSING, ErrorMessages.SHORT_TIME
            ),
            (
                time_data.right_morning, time_data.wrong_time_string, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening ,
                ('monday_end',), ErrorTypes.TIME_PARSING, ErrorMessages.SHORT_TIME
            ),
            (
                time_data.right_morning, time_data.wrong_time_true, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening ,
                ('monday_end',), ErrorTypes.TIME_TYPE, ErrorMessages.VALID_TIME
            ),
            (
                time_data.right_morning, time_data.wrong_time_false, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening ,
                ('monday_end',), ErrorTypes.TIME_TYPE, ErrorMessages.VALID_TIME
            ),
            (
                time_data.right_morning, time_data.wrong_time_empty, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening ,
                ('monday_end',), ErrorTypes.TIME_PARSING, ErrorMessages.SHORT_TIME
            ),
            (
                time_data.right_morning, time_data.right_evening, time_data.wrong_time_string, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening ,
                ('tuesday_start',), ErrorTypes.TIME_PARSING, ErrorMessages.SHORT_TIME
            ),
            (
                time_data.right_morning, time_data.right_evening, time_data.wrong_time_true, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening ,
                ('tuesday_start',), ErrorTypes.TIME_TYPE, ErrorMessages.VALID_TIME
            ),
            (
                time_data.right_morning, time_data.right_evening, time_data.wrong_time_false, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening ,
                ('tuesday_start',), ErrorTypes.TIME_TYPE, ErrorMessages.VALID_TIME
            ),
            (
                time_data.right_morning, time_data.right_evening, time_data.wrong_time_empty, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening ,
                ('tuesday_start',), ErrorTypes.TIME_PARSING, ErrorMessages.SHORT_TIME
            ),
            (
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.wrong_time_string,
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening ,
                ('tuesday_end',), ErrorTypes.TIME_PARSING, ErrorMessages.SHORT_TIME
            ),
            (
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.wrong_time_true,
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening ,
                ('tuesday_end',), ErrorTypes.TIME_TYPE, ErrorMessages.VALID_TIME
            ),
            (
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.wrong_time_false,
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening ,
                ('tuesday_end',), ErrorTypes.TIME_TYPE, ErrorMessages.VALID_TIME
            ),
            (
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.wrong_time_empty,
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening ,
                ('tuesday_end',), ErrorTypes.TIME_PARSING, ErrorMessages.SHORT_TIME
            ),
            (
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.wrong_time_string, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening ,
                ('wednesday_start',), ErrorTypes.TIME_PARSING, ErrorMessages.SHORT_TIME
            ),
            (
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.wrong_time_true, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening ,
                ('wednesday_start',), ErrorTypes.TIME_TYPE, ErrorMessages.VALID_TIME
            ),
            (
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.wrong_time_false, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening ,
                ('wednesday_start',), ErrorTypes.TIME_TYPE, ErrorMessages.VALID_TIME
            ),
            (
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.wrong_time_empty, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening ,
                ('wednesday_start',), ErrorTypes.TIME_PARSING, ErrorMessages.SHORT_TIME
            ),
            (
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.wrong_time_string, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening ,
                ('wednesday_end',), ErrorTypes.TIME_PARSING, ErrorMessages.SHORT_TIME
            ),
            (
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.wrong_time_true, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening ,
                ('wednesday_end',), ErrorTypes.TIME_TYPE, ErrorMessages.VALID_TIME
            ),
            (
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.wrong_time_false, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening ,
                ('wednesday_end',), ErrorTypes.TIME_TYPE, ErrorMessages.VALID_TIME
            ),
            (
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.wrong_time_empty, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening ,
                ('wednesday_end',), ErrorTypes.TIME_PARSING, ErrorMessages.SHORT_TIME
            ),
            (
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, time_data.wrong_time_string, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening ,
                ('thursday_start',), ErrorTypes.TIME_PARSING, ErrorMessages.SHORT_TIME
            ),
            (
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, time_data.wrong_time_true, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening ,
                ('thursday_start',), ErrorTypes.TIME_TYPE, ErrorMessages.VALID_TIME
            ),
            (
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, time_data.wrong_time_false, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening ,
                ('thursday_start',), ErrorTypes.TIME_TYPE, ErrorMessages.VALID_TIME
            ),
            (
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, time_data.wrong_time_empty, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening ,
                ('thursday_start',), ErrorTypes.TIME_PARSING, ErrorMessages.SHORT_TIME
            ),
            (
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.wrong_time_string,
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening ,
                ('thursday_end',), ErrorTypes.TIME_PARSING, ErrorMessages.SHORT_TIME
            ),
            (
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.wrong_time_true,
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening ,
                ('thursday_end',), ErrorTypes.TIME_TYPE, ErrorMessages.VALID_TIME
            ),
            (
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.wrong_time_false,
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening ,
                ('thursday_end',), ErrorTypes.TIME_TYPE, ErrorMessages.VALID_TIME
            ),
            (
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.wrong_time_empty,
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening ,
                ('thursday_end',), ErrorTypes.TIME_PARSING, ErrorMessages.SHORT_TIME
            ),
            (
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.wrong_time_string, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening ,
                ('friday_start',), ErrorTypes.TIME_PARSING, ErrorMessages.SHORT_TIME
            ),
            (
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.wrong_time_true, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening ,
                ('friday_start',), ErrorTypes.TIME_TYPE, ErrorMessages.VALID_TIME
            ),
            (
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.wrong_time_false, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening ,
                ('friday_start',), ErrorTypes.TIME_TYPE, ErrorMessages.VALID_TIME
            ),
            (
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.wrong_time_empty, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening ,
                ('friday_start',), ErrorTypes.TIME_PARSING, ErrorMessages.SHORT_TIME
            ),
            (
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.wrong_time_string, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening ,
                ('friday_end',), ErrorTypes.TIME_PARSING, ErrorMessages.SHORT_TIME
            ),
            (
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.wrong_time_true, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening ,
                ('friday_end',), ErrorTypes.TIME_TYPE, ErrorMessages.VALID_TIME
            ),
            (
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.wrong_time_false, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening ,
                ('friday_end',), ErrorTypes.TIME_TYPE, ErrorMessages.VALID_TIME
            ),
            (
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.wrong_time_empty, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening ,
                ('friday_end',), ErrorTypes.TIME_PARSING, ErrorMessages.SHORT_TIME
            ),
            (
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, time_data.wrong_time_string, time_data.right_evening,
                time_data.right_morning, time_data.right_evening ,
                ('saturday_start',), ErrorTypes.TIME_PARSING, ErrorMessages.SHORT_TIME
            ),
            (
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, time_data.wrong_time_true, time_data.right_evening,
                time_data.right_morning, time_data.right_evening ,
                ('saturday_start',), ErrorTypes.TIME_TYPE, ErrorMessages.VALID_TIME
            ),
            (
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, time_data.wrong_time_false, time_data.right_evening,
                time_data.right_morning, time_data.right_evening ,
                ('saturday_start',), ErrorTypes.TIME_TYPE, ErrorMessages.VALID_TIME
            ),
            (
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, time_data.wrong_time_empty, time_data.right_evening,
                time_data.right_morning, time_data.right_evening ,
                ('saturday_start',), ErrorTypes.TIME_PARSING, ErrorMessages.SHORT_TIME
            ),
            (
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.wrong_time_string,
                time_data.right_morning, time_data.right_evening ,
                ('saturday_end',), ErrorTypes.TIME_PARSING, ErrorMessages.SHORT_TIME
            ),
            (
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.wrong_time_true,
                time_data.right_morning, time_data.right_evening ,
                ('saturday_end',), ErrorTypes.TIME_TYPE, ErrorMessages.VALID_TIME
            ),
            (
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.wrong_time_false,
                time_data.right_morning, time_data.right_evening ,
                ('saturday_end',), ErrorTypes.TIME_TYPE, ErrorMessages.VALID_TIME
            ),
            (
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.wrong_time_empty,
                time_data.right_morning, time_data.right_evening ,
                ('saturday_end',), ErrorTypes.TIME_PARSING, ErrorMessages.SHORT_TIME
            ),
            (
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.wrong_time_string, time_data.right_evening ,
                ('sunday_start',), ErrorTypes.TIME_PARSING, ErrorMessages.SHORT_TIME
            ),
            (
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.wrong_time_true, time_data.right_evening ,
                ('sunday_start',), ErrorTypes.TIME_TYPE, ErrorMessages.VALID_TIME
            ),
            (
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.wrong_time_false, time_data.right_evening ,
                ('sunday_start',), ErrorTypes.TIME_TYPE, ErrorMessages.VALID_TIME
            ),
            (
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.wrong_time_empty, time_data.right_evening ,
                ('sunday_start',), ErrorTypes.TIME_PARSING, ErrorMessages.SHORT_TIME
            ),
            (
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.wrong_time_string ,
                ('sunday_end',), ErrorTypes.TIME_PARSING, ErrorMessages.SHORT_TIME
            ),
            (
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.wrong_time_true ,
                ('sunday_end',), ErrorTypes.TIME_TYPE, ErrorMessages.VALID_TIME
            ),
            (
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.wrong_time_false ,
                ('sunday_end',), ErrorTypes.TIME_TYPE, ErrorMessages.VALID_TIME
            ),
            (
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.right_evening, time_data.right_morning, time_data.right_evening,
                time_data.right_morning, time_data.wrong_time_empty ,
                ('sunday_end',), ErrorTypes.TIME_PARSING, ErrorMessages.SHORT_TIME
            ),
        ]
    )
    def test_update_schedule_wrong(
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
            error_loc,
            error_type,
            error_msg,
    ):
        with pytest.raises(ValidationError) as error:
            schedule = ScheduleUpdate(
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
