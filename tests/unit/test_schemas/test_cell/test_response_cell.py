import datetime

import pytest
from pydantic import ValidationError

from app.models import Cell
from app.schemas.Cell import CellResponse
from tests.unit.test_schemas.conftest import assert_single_validation_error
from tests.unit.test_schemas.test_cell.conftest import Time, Status, Date
from tests.unit.test_schemas.conftest_exceptions import ErrorMessages, ErrorTypes, DataForId

time = Time()
status = Status()
date = Date()
data_for_id = DataForId()


class TestResponseCell:

    @pytest.mark.parametrize("cell, date, time, status, master_id, cell_id", [
        (Cell(date=date.correct_today, time=time.correct_morning, status=status.correct_free, master_id=data_for_id.correct_id, id=data_for_id.correct_id),
        date.correct_today, time.correct_morning, status.correct_free, data_for_id.correct_id, data_for_id.correct_id),
        (Cell(date=date.correct_tomorrow, time=time.correct_morning, status=status.correct_free, master_id=data_for_id.correct_id, id=data_for_id.correct_id),
        date.correct_tomorrow, time.correct_morning, status.correct_free, data_for_id.correct_id, data_for_id.correct_id),
        (Cell(date=date.correct_on_week_bigger, time=time.correct_morning, status=status.correct_free, master_id=data_for_id.correct_id, id=data_for_id.correct_id),
        date.correct_on_week_bigger, time.correct_morning, status.correct_free, data_for_id.correct_id, data_for_id.correct_id),
        (Cell(date=date.correct_date_string, time=time.correct_morning, status=status.correct_free, master_id=data_for_id.correct_id, id=data_for_id.correct_id),
        date.correct_date_string, time.correct_morning, status.correct_free, data_for_id.correct_id, data_for_id.correct_id),
        (Cell(date=date.correct_today, time=time.correct_evening, status=status.correct_free, master_id=data_for_id.correct_id, id=data_for_id.correct_id),
        date.correct_today, time.correct_evening, status.correct_free, data_for_id.correct_id, data_for_id.correct_id),
        (Cell(date=date.correct_today, time=time.correct_afternoon, status=status.correct_free, master_id=data_for_id.correct_id, id=data_for_id.correct_id),
        date.correct_today, time.correct_afternoon, status.correct_free, data_for_id.correct_id, data_for_id.correct_id),
        (Cell(date=date.correct_today, time=time.correct_string, status=status.correct_free, master_id=data_for_id.correct_id, id=data_for_id.correct_id),
        date.correct_today, time.correct_string, status.correct_free, data_for_id.correct_id, data_for_id.correct_id),
        (Cell(date=date.correct_today, time=time.wrong_time_integer, status=status.correct_free, master_id=data_for_id.correct_id, id=data_for_id.correct_id),
        date.correct_today, time.wrong_time_integer, status.correct_free, data_for_id.correct_id, data_for_id.correct_id),
        (Cell(date=date.correct_today, time=time.wrong_time_float, status=status.correct_free, master_id=data_for_id.correct_id, id=data_for_id.correct_id),
        date.correct_today, time.wrong_time_float, status.correct_free, data_for_id.correct_id, data_for_id.correct_id),
        (Cell(date=date.correct_today, time=time.correct_evening, status=status.correct_occupied, master_id=data_for_id.correct_id, id=data_for_id.correct_id),
        date.correct_today, time.correct_evening, status.correct_occupied, data_for_id.correct_id, data_for_id.correct_id),
        (Cell(date=date.wrong_yesterday, time=time.correct_evening, status=status.correct_occupied, master_id=data_for_id.correct_id, id=data_for_id.correct_id),
        date.wrong_yesterday, time.correct_evening, status.correct_occupied, data_for_id.correct_id, data_for_id.correct_id),
        (Cell(date=date.wrong_on_week_smaller, time=time.correct_evening, status=status.correct_occupied, master_id=data_for_id.correct_id, id=data_for_id.correct_id),
        date.wrong_on_week_smaller, time.correct_evening, status.correct_occupied, data_for_id.correct_id, data_for_id.correct_id),
        (Cell(date=date.correct_today, time=time.correct_morning, status=status.correct_free, master_id=data_for_id.big_correct_id, id=data_for_id.correct_id),
        date.correct_today, time.correct_morning, status.correct_free, data_for_id.big_correct_id, data_for_id.correct_id),
        (Cell(date=date.correct_today, time=time.correct_morning, status=status.correct_free, master_id=data_for_id.correct_id, id=data_for_id.big_correct_id),
        date.correct_today, time.correct_morning, status.correct_free, data_for_id.correct_id, data_for_id.big_correct_id),
    ])
    def test_response_cell_correct(self, cell, date, time, status, master_id, cell_id):
        cell = CellResponse.model_validate(cell)
        assert isinstance(cell, CellResponse)
        assert cell.id == cell_id
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

    @pytest.mark.parametrize("cell, error_loc, error_type, error_msg",[
        (Cell(date=date.wrong_type_string, time=time.correct_morning, status=status.correct_free, master_id=data_for_id.correct_id, id=data_for_id.correct_id),
         ("date",), ErrorTypes.DATE_FROM_DATETIME_PARSING, ErrorMessages.SHORT_DATE),
        (Cell(date=date.wrong_type_integer, time=time.correct_morning, status=status.correct_free, master_id=data_for_id.correct_id, id=data_for_id.correct_id),
         ("date",), ErrorTypes.DATE_FROM_DATETIME_INEXACT, ErrorMessages.WRONG_DATE),
        (Cell(date=date.wrong_type_float, time=time.correct_morning, status=status.correct_free, master_id=data_for_id.correct_id, id=data_for_id.correct_id),
         ("date",), ErrorTypes.DATE_FROM_DATETIME_INEXACT, ErrorMessages.WRONG_DATE),
        (Cell(date=date.wrong_type_boolean, time=time.correct_morning, status=status.correct_free, master_id=data_for_id.correct_id, id=data_for_id.correct_id),
         ("date",), ErrorTypes.DATE_TYPE, ErrorMessages.VALID_DATE),
        (Cell(date=date.wrong_type_empty, time=time.correct_morning, status=status.correct_free, master_id=data_for_id.correct_id, id=data_for_id.correct_id),
         ("date",), ErrorTypes.DATE_FROM_DATETIME_PARSING, ErrorMessages.SHORT_DATE),
        (Cell(date=date.wrong_type_none, time=time.correct_morning, status=status.correct_free, master_id=data_for_id.correct_id, id=data_for_id.correct_id),
         ("date",), ErrorTypes.DATE_TYPE, ErrorMessages.VALID_DATE),
        (Cell(date=date.correct_today, time=time.wrong_time_string, status=status.correct_free, master_id=data_for_id.correct_id, id=data_for_id.correct_id),
         ("time",), ErrorTypes.TIME_PARSING, ErrorMessages.SHORT_TIME),
        (Cell(date=date.correct_today, time=time.wrong_time_boolean, status=status.correct_free, master_id=data_for_id.correct_id, id=data_for_id.correct_id),
         ("time",), ErrorTypes.TIME_TYPE, ErrorMessages.VALID_TIME),
        (Cell(date=date.correct_today, time=time.wrong_time_empty, status=status.correct_free, master_id=data_for_id.correct_id, id=data_for_id.correct_id),
         ("time",), ErrorTypes.TIME_PARSING, ErrorMessages.SHORT_TIME),
        (Cell(date=date.correct_today, time=time.wrong_time_none, status=status.correct_free, master_id=data_for_id.correct_id, id=data_for_id.correct_id),
         ("time",), ErrorTypes.TIME_TYPE, ErrorMessages.VALID_TIME),
        (Cell(date=date.correct_today, time=time.correct_morning, status=status.wrong_status, master_id=data_for_id.correct_id, id=data_for_id.correct_id),
         ("status",), ErrorTypes.ENUM, ErrorMessages.ENUM_CELL),
        (Cell(date=date.correct_today, time=time.correct_morning, status=status.wrong_status_empty, master_id=data_for_id.correct_id, id=data_for_id.correct_id),
         ("status",), ErrorTypes.ENUM, ErrorMessages.ENUM_CELL),
        (Cell(date=date.correct_today, time=time.correct_morning, status=status.wrong_status_none, master_id=data_for_id.correct_id, id=data_for_id.correct_id),
         ("status",), ErrorTypes.ENUM, ErrorMessages.ENUM_CELL),
        (Cell(date=date.correct_today, time=time.correct_morning, status=status.wrong_status_float, master_id=data_for_id.correct_id, id=data_for_id.correct_id),
         ("status",), ErrorTypes.ENUM, ErrorMessages.ENUM_CELL),
        (Cell(date=date.correct_today, time=time.correct_morning, status=status.wrong_status_integer, master_id=data_for_id.correct_id, id=data_for_id.correct_id),
         ("status",), ErrorTypes.ENUM, ErrorMessages.ENUM_CELL),
        (Cell(date=date.correct_today, time=time.correct_morning, status=status.wrong_status_boolean, master_id=data_for_id.correct_id, id=data_for_id.correct_id),
         ("status",), ErrorTypes.ENUM, ErrorMessages.ENUM_CELL),
        (Cell(date=date.correct_today, time=time.correct_morning, status=status.correct_free, master_id=data_for_id.wrong_id_zero, id=data_for_id.correct_id),
         ("master_id",), ErrorTypes.GREATER_THAN_EQUAL, ErrorMessages.ID_GREATER_ONE),
        (Cell(date=date.correct_today, time=time.correct_morning, status=status.correct_free, master_id=data_for_id.wrong_negative_id, id=data_for_id.correct_id),
         ("master_id",), ErrorTypes.GREATER_THAN_EQUAL, ErrorMessages.ID_GREATER_ONE),
        (Cell(date=date.correct_today, time=time.correct_morning, status=status.correct_free, master_id=data_for_id.big_wrong_negative_id, id=data_for_id.correct_id),
         ("master_id",), ErrorTypes.GREATER_THAN_EQUAL, ErrorMessages.ID_GREATER_ONE),
        (Cell(date=date.correct_today, time=time.correct_morning, status=status.correct_free, master_id=data_for_id.wrong_id_str, id=data_for_id.correct_id),
         ("master_id",), ErrorTypes.INT_TYPE, ErrorMessages.INT_TYPE),
        (Cell(date=date.correct_today, time=time.correct_morning, status=status.correct_free, master_id=data_for_id.wrong_id_none, id=data_for_id.correct_id),
         ("master_id",), ErrorTypes.INT_TYPE, ErrorMessages.INT_TYPE),
        (Cell(date=date.correct_today, time=time.correct_morning, status=status.correct_free, master_id=data_for_id.wrong_id_float, id=data_for_id.correct_id),
         ("master_id",), ErrorTypes.INT_TYPE, ErrorMessages.INT_TYPE),
        (Cell(date=date.correct_today, time=time.correct_morning, status=status.correct_free, master_id=data_for_id.wrong_id_true, id=data_for_id.correct_id),
         ("master_id",), ErrorTypes.INT_TYPE, ErrorMessages.INT_TYPE),
        (Cell(date=date.correct_today, time=time.correct_morning, status=status.correct_free, master_id=data_for_id.wrong_id_false, id=data_for_id.correct_id),
         ("master_id",), ErrorTypes.INT_TYPE, ErrorMessages.INT_TYPE),
        (Cell(date=date.correct_today, time=time.correct_morning, status=status.correct_free, master_id=data_for_id.correct_id, id=data_for_id.wrong_id_zero),
         ("id",), ErrorTypes.GREATER_THAN_EQUAL, ErrorMessages.ID_GREATER_ONE),
        (Cell(date=date.correct_today, time=time.correct_morning, status=status.correct_free, master_id=data_for_id.correct_id, id=data_for_id.wrong_negative_id),
         ("id",), ErrorTypes.GREATER_THAN_EQUAL, ErrorMessages.ID_GREATER_ONE),
        (Cell(date=date.correct_today, time=time.correct_morning, status=status.correct_free, master_id=data_for_id.correct_id, id=data_for_id.big_wrong_negative_id),
         ("id",), ErrorTypes.GREATER_THAN_EQUAL, ErrorMessages.ID_GREATER_ONE),
        (Cell(date=date.correct_today, time=time.correct_morning, status=status.correct_free, master_id=data_for_id.correct_id, id=data_for_id.wrong_id_str),
         ("id",), ErrorTypes.INT_TYPE, ErrorMessages.INT_TYPE),
        (Cell(date=date.correct_today, time=time.correct_morning, status=status.correct_free, master_id=data_for_id.correct_id, id=data_for_id.wrong_id_none),
         ("id",), ErrorTypes.INT_TYPE, ErrorMessages.INT_TYPE),
        (Cell(date=date.correct_today, time=time.correct_morning, status=status.correct_free, master_id=data_for_id.correct_id, id=data_for_id.wrong_id_float),
         ("id",), ErrorTypes.INT_TYPE, ErrorMessages.INT_TYPE),
        (Cell(date=date.correct_today, time=time.correct_morning, status=status.correct_free, master_id=data_for_id.correct_id, id=data_for_id.wrong_id_true),
         ("id",), ErrorTypes.INT_TYPE, ErrorMessages.INT_TYPE),
        (Cell(date=date.correct_today, time=time.correct_morning, status=status.correct_free, master_id=data_for_id.correct_id, id=data_for_id.wrong_id_false),
         ("id",), ErrorTypes.INT_TYPE, ErrorMessages.INT_TYPE),
    ])
    def test_response_cell_wrong(self, cell, error_loc, error_type, error_msg):
        with pytest.raises(ValidationError) as exc_info:
            CellResponse.model_validate(cell)
        assert_single_validation_error(exc_info.value.errors(), error_loc, error_type, error_msg)
