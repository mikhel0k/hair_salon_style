import datetime

import pytest
from pydantic import ValidationError

from app.schemas.Cell import CellCreate
from conftest import Time, Status, Date
from tests.unit.test_schemas.conftest_exceptions import ErrorMessages, ErrorTypes


class TestCreateCell:
    time = Time()
    status = Status()
    date = Date()

    @pytest.mark.parametrize("date, time, status", [
        (date.right_today ,time.right_morning , status.right_free),
        (date.right_tomorrow ,time.right_morning , status.right_free),
        (date.right_on_week_bigger ,time.right_morning , status.right_free),
        (date.right_date_string ,time.right_morning , status.right_free),
        (date.right_today ,time.right_evening , status.right_free),
        (date.right_today ,time.right_afternoon , status.right_free),
        (date.right_today ,time.right_string , status.right_free),
        (date.right_today, time.wrong_time_integer, status.right_free),
        (date.right_today, time.wrong_time_float, status.right_free),
        (date.right_today ,time.right_evening , status.right_occupied),
    ])
    def test_create_cell(self, date, time, status):
        cell = CellCreate(master_id=1, date=date, time=time, status=status)
        assert isinstance(cell, CellCreate)
        assert cell.master_id == 1
        assert cell.status == status

        actual_time = cell.time.replace(tzinfo=None)

        if isinstance(time, datetime.time):
            assert actual_time == time
        elif isinstance(time, str):
            assert actual_time == datetime.time.fromisoformat(time)
        elif isinstance(time, (int, float)):
            assert actual_time == datetime.time(second=int(time))

        if isinstance(date, datetime.date):
            assert cell.date == date
        elif isinstance(date, str):
            assert cell.date == datetime.date.fromisoformat(date)

    @pytest.mark.parametrize("date, time, status, error_type, error_msg",[
        (date.wrong_yesterday, time.right_morning, status.right_free,
         ErrorTypes.VALUE_ERROR , ErrorMessages.DATE_IN_THE_PAST ),
        (date.wrong_on_week_smaller, time.right_morning, status.right_free,
         ErrorTypes.VALUE_ERROR , ErrorMessages.DATE_IN_THE_PAST ),
        (date.wrong_type_string, time.right_morning, status.right_free,
         ErrorTypes.DATE_FROM_DATETIME_PARSING , ErrorMessages.SHORT_DATE ),
        (date.wrong_type_integer, time.right_morning, status.right_free,
         ErrorTypes.DATE_FROM_DATETIME_INEXACT , ErrorMessages.WRONG_DATE ),
        (date.wrong_type_float, time.right_morning, status.right_free,
         ErrorTypes.DATE_FROM_DATETIME_INEXACT , ErrorMessages.WRONG_DATE ),
        (date.wrong_type_boolean, time.right_morning, status.right_free,
         ErrorTypes.DATE_TIPE , ErrorMessages.VALID_DATE ),
        (date.wrong_type_empty, time.right_morning, status.right_free,
         ErrorTypes.DATE_FROM_DATETIME_PARSING , ErrorMessages.SHORT_DATE ),
        (date.wrong_type_none, time.right_morning, status.right_free,
         ErrorTypes.DATE_TIPE , ErrorMessages.VALID_DATE ),
        (date.right_today, time.wrong_time_string, status.right_free,
         ErrorTypes.TIME_PARSING , ErrorMessages.SHORT_TIME ),
        (date.right_today, time.wrong_time_boolean, status.right_free,
         ErrorTypes.TIME_TYPE , ErrorMessages.VALID_TIME ),
        (date.right_today, time.wrong_time_empty, status.right_free,
         ErrorTypes.TIME_PARSING , ErrorMessages.SHORT_TIME ),
        (date.right_today, time.wrong_time_none, status.right_free,
         ErrorTypes.TIME_TYPE , ErrorMessages.VALID_TIME ),
        (date.right_today, time.right_morning, status.wrong_status,
         ErrorTypes.ENUM , ErrorMessages.ENUM_CELL ),
        (date.right_today, time.right_morning, status.wrong_status_none,
         ErrorTypes.ENUM , ErrorMessages.ENUM_CELL ),
        (date.right_today, time.right_morning, status.wrong_status_empty,
         ErrorTypes.ENUM , ErrorMessages.ENUM_CELL ),
        (date.right_today, time.right_morning, status.wrong_status_boolean,
         ErrorTypes.ENUM , ErrorMessages.ENUM_CELL ),
        (date.right_today, time.right_morning, status.wrong_status_integer,
         ErrorTypes.ENUM , ErrorMessages.ENUM_CELL ),
        (date.right_today, time.right_morning, status.wrong_status_float,
         ErrorTypes.ENUM , ErrorMessages.ENUM_CELL ),
    ])
    def test_create_cell_wrong(self, date, time, status, error_type, error_msg):
        with pytest.raises(ValidationError) as error:
            cell = CellCreate(master_id=1, date=date, time=time, status=status)
        assert len(error.value.errors()) == 1
        assert error.value.errors()[0]["type"] == error_type
        assert error_msg in error.value.errors()[0]["msg"]
