import datetime

import pytest
from pydantic import ValidationError

from app.schemas.Cell import CellCreate
from tests.unit.test_schemas.conftest import assert_single_validation_error
from tests.unit.test_schemas.test_cell.conftest import Time, Status, Date
from tests.unit.test_schemas.conftest_exceptions import ErrorMessages, ErrorTypes, DataForId

time = Time()
status = Status()
date = Date()
data_for_id = DataForId()


class TestCreateCell:

    @pytest.mark.parametrize("date, time, status, master_id", [
        (date.correct_today ,time.correct_morning , status.correct_free, data_for_id.correct_id),
        (date.correct_tomorrow ,time.correct_morning , status.correct_free, data_for_id.correct_id),
        (date.correct_on_week_bigger ,time.correct_morning , status.correct_free, data_for_id.correct_id),
        (date.correct_date_string ,time.correct_morning , status.correct_free, data_for_id.correct_id),
        (date.correct_today ,time.correct_evening , status.correct_free, data_for_id.correct_id),
        (date.correct_today ,time.correct_afternoon , status.correct_free, data_for_id.correct_id),
        (date.correct_today ,time.correct_string , status.correct_free, data_for_id.correct_id),
        (date.correct_today, time.wrong_time_integer, status.correct_free, data_for_id.correct_id),
        (date.correct_today, time.wrong_time_float, status.correct_free, data_for_id.correct_id),
        (date.correct_today ,time.correct_evening , status.correct_occupied, data_for_id.correct_id),
        (date.correct_today ,time.correct_morning , status.correct_free, data_for_id.big_correct_id),
    ])
    def test_create_cell_correct(self, date, time, status, master_id):
        cell = CellCreate(master_id=master_id, date=date, time=time, status=status)
        assert isinstance(cell, CellCreate)
        assert cell.master_id == master_id
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

    @pytest.mark.parametrize("date, time, status, master_id, error_loc, error_type, error_msg",[
        (date.wrong_yesterday, time.correct_morning, status.correct_free, data_for_id.correct_id,
         ("date",), ErrorTypes.VALUE_ERROR , ErrorMessages.DATE_IN_THE_PAST ),
        (date.wrong_on_week_smaller, time.correct_morning, status.correct_free, data_for_id.correct_id,
         ("date",), ErrorTypes.VALUE_ERROR , ErrorMessages.DATE_IN_THE_PAST ),
        (date.wrong_type_string, time.correct_morning, status.correct_free, data_for_id.correct_id,
         ("date",), ErrorTypes.DATE_FROM_DATETIME_PARSING , ErrorMessages.SHORT_DATE ),
        (date.wrong_type_integer, time.correct_morning, status.correct_free, data_for_id.correct_id,
         ("date",), ErrorTypes.DATE_FROM_DATETIME_INEXACT , ErrorMessages.WRONG_DATE ),
        (date.wrong_type_float, time.correct_morning, status.correct_free, data_for_id.correct_id,
         ("date",), ErrorTypes.DATE_FROM_DATETIME_INEXACT , ErrorMessages.WRONG_DATE ),
        (date.wrong_type_boolean, time.correct_morning, status.correct_free, data_for_id.correct_id,
         ("date",), ErrorTypes.DATE_TYPE , ErrorMessages.VALID_DATE ),
        (date.wrong_type_empty, time.correct_morning, status.correct_free, data_for_id.correct_id,
         ("date",), ErrorTypes.DATE_FROM_DATETIME_PARSING , ErrorMessages.SHORT_DATE ),
        (date.wrong_type_none, time.correct_morning, status.correct_free, data_for_id.correct_id,
         ("date",), ErrorTypes.DATE_TYPE , ErrorMessages.VALID_DATE ),
        (date.correct_today, time.wrong_time_string, status.correct_free, data_for_id.correct_id,
         ("time",), ErrorTypes.TIME_PARSING , ErrorMessages.SHORT_TIME ),
        (date.correct_today, time.wrong_time_boolean, status.correct_free, data_for_id.correct_id,
         ("time",), ErrorTypes.TIME_TYPE , ErrorMessages.VALID_TIME ),
        (date.correct_today, time.wrong_time_empty, status.correct_free, data_for_id.correct_id,
         ("time",), ErrorTypes.TIME_PARSING , ErrorMessages.SHORT_TIME ),
        (date.correct_today, time.wrong_time_none, status.correct_free, data_for_id.correct_id,
         ("time",), ErrorTypes.TIME_TYPE , ErrorMessages.VALID_TIME ),
        (date.correct_today, time.correct_morning, status.wrong_status, data_for_id.correct_id,
         ("status",), ErrorTypes.ENUM , ErrorMessages.ENUM_CELL ),
        (date.correct_today, time.correct_morning, status.wrong_status_none, data_for_id.correct_id,
         ("status",), ErrorTypes.ENUM , ErrorMessages.ENUM_CELL ),
        (date.correct_today, time.correct_morning, status.wrong_status_empty, data_for_id.correct_id,
         ("status",), ErrorTypes.ENUM , ErrorMessages.ENUM_CELL ),
        (date.correct_today, time.correct_morning, status.wrong_status_boolean, data_for_id.correct_id,
         ("status",), ErrorTypes.ENUM , ErrorMessages.ENUM_CELL ),
        (date.correct_today, time.correct_morning, status.wrong_status_integer, data_for_id.correct_id,
         ("status",), ErrorTypes.ENUM , ErrorMessages.ENUM_CELL ),
        (date.correct_today, time.correct_morning, status.wrong_status_float, data_for_id.correct_id,
         ("status",), ErrorTypes.ENUM , ErrorMessages.ENUM_CELL ),
        (date.correct_today, time.correct_morning, status.correct_free, data_for_id.wrong_id_zero,
         ("master_id",), ErrorTypes.GREATER_THAN_EQUAL , ErrorMessages.ID_GREATER_ONE ),
        (date.correct_today, time.correct_morning, status.correct_free, data_for_id.wrong_negative_id,
         ("master_id",), ErrorTypes.GREATER_THAN_EQUAL , ErrorMessages.ID_GREATER_ONE ),
        (date.correct_today, time.correct_morning, status.correct_free, data_for_id.big_wrong_negative_id,
         ("master_id",), ErrorTypes.GREATER_THAN_EQUAL , ErrorMessages.ID_GREATER_ONE ),
        (date.correct_today, time.correct_morning, status.correct_free, data_for_id.wrong_id_str,
         ("master_id",), ErrorTypes.INT_TYPE , ErrorMessages.INT_TYPE ),
        (date.correct_today, time.correct_morning, status.correct_free, data_for_id.wrong_id_none,
         ("master_id",), ErrorTypes.INT_TYPE , ErrorMessages.INT_TYPE ),
        (date.correct_today, time.correct_morning, status.correct_free, data_for_id.wrong_id_float,
         ("master_id",), ErrorTypes.INT_TYPE , ErrorMessages.INT_TYPE ),
        (date.correct_today, time.correct_morning, status.correct_free, data_for_id.wrong_id_true,
         ("master_id",), ErrorTypes.INT_TYPE , ErrorMessages.INT_TYPE ),
        (date.correct_today, time.correct_morning, status.correct_free, data_for_id.wrong_id_false,
         ("master_id",), ErrorTypes.INT_TYPE , ErrorMessages.INT_TYPE ),
    ])
    def test_create_cell_wrong(self, date, time, status, master_id, error_loc, error_type, error_msg):
        with pytest.raises(ValidationError) as exc_info:
            CellCreate(master_id=master_id, date=date, time=time, status=status)
        assert_single_validation_error(exc_info.value.errors(), error_loc, error_type, error_msg)
